# SPDX-License-Identifier: GPL-3.0-or-later

import bpy


def load_rust_module():
    import os
    import sys
    import importlib

    current_dir = os.path.dirname(os.path.realpath(__file__))
    print(f"-------- DEBUG START --------")
    print(f"Addon Directory: {current_dir}")

    if current_dir not in sys.path:
        sys.path.append(current_dir)
        print(f"Added to sys.path: Yes")
    else:
        print(f"Added to sys.path: Already exists")

    files = os.listdir(current_dir)
    print(f"Files in directory: {files}")

    target_file = "my_rust_core.so"
    if target_file in files:
        print(f"✅ Found '{target_file}'!")
    else:
        print(f"❌ '{target_file}' NOT found in this list!")
        candidates = [f for f in files if "my_rust_core" in f]
        if candidates:
            print(f"⚠️  Did you mean one of these?: {candidates}")

    try:
        if "my_rust_core" in sys.modules:
            mod = importlib.reload(sys.modules["my_rust_core"])
        else:
            mod = importlib.import_module("my_rust_core")
        print("✅ Import Successful!")
        print(f"-------- DEBUG END --------")
        return mod
    except ImportError as e:
        print(f"❌ Import Failed: {e}")
        print(f"-------- DEBUG END --------")
        return None


rust_mod = load_rust_module()


class HelloOperator(bpy.types.Operator):
    bl_idname = "myaddon.hello"
    bl_label = "Say Hello"
    bl_description = "hello world message"

    def execute(self, context):
        if rust_mod:
            res = rust_mod.solve_heavy_math(100, 200)
            self.report({"INFO"}, f"with rust: {res}")
        else:
            self.report({"INFO"}, "rust not loaded")
        return {"FINISHED"}


def register():
    bpy.utils.register_class(HelloOperator)


def unregister():
    bpy.utils.unregister_class(HelloOperator)
