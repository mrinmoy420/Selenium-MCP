# selenium_fastmcp_server.py

import base64
import uuid
import os
import subprocess
import re
from mcp.server.fastmcp import FastMCP
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Get Chrome version
def get_chrome_version():
    try:
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        if os.path.exists(chrome_path):
            output = subprocess.check_output(f'wmic datafile where name="{chrome_path}" get Version /value', shell=True)
            version = re.search(r"Version=(.+)", output.decode()).group(1)
            return version.strip()
    except:
        pass
    return None

# Initialize the FastMCP server
mcp = FastMCP("selenium-mcp")

# State: sessions + active
sessions = {}
active_session = None

# --------------------------
# Helpers
# --------------------------

def _create_driver(headless=True):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
    chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    driver_path = r"C:\selenium-mcp\chromedriver-win64\chromedriver.exe"
    service = ChromeService(executable_path=driver_path)
    return webdriver.Chrome(service=service, options=chrome_options)

def _get_driver(session_id=None):
    global active_session
    sid = session_id or active_session
    return sessions.get(sid)

# --------------------------
# Tools via decorator
# --------------------------

@mcp.tool()
def start_browser(headless: bool = True) -> str:
    """Start a new browser session and make it active."""
    global active_session
    session_id = str(uuid.uuid4())
    driver = _create_driver(headless=headless)
    sessions[session_id] = driver
    active_session = session_id
    return f"✅ Started browser session {session_id}"

@mcp.tool()
def go_to_url(url: str, session_id: str = None) -> str:
    """Navigate browser to the given URL in the active or given session."""
    driver = _get_driver(session_id)
    if not driver:
        return "❌ No active session"
    driver.get(url)
    import time
    time.sleep(2)  # Wait for page to stabilize
    driver.implicitly_wait(10)  # Wait up to 10 seconds for elements
    return f"🌐 Opened {url}"

@mcp.tool()
def click_element(selector: str, session_id: str = None) -> str:
    """Click an element matching the CSS selector."""
    driver = _get_driver(session_id)
    if not driver:
        return "❌ No active session"
    try:
        element = driver.find_element("css selector", selector)
        element.click()
        return f"🖱️ Clicked {selector}"
    except NoSuchElementException:
        return f"❌ Element not found: {selector}"

@mcp.tool()
def type_text(selector: str, text: str, session_id: str = None) -> str:
    """Type text into input field matching CSS selector."""
    driver = _get_driver(session_id)
    if not driver:
        return "❌ No active session"
    try:
        # Wait up to 10 seconds for element to be present and visible
        wait = WebDriverWait(driver, 10)
        # Try different selectors for Google search
        selectors = [
            "textarea[name=q]",  # Google now uses textarea
            "input[name=q]",
            "input[title='Search']",
            ".gLFyf"  # Google search class
        ]
        for sel in selectors:
            try:
                element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, sel)))
                element.clear()
                element.send_keys(text)
                return f"⌨️ Typed '{text}' into {sel}"
            except:
                continue
        return f"❌ Element not found: {selector}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

@mcp.tool()
def take_screenshot(session_id: str = None) -> str:
    """Take screenshot and return it as base64."""
    driver = _get_driver(session_id)
    if not driver:
        return "❌ No active session"
    png = driver.get_screenshot_as_png()
    encoded = base64.b64encode(png).decode("utf-8")
    return encoded

@mcp.tool()
def close_browser(session_id: str = None) -> str:
    """Close the active or specified browser session."""
    global active_session
    sid = session_id or active_session
    driver = sessions.pop(sid, None)
    if driver:
        driver.quit()
        if sid == active_session:
            active_session = None
        return f"✅ Closed session {sid}"
    return f"❌ Session not found {sid}"

# --------------------------
# Run the server
# --------------------------
if __name__ == "__main__":
    mcp.run()
