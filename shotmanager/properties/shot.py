# GPLv3 License
#
# Copyright (C) 2021 Ubisoft
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
To do: module description here.
"""

import bpy

from bpy.types import Scene

# from bpy.types import SoundSequence
from bpy.types import PropertyGroup
from bpy.props import StringProperty, IntProperty, BoolProperty, PointerProperty, FloatVectorProperty

from shotmanager.utils import utils
from shotmanager.rrs_specific.montage.montage_interface import ShotInterface

import logging

_logger = logging.getLogger(__name__)


class UAS_ShotManager_Shot(ShotInterface, PropertyGroup):
    # def _get_parentScene(self):
    #     val = self.get("parentScene", None)
    #     if val is None:
    #         matches = [
    #             s for s in bpy.data.scenes if "UAS_shot_manager_props" in s and self == s["UAS_shot_manager_props"]
    #         ]
    #         self["parentScene"] = matches[0] if len(matches) > 0 else None
    #     return self["parentScene"]

    # def _set_parentScene(self, value):
    #     self["parentScene"] = value

    # parentScene: PointerProperty(type=Scene, get=_get_parentScene, set=_set_parentScene)
    parentScene: PointerProperty(type=Scene)
    # parentTakeIndex: IntProperty(name="Parent Take Index", default=-1)

    def getParentTakeIndex(self):
        return self.parentScene.UAS_shot_manager_props.getShotParentTakeIndex(self)

    def getParentTake(self):
        return self.parentScene.UAS_shot_manager_props.getShotParentTake(self)

    # for backward compatibility - before V1.2.21
    # used by data version patches.
    # For general purpose use the property self.parentScene
    def getParentScene(self):
        if self.parentScene is not None:
            return self.parentScene

        for scn in bpy.data.scenes:
            if "UAS_shot_manager_props" in scn:
                props = scn.UAS_shot_manager_props
                for take in props.takes:
                    #    print("Take name: ", take.name)
                    for shot in take.shots:
                        #        print("  Shot name: ", shot.name)
                        if shot.name == self.name:
                            self.parentScene = scn
                            return scn
        return None

    # def shotManager(self):
    #     """Return the shot manager properties instance the shot is belonging to.
    #     """
    #     parentShotManager = None
    #     parentScene = self.getParentScene()

    #     if parentScene is not None:
    #         parentShotManager = parentScene.UAS_shot_manager_props
    #     return parentShotManager

    def getOutputFileName(
        self, rootFilePath="", fullPath=False, fullPathOnly=False, specificFrame=None, noExtension=False
    ):
        _logger.debug(
            "*** shot.getOutputFileName: Deprecated - use getOutputMediaPath"
        )

        return self.parentScene.UAS_shot_manager_props.getShotOutputFileName(
            self,
            rootFilePath=rootFilePath,
            fullPath=fullPath,
            fullPathOnly=fullPathOnly,
            specificFrame=specificFrame,
            noExtension=noExtension,
        )

    def getOutputMediaPath(
        self,
        rootPath=None,
        insertTakeName=True,
        providePath=True,
        provideName=True,
        provideExtension=True,
        specificFrame=None,
        genericFrame=False,
    ):
        return self.parentScene.UAS_shot_manager_props.getShotOutputMediaPath(
            self,
            rootPath=rootPath,
            insertTakeName=insertTakeName,
            providePath=providePath,
            provideName=provideName,
            provideExtension=provideExtension,
            specificFrame=specificFrame,
            genericFrame=genericFrame,
        )

    def getCompositedMediaPath(self, rootFilePath, specificFrame=None):
        # props = shot.parentScene.UAS_shot_manager_props
        takeName = self.getParentTake().getName_PathCompliant()
        #    outputFileFormat = props.getOutputFileFormat(isVideo=specificFrame is None)

        if not (rootFilePath.endswith("/") or rootFilePath.endswith("\\")):
            rootFilePath += "\\"
        compositedMediaPath = (
            f"{rootFilePath}{takeName}\\{self.getOutputFileName(fullPath=False)}"  # .{outputFileFormat}"
        )
        if specificFrame is not None:
            compositedMediaPath = (
                f"{rootFilePath}{takeName}\\{self.getOutputFileName(fullPath=False, specificFrame=specificFrame)}"
            )

        # compositedMediaPath.replace("\\", "/")

        return compositedMediaPath

    def getName_PathCompliant(self, withPrefix=False):
        shotName = self.name.replace(" ", "_")
        if withPrefix:
            shotName = f"{self.parentScene.UAS_shot_manager_props.renderShotPrefix()}_{shotName}"
        return shotName

    def _get_name(self):
        return self.get("name", "-")

    def _set_name(self, value):
        """ Set a unique name to the shot
        """
        shots = self.parentScene.UAS_shot_manager_props.getShotsList(takeIndex=self.getParentTakeIndex())
        newName = utils.findFirstUniqueName(self, value, shots)
        self["name"] = newName

    name: StringProperty(name="Name", get=_get_name, set=_set_name)

    def _update_enabled(self, context):
        self.selectShotInUI()

    enabled: BoolProperty(
        name="Enable / Disable Shots",
        description="Use - or not - the shot in the edit",
        update=_update_enabled,
        default=True,
        options=set(),
    )

    def selectShotInUI(self):
        currentTakeInd = self.parentScene.UAS_shot_manager_props.getCurrentTakeIndex()
        if currentTakeInd == self.getParentTakeIndex():
            self.parentScene.UAS_shot_manager_props.setSelectedShot(self)

    #############
    # start #####
    #############

    def _get_start(self):
        return self.get("start", 25)

    # *** behavior here must match the one of start and end of shot preferences ***
    def _set_start(self, value):
        duration = self.getDuration()
        self["start"] = value
        if self.durationLocked:
            self["end"] = self.start + duration - 1
        elif self.start > self.end:
            self["start"] = self.end

    def _update_start(self, context):
        self.selectShotInUI()
        self.updateClipLinkToShotStart()

    start: IntProperty(
        name="Start",
        description="Index of the first included frame of the shot.\nNote that start frame cannot exceed end frame",
        get=_get_start,
        set=_set_start,
        update=_update_start,
    )

    #############
    # end #####
    #############

    def _get_end(self):
        return self.get("end", 30)

    # *** behavior here must match the one of start and end of shot preferences ***
    def _set_end(self, value):
        duration = self.getDuration()
        self["end"] = value
        if self.durationLocked:
            self["start"] = self.end - duration + 1
        elif self.start > self.end:
            self["end"] = self.start

    def _update_end(self, context):
        self.selectShotInUI()

    end: IntProperty(
        name="End",
        description="Index of the last included frame of the shot.\nNote that end frame cannot be lower than start frame",
        get=_get_end,
        set=_set_end,
        update=_update_end,
    )

    #############
    # duration #####
    #############

    def getDuration(self):
        """ Returns the shot duration in frames
            In Blender - and in Shot Manager - the last frame of the shot is included in the rendered images
        """
        return self.end - self.start + 1

    def setDuration(self, duration, bypassLock=False):
        """ Set the shot duration in frames
            In Blender - and in Shot Manager - the last frame of the shot is included in the rendered images
        """
        newDuration = max(duration, 1)
        if not self.durationLocked:
            self.end = self.start + newDuration - 1
        elif bypassLock:
            self.durationLocked = False
            self.end = self.start + newDuration - 1
            self.durationLocked = True

    def _get_duration_fp(self):
        #   print("\n*** _get_duration_fp: New state: ", self.duration_fp)

        # not used, normal it's the fake property
        self.get("duration_fp", -1)

        return self.getDuration()

    def _set_duration_fp(self, value):
        # print("\n*** _update_duration_fp: New state: ", self.duration_fp)
        if not self.durationLocked:
            self["duration_fp"] = value
            self.end = self.start + max(value, 1) - 1

    def _update_duration_fp(self, context):
        #  print("\n*** _update_duration_fp: New state: ", self.duration_fp)
        pass

    # fake property: value never used in itself, its purpose is to update ofher properties
    duration_fp: IntProperty(
        name="Shot Duration",
        description="Duration is a frame number given by end - start + 1.\nIf set in the Shots Settings panel, the duration is displayed in red\nwhen the current time is in the shot range",
        min=1,
        get=_get_duration_fp,
        set=_set_duration_fp,
        update=_update_duration_fp,
        options=set(),
    )

    def _update_durationLocked(self, context):
        self.selectShotInUI()

    durationLocked: BoolProperty(
        name="Lock Duration",
        description="Lock - or not - the shot duration.\nWhen locked, changing one boundary will also affect the other",
        default=False,
        update=_update_durationLocked,
        options=set(),
    )

    ##############
    # camera
    ##############

    def _filter_cameras(self, object):
        """ Return true only for cameras from the same scene as the shot
        """
        # print("self", str(self))  # this shot
        # print("object", str(object))  # all the objects of the property type

        return object.type == "CAMERA" and object.name in self.parentScene.objects

    camera: PointerProperty(
        name="Camera",
        description="Select a Camera",
        type=bpy.types.Object,
        # poll=lambda self, obj: True if obj.type == "CAMERA" else False,
        poll=_filter_cameras,
    )

    def isCameraValid(self):
        """ Sometimes a pointed camera can seem to work but the camera object doesn't exist anymore in the scene.
            Return True if the camera is really there, False otherwise
            Note: This doesn't change the camera attribute of the shot
        """
        cameraIsInvalid = self.camera is not None
        if self.camera is not None:
            try:
                if bpy.context.scene.objects[self.camera.name] is None:
                    self.camera = None
            except Exception as e:
                # item.camera = None     # not working, often invalid context to write in
                cameraIsInvalid = False
            # _logger.error(f"Error: Shot {self.name} uses a camera {self.camera.name} not found in the scene")

        return cameraIsInvalid

    def makeCameraUnique(self):
        if (
            self.camera is not None
            and self.parentScene.UAS_shot_manager_props.getNumSharedCamera(
                self.camera
            )
            > 1
        ):
            self.camera = utils.duplicateObject(self.camera, newName=f"Cam_{self.name}")

    ##############
    # color
    ##############

    def _get_color(self):
        defaultVal = [1.0, 1.0, 1.0, 1.0]
        props = self.parentScene.UAS_shot_manager_props

        if props.use_camera_color and self.camera is not None:
            defaultVal[0] = self.camera.color[0]
            defaultVal[1] = self.camera.color[1]
            defaultVal[2] = self.camera.color[2]

        val = self.get("color", defaultVal)

        if props.use_camera_color:
            if self.camera is not None:
                val[0] = self.camera.color[0]
                val[1] = self.camera.color[1]
                val[2] = self.camera.color[2]
            else:
                val = [0.0, 0.0, 0.0, 1.0]

        return val

    def _set_color(self, value):
        self["color"] = value
        props = self.parentScene.UAS_shot_manager_props
        if props.use_camera_color and self.camera is not None:
            self.camera.color[0] = self["color"][0]
            self.camera.color[1] = self["color"][1]
            self.camera.color[2] = self["color"][2]
            self.camera.color[3] = self["color"][3]

    def _update_color(self, context):
        self.selectShotInUI()

    color: FloatVectorProperty(
        name="Set the Camera (or Shot) Color",
        description="Color of the camera used by the shot or, according to\nthe settings, color of the shot",
        subtype="COLOR",
        min=0.0,
        max=1.0,
        size=4,
        default=(1.0, 1.0, 1.0, 1.0),
        get=_get_color,
        set=_set_color,
        update=_update_color,
        options=set(),
    )

    def getEditStart(self, referenceLevel="TAKE"):
        """
            referenceLevel can be "TAKE" or "GLOBAL_EDIT"
        """
        return self.parentScene.UAS_shot_manager_props.getEditTime(self, self.start, referenceLevel=referenceLevel)

    def getEditEnd(self, referenceLevel="TAKE"):
        """
            referenceLevel can be "TAKE" or "GLOBAL_EDIT"
        """
        return self.parentScene.UAS_shot_manager_props.getEditTime(self, self.end, referenceLevel=referenceLevel)

    ##############
    # background images
    ##############

    def hasBGImage(self):
        return self.camera is not None and len(self.camera.data.background_images)

    def updateClipLinkToShotStart(self):
        if self.camera is None or not len(self.camera.data.background_images):
            return
        bgClip = self.camera.data.background_images[0].clip
        bgSoundSequence = self.getSoundSequence()

        if self.bgImages_linkToShotStart:
            if bgClip is not None:
                bgClip.frame_start = self.start + self.bgImages_offset
            if bgSoundSequence is not None:
                bgSoundSequence.frame_start = self.start + self.bgImages_offset
        else:
            if bgClip is not None:
                bgClip.frame_start = self.bgImages_offset
            if bgSoundSequence is not None:
                bgSoundSequence.frame_start = self.bgImages_offset

    def _get_bgImages_linkToShotStart(self):
        return self.get("bgImages_linkToShotStart", True)

    def _set_bgImages_linkToShotStart(self, value):
        self["bgImages_linkToShotStart"] = value
        self.updateClipLinkToShotStart()

    # def _update_bgImages_linkToShotStart(self, context):
    #     if self.camera is not None and len(self.camera.data.background_images):
    #         bgClip = self.camera.data.background_images[0].clip
    #         if bgClip is not None:
    #             if self._update_bgImages_linkToShotStart:
    #                 bgClip.frame_start = self.start + self.bgImages_offset
    #             else:
    #                 bgClip.frame_start = self.bgImages_offset

    bgImages_linkToShotStart: BoolProperty(
        name="Link BG to Start",
        description="Link the background image clip to the shot start.\n"
        "If linked the background clip start frame is relative to the shot start.\n"
        "If not linked the clip starts at frame 0 + offset",
        default=True,
        get=_get_bgImages_linkToShotStart,
        set=_set_bgImages_linkToShotStart,
        # update=_update_bgImages_linkToShotStart,
        options=set(),
    )

    def _get_bgImages_offset(self):
        return self.get("bgImages_offset", 0)

    def _set_bgImages_offset(self, value):
        self["bgImages_offset"] = value
        self.updateClipLinkToShotStart()
        # if self.camera is not None and len(self.camera.data.background_images):
        #     bgClip = self.camera.data.background_images[0].clip
        #     if bgClip is not None:
        #         if self.bgImages_linkToShotStart:
        #             bgClip.frame_start = self.start + self.bgImages_offset
        #         else:
        #             bgClip.frame_start = self.bgImages_offset

    bgImages_offset: IntProperty(
        name="BG Clip Offset",
        description="Time offset for the clip used as background for the camera",
        soft_min=-20,
        soft_max=20,
        get=_get_bgImages_offset,
        set=_set_bgImages_offset,
        default=0,
    )

    def addBGImages(self, mediaFile, frame_start=0, alpha=1.0, addSoundFromVideo=False):
        if self.camera is not None:
            if len(self.camera.data.background_images):
                self.removeBGImages()
            print("addBGImages 01")
            utils.add_background_video_to_cam(self.camera.data, str(mediaFile), frame_start, alpha=alpha)
            print(f"addBGImages 02 {self.camera.data.background_images[0].clip.name}")

        if addSoundFromVideo:
            soundClip = self.parentScene.UAS_shot_manager_props.addBGSoundToShot(mediaFile, self)
            if soundClip is not None:
                soundClip.frame_start = frame_start

    def removeBGImages(self):
        if self.camera is not None and len(self.camera.data.background_images):
            # if shot.camera.data.background_images[0].clip is not None:
            self.camera.data.show_background_images = False
            # shot.camera.data.background_images[0].clip = None
            self.camera.data.background_images.clear()
            # shot.camera.data.background_images[0].clip.filepath = ""

        self.parentScene.UAS_shot_manager_props.removeBGSoundFromShot(self)
        # if "" != self.bgSoundClipName:
        #     soundSeq = self.getSoundSequence()
        #     if soundSeq is not None:
        #         self.parentScene.sequence_editor.sequences.remove(soundSeq)
        #     self.bgSoundClipName = ""

    ##############
    # background sounds
    ##############

    bgImages_sound_trackIndex: IntProperty(name="Sound Track Index", min=-1, max=32, default=-1)
    # bgSoundClip: PointerProperty(type=SoundSequence)
    bgSoundClipName: StringProperty(default="")

    def enableBGSound(self, useBgSound):
        # if self.bgSoundClip is not None:
        #     self.bgSoundClip.mute = not useBgSound
        if self.bgSoundClipName != "":
            soundClip = self.parentScene.sequence_editor.sequences[self.bgSoundClipName]
            if soundClip is not None:
                soundClip.mute = not useBgSound

    def isSoundSequenceValid(self):
        """ Return true if there is no sound sequence -ie self.bgSoundClipName is "") or if a sequence with this name
            is found in the VSE, false otherwise
        """
        return (
            self.bgSoundClipName == ""
            or self.bgSoundClipName in self.parentScene.sequence_editor.sequences
        )

    def getSoundSequence(self):
        soundClip = None
        print("Soundseq")
        if (
            self.bgSoundClipName != ""
            and self.bgSoundClipName
            in self.parentScene.sequence_editor.sequences_all
        ):
            soundClip = self.parentScene.sequence_editor.sequences_all[self.bgSoundClipName]
        if soundClip is not None:
            print(f"Sounclip: {soundClip.name}")

        return soundClip

    #############
    # grease pencil
    #############

    def hasGreasePencil(self):
        if self.camera is None:
            return False
        gp_child = utils.get_greasepencil_child(self.camera)
        return gp_child is not None

    #############
    # notes #####
    #############

    note01: StringProperty(name="Note 1", description="")
    note02: StringProperty(name="Note 2", description="")
    note03: StringProperty(name="Note 3", description="")

    def hasNotes(self):
        return self.note01 != "" or self.note02 != "" or self.note03 != ""

    #############
    # interface for Montage #####
    # Note: Shot inherits from ShotInterface
    #############

    # def __init__(self, parent, shot):      # cannot use this constructor since new shots are added directly to the array of take
    def __init__(self):
        """
            parent: reference to the parent take
        """
        #  self.parent = None
        super().__init__()

    def initialize(self, parent):
        """ Parent is the parent take
        """
        # if "parent" not in self:
        # props = self.parentScene.UAS_shot_manager_props
        # #  print(" icicicic parent in shot")

        # UAS_ShotManager_Shot.parent = property(lambda self: parent)
        # self.parent = parent
        pass

    def get_index_in_parent(self):
        props = self.parentScene.UAS_shot_manager_props
        return props.getShotIndex(self)

    def get_name(self):
        return self.name

    def printInfo(self, only_clip_info=False):
        super().printInfo(only_clip_info=True)

    #   infoStr = f"             - Media:"
    #   print(infoStr)

    ############
    # Note that all these interface functions are refering to timings in the EDIT, not in the 3D environment !!
    ############

    def get_frame_start(self):
        return self.getEditStart()

    def get_frame_end(self):
        """get_frame_end is exclusive in order to follow the Blender implementation of get_frame_end for its clips
        """
        return self.getEditEnd() + 1

    def get_frame_duration(self):
        return self.getDuration()

    def get_frame_final_start(self):
        return self.get_frame_start()

    def get_frame_final_end(self):
        """get_frame_final_end is exclusive in order to follow the Blender implementation of get_frame_end for its clips
        """
        return self.get_frame_end()

    def get_frame_final_duration(self):
        return self.get_frame_duration()

    def get_frame_offset_start(self):
        return 0

    def get_frame_offset_end(self):
        return 0

