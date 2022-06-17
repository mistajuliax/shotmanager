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
from bpy.types import Panel, Operator
from bpy.props import IntProperty, EnumProperty, BoolProperty, FloatProperty, StringProperty

from . import retimer


##########
# Retimer
##########


class UAS_PT_ShotManagerRetimer(Panel):
    bl_idname = "UAS_PT_ShotManagerRetimerPanel"
    bl_label = "Retimer"
    bl_description = "Manage the global timing of the action in the scene and the shots"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Shot Mng"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        props = context.scene.UAS_shot_manager_props
        return props.display_retimer_in_properties and not props.dontRefreshUI()

    def draw(self, context):

        retimerProps = context.scene.UAS_shot_manager_props.retimer

        layout = self.layout
        layout.prop(retimerProps, "mode")

        box = layout.box()

        row = box.row()
        row.separator(factor=0.1)
        # row = box.row()
        # row.separator(factor=1)
        # row.prop(retimerProps, "start_frame", text="Move Frame")
        # row.prop(retimerProps, "end_frame", text="To")

        # row.operator("uas_shot_manager.gettimerange", text="", icon="SEQ_STRIP_META")
        # row.separator(factor=1)

        if retimerProps.mode == "INSERT":
            row = box.row(align=True)
            row.separator(factor=1)

            row.prop(retimerProps, "start_frame", text="Insert After")
            row.operator(
                "uas_shot_manager.getcurrentframefor", text="", icon="TRIA_UP_BAR"
            ).propertyToUpdate = "start_frame"
            row.separator()

            row.prop(retimerProps, "insert_duration", text="Duration")
            row.separator(factor=1)

            row = box.row(align=True)
            newStart = retimerProps.start_frame
            newStartStr = f"Start: {retimerProps.start_frame} \u2192 {newStart}"
            newEnd = retimerProps.start_frame + 1 + retimerProps.insert_duration
            newEndStr = f"End: {retimerProps.start_frame + 1} \u2192 {newEnd}"
            newRangeStr = f"Duration: 0 fr \u2192 {retimerProps.insert_duration} fr"
            row.separator(factor=1)
            row.label(text=f"{newStartStr},      {newEndStr},      {newRangeStr}")
            row.separator(factor=1)

            # apply ###
            row = box.row()
            row.separator(factor=0.1)
            compo = layout.row()
            compo.separator(factor=2)
            compo.scale_y = 1.2
            compo.operator("uas_shot_manager.retimerapply", text="Insert")
            compo.separator(factor=2)

        elif retimerProps.mode == "DELETE":
            row = box.row(align=True)
            row.separator(factor=1)
            row.prop(retimerProps, "start_frame", text="Delete After")
            row.operator(
                "uas_shot_manager.getcurrentframefor", text="", icon="TRIA_UP_BAR"
            ).propertyToUpdate = "start_frame"
            row.separator()

            row.prop(retimerProps, "end_frame", text="Up To (excl.)")
            row.operator(
                "uas_shot_manager.getcurrentframefor", text="", icon="TRIA_UP_BAR"
            ).propertyToUpdate = "end_frame"

            #            row.operator("uas_shot_manager.gettimerange", text="", icon="SEQ_STRIP_META")
            row.separator(factor=1)

            row = box.row(align=True)
            newStart = retimerProps.start_frame
            newStartStr = f"Start: {retimerProps.start_frame} \u2192 {newStart}"
            newEnd = retimerProps.start_frame + 1
            newEndStr = f"End: {retimerProps.end_frame} \u2192 {newEnd}"
            newRangeStr = f"Duration: {retimerProps.end_frame - retimerProps.start_frame - 1} fr. \u2192 {newEnd - retimerProps.start_frame - 1} fr.,"
            row.separator(factor=1)
            row.label(text=f"{newStartStr},      {newEndStr},      {newRangeStr}")
            row.separator(factor=1)

            # apply ###
            row = box.row()
            row.separator(factor=0.1)
            compo = layout.row()
            compo.separator(factor=2)
            compo.scale_y = 1.2
            compo.operator("uas_shot_manager.retimerapply", text="Delete")
            compo.separator(factor=2)

        elif retimerProps.mode == "RESCALE":
            row = box.row(align=True)
            row.separator(factor=1)
            row.prop(retimerProps, "start_frame", text="Rescale After")
            row.operator(
                "uas_shot_manager.getcurrentframefor", text="", icon="TRIA_UP_BAR"
            ).propertyToUpdate = "start_frame"
            row.separator()

            row.prop(retimerProps, "end_frame", text="Up To (excl.)")
            row.operator(
                "uas_shot_manager.getcurrentframefor", text="", icon="TRIA_UP_BAR"
            ).propertyToUpdate = "end_frame"
            row.separator()

            # row.operator("uas_shot_manager.gettimerange", text="", icon="SEQ_STRIP_META")
            # row.separator(factor=1)

            row = box.row(align=True)

            row.separator(factor=2)
            row.label(text="")
            row.prop(retimerProps, "factor", text="Scale Factor")
            row.separator(factor=1)

            row = box.row(align=True)
            newStart = retimerProps.start_frame
            newStartStr = f"Start: {retimerProps.start_frame} \u2192 {newStart}"
            newEnd = round(
                (retimerProps.end_frame - retimerProps.start_frame) * retimerProps.factor + retimerProps.start_frame
            )
            newEndStr = f"End: {retimerProps.end_frame} \u2192 {newEnd}"
            newRangeStr = f"Duration: {retimerProps.end_frame - retimerProps.start_frame} fr. \u2192 {newEnd - retimerProps.start_frame} fr.,"
            row.separator(factor=1)
            row.label(text=f"{newStartStr},      {newEndStr},      {newRangeStr}")
            row.separator(factor=1)
            # row.prop(retimerProps, "pivot")

            # apply ###
            row = box.row()
            row.separator(factor=0.1)
            compo = layout.row()
            compo.separator(factor=2)
            compo.scale_y = 1.2
            compo.operator("uas_shot_manager.retimerapply", text="Rescale")
            compo.separator(factor=2)

        elif retimerProps.mode == "CLEAR_ANIM":
            row = box.row(align=True)
            row.separator(factor=1)
            row.prop(retimerProps, "start_frame", text="Clear After")
            row.operator(
                "uas_shot_manager.getcurrentframefor", text="", icon="TRIA_UP_BAR"
            ).propertyToUpdate = "start_frame"
            row.separator()

            row.prop(retimerProps, "end_frame", text="Up To (incl.)")
            row.operator(
                "uas_shot_manager.getcurrentframefor", text="", icon="TRIA_UP_BAR"
            ).propertyToUpdate = "end_frame"

            row.separator(factor=1)

            row = box.row(align=True)
            newStart = retimerProps.start_frame
            newStartStr = f"Start: {retimerProps.start_frame} \u2192 {newStart}"
            newEnd = retimerProps.end_frame
            newEndStr = f"End: {retimerProps.end_frame} \u2192 {newEnd}"
            newRangeStr = f"Duration: {retimerProps.end_frame - retimerProps.start_frame} fr.,"
            row.separator(factor=1)
            row.label(text=f"Animation in range  [ {newStart + 1},  {newEnd} ]  will be cleared,      {newRangeStr}")
            row.separator(factor=1)

            # apply ###
            row = box.row()
            row.separator(factor=0.1)
            compo = layout.row()
            compo.separator(factor=2)
            compo.scale_y = 1.2
            compo.operator("uas_shot_manager.retimerapply", text="Clear Animation")
            compo.separator(factor=2)

        elif retimerProps.mode == "MOVE":
            row = box.row()
            row.separator(factor=1)
            row.prop(retimerProps, "start_frame", text="Move Frame")
            row.prop(retimerProps, "end_frame", text="To")

            row.operator("uas_shot_manager.gettimerange", text="", icon="SEQ_STRIP_META")
            row.separator(factor=1)

            # apply ###
            row = box.row()
            row.separator(factor=0.1)
            compo = layout.row()
            compo.separator(factor=2)
            compo.scale_y = 1.2
            compo.operator("uas_shot_manager.retimerapply", text="Move")
            compo.separator(factor=2)


