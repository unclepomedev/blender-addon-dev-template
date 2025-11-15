# blender-addon-dev-template

A minimal, production-ready template for creating Blender add-ons.

### LICENSE

Add-ons
are [recommended](https://docs.blender.org/manual/en/latest/advanced/extensions/licenses.html) to be licensed under GPL
v3 or later.
This repository provides an example of publishing a Blender add-on under a compatible license, GPL v3 or later, using
the SPDX format.

### TEST

Separate tests into Blender-dependent and pure logic parts.
To enable testing of the logic layer, defer importing any modules that rely on bpy or its stubs.

The tests under tests/blender are executed within a Blender environment.
For example, on macOS you can run them with the following command:

```bash
/Applications/Blender.app/Contents/MacOS/Blender \
  --background --factory-startup --python tests/blender/test_in_blender.py
```

The tests under `tests/unit` can be executed independently of Blender.
Just like typical Python tests, you can run them after performing an editable install, for example:

```bash
uv pip install -e .
uv run pytest
```

### CI

TODO
