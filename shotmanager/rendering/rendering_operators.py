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

from pathlib import Path

import bpy
from bpy.types import Operator
from bpy.props import EnumProperty, BoolProperty, StringProperty

from .rendering import launchRender

from shotmanager.utils import utils


def get_media_path(out_path, take_name, shot_name):

    if out_path.startswith("//"):
        out_path = str(Path(bpy.data.filepath).parent.absolute()) + out_path[1:]
    return f"{out_path}/{take_name}/{bpy.context.scene.UAS_shot_manager_props.renderShotPrefix()}_{shot_name}.mp4"


##########
# Render
##########


class UAS_OT_OpenPathBrowser(Operator):
    bl_idname = "uas_shot_manager.openpathbrowser"
    bl_label = "Open"
    bl_description = (
        "Open a path browser to define the directory to use to render the images\n"
        "Relative path must be set directly in the text field and must start with ''//''"
    )

    # https://docs.blender.org/api/current/bpy.props.html
    #  filepath = bpy.props.StringProperty(subtype="FILE_PATH")
    directory: StringProperty(subtype="DIR_PATH")

    # filter_glob : StringProperty(
    #     default = '*',
    #     options = {'HIDDEN'} )

    def invoke(self, context, event):  # See comments at end  [1]
        #  self.filepath = bpy.context.scene.UAS_shot_manager_props.renderRootPath
        # https://docs.blender.org/api/current/bpy.types.WindowManager.html

        self.directory = context.scene.UAS_shot_manager_props.renderRootPath

        context.window_manager.fileselect_add(self)

        return {"RUNNING_MODAL"}

    def execute(self, context):
        """Open a path browser to define the directory to use to render the images"""
        context.scene.UAS_shot_manager_props.renderRootPath = self.directory
        return {"FINISHED"}


class UAS_PT_ShotManager_Render(Operator):
    bl_idname = "uas_shot_manager.render"
    bl_label = "Render"
    bl_description = "Render."
    bl_options = {"INTERNAL"}

    renderMode: EnumProperty(
        name="Display Shot Properties Mode",
        description="Update the content of the Shot Properties panel either on the current shot\nor on the shot seleted in the shots list",
        items=(
            ("STILL", "Still", ""),
            ("ANIMATION", "Animation", ""),
            ("ALL", "All Edits", ""),
            ("OTIO", "OTIO", ""),
            ("PLAYBLAST", "PLAYBLAST", ""),
        ),
        default="STILL",
    )

    @classmethod
    def description(cls, context, properties):
        descr = "_"
        # print("properties: ", properties)
        # print("properties action: ", properties.action)
        if properties.renderMode == "STILL":
            descr = "Render a still image, at current frame and with the current shot"
        elif properties.renderMode == "ANIMATION":
            descr = "Render the current shot"
        elif properties.renderMode == "ALL":
            descr = "Render all: shots, takes, EDL..."
        elif properties.renderMode == "OTIO":
            descr = "Render the EDL"
        elif properties.renderMode == "PLAYBLAST":
            descr = "Fast-render the enabled shots to a single video based on the current viewport settings."

        return descr

    # def invoke(self, context, event):
    #     # context.window_manager.modal_handler_add(self)
    #     return {"RUNNING_MODAL"}

    # def modal(self, context, event):
    #     # https://blender.stackexchange.com/questions/78069/modal-function-of-a-modal-operator-is-never-called
    #     if event.type == "SPACE":
    #         # wm = context.window_manager
    #         # wm.invoke_popup(self)
    #         # #wm.invoke_props_dialog(self)
    #         print("Space")

    #     if event.type in {"ESC"}:
    #         return {"CANCELLED"}

    #     return {"RUNNING_MODAL"}

    def execute(self, context):
        props = context.scene.UAS_shot_manager_props
        prefs = context.preferences.addons["shotmanager"].preferences
        prefs.renderMode = self.renderMode

        # update UI
        if prefs.renderMode == "STILL":
            props.displayStillProps = True
        elif prefs.renderMode == "ANIMATION":
            props.displayAnimationProps = True
        elif prefs.renderMode == "ALL":
            props.displayAllEditsProps = True
        elif prefs.renderMode == "OTIO":
            props.displayOtioProps = True
        elif prefs.renderMode == "PLAYBLAST":
            props.displayPlayblastProps = True

        if not props.sceneIsReady():
            return {"CANCELLED"}

        if prefs.renderMode == "ANIMATION":
            currentShot = props.getCurrentShot()
            if currentShot is None:
                utils.ShowMessageBox("Current Shot not found - Rendering aborted", "Render aborted")
                return {"CANCELLED"}
            if not currentShot.enabled:
                utils.ShowMessageBox("Current Shot is not enabled - Rendering aborted", "Render aborted")
                return {"CANCELLED"}

        # renderWarnings = ""
        # if props.renderRootPath.startswith("//"):
        #     if "" == bpy.data.filepath:
        #         renderWarnings = "*** Save file first ***"
        # elif "" == props.renderRootPath:
        #     renderWarnings = "*** Invalid Output File Name ***"

        # if "" != renderWarnings:
        #     from ..utils.utils import ShowMessageBox

        #     ShowMessageBox(renderWarnings, "Render Aborted", "ERROR")
        #     print("Render aborted before start: " + renderWarnings)
        #     return {"CANCELLED"}

        if prefs.renderMode == "OTIO":
            bpy.ops.uas_shot_manager.export_otio()
        else:
            renderRootPath = props.renderRootPath if props.renderRootPath != "" else "//"
            bpy.path.abspath(renderRootPath)
            if not (renderRootPath.endswith("/") or renderRootPath.endswith("\\")):
                renderRootPath += "\\"

            # if props.isRenderRootPathValid():
            launchRender(
                context,
                prefs.renderMode,
                renderRootPath,
                # useStampInfo=props.useStampInfoDuringRendering,
                area=context.area,
            )

        #   return {"RUNNING_MODAL"}
        return {"FINISHED"}