class UAS_PT_ShotManagerRetimer_Settings(Panel):
    bl_label = "Apply to"
    bl_idname = "UAS_PT_ShotManagerRetimer_SettingsPanel"
    bl_description = "Manage the global timing of the action in the scene and the shots"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Shot Mng"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "UAS_PT_ShotManagerRetimerPanel"

    def draw(self, context):
        retimerProps = context.scene.UAS_shot_manager_props.retimer

        layout = self.layout

        row = layout.row()
        row.prop(retimerProps, "onlyOnSelection", text="Selection Only")

        box = layout.box()
        col = box.column()
        row = col.row(align=True)
        row.prop(retimerProps, "applyToShots")
        row.prop(retimerProps, "applyToObjects")
        row.label(text=" ")

        row = col.row(align=True)
        row.prop(retimerProps, "applyToShapeKeys")
        row.prop(retimerProps, "applytToGreasePencil")
        row.prop(retimerProps, "applytToVSE")
        row = col.row(align=True)


class UAS_ShotManager_GetTimeRange(Operator):
    bl_idname = "uas_shot_manager.gettimerange"
    bl_label = "Get Time Range"
    bl_description = "Get current time range and use it for the time changes"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        retimerProps = context.scene.UAS_shot_manager_props.retimer
        scene = context.scene

        if scene.use_preview_range:
            retimerProps.start_frame = scene.frame_preview_start
            retimerProps.end_frame = scene.frame_preview_end
        else:
            retimerProps.start_frame = scene.frame_start
            retimerProps.end_frame = scene.frame_end

        return {"FINISHED"}


