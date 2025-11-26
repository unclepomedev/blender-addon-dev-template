# blender-addon-dev-template

A minimal, production-ready template for creating Blender add-ons.

Use the repository below to instantly initialize a project structure based on this template: https://github.com/unclepomedev/blender-addon-dev-template-loader

## 📁 Project Structure

```bash
.
├─ addon_hello_world/        # Blender add-on source
│  ├─ __init__.py
│  ├─ blender_manifest.toml
│  ├─ *.py
│  └─ prefs.py
├─ tools/
│  └─ build_addon_zip.py     # Creates an installable ZIP
├─ tests/
│  ├─ unit/                  # Pure Python tests
│  └─ blender/               # Blender integration test
├─ .github/
│  └─ workflows/
│     └─ ci.yml              # Lint + test + zip build
├─ pyproject.toml            # uv-based dev environment
└─ README.md
```

### TEST

Separate tests into Blender-dependent and pure logic parts.
To enable testing of the logic layer, defer importing any modules that rely on bpy or its stubs.

You can run tests using `uv` tasks or `make`.

**Prerequisite**: To run integration tests, the `blender` command must be in your system PATH.
*(e.g. On macOS, you may need to add `/Applications/Blender.app/Contents/MacOS/Blender` to your PATH or alias it).*

**Run all tests (Unit + Integration):**
```bash
uv run poe test
# or
make test
```

**Run only Unit tests:**
```bash
uv run poe unit
# or
make unit
```

**Run only Blender Integration tests:**
```bash
uv run poe test-blender
# or
make test-blender
```

### CI

In CI, run linting, execute Pytest, and generate a ZIP file that can be installed in Blender.

Blender is not included in the CI workflow because running Blender itself on GitHub Actions requires heavy setup, varies
by platform, and provides little benefit for this template.
Logic tests run without Blender are sufficient, and actual Blender execution should be validated locally.
(Depending on project requirements, adding Blender execution to CI may still be appropriate.)

### LICENSE

Add-ons
are [recommended](https://docs.blender.org/manual/en/latest/advanced/extensions/licenses.html) to be licensed under GPL
v3 or later.
This repository provides an example of publishing a Blender add-on under a compatible license, GPL v3 or later, using
the SPDX format.