###############
# wkip clean: doesn't seem to be used anymore...

# class UAS_PT_ShotManager_RenderDialog(Operator):
#     bl_idname = "uas_shot_manager.renderdialog"
#     bl_label = "Render"
#     bl_description = "Render"
#     bl_options = {"INTERNAL"}

#     only_active: BoolProperty(name="Render Only Active", default=False)

#     renderer: EnumProperty(
#         items=(("BLENDER_EEVEE", "Eevee", ""), ("CYCLES", "Cycles", ""), ("OPENGL", "OpenGL", "")),
#         default="BLENDER_EEVEE",
#     )

#     def execute(self, context):

#         print("*** uas_shot_manager.renderDialog ***")

#         scene = context.scene
#         context.space_data.region_3d.view_perspective = "CAMERA"
#         handles = context.scene.UAS_shot_manager_props.handles
#         props = scene.UAS_shot_manager_props

#         with utils.PropertyRestoreCtx(
#             (scene.render, "filepath"),
#             (scene, "frame_start"),
#             (scene, "frame_end"),
#             (scene.render.image_settings, "file_format"),
#             (scene.render.ffmpeg, "format"),
#             (scene.render, "engine"),
#             (scene.render, "resolution_x"),
#             (scene.render, "resolution_y"),
#         ):

#             scene.render.image_settings.file_format = "FFMPEG"
#             scene.render.ffmpeg.format = "MPEG4"

#             if self.renderer != "OPENGL":
#                 scene.render.engine = self.renderer

#             context.window_manager.UAS_shot_manager_shots_play_mode = False
#             context.window_manager.UAS_shot_manager_display_timeline = False

#             out_path = scene.render.filepath
#             shots = props.get_shots()
#             take = props.getCurrentTake()
#             if take is None:
#                 take_name = ""
#             else:
#                 take_name = take.name

#             if self.only_active:
#                 shot = scene.UAS_shot_manager_props.getCurrentShot()
#                 if shot is None:
#                     return {"CANCELLED"}
#                 scene.frame_start = shot.start - handles
#                 scene.frame_end = shot.end + handles
#                 scene.render.filepath = get_media_path(out_path, take_name, shot.name)
#                 print("      scene.render.filepath: ", scene.render.filepath)

#                 scene.camera = shot.camera

#                 if getattr(scene, "UAS_StampInfo_Settings", None) is not None:
#                     RRS_StampInfo.setRRS_StampInfoSettings(scene)

#                 if self.renderer == "OPENGL":
#                     bpy.ops.render.opengl(animation=True)
#                 else:
#                     bpy.ops.render.render(animation=True)

#                 if getattr(scene, "UAS_StampInfo_Settings", None) is not None:
#                     scene.UAS_StampInfo_Settings.stampInfoUsed = False
#             else:
#                 for shot in shots:
#                     if shot.enabled:
#                         scene.frame_start = shot.start - handles
#                         scene.frame_end = shot.end + handles
#                         scene.render.filepath = get_media_path(out_path, take_name, shot.name)
#                         scene.camera = shot.camera
#                         if getattr(scene, "UAS_StampInfo_Settings", None) is not None:
#                             scene.UAS_StampInfo_Settings.stampInfoUsed = True
#                             scene.UAS_StampInfo_Settings.shotName = shot.name

#                         if self.renderer == "OPENGL":
#                             bpy.ops.render.opengl(animation=True)
#                         else:
#                             bpy.ops.render.render(animation=True)

#                         if getattr(scene, "UAS_StampInfo_Settings", None) is not None:
#                             scene.UAS_StampInfo_Settings.stampInfoUsed = False

#             scene.UAS_StampInfo_Settings.restorePreviousValues(scene)
#             print(" --- RRS Settings Restored ---")
#         # return {"RUNNING_MODAL"}

#         return {"FINISHED"}

#     def draw(self, context):
#         l = self.layout
#         row = l.row()
#         row.prop(self, "renderer")

# def invoke ( self, context, event ):
#     wm = context.window_manager
#     return wm.invoke_props_dialog ( self )


###########
# utils
###########


class UAS_ShotManager_Render_RestoreProjectSettings(Operator):
    bl_idname = "uas_shot_manager.render_restore_project_settings"
    bl_label = "Apply Project Settings"
    bl_description = "Apply Project Settings"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        context.scene.UAS_shot_manager_props.applyProjectSettings()
        return {"FINISHED"}


class UAS_ShotManager_Render_OpenLastRenderResults(Operator):
    bl_idname = "uas_shot_manager.open_last_render_results"
    bl_label = "Last Render Results"
    bl_description = "Open last render results log file"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        # to do
        return {"FINISHED"}


class UAS_ShotManager_Render_ClearLastRenderResults(Operator):
    bl_idname = "uas_shot_manager.clear_last_render_results"
    bl_label = "Clear Last Render Results"
    bl_description = "Clear last render results log file"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        # to do
        return {"FINISHED"}


_classes = (
    UAS_PT_ShotManager_Render,
    # UAS_PT_ShotManager_RenderDialog,
    UAS_OT_OpenPathBrowser,
    UAS_ShotManager_Render_RestoreProjectSettings,
    UAS_ShotManager_Render_OpenLastRenderResults,
    UAS_ShotManager_Render_ClearLastRenderResults,
)


def register():
    for cls in _classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
