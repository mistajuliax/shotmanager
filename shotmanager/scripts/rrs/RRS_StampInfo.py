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


def setRRS_StampInfoSettings(scene):
    print(" -- * setRRS_StampInfoSettings * --")

    if bpy.context.scene.UAS_StampInfo_Settings is not None:

        props = scene.UAS_shot_manager_props

        stampInfoSettings = scene.UAS_StampInfo_Settings

        stampInfoSettings.stampInfoUsed = scene.UAS_shot_manager_props.useStampInfoDuringRendering

        if stampInfoSettings.stampInfoUsed:

            stampInfoSettings.tmp_usePreviousValues = True

            projProp_resolution_x = 1280
            stampInfoSettings.tmp_previousResolution_x = projProp_resolution_x  # scene.render.resolution_x
            projProp_resolution_y = 720

            stampInfoSettings.tmp_previousResolution_y = projProp_resolution_y  # scene.render.resolution_y
            # scene.render.resolution_x = 1280
            # scene.render.resolution_y = 960

            stampInfoSettings.tmp_stampRenderResYDirToCompo_percentage = (
                stampInfoSettings.stampRenderResYDirToCompo_percentage
            )
            stampInfoSettings.stampRenderResYDirToCompo_percentage = 75.0

            stampInfoSettings.tmp_stampInfoRenderMode = stampInfoSettings.stampInfoRenderMode
            stampInfoSettings.stampInfoRenderMode = "DIRECTTOCOMPOSITE"

            stampInfoSettings.stampPropertyLabel = False
            stampInfoSettings.stampPropertyValue = True

            stampInfoSettings.automaticTextSize = False
            stampInfoSettings.extPaddingNorm = 0.020
            stampInfoSettings.fontScaleHNorm = 0.0168
            stampInfoSettings.interlineHNorm = 0.0072

            # top
            stampInfoSettings.logoUsed = True
            stampInfoSettings.logoBuiltinName = "RRSpecial_Logo.png"
            stampInfoSettings.logoScaleH = 0.05
            stampInfoSettings.logoPosNormX = 0.018
            stampInfoSettings.logoPosNormY = 0.014

            projProp_Name = props.project_name
            stampInfoSettings.projectName = projProp_Name
            stampInfoSettings.projectUsed = False

            stampInfoSettings.dateUsed = True
            stampInfoSettings.timeUsed = True

            stampInfoSettings.videoDurationUsed = True

            stampInfoSettings.videoFrameUsed = True
            stampInfoSettings.videoRangeUsed = True
            stampInfoSettings.videoHandlesUsed = True

            stampInfoSettings.edit3DFrameUsed = True
            # stampInfoSettings.edit3DFrame = props.     # set in the render loop
            stampInfoSettings.edit3DTotalNumberUsed = True
            # stampInfoSettings.edit3DTotalNumber = props.getEditDuration()

            stampInfoSettings.framerateUsed = True

            # bottom
            stampInfoSettings.sceneUsed = True
            stampInfoSettings.takeUsed = True
            #  stampInfoSettings.shotName       = shotName
            stampInfoSettings.shotUsed = True
            stampInfoSettings.cameraUsed = True
            stampInfoSettings.cameraLensUsed = True

            stampInfoSettings.shotDurationUsed = False

            stampInfoSettings.filenameUsed = True
            stampInfoSettings.filepathUsed = True

            stampInfoSettings.currentFrameUsed = True
            stampInfoSettings.frameRangeUsed = True
            stampInfoSettings.frameHandlesUsed = True
            # stampInfoSettings.shotHandles = props.handles

            stampInfoSettings.debug_DrawTextLines = False


#############
# wkip clean: not used anymore?

# def set_StampInfoShotSettings(
#     scene,
#     shotName,
#     takeName,
#     # shot.notes,
#     cameraName,
#     cameraLens,
#     edit3DFrame=-1,
#     edit3DTotalNumber=-1,
# ):

#     stampInfoSettings = scene.UAS_StampInfo_Settings
#     stampInfoSettings.shotName = shotName
#     stampInfoSettings.takeName = takeName
#     stampInfoSettings.edit3DFrame = edit3DFrame
#     stampInfoSettings.edit3DTotalNumber = edit3DTotalNumber

#############
# wkip clean: not used anymore?

# def setRRSRenderFromShotManager(scene, shotName):
#     print(" -- * setRRSRenderFromShotManager * --")

#     # stampInfoSettings = bpy.context.scene.UAS_StampInfo_Settings

#     setRRS_StampInfoSettings(scene, shotName)

#     bpy.ops.render.render("INVOKE_DEFAULT", animation=False, write_still=True)
#     #  bpy.ops.render.view_show()
#     #  bpy.ops.render.render(animation=True, use_viewport=True)

#     print(" --- RRS Render Finished ---")

#     bpy.context.scene.UAS_StampInfo_Settings.restorePreviousValues(scene)

#     print(" --- RRS Settings Restored ---")
