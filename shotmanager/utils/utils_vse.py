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

import os
import bpy


###################
# sequence editor
###################


# wkip works but applies the modifs on every sequence editor occurence of the file
# applies to the current workspace
def showSecondsInVSE(showSeconds, workspace=None):
    # startup_blend = os.path.join(
    #     bpy.utils.resource_path("LOCAL"),
    #     "scripts",
    #     "startup",
    #     "bl_app_templates_system",
    #     "Video_Editing",
    #     "startup.blend",
    # )

    # if "Video Editing" not in bpy.data.workspaces:
    #     bpy.ops.workspace.append_activate(idname="Video Editing", filepath=startup_blend)

    # if "Video Editing" not in bpy.data.workspaces:
    #     print(f"*** showSecondsInVSE: Video Editing workspace not found ***")

    if workspace is None:
        workspace = bpy.context.workspace

    #   edSeqWksp = bpy.data.workspaces["Video Editing"]
    for screen in workspace.screens:
        #   print(f"Screen type: {screen.name}")
        for area in screen.areas:
            #      print(f"Area type: {area.type}")
            if area.type == "SEQUENCE_EDITOR":
                #         print("Area seq ed")
                override = bpy.context.copy()
                override["area"] = area
                override["region"] = area.regions[-1]

                for space_data in area.spaces:
                    if space_data.type == "SEQUENCE_EDITOR":
                        space_data.show_seconds = showSeconds


###################
# vse sequences
###################


def clearChannel(scene, channelIndex):
    sequencesList = [
        seq
        for seq in scene.sequence_editor.sequences
        if channelIndex == seq.channel
    ]

    for seq in sequencesList:
        scene.sequence_editor.sequences.remove(seq)
    bpy.ops.sequencer.refresh_all()


def clearAllChannels(scene):
    for seq in scene.sequence_editor.sequences:
        scene.sequence_editor.sequences.remove(seq)
    bpy.ops.sequencer.refresh_all()


def getChannelClips(scene, channelIndex):
    return [
        seq
        for seq in scene.sequence_editor.sequences
        if channelIndex == seq.channel
    ]


def getNumUsedChannels(scene):
    numChannels = 0
    for seq in scene.sequence_editor.sequences:
        numChannels = max(seq.channel, numChannels)
    return numChannels


def changeClipsChannel(scene, sourceChannelIndex, targetChannelIndex):
    sourceSequencesList = getChannelClips(scene, sourceChannelIndex)
    targetSequencesList = []

    if len(sourceSequencesList):
        targetSequencesList = getChannelClips(scene, targetChannelIndex)

        # we need to clear the target channel before doing the switch otherwise some clips may get moved to another channel
        if len(targetSequencesList):
            clearChannel(scene, targetChannelIndex)

        for clip in sourceSequencesList:
            clip.channel = targetChannelIndex

    return targetSequencesList


def swapChannels(scene, channelIndexA, channelIndexB):
    tempChannelInd = 0
    changeClipsChannel(scene, channelIndexA, tempChannelInd)
    changeClipsChannel(scene, channelIndexB, channelIndexA)
    changeClipsChannel(scene, tempChannelInd, channelIndexB)


def muteChannel(scene, channelIndex, mute):
    if scene.sequence_editor is not None:
        for seq in scene.sequence_editor.sequences:
            if channelIndex == seq.channel:
                seq.mute = mute


def setChannelAlpha(scene, channelIndex, alpha):
    """Alpha is in range [0, 1]
    """
    channelClips = getChannelClips(scene, channelIndex)
    for clip in channelClips:
        clip.blend_alpha = alpha


def setChannelVolume(scene, channelIndex, volume):
    """Volume is in range [0, 10 or above]
    """
    channelClips = getChannelClips(scene, channelIndex)
    for clip in channelClips:
        clip.volume = volume

