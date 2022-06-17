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

import json

import bpy
from bpy.types import Menu

from shotmanager.config import config
from shotmanager.utils import utils

import logging

_logger = logging.getLogger(__name__)


#############
# Shot Item
#############


class UAS_UL_ShotManager_Items(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        props = context.scene.UAS_shot_manager_props
        current_shot_index = props.current_shot_index

        itemHasWarnings = False

        cam = "Cam" if current_shot_index == index else ""
        currentFrame = context.scene.frame_current

        # check if the camera still exists in the scene
        cameraIsValid = item.isCameraValid()
        itemHasWarnings = not cameraIsValid

        # draw the Duration components

        if item.enabled:
            icon = config.icons_col[f"ShotMan_Enabled{cam}"]
            if item.start <= context.scene.frame_current <= item.end:
                icon = config.icons_col[f"ShotMan_EnabledCurrent{cam}"]
        else:
            icon = config.icons_col[f"ShotMan_Disabled{cam}"]

        if item.camera is None or itemHasWarnings:
            layout.alert = True

        row = layout.row()

        row.operator("uas_shot_manager.set_current_shot", icon_value=icon.icon_id, text="").index = index

        if (
            props.display_selectbut_in_shotlist
            or props.display_color_in_shotlist
            or props.display_cameraBG_in_shotlist
            or props.display_greasepencil_in_shotlist
        ):
            row = layout.row(align=True)
            row.scale_x = 1.0
            if props.display_selectbut_in_shotlist:
                row.operator("uas_shot_manager.shots_selectcamera", text="", icon="RESTRICT_SELECT_OFF").index = index

            if props.display_notes_in_properties and props.display_notes_in_shotlist:
                row = row.row(align=True)
                row.scale_x = 1.0

                if item.hasNotes():
                    icon = config.icons_col["ShotManager_NotesData_32"]
                else:
                    icon = config.icons_col["ShotManager_NotesNoData_32"]
                                # emptyIcon = config.icons_col["General_Empty_32"]
                                # row.operator(
                                #     "uas_shot_manager.shots_shownotes", text="", icon_value=emptyIcon.icon_id
                                # ).index = index
                row.operator("uas_shot_manager.shots_shownotes", text="", icon_value=icon.icon_id).index = index
                row.scale_x = 0.9

        if props.display_cameraBG_in_shotlist:
            row = row.row(align=True)
            row.scale_x = 1.0
            icon = "VIEW_CAMERA" if item.hasBGImage() else "BLANK1"
            row.operator("uas_shot_manager.cambgitem", text="", icon=icon).index = index
            row.scale_x = 0.9

        if props.display_greasepencil_in_shotlist:
            row = row.row(align=True)
            row.scale_x = 1.0
            icon = "OUTLINER_OB_GREASEPENCIL" if item.hasGreasePencil() else "BLANK1"
            row.operator("uas_shot_manager.greasepencilitem", text="", icon=icon).index = index
            row.scale_x = 0.9

        if props.display_color_in_shotlist:
            row = row.row(align=True)
            row.scale_x = 0.2
            row.prop(item, "color", text="")
            row.scale_x = 0.45

        row = layout.row(align=True)

        row.scale_x = 1.0
        if props.display_enabled_in_shotlist:
            row.prop(item, "enabled", text="")
            row.separator(factor=0.9)
        row.scale_x = 0.8
        row.label(text=item.name)

        ###########
        # shot values
        ###########

        row = layout.row(align=True)
        row.scale_x = 2.0
        grid_flow = row.grid_flow(align=True, columns=7, even_columns=False)
        grid_flow.use_property_split = False
        button_x_factor = 0.6

        # currentFrameInEdit = props.
        # start
        ###########
        if props.display_edit_times_in_shotlist:
            # grid_flow.scale_x = button_x_factor
            # if props.display_getsetcurrentframe_in_shotlist:
            #     grid_flow.operator(
            #         "uas_shot_manager.getsetcurrentframe", text="", icon="TRIA_DOWN_BAR"
            #     ).shotSource = f"[{index},0]"

            grid_flow.scale_x = 0.4
            shotEditStart = item.getEditStart()
            if currentFrame == item.start and (
                props.highlight_all_shot_frames or current_shot_index == index
            ):
                grid_flow.alert = True
            # grid_flow.prop(item, "start", text="")
            # grid_flow.label(text=str(shotDuration))
            grid_flow.operator("uas_shot_manager.shottimeinedit", text=str(shotEditStart)).shotSource = f"[{index},0]"
        else:
            grid_flow.scale_x = button_x_factor
            if props.display_getsetcurrentframe_in_shotlist:
                grid_flow.operator(
                    "uas_shot_manager.getsetcurrentframe", text="", icon="TRIA_DOWN_BAR"
                ).shotSource = f"[{index},0]"

            grid_flow.scale_x = 0.4
            if currentFrame == item.start and (
                props.highlight_all_shot_frames or current_shot_index == index
            ):
                grid_flow.alert = True
            grid_flow.prop(item, "start", text="")
        grid_flow.alert = False
        # duration
        ###########

        # display_duration_after_time_range
        if not props.display_duration_after_time_range:
            grid_flow.scale_x = button_x_factor - 0.1
            grid_flow.prop(
                item,
                "durationLocked",
                text="",
                icon="DECORATE_LOCKED" if item.durationLocked else "DECORATE_UNLOCKED",
                toggle=True,
            )

            if (
                props.highlight_all_shot_frames or current_shot_index == index
            ) and item.start <= currentFrame <= item.end:
                grid_flow.alert = True

            if props.display_duration_in_shotlist:
                grid_flow.scale_x = 0.3
                grid_flow.prop(item, "duration_fp", text="")
            else:
                grid_flow.scale_x = 0.05
                grid_flow.operator("uas_shot_manager.shot_duration", text="").index = index
            grid_flow.alert = False
        else:
            grid_flow.scale_x = 1.5

        grid_flow.scale_x = 0.4
        # end
        ###########
        if props.display_edit_times_in_shotlist:
            shotEditEnd = item.getEditEnd()
            if currentFrame == item.end and (
                props.highlight_all_shot_frames or current_shot_index == index
            ):
                grid_flow.alert = True
            grid_flow.operator("uas_shot_manager.shottimeinedit", text=str(shotEditEnd)).shotSource = f"[{index},1]"
            grid_flow.alert = False

                # grid_flow.scale_x = button_x_factor - 0.2
                # if props.display_getsetcurrentframe_in_shotlist:
                #     grid_flow.operator(
                #         "uas_shot_manager.getsetcurrentframe", text="", icon="TRIA_DOWN_BAR"
                #     ).shotSource = f"[{index},1]"
        else:
            if currentFrame == item.end and (
                props.highlight_all_shot_frames or current_shot_index == index
            ):
                grid_flow.alert = True
            grid_flow.prop(item, "end", text="")
            grid_flow.alert = False

            grid_flow.scale_x = button_x_factor - 0.2
            if props.display_getsetcurrentframe_in_shotlist:
                grid_flow.operator(
                    "uas_shot_manager.getsetcurrentframe", text="", icon="TRIA_DOWN_BAR"
                ).shotSource = f"[{index},1]"

        if props.display_duration_after_time_range:
            row = layout.row(align=True)
            grid_flow = row.grid_flow(align=True, columns=2, even_columns=False)
            grid_flow.use_property_split = False
            # grid_flow.scale_x = button_x_factor - 0.1
            if props.display_duration_in_shotlist:
                grid_flow.scale_x = 1.5
            grid_flow.prop(
                item,
                "durationLocked",
                text="",
                icon="DECORATE_LOCKED" if item.durationLocked else "DECORATE_UNLOCKED",
                toggle=True,
            )

            if (
                props.highlight_all_shot_frames or current_shot_index == index
            ) and item.start <= currentFrame <= item.end:
                grid_flow.alert = True

            if props.display_duration_in_shotlist:
                grid_flow.scale_x = 0.6
                grid_flow.prop(item, "duration_fp", text="")
            grid_flow.alert = False

        # camera
        ###########
        row = layout.row(align=True)
        grid_flow = row.grid_flow(align=True, columns=3, even_columns=False)
        grid_flow.use_property_split = False
        grid_flow.scale_x = 2.6

        if props.display_camera_in_shotlist:
            if item.camera is None:
                grid_flow.alert = True
            grid_flow.prop(item, "camera", text="")
            grid_flow.scale_x = 0.3
            grid_flow.operator(
                "uas_shot_manager.list_camera_instances", text=str(props.getNumSharedCamera(item.camera))
            ).index = index
            if item.camera is None:
                grid_flow.alert = False

        if props.display_lens_in_shotlist:
            grid_flow.scale_x = 0.4
            grid_flow.use_property_decorate = True
            if item.camera is not None:
                grid_flow.prop(item.camera.data, "lens", text="Lens")
            else:
                grid_flow.alert = True
                grid_flow.operator("uas_shot_manager.nolens", text="-").index = index
                grid_flow.alert = False
            grid_flow.scale_x = 1.0


#################
# tools for shots
#################


class UAS_MT_ShotManager_Shots_ToolsMenu(Menu):
    bl_idname = "UAS_MT_Shot_Manager_shots_toolsmenu"
    bl_label = "Shots Tools"
    bl_description = "Shots Tools"

    def draw(self, context):
        props = context.scene.UAS_shot_manager_props

        # Copy menu entries[ ---
        layout = self.layout
        row = layout.row(align=True)

        # row.label(text="Tools for Shots:")

        row = layout.row(align=True)
        row.operator_context = "INVOKE_DEFAULT"
        row.operator("uas_shot_manager.create_shots_from_each_camera", icon="ADD")

        row = layout.row(align=True)
        row.operator_context = "INVOKE_DEFAULT"
        row.operator("uas_shot_manager.create_n_shots", icon="ADD")

        row = layout.row(align=True)
        row.operator_context = "INVOKE_DEFAULT"
        row.operator("uas_shot_manager.shot_duplicates_to_other_take", icon="DUPLICATE")

        row = layout.row(align=True)
        row.operator_context = "INVOKE_DEFAULT"
        row.operator("uas_shot_manager.remove_multiple_shots", text="Remove Disabled Shots...", icon="REMOVE")

        row = layout.row(align=True)
        row.operator_context = "INVOKE_DEFAULT"
        row.operator("uas_shot_manager.remove_multiple_shots", text="Remove All Shots...", icon="REMOVE").action = "ALL"

        layout.separator()

        # tools for shots ###
        row = layout.row(align=True)
        row.label(text="Tools for Shots:")

        row = layout.row(align=True)
        row.operator_context = "INVOKE_DEFAULT"
        row.operator("uas_shot_manager.unique_cameras", text="   Make All Cameras Unique")

        row = layout.row(align=True)
        row.operator_context = "INVOKE_DEFAULT"
        row.operator("uas_shot_manager.shots_removecamera", text="   Remove Camera From All Shots...")

        #############
        # import EDL
        #############
        layout.separator()
        row = layout.row(align=True)
        row.label(text="EDL / XML / OTIO:")

        row = layout.row(align=True)
        row.operator_context = "INVOKE_DEFAULT"
        row.operator("uasotio.openfilebrowser", text="   Create Shots From EDL...").importMode = "CREATE_SHOTS"

        row = layout.row(align=True)
        #    row.operator_context = "INVOKE_DEFAULT"

        # tools for precut ###
        layout.separator()
        row = layout.row(align=True)
        row.label(text="Tools for Precut:")

        # row = layout.row(align=True)
        # row.operator_context = "INVOKE_DEFAULT"
        # row.operator("uas_shot_manager.predec_shots_from_single_cam", text="   Create Shots From Single Camera...")

        row = layout.row(align=True)
        row.operator_context = "INVOKE_DEFAULT"
        row.operator("uas_shot_manager.print_montage_info", text="   Print montage information in the console")

        # tools for precut ###
        layout.separator()
        row = layout.row(align=True)
        row.label(text="Various:")

        row = layout.row(align=True)
        row.operator_context = "INVOKE_DEFAULT"
        row.operator("uas_shot_manager.predec_sort_versions_shots", text="   Sort Version Shots")


classes = (
    UAS_UL_ShotManager_Items,
    UAS_MT_ShotManager_Shots_ToolsMenu,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

