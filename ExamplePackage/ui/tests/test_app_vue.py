# To run this test:
# 1. Ensure Python 3.7+ is installed.
# 2. Install Playwright: pip install playwright
# 3. Install browser drivers: playwright install
# 4. Ensure the Vue app in ../ (ExamplePackage/ui) has been built (e.g., using pnpm run build or npm run build).
#    This will create the ../dist/ directory with necessary bundles.
# 5. Run this script from the repository root or from ExamplePackage/ui/tests/:
#    python ExamplePackage/ui/tests/test_app_vue.py

import subprocess
import time
import os
import shutil
from playwright.sync_api import sync_playwright, expect
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Configuration
SERVER_HOST = 'localhost'
SERVER_PORT = 8001
# The test HTML file is in ExamplePackage/ui/tests/index.html
# The server root needs to be ExamplePackage/ui/ so that
# ../dist/ paths in the HTML file correctly resolve to ExamplePackage/ui/dist/
SERVER_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEST_PAGE_URL = f'http://{SERVER_HOST}:{SERVER_PORT}/tests/index.html'

class QuietHTTPRequestHandler(SimpleHTTPRequestHandler):
    """
    A SimpleHTTPRequestHandler that doesn't log requests to stderr.
    """
    def log_message(self, format, *args):
        # Override to prevent logging to stderr/stdout
        pass

def start_http_server(server_root_dir, host, port):
    """Starts an HTTP server in a separate thread."""
    os.chdir(server_root_dir) # Important: Server serves from its CWD
    httpd = HTTPServer((host, port), QuietHTTPRequestHandler)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True  # Allow main thread to exit even if server thread is running
    thread.start()
    print(f"HTTP server started on {host}:{port} serving from {server_root_dir}")
    return httpd, thread

def test_app_vue_renders():
    """
    Tests if the basic App.vue structure renders by checking for the #app div.
    """
    http_server = None
    server_thread = None
    original_cwd = os.getcwd() # Save original CWD

    try:
        # Start the HTTP server
        # The SimpleHTTPRequestHandler serves files relative to the CWD where it's run.
        # We want to serve from ExamplePackage/ui/
        http_server, server_thread = start_http_server(SERVER_ROOT_DIR, SERVER_HOST, SERVER_PORT)
        
        # Wait a moment for the server to be ready
        time.sleep(1) 

        with sync_playwright() as p:
            # Try launching with headless=False for debugging if needed
            # browser = p.chromium.launch(headless=False) 
            browser = p.chromium.launch()
            page = browser.new_page()
            
            print(f"Navigating to {TEST_PAGE_URL}")
            page.goto(TEST_PAGE_URL, timeout=10000) # Increased timeout for page load

            # Basic assertion: Check if the #app div is present and visible
            app_div = page.locator('#app')
            expect(app_div).to_be_visible(timeout=5000) # Wait up to 5s for visibility
            print("#app div is visible.")

            # Specific assertions based on App.vue's content
            # a. Assert that an element with the class `title` and text "Hello Synology Package" is visible.
            title_element = page.locator('.title')
            expect(title_element).to_have_text('Hello Synology Package', timeout=5000)
            expect(title_element).to_be_visible()
            print("Title element '.title' with text 'Hello Synology Package' is visible.")

            # b. Assert that a button with the text "Documents" is visible.
            documents_button = page.locator('button:has-text("Documents")')
            expect(documents_button).to_be_visible(timeout=5000)
            print("Button with text 'Documents' is visible.")

            # c. Assert that a button with the text "Close" is visible.
            close_button = page.locator('button:has-text("Close")')
            expect(close_button).to_be_visible(timeout=5000)
            print("Button with text 'Close' is visible.")

            browser.close()
            print("Browser closed.")

    except Exception as e:
        print(f"An error occurred during the test: {e}")
        raise # Re-raise the exception to mark the test as failed
    finally:
        if http_server:
            print("Shutting down HTTP server...")
            http_server.shutdown() # Signal the server to stop
            http_server.server_close() # Close the server socket
        if server_thread:
            server_thread.join(timeout=5) # Wait for the server thread to finish
            if server_thread.is_alive():
                print("Warning: HTTP server thread did not shut down cleanly.")
        print("HTTP server shut down.")
        os.chdir(original_cwd) # Restore original CWD

if __name__ == '__main__':
    print(f"Starting test_app_vue.py...")
    print(f"Server root directory will be: {SERVER_ROOT_DIR}")
    print(f"Test page will be loaded from: {TEST_PAGE_URL}")
    
    # Check if dist directory exists
    dist_dir = os.path.join(SERVER_ROOT_DIR, 'dist')
    if not os.path.exists(dist_dir) or not os.path.isdir(dist_dir):
        print(f"Error: The build directory '{dist_dir}' does not exist.")
        print("Please build the Vue application (e.g., pnpm run build in ExamplePackage/ui) before running this test.")
    else:
        print(f"Build directory '{dist_dir}' found.")
        test_app_vue_renders()
        print("Test completed successfully!")
