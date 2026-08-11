# To install Just, see: https://github.com/casey/just#installation

set positional-arguments := true

# Default recipe that runs if you type "just".
default: format check test

# Install dependencies for local development and generate the test protos.
install: && gen-protos
    uv sync

# Regenerate the gitignored test proto gencode (needed before running tests).
gen-protos:
    uv run python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. proto_matcher/testdata/test.proto

format:
    uv run ruff format
    uv run ruff check --fix-only

check:
    uv lock --check
    uv run ruff format --check
    uv run ruff check
    uv run pyright
    uv run deptry .

test *ARGS=".":
    uv run pytest {{ARGS}}
