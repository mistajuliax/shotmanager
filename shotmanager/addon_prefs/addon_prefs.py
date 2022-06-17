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
from bpy.types import AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty, EnumProperty

from ..config import config

from .addon_prefs_ui import draw_shotmanager_addon_prefs


class UAS_ShotManager_AddonPrefs(AddonPreferences):
    """
        Use this to get these prefs:
        prefs = context.preferences.addons["shotmanager"].preferences
    """

    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package
    bl_idname = "shotmanager"

    ########################################################################
    # general ###
    ########################################################################

    # ****** settings exposed to the user in the prefs panel:
    # ------------------------------

    new_shot_duration: IntProperty(
        min=0, default=50,
    )

    # ****** hidden settings:
    # ------------------------------

    take_properties_extended: BoolProperty(
        name="Extend Take Properties", default=False,
    )
    take_notes_extended: BoolProperty(
        name="Extend Take Notes", default=False,
    )

    shot_properties_extended: BoolProperty(
        name="Extend Shot Properties", default=True,
    )
    shot_notes_extended: BoolProperty(
        name="Extend Shot Notes", default=False,
    )
    shot_cameraBG_extended: BoolProperty(
        name="Extend Shot Camera BG", default=False,
    )
    shot_greasepencil_extended: BoolProperty(
        name="Extend Shot Grease Pencil", default=False,
    )

    current_shot_changes_current_time: BoolProperty(
        name="Set Current Frame To Shot Start When Current Shot Is Changed", description="", default=True,
    )
    current_shot_changes_time_range: BoolProperty(
        name="Set Time Range To Shot Range When Current Shot Is Changed", description="", default=False,
    )

    playblastFileName: StringProperty(name="Temporary Playblast File", default="toto.mp4")

    # def _get_useLockCameraView(self):
    #     # Can also use area.spaces.active to get the space assoc. with the area
    #     for area in bpy.context.screen.areas:
    #         if area.type == "VIEW_3D":
    #             for space in area.spaces:
    #                 if space.type == "VIEW_3D":
    #                     realVal = space.lock_camera

    #     # not used, normal it's the fake property
    #     self.get("useLockCameraView", realVal)

    #     return realVal

    # def _set_useLockCameraView(self, value):
    #     self["useLockCameraView"] = value
    #     for area in bpy.context.screen.areas:
    #         if area.type == "VIEW_3D":
    #             for space in area.spaces:
    #                 if space.type == "VIEW_3D":
    #                     space.lock_camera = value

    # # fake property: value never used in itself, its purpose is to update ofher properties
    # useLockCameraView: BoolProperty(
    #     name="Lock Cameras to View",
    #     description="Enable view navigation within the camera view",
    #     get=_get_useLockCameraView,
    #     set=_set_useLockCameraView,
    #     # update=_update_useLockCameraView,
    #     options=set(),
    # )

    ########################################################################
    # rendering ui   ###
    ########################################################################

    # ****** settings exposed to the user in the prefs panel:
    # ------------------------------

    separatedRenderPanel: BoolProperty(
        name="Separated Render Panel",
        description="If checked, the render panel will be a tab separated from Shot Manager panel",
        default=True,
    )

    # ****** hidden settings:
    # ------------------------------

    renderMode: EnumProperty(
        name="Display Shot Properties Mode",
        description="Update the content of the Shot Properties panel either on the current shot\nor on the shot selected in the shots list",
        items=(
            ("STILL", "Still", ""),
            ("ANIMATION", "Animation", ""),
            ("ALL", "All Edits", ""),
            ("OTIO", "OTIO", ""),
            ("PLAYBLAST", "PLAYBLAST", ""),
        ),
        default="STILL",
    )

    ########################################################################
    # tools ui   ###
    ########################################################################

    toggleShotsEnabledState: BoolProperty(name=" ", default=False)

    ##################
    # shots features #
    ##################
    toggleCamsBG: BoolProperty(name=" ", default=False)
    toggleCamsSoundBG: BoolProperty(name=" ", default=False)
    toggleGreasePencil: BoolProperty(name=" ", default=False)

    ##################
    # ui helpers   ###
    ##################

    # used for example as a placehoder in VSM to have a text field when no strip is selected
    emptyField: StringProperty(name=" ")
    emptyBool: BoolProperty(name=" ", default=False)

    ##################
    # add new shot ###
    ##################

    def _get_addShot_start(self):
        return self.get("addShot_start", 25)

    # *** behavior here must match the one of start and end of shot properties ***
    def _set_addShot_start(self, value):
        self["addShot_start"] = value
        # increase end value if start is superior to end
        # if self.addShot_start > self.addShot_end:
        #     self["addShot_end"] = self.addShot_start

        # prevent start to go above end (more user error proof)
        if self.addShot_start > self.addShot_end:
            self["addShot_start"] = self.addShot_end

    addShot_start: IntProperty(
        name="Add Shot Start UI Only", soft_min=0, get=_get_addShot_start, set=_set_addShot_start, default=25,
    )

    def _get_addShot_end(self):
        return self.get("addShot_end", 30)

    # *** behavior here must match the one of start and end of shot properties ***
    def _set_addShot_end(self, value):
        self["addShot_end"] = value
        # reduce start value if end is lowr than start
        # if self.addShot_start > self.addShot_end:
        #    self["addShot_start"] = self.addShot_end

        # prevent end to go below start (more user error proof)
        if self.addShot_start > self.addShot_end:
            self["addShot_end"] = self.addShot_start

    addShot_end: IntProperty(
        name="Add Shot End UI Only", soft_min=0, get=_get_addShot_end, set=_set_addShot_end, default=50,
    )

    ##################
    # global temps values   ###
    ##################

    # Playblast
    ####################

    ##################
    # markers ###
    ##################

    mnavbar_use_filter: BoolProperty(
        name="Filter Markers", default=False,
    )

    mnavbar_filter_text: StringProperty(
        name="Filter Text", default="",
    )

    ##################################################################################
    # Draw
    ##################################################################################
    def draw(self, context):
        draw_shotmanager_addon_prefs(self, context)


_classes = (UAS_ShotManager_AddonPrefs,)


def register():
    for cls in _classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
