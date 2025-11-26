.PHONY: test unit test-blender

# Run all tests (unit + blender integration)
test:
	uv run poe test

# Run only unit tests
unit:
	uv run poe unit

# Run only blender integration tests
# Requires 'blender' command to be in PATH
test-blender:
	uv run poe test-blender
