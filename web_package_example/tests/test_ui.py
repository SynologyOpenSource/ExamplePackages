# To run this test:
# 1. Install Python if you haven't already.
# 2. Install Playwright: pip install playwright
# 3. Install browser drivers: playwright install
# 4. Ensure PHP is installed and in your system's PATH.
# 5. Run the script: python test_ui.py 
#    (or from the repo root: python web_package_example/tests/test_ui.py)

import subprocess
import time
from playwright.sync_api import sync_playwright, expect

def test_phpinfo_page():
    # Start the PHP development server
    # The document root is web_package_example/src
    # The script is in web_package_example/tests, so ../src
    process = subprocess.Popen(
        ['php', '-S', 'localhost:8000', '-t', '../src'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    try:
        # Wait for the server to start
        time.sleep(1)

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto('http://localhost:8000/index.php')
            
            # Assert that the page content contains "PHP Version"
            expect(page.locator('body')).to_contain_text('PHP Version')
            
            browser.close()
    finally:
        # Terminate the PHP server subprocess
        process.terminate()
        process.wait()

if __name__ == '__main__':
    test_phpinfo_page()
    print("Test completed successfully!")
