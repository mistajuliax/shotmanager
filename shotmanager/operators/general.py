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
from bpy.types import Operator
from bpy.props import BoolProperty, StringProperty

from shotmanager.config import config
from ..utils.utils import getSceneVSE, convertVersionIntToStr
from ..utils import utils


class UAS_ShotManager_OT_GoToVideoShotManager(Operator):
    bl_idname = "uas_shot_manager.go_to_video_shot_manager"
    bl_label = "Go To Updated Video Shot Manager"
    bl_description = "Go to Updated Video Shot Manager"
    bl_options = {"INTERNAL"}

    vseSceneName: StringProperty(default="")

    def invoke(self, context, event):

        vsm_scene = None
        if self.vseSceneName == "":
            self.vseSceneName = "VideoShotManager"
        vsm_scene = getSceneVSE(self.vseSceneName, createVseTab=True)

        # startup_blend = os.path.join(
        #     bpy.utils.resource_path("LOCAL"),
        #     "scripts",
        #     "startup",
        #     "bl_app_templates_system",
        #     "Video_Editing",
        #     "startup.blend",
        # )

        # bpy.context.window.scene = vsm_scene
        # if "Video Editing" not in bpy.data.workspaces:
        #     bpy.ops.workspace.append_activate(idname="Video Editing", filepath=startup_blend)
        bpy.context.window.workspace = bpy.data.workspaces["Video Editing"]

        return {"FINISHED"}


class UAS_ShotManager_OT_FileInfo(Operator):
    bl_idname = "uas_shot_manager.file_info"
    bl_label = "File Info"
    bl_description = "Display information about the current file content"
    bl_options = {"INTERNAL"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)

    def draw(self, context):
        scene = context.scene
        props = scene.UAS_shot_manager_props
        layout = self.layout
        # box = layout.box()

        # Scene
        ###############
        row = layout.row()
        row.label(text=f"Current Scene:  {context.scene.name}")

        row = layout.row()
        box = row.box()

        subRow = box.row()
        subRow.separator()
        subRow.label(text="Fps:")
        subRow.label(text=f"{scene.render.fps}")

        if scene.render.fps_base != 1.0:
            subRow = box.row()
            subRow.alert = True
            subRow.separator()
            subRow.label(text="FPS Base:")
            subRow.label(text=f"{scene.render.fps_base:0.3f}")

        subRow = box.row()
        subRow.separator()
        subRow.label(text="Resolution:")
        subRow.label(text=f"{scene.render.resolution_x} x {scene.render.resolution_y}")
        if scene.render.resolution_percentage != 100:
            subRow = box.row()
            subRow.alert = True
            subRow.separator()
            subRow.label(text="Percentage:")
            subRow.label(text=f"{scene.render.resolution_percentage} %")

        # Project
        ###############
        layout.separator()
        layout.label(text=f"Project Used: {props.use_project_settings}")
        if props.use_project_settings:
            box = layout.box()

            subRow = box.row()
            subRow.separator()
            subRow.label(text="Fps:")
            subRow.label(text=f"{props.project_fps}")

            subRow = box.row()
            subRow.separator()
            subRow.label(text="Resolution:")
            subRow.label(text=f"{props.project_resolution_x} x {props.project_resolution_y}")

            subRow = box.row()
            subRow.separator()
            subRow.label(text="Framed Resolution:")
            subRow.label(text=f"{props.project_resolution_framed_x} x {props.project_resolution_framed_y}")

        # Version
        ###############
        layout.separator()
        box = layout.box()
        row = box.row()
        row.separator()
        row.label(text="Shot Manager Version: ")
        row.label(text=f"{props.version()[0]}")

        row = box.row()
        row.separator()
        row.label(text="Shot Manager Data Version: ")
        row.label(text=f"  {convertVersionIntToStr(props.dataVersion)}")

        # # Authors
        # ###############
        # row = box.row()
        # row.separator()
        # row.label(text="Written by Julien Blervaque (aka Werwack), Romain Carriquiry Borchiari")

        # # Purpose
        # ###############
        # row = box.row()
        # row.label(text="Purpose:")
        # row = box.row()
        # row.separator()
        # row.label(text="Create a set of camera shots and edit them")
        # row = box.row()
        # row.separator()
        # row.label(text="in the 3D View as you would do with video clips.")

        # # Dependencies
        # ###############
        # row = box.row()
        # row.label(text="Dependencies:")
        # row = box.row()
        # row.separator()

        # row.label(text="- OpenTimelineIO")
        # try:
        #     import opentimelineio as otio

        #     otioVersion = otio.__version__
        #     row.label(text="V." + otioVersion)
        # except Exception as e:
        #     row.label(text="Module not found")

        # row = box.row()
        # row.separator()
        # row.label(text="- UAS Stamp Info")
        # if props.isStampInfoAvailable():
        #     versionStr = utils.addonVersion("UAS_StampInfo")
        #     row.label(text="V." + versionStr[0])
        # else:
        #     row.label(text="Add-on not found")

        row.separator()

        layout.separator(factor=1)

    def execute(self, context):
        return {"FINISHED"}


class UAS_ShotManager_OT_EnableDebug(Operator):
    bl_idname = "uas_shot_manager.enable_debug"
    bl_label = "Enable Debug Mode"
    bl_description = "Enable or disable debug mode"
    bl_options = {"INTERNAL"}

    enable_debug: BoolProperty(name="Enable Debug Mode", description="Enable or disable debug mode", default=False)

    def execute(self, context):
        config.uasDebug = self.enable_debug
        return {"FINISHED"}


_classes = (
    UAS_ShotManager_OT_GoToVideoShotManager,
    UAS_ShotManager_OT_FileInfo,
    UAS_ShotManager_OT_EnableDebug,
)


def register():
    for cls in _classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