class UAS_ShotManager_GetCurrentFrameFor(Operator):
    bl_idname = "uas_shot_manager.getcurrentframefor"
    bl_label = "Get Current Frame"
    bl_description = "Use the current frame for the specifed component"
    bl_options = {"INTERNAL"}

    propertyToUpdate: StringProperty()

    def execute(self, context):
        scene = context.scene
        props = scene.UAS_shot_manager_props
        retimerProps = props.retimer

        currentFrame = scene.frame_current

        if self.propertyToUpdate == "start_frame":
            retimerProps.start_frame = currentFrame
        elif self.propertyToUpdate == "end_frame":
            retimerProps.end_frame = currentFrame
        else:
            retimerProps[self.propertyToUpdate] = currentFrame

        return {"FINISHED"}


class UAS_ShotManager_RetimerApply(Operator):
    bl_idname = "uas_shot_manager.retimerapply"
    bl_label = "Apply Retime"
    bl_description = "Apply retime"
    bl_options = {"UNDO"}

    def execute(self, context):
        retimerProps = context.scene.UAS_shot_manager_props.retimer
        # wkip wkip wkip temp
        applToVSE = setattr(retimerProps, "applyToVse", True)

        if retimerProps.onlyOnSelection:
            obj_list = context.selected_objects
        else:
            obj_list = context.scene.objects

        startFrame = retimerProps.start_frame
        endFrame = retimerProps.end_frame

        # wkip travail en cours
        if retimerProps.mode == "INSERT":

            print(" start frame for Insert: ", startFrame)

            retimer.retimeScene(
                context.scene,
                retimerProps.mode,
                obj_list,
                startFrame + 1,
                retimerProps.insert_duration,
                retimerProps.gap,
                1.0,
                retimerProps.pivot,
                retimerProps.applyToObjects,
                retimerProps.applyToShapeKeys,
                retimerProps.applytToGreasePencil,
                retimerProps.applyToShots,
                retimerProps.applyToVse,
            )
        elif retimerProps.mode == "DELETE":
            retimer.retimeScene(
                context.scene,
                retimerProps.mode,
                obj_list,
                startFrame + 1,
                endFrame - startFrame - 1,
                True,
                1.0,
                retimerProps.pivot,
                retimerProps.applyToObjects,
                retimerProps.applyToShapeKeys,
                retimerProps.applytToGreasePencil,
                retimerProps.applyToShots,
                retimerProps.applyToVse,
            )
        elif retimerProps.mode == "RESCALE":
            retimer.retimeScene(
                context.scene,
                retimerProps.mode,
                obj_list,
                startFrame,
                endFrame - startFrame,
                True,
                retimerProps.factor,
                startFrame,
                retimerProps.applyToObjects,
                retimerProps.applyToShapeKeys,
                retimerProps.applytToGreasePencil,
                retimerProps.applyToShots,
                retimerProps.applyToVse,
            )
        elif retimerProps.mode == "CLEAR_ANIM":
            retimer.retimeScene(
                context.scene,
                retimerProps.mode,
                obj_list,
                startFrame + 1,
                endFrame - startFrame,
                False,
                retimerProps.factor,
                retimerProps.pivot,
                retimerProps.applyToObjects,
                retimerProps.applyToShapeKeys,
                retimerProps.applytToGreasePencil,
                False,
                retimerProps.applyToVse,
            )
        else:
            retimer.retimer(
                context.scene,
                retimerProps.mode,
                obj_list,
                startFrame,
                endFrame,
                retimerProps.gap,
                retimerProps.factor,
                retimerProps.pivot,
                retimerProps.applyToObjects,
                retimerProps.applyToShapeKeys,
                retimerProps.applytToGreasePencil,
                retimerProps.applyToShots,
                retimerProps.applyToVse,
            )

        context.area.tag_redraw()
        # context.region.tag_redraw()
        bpy.ops.wm.redraw_timer(type="DRAW_WIN_SWAP", iterations=1)

        if retimerProps.move_current_frame and retimerProps.mode == "INSERT":
            context.scene.frame_current = context.scene.frame_current + (
                retimerProps.end_frame - retimerProps.start_frame
            )

        return {"FINISHED"}


_classes = (
    UAS_PT_ShotManagerRetimer,
    #    UAS_Retimer_Properties,
    UAS_PT_ShotManagerRetimer_Settings,
    UAS_ShotManager_GetTimeRange,
    UAS_ShotManager_GetCurrentFrameFor,
    UAS_ShotManager_RetimerApply,
)


def register():
    for cls in _classes:
        bpy.utils.register_class(cls)

    # bpy.types.WindowManager.UAS_Retimer = PointerProperty(type=UAS_Retimer_Properties)


def unregister():
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)

    # del bpy.types.WindowManager.UAS_Retimer
