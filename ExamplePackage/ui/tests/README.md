# UI Test for ExamplePackage/ui (App.vue)

This directory contains an end-to-end UI test for the main Vue.js application (`App.vue`) of the `ExamplePackage`.
The test uses Playwright with Python to build the Vue app, serve it locally, and verify that `App.vue` renders expected content.

## Prerequisites

1.  **Node.js and pnpm/npm:** Ensure Node.js (which includes npm) is installed. If you prefer `pnpm` (recommended as `pnpm-lock.yaml` is present), install it globally: `npm install -g pnpm`. You can download Node.js from [nodejs.org](https://nodejs.org/).
2.  **Python:** Ensure Python 3.7+ is installed. You can download it from [python.org](https://www.python.org/).
3.  **pip:** Python's package installer, usually comes with Python.

## Setup

1.  **Install Node.js Dependencies:**
    Navigate to the `ExamplePackage/ui/` directory and run:
    ```bash
    # Using pnpm (recommended)
    pnpm install

    # Or, if you prefer npm
    # npm install
    ```

2.  **Build the Vue.js Application:**
    From the `ExamplePackage/ui/` directory, run the build script:
    ```bash
    # Using pnpm
    pnpm run build

    # Or, using npm
    # npm run build
    ```
    This will generate the necessary static assets in the `ExamplePackage/ui/dist/` directory.

3.  **Install Playwright:**
    If you haven't already, install Playwright for Python:
    ```bash
    pip install playwright
    ```

4.  **Install browser drivers:**
    Playwright needs browser binaries to run tests. Install them with:
    ```bash
    playwright install
    ```

## Running the Test

1.  Ensure you have completed all the setup steps above (Node dependencies installed, Vue app built, Playwright installed).
2.  Navigate to the root of this repository in your terminal.
3.  Run the test script using:
    ```bash
    python ExamplePackage/ui/tests/test_app_vue.py
    ```

The test will:
- Start a temporary local HTTP server.
- Launch a browser and navigate to a test HTML page that loads the built `App.vue`.
- Check for the presence of specific elements like the title "Hello Synology Package" and the "Documents" and "Close" buttons.
- Shut down the local HTTP server.
- Print whether the test passed or failed.
