# Layout of audioinfo Project

- `pyproject.toml` contains the build system requirements and build backend tools to use for the creation of the package. Please check if your pip version is higher than 22.
- `docs/` contains the Sphinx source files for the package documentation.
- `tests/` contains the unit test suite for the package.
- `src/` contains the code modules. The `__init__.py` in this directory provides the package version identifier string as a variable named `__version__`.