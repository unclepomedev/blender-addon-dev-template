# SPDX-License-Identifier: GPL-3.0-or-later

from . import hello_operator, hello_ui_panel

modules = (hello_operator, hello_ui_panel)


def register():
    for m in modules:
        m.register()


def unregister():
    for m in reversed(modules):
        m.unregister()
