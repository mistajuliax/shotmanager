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

from bpy.types import PropertyGroup
from bpy.props import StringProperty, IntProperty, BoolProperty, PointerProperty, FloatVectorProperty

import logging

_logger = logging.getLogger(__name__)


class UAS_ShotManager_OutputParams_Resolution(PropertyGroup):
    def copyPropertiesFrom(self, source):
        """
        Copy properties from the specified source to this one
        """
        self.resolution_x = source.resolution_x
        self.resolution_y = source.resolution_y
        self.resolution_framed_x = source.resolution_framed_x
        self.resolution_framed_y = source.resolution_framed_y

        self.useStampInfoDuringRendering = source.useStampInfoDuringRendering

    def _update_resolution(self, context):
        props = bpy.context.scene.UAS_shot_manager_props
        if (
            props is not None
            and self == props.getCurrentTake().outputParams_Resolution
        ):
            props.setResolutionToScene()

    resolution_x: IntProperty(name="Res. X", min=0, default=1280, update=_update_resolution)
    resolution_y: IntProperty(name="Res. Y", min=0, default=720, update=_update_resolution)
    resolution_framed_x: IntProperty(name="Res. Framed X", min=0, default=1280)
    resolution_framed_y: IntProperty(name="Res. Framed Y", min=0, default=960)

    def get_useStampInfoDuringRendering(self):
        # print("*** get_useStampInfoDuringRendering: value: ", val)
        return self.get("useStampInfoDuringRendering", True)

    def set_useStampInfoDuringRendering(self, value):
        print("*** set_useStampInfoDuringRendering: value: ", value)
        self["useStampInfoDuringRendering"] = value

        if getattr(bpy.context.scene, "UAS_StampInfo_Settings", None) is not None:
            # bpy.context.scene.UAS_StampInfo_Settings.activateStampInfo(value)
            bpy.context.scene.UAS_StampInfo_Settings.stampInfoUsed = value

    useStampInfoDuringRendering: BoolProperty(
        name="Stamp Info on Output",
        description="Stamp render information on rendered images thanks to Stamp Info add-on",
        default=True,
        get=get_useStampInfoDuringRendering,  # removed cause the use of Stamp Info in this add-on is independent from the one of Stamp Info add-on itself
        set=set_useStampInfoDuringRendering,
        options=set(),
    )

    def draw(self, context, ui_component):
        row = ui_component.row(align=False)
        row.use_property_split = False
        row.alignment = "RIGHT"
        row.label(text="Resolution")
        row.prop(self, "resolution_x", text="Width:")
        row.prop(self, "resolution_y", text="Height:")

        row = ui_component.row(align=False)
        row.use_property_split = False
        row.alignment = "RIGHT"
        row.label(text="Frame Resolution")
        row.prop(self, "resolution_framed_x", text="Width:")
        row.prop(self, "resolution_framed_y", text="Height:")

        stampInfoStr = "Use Stamp Info Add-on"
        # if not props.isStampInfoAvailable():
        #     stampInfoStr += "  (Warning: Currently NOT installed)"
        ui_component.prop(self, "useStampInfoDuringRendering", text=stampInfoStr)
