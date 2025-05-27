# UI Test for web_package_example

This directory contains an end-to-end UI test for the `web_package_example`.
The test uses Playwright with Python to verify that the `index.php` page (which displays `phpinfo()`) loads and shows expected content.

## Prerequisites

1.  **Python:** Ensure Python 3.7+ is installed. You can download it from [python.org](https://www.python.org/).
2.  **PHP:** Ensure PHP is installed and available in your system's PATH. The test will attempt to start a PHP development server (`php -S`).
3.  **pip:** Python's package installer, usually comes with Python.

## Setup

1.  **Install Playwright:**
    ```bash
    pip install playwright
    ```

2.  **Install browser drivers:**
    Playwright needs browser binaries to run tests. Install them with:
    ```bash
    playwright install
    ```
    This will download default browsers (Chromium, Firefox, WebKit).

## Running the Test

1.  Navigate to the root of this repository in your terminal.
2.  Run the test script using:
    ```bash
    python web_package_example/tests/test_ui.py
    ```

The test will:
- Start a temporary PHP web server on `localhost:8000`.
- Launch a browser and navigate to the `index.php` page.
- Check if the text "PHP Version" is present on the page.
- Shut down the PHP web server.
- Print whether the test passed or failed.
