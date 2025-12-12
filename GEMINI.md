# GEMINI.md - jText Project

This document provides a comprehensive overview of the jText project, intended for developers and contributors.

## Project Overview

jText is a lightweight, feature-rich text editor for macOS, designed as a Notepad++ alternative. It is built with Python and the PyQt6 framework.

**Key Technologies:**

*   **Language:** Python 3.14+
*   **UI Framework:** PyQt6
*   **Package Manager:** uv
*   **Testing:** pytest, pytest-cov

**Architecture:**

The project follows a clean architecture with a separation of concerns:

*   **`src/`:** Contains the core application logic, including UI components, file management, text manipulation features, and more.
    *   **`src/ui/`:** Houses the PyQt6 main window and other UI-related components.
    *   **`src/` (root):** Contains modules for handling documents, files, JSON, themes, and other core functionalities.
*   **`tests/`:** Contains an extensive suite of unit tests, with 100% test coverage for all core modules.
*   **`main.py`:** The main entry point for the application.
*   **`pyproject.toml`:** Defines project metadata and dependencies.

## Building and Running

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/jaysuzi5/jText.git
    cd jText
    ```

2.  **Set up the virtual environment:**
    The project uses `uv`. The virtual environment is already set up in `.venv/`.
    ```bash
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    uv sync
    ```

### Running the Application

To run the jText application, execute the following command:

```bash
uv run python main.py
```

Or, if the virtual environment is activated:

```bash
python main.py
```

### Running Tests

The project has a comprehensive test suite. To run the tests:

```bash
uv run pytest tests/ -v
```

To run tests with a coverage report:

```bash
uv run pytest tests/ -v --cov=src --cov-report=term-missing
```

## Development Conventions

*   **Testing:** All new features must have corresponding unit tests. The project aims for 100% test coverage on all core modules.
*   **Code Style:** While not explicitly defined in the provided files, the code appears to follow standard Python conventions (PEP 8).
*   **Contributions:** Contributions are welcome. Ensure that all tests pass and that new code is accompanied by tests.
*   **Development Guide:** For more detailed development guidelines, refer to `CLAUDE.md`.
