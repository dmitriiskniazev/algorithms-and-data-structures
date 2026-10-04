.PHONY: help setup setup-cpp setup-python test test-cpp test-python format-cpp check-format-cpp docs clean

BUILD_DIR ?= build/cpp
CMAKE_GENERATOR ?= Ninja
CXX_COMPILER ?= $(shell if command -v clang-scan-deps >/dev/null 2>&1; then command -v clang++; elif test -x /opt/homebrew/opt/llvm/bin/clang++ && test -x /opt/homebrew/opt/llvm/bin/clang-scan-deps; then printf '%s' /opt/homebrew/opt/llvm/bin/clang++; else command -v clang++; fi)
LLVM_BIN := $(dir $(CXX_COMPILER))

help:
	@printf '%s\n' 'setup          Set up Python dependencies and configure C++' \
	  'test           Run C++ and Python test suites' \
	  'test-cpp       Build C++ and run CTest' \
	  'test-python    Run pytest through uv' \
	  'format-cpp     Format C++ sources with clang-format' \
	  'check-format-cpp Check C++ formatting without changes' \
	  'docs           Build Sphinx documentation' \
	  'clean          Remove generated build output'

setup: setup-cpp setup-python

setup-cpp:
	PATH="$(LLVM_BIN):$$PATH" cmake -G "$(CMAKE_GENERATOR)" -DCMAKE_CXX_COMPILER="$(CXX_COMPILER)" -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -S . -B $(BUILD_DIR)

setup-python:
	uv sync --all-groups

test: test-cpp test-python

test-cpp:
	@if test -d impl/cpp/tests && rg --files impl/cpp/tests -g '*.cpp' | rg -q .; then \
	  PATH="$(LLVM_BIN):$$PATH" cmake -G "$(CMAKE_GENERATOR)" -DCMAKE_CXX_COMPILER="$(CXX_COMPILER)" -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -S . -B $(BUILD_DIR) && \
	  cmake --build $(BUILD_DIR) && \
	  ctest --test-dir $(BUILD_DIR) --output-on-failure; \
	else printf '%s\n' 'No C++ tests yet.'; fi

test-python:
	@if test -d impl/python/tests && rg --files impl/python/tests -g 'test_*.py' | rg -q .; then uv run pytest; else printf '%s\n' 'No Python tests yet.'; fi

format-cpp:
	@if test -d impl/cpp; then files=$$(rg --files impl/cpp -g '*.cpp' -g '*.cppm' 2>/dev/null); if test -n "$$files"; then clang-format -i $$files; else printf '%s\n' 'No C++ sources yet.'; fi; else printf '%s\n' 'No C++ sources yet.'; fi

check-format-cpp:
	@if test -d impl/cpp; then files=$$(rg --files impl/cpp -g '*.cpp' -g '*.cppm' 2>/dev/null); if test -n "$$files"; then clang-format --dry-run --Werror $$files; else printf '%s\n' 'No C++ sources yet.'; fi; else printf '%s\n' 'No C++ sources yet.'; fi

docs:
	uv run --group docs sphinx-build -W --keep-going -b html docs docs/_build/html

clean:
	rm -rf $(BUILD_DIR) .venv docs/_build
