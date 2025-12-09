# Path to Blender executable
# macOS
blender_exe := '/Applications/Blender.app/Contents/MacOS/Blender'
# Windows
# blender_exe := 'C:\Program Files\Blender Foundation\Blender 4.2\blender.exe'
# Linux
# blender_exe := '/usr/bin/blender'

# Run all tests (unit + blender integration)
test: unit test-blender

# Run only unit tests
unit:
    uv run poe unit

# Run E2E tests in Blender
test-blender:
    "{{blender_exe}}" --factory-startup -b -P tests/blender/test_in_blender.py


name := "my_rust_core"
dest := "addon_hello_world"

build:
    cargo build --release
    cp target/release/lib{{name}}.dylib {{dest}}/{{name}}.so

clean:
    cargo clean
    rm {{dest}}/{{name}}.so