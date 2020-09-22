import bpy

from bpy.types import Scene
from bpy.types import PropertyGroup
from bpy.props import StringProperty, IntProperty, BoolProperty, PointerProperty, FloatVectorProperty

from shotmanager.utils.utils import findFirstUniqueName
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

    def getDuration(self):
        """ Returns the shot duration in frames
            in Blender - and in Shot Manager - the last frame of the shot is included in the rendered images
        """
        duration = self.end - self.start + 1
        return duration

    def getOutputFileName(self, frameIndex=-1, fullPath=False, fullPathOnly=False, rootFilePath=""):
        return self.parentScene.UAS_shot_manager_props.getShotOutputFileName(
            self, frameIndex=frameIndex, fullPath=fullPath, fullPathOnly=fullPathOnly, rootFilePath=rootFilePath
        )

    def getName_PathCompliant(self):
        shotName = self.name.replace(" ", "_")
        return shotName

    def _get_name(self):
        val = self.get("name", "-")
        return val

    def _set_name(self, value):
        """ Set a unique name to the shot
        """
        shots = self.parentScene.UAS_shot_manager_props.getShotsList(takeIndex=self.getParentTakeIndex())
        newName = findFirstUniqueName(self, value, shots)
        self["name"] = newName

    name: StringProperty(name="Name", get=_get_name, set=_set_name)

    #############
    # start #####
    #############

    def _get_start(self):
        val = self.get("start", 25)
        return val

    # *** behavior here must match the one of start and end of shot preferences ***
    def _set_start(self, value):
        duration = self.getDuration()
        self["start"] = value
        if self.durationLocked:
            self["end"] = self.start + duration - 1
        else:
            # increase end value if start is superior to end
            # if self.start > self.end:
            #     self["end"] = self.start

            # prevent start to go above end (more user error proof)
            if self.start > self.end:
                self["start"] = self.end

    def _update_start(self, context):
        self.selectShotInUI()

        if self.camera is not None and len(self.camera.data.background_images):
            bgClip = self.camera.data.background_images[0].clip
            if bgClip is not None and self.bgImages_linkToShotStart:
                bgClip.frame_start = self.start + self.bgImages_offset

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
        val = self.get("end", 30)
        return val

    # *** behavior here must match the one of start and end of shot preferences ***
    def _set_end(self, value):
        duration = self.getDuration()
        self["end"] = value
        if self.durationLocked:
            self["start"] = self.end - duration + 1
        else:
            # reduce start value if end is lowr than start
            # if self.start > self.end:
            #    self["start"] = self.end

            # prevent end to go below start (more user error proof)
            if self.start > self.end:
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

    def _get_duration_fp(self):
        #   print("\n*** _get_duration_fp: New state: ", self.duration_fp)

        # not used, normal it's the fake property
        self.get("duration_fp", -1)

        realVal = self.getDuration()
        return realVal

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
        description="Duration is a frame number given by end - start + 1",
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

    def _update_enabled(self, context):
        self.selectShotInUI()

    enabled: BoolProperty(
        name="Enable / Disable Shots",
        description="Use - or not - the shot in the edit",
        update=_update_enabled,
        default=True,
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

        if object.type == "CAMERA" and object.name in self.parentScene.objects:
            return True
        else:
            return False

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
        cameraIsInvalid = not self.camera is None
        if self.camera is not None:
            try:
                if bpy.context.scene.objects[self.camera.name] is None:
                    self.camera = None
            except Exception as e:
                # item.camera = None     # not working, often invalid context to write in
                cameraIsInvalid = False
            # _logger.error(f"Error: Shot {self.name} uses a camera {self.camera.name} not found in the scene")

        return cameraIsInvalid

    ##############
    # color
    ##############

    def _get_color(self):
        defaultVal = [1.0, 1.0, 1.0, 1.0]
        props = self.parentScene.UAS_shot_manager_props

        if props.use_camera_color:
            if self.camera is not None:
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

    def getEditStart(self):
        return self.parentScene.UAS_shot_manager_props.getEditTime(self, self.start)

    def getEditEnd(self):
        return self.parentScene.UAS_shot_manager_props.getEditTime(self, self.end)

    def updateClipLinkToShotStart(self):
        if self.camera is not None and len(self.camera.data.background_images):
            bgClip = self.camera.data.background_images[0].clip
            if bgClip is not None:
                if self.bgImages_linkToShotStart:
                    bgClip.frame_start = self.start + self.bgImages_offset
                else:
                    bgClip.frame_start = self.bgImages_offset

    ##############
    # background images
    ##############

    def _get_bgImages_linkToShotStart(self):
        val = self.get("bgImages_linkToShotStart", True)
        return val

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
        val = self.get("bgImages_offset", 0)
        return val

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

    def selectShotInUI(self):
        currentTakeInd = self.parentScene.UAS_shot_manager_props.getCurrentTakeIndex()
        if currentTakeInd == self.getParentTakeIndex():
            self.parentScene.UAS_shot_manager_props.setSelectedShot(self)

    #############
    # notes #####
    #############

    note01: StringProperty(name="Note 1", description="")
    note02: StringProperty(name="Note 2", description="")
    note03: StringProperty(name="Note 3", description="")

    def hasNotes(self):
        return "" != self.note01 or "" != self.note02 or "" != self.note03

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
        print(" icicicic parent in shot")
        super().__init__()
        pass

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

