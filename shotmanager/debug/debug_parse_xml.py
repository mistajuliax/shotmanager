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

print("debug_parse_xml.py")


# from xml.dom import minidom

# doc = minidom.parse(r"Z:\EvalSofts\Blender\DevPython_Data\XML\Act01_Seq0060_Main_Take_ModifsSwap.xml")

# # doc.getElementsByTagName returns NodeList
# name = doc.getElementsByTagName("sequence")
# print(f"name: {name}")
# # print(f"name: {name.firstChild.data}")

# import xml.etree.ElementTree as ET

# tree = ET.parse(filename)
# root = tree.getroot()
# print(f"root: {root}")
# # print(f"root.tagName: {root.nodeName()}")

# children = doc.childNodes()
# print(f"children: {children}")

# # formatElems = root.getElementsByTagName("format")
# # print(f"roformatElemsot: {formatElems}")


def _getFirstChildWithName(parentNode, name):
    return next(
        (node for node in parentNode.childNodes if name == node.localName),
        None,
    )


readFile = False

from xml.dom.minidom import parse

# seq.tagName
#'sequence'

# media = seq.getElementsByTagName("media")
# mediaVideo = media.getElementsByTagName("video")
# mediaVideoFormat = mediaVideo.getElementsByTagName("format")

seqMedia = None
seqMediaVideo = None
seqMediaVideoFormat = None
videoSampleCharacteristics = None

if readFile:

    filename = r"Z:\EvalSofts\Blender\DevPython_Data\XML\Act01_Seq0060_Main_Take_ModifsSwap.xml"

    dom1 = parse(filename)

    seq = dom1.getElementsByTagName("sequence")[0]
    seqCharacteristics = {}

    for node in seq.childNodes:
        print(f"media - node.localName: {node.localName}")
        if node.localName == "media":
            seqMedia = node
            break

    if seqMedia is not None:
        for node in seqMedia.childNodes:
            print(f"video - node.localName: {node.localName}")
            if node.localName == "video":
                seqMediaVideo = node
                break

    if seqMediaVideo is not None:
        for node in seqMediaVideo.childNodes:
            print(f"format - node.localName: {node.localName}")
            if node.localName == "format":
                seqMediaVideoFormat = node
                break

    if seqMediaVideoFormat is not None:
        for node in seqMediaVideoFormat.childNodes:
            print(f"samplecharacteristics - node.localName: {node.localName}")
            if node.localName == "samplecharacteristics":
                videoSampleCharacteristics = node
                break

    print(f"videoSampleCharacteristics: {videoSampleCharacteristics}")

    if videoSampleCharacteristics is not None:
        # elem = videoSampleCharacteristics.getElementsByTagName("width")
        elem = None

        # for node in videoSampleCharacteristics.childNodes:
        #     print(f"videoSampleCharacteristics - node.localName: {node.localName}")
        #     if "width" == node.localName:
        #         elem = node
        #         break
        #  print(f"elem: {elem}")

        seqRate = _getFirstChildWithName(videoSampleCharacteristics, "rate")

        seqRateDict = {
            "timebase": float(_getFirstChildWithName(seqRate, "timebase").childNodes[0].nodeValue),
            "ntsc": _getFirstChildWithName(seqRate, "ntsc").childNodes[0].nodeValue,
        }

        seqCharacteristics["rate"] = seqRateDict
        seqCharacteristics["width"] = int(
            _getFirstChildWithName(videoSampleCharacteristics, "width").childNodes[0].nodeValue
        )
        seqCharacteristics["height"] = int(
            _getFirstChildWithName(videoSampleCharacteristics, "height").childNodes[0].nodeValue
        )
        seqCharacteristics["anamorphic"] = (
            _getFirstChildWithName(videoSampleCharacteristics, "anamorphic").childNodes[0].nodeValue
        )
        seqCharacteristics["pixelaspectratio"] = (
            _getFirstChildWithName(videoSampleCharacteristics, "pixelaspectratio").childNodes[0].nodeValue
        )
        seqCharacteristics["fielddominance"] = (
            _getFirstChildWithName(videoSampleCharacteristics, "fielddominance").childNodes[0].nodeValue
        )
        seqCharacteristics["colordepth"] = int(
            _getFirstChildWithName(videoSampleCharacteristics, "colordepth").childNodes[0].nodeValue
        )
        # seqCharacteristics["width"] = elem.nodeValue
        # print(f"width: {seqCharacteristics['width']}")
        print(f"seqCharacteristics: {seqCharacteristics}")

else:  # write to file

    filename = r"Z:\EvalSofts\Blender\DevPython_Data\XML\Act01_Seq0060_Main_Take_FromPublish-Copie.xml"
    dom1 = parse(filename)

    seq = dom1.getElementsByTagName("sequence")[0]

    videoCharacteristics = {}

    seqMedia = _getFirstChildWithName(seq, "media")
    if seqMedia is not None:
        seqMediaVideo = _getFirstChildWithName(seqMedia, "video")
        print(f"seqMediaVideo: {seqMediaVideo}")

        newNodeFormat = dom1.createElement("format")
        newNodeCharact = dom1.createElement("samplecharacteristics")
        newNodeFormat.appendChild(newNodeCharact)

        newNodeRate = dom1.createElement("rate")

        newNodeTimebase = dom1.createElement("timebase")
        nodeText = dom1.createTextNode("46")
        newNodeTimebase.appendChild(nodeText)
        newNodeRate.appendChild(newNodeTimebase)
        newNodeNtsc = dom1.createElement("ntsc")
        nodeText = dom1.createTextNode("FALSE")
        newNodeNtsc.appendChild(nodeText)
        newNodeRate.appendChild(newNodeNtsc)

        newNodeCharact.appendChild(newNodeRate)

        newNode = dom1.createElement("width")
        nodeText = dom1.createTextNode("1280")
        newNode.appendChild(nodeText)
        newNodeCharact.appendChild(newNode)

        newNode = dom1.createElement("height")
        nodeText = dom1.createTextNode("960")
        newNode.appendChild(nodeText)
        newNodeCharact.appendChild(newNode)

        newNode = dom1.createElement("anamorphic")
        nodeText = dom1.createTextNode("FALSE")
        newNode.appendChild(nodeText)
        newNodeCharact.appendChild(newNode)

        newNode = dom1.createElement("square")
        nodeText = dom1.createTextNode("FALSE")
        newNode.appendChild(nodeText)
        newNodeCharact.appendChild(newNode)

        newNode = dom1.createElement("fielddominance")
        nodeText = dom1.createTextNode("none")
        newNode.appendChild(nodeText)
        newNodeCharact.appendChild(newNode)

        newNode = dom1.createElement("colordepth")
        nodeText = dom1.createTextNode("24")
        newNode.appendChild(nodeText)
        newNodeCharact.appendChild(newNode)

        seqMediaVideo.insertBefore(newNodeFormat, seqMediaVideo.firstChild)

    # print(f"dom1.toxml(): {dom1.toprettyxml()}")
    print(f"dom1.toxml(): {dom1.toxml()}")

    # file_handle = open(filename, "w")

    # dom1.writexml(file_handle)
    # # print(f"dom1.toxml(): {dom1.toxml()}")
    # # file_handle.write(dom1.toxml())

    dom1.unlink()

    # file_handle.close()
