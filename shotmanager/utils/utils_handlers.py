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

# -*- coding: utf-8 -*-

# werwack 2020/05/14
# V 1.0.0

import bpy


# Eg: wkutils_handlers.displayHandlers( handlerCategName = "render_init" )
def displayHandlers(handlerCategName=""):
    handlerCat = handlerCategName

    def _displayHandlersOfCateg(hCategName):
        print(f"  {hCategName}:")

        if hCategName == "depsgraph_update_post":
            for h in bpy.app.handlers.depsgraph_update_post:
                print(f"     {h.__name__}")
        elif hCategName == "depsgraph_update_pre":
            for h in bpy.app.handlers.depsgraph_update_pre:
                print(f"     {h.__name__}")
        elif hCategName == "frame_change_post":
            for h in bpy.app.handlers.frame_change_post:
                print(f"     {h.__name__}")
        elif hCategName == "frame_change_pre":
            for h in bpy.app.handlers.frame_change_pre:
                print(f"     {h.__name__}")
        elif hCategName == "load_factory_preferences_post":
            for h in bpy.app.handlers.load_factory_preferences_post:
                print(f"     {h.__name__}")
        elif hCategName == "load_factory_startup_post":
            for h in bpy.app.handlers.load_factory_startup_post:
                print(f"     {h.__name__}")
        elif hCategName == "load_post":
            for h in bpy.app.handlers.load_post:
                print(f"     {h.__name__}")
        elif hCategName == "load_pre":
            for h in bpy.app.handlers.load_pre:
                print(f"     {h.__name__}")
        elif hCategName == "redo_post":
            for h in bpy.app.handlers.redo_post:
                print(f"     {h.__name__}")
        elif hCategName == "redo_pre":
            for h in bpy.app.handlers.redo_pre:
                print(f"     {h.__name__}")
        elif hCategName == "render_cancel":
            for h in bpy.app.handlers.render_cancel:
                print(f"     {h.__name__}")
        elif hCategName == "render_complete":
            for h in bpy.app.handlers.render_complete:
                print(f"     {h.__name__}")
        elif hCategName == "render_init":
            for h in bpy.app.handlers.render_init:
                print(f"     {h.__name__}")
        elif hCategName == "render_post":
            for h in bpy.app.handlers.render_post:
                print(f"     {h.__name__}")
        elif hCategName == "render_pre":
            for h in bpy.app.handlers.render_pre:
                print(f"     {h.__name__}")
        elif hCategName == "render_stats":
            for h in bpy.app.handlers.render_stats:
                print(f"     {h.__name__}")
        elif hCategName == "render_write":
            for h in bpy.app.handlers.render_write:
                print(f"     {h.__name__}")
        elif hCategName == "save_post":
            for h in bpy.app.handlers.save_post:
                print(f"     {h.__name__}")
        elif hCategName == "save_pre":
            for h in bpy.app.handlers.save_pre:
                print(f"     {h.__name__}")
        elif hCategName == "undo_post":
            for h in bpy.app.handlers.undo_post:
                print(f"     {h.__name__}")
        elif hCategName == "undo_pre":
            for h in bpy.app.handlers.undo_pre:
                print(f"     {h.__name__}")
        elif hCategName == "version_update":
            for h in bpy.app.handlers.version_update:
                print(f"     {h.__name__}")

    print("\nCurrent registered handlers:")
    print("-----------------------------")

    if "" == handlerCat:
        _displayHandlersOfCateg("depsgraph_update_post")
        _displayHandlersOfCateg("depsgraph_update_pre")
        _displayHandlersOfCateg("frame_change_post")
        _displayHandlersOfCateg("frame_change_pre")
        _displayHandlersOfCateg("load_factory_preferences_post")
        _displayHandlersOfCateg("load_factory_startup_post")
        _displayHandlersOfCateg("load_post")
        _displayHandlersOfCateg("load_pre")
        _displayHandlersOfCateg("redo_post")
        _displayHandlersOfCateg("redo_pre")
        _displayHandlersOfCateg("render_cancel")
        _displayHandlersOfCateg("render_complete")
        _displayHandlersOfCateg("render_init")
        _displayHandlersOfCateg("render_post")
        _displayHandlersOfCateg("render_pre")
        _displayHandlersOfCateg("render_stats")
        _displayHandlersOfCateg("render_write")
        _displayHandlersOfCateg("save_post")
        _displayHandlersOfCateg("save_pre")
        _displayHandlersOfCateg("undo_post")
        _displayHandlersOfCateg("undo_pre")
        _displayHandlersOfCateg("version_update")

    else:
        _displayHandlersOfCateg(handlerCategName)

    print("")
    return


# eg: removeAllHandlerOccurences(bpy.app.handlers.render_init, wkhandlersops_renderInitHandlder)
def removeAllHandlerOccurences(handlerFunction, handlerCateg=None):
    handlerCat = handlerCateg

    if handlerCat is not None:
        i = 0
        while i < len(handlerCat):
            if handlerFunction.__name__ == handlerCat[i].__name__:
                handlerCat.remove(handlerCat[i])
            else:
                i += 1


# returns first occurence
# eg: getHandlerByFunction( wkhandlersops_renderInitHandlder, handlerCateg = bpy.app.handlers.render_init )
def getHandlerByFunction(handlerFunction, handlerCateg=None):
    """ returns the first occurence of the specified function found in the specified hanndler category
    """
    handlerCat = handlerCateg
    myHandlerFunc = None

    # search in all handler categories
    if handlerCat is not None:
        i = 0
        # while i < len(bpy.app.handlers.render_init) and myHandlerFunc is None:
        while i < len(handlerCateg) and myHandlerFunc is None:
            if handlerFunction.__name__ == handlerCateg[i].__name__:
                myHandlerFunc = handlerCateg[i]
            else:
                i += 1

    return myHandlerFunc
