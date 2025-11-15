# SPDX-License-Identifier: GPL-3.0-or-later

import bpy


class HwAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__  # "addon_hello_world"

    sample_text: bpy.props.StringProperty(
        name="Sample Text",
        default="Hello",
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "sample_text")


def register():
    bpy.utils.register_class(HwAddonPreferences)


def unregister():
    bpy.utils.unregister_class(HwAddonPreferences)
