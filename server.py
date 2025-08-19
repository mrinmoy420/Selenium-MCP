# server.py
from SeleniumLibrary import SeleniumLibrary as _SeleniumLibrary
from mcp.server.fastmcp import FastMCP
from selenium.webdriver.remote.webelement import WebElement

class SeleniumLibraryMCP(_SeleniumLibrary):
    def to_mcp(self):
        mcp = FastMCP("SeleniumLibrary")

        for name, kw in self.keywords.items():
            safe_fn = self._make_safe_wrapper(name, kw)
            if safe_fn:
                mcp.add_tool(safe_fn)

        return mcp

    def _make_safe_wrapper(self, name, kw):
        """Wrap a SeleniumLibrary keyword so it always returns JSON-serializable values."""
        def wrapper(*args, **kwargs):
            try:
                result = kw(*args, **kwargs)
                return self._sanitize(result)
            except Exception as e:
                return f"Error in {name}: {str(e)}"
        wrapper.__name__ = name.replace(" ", "_")  # Python-safe name
        wrapper.__doc__ = kw.__doc__
        return wrapper

    def _sanitize(self, value):
        """Convert Selenium objects into safe types."""
        if isinstance(value, WebElement):
            return f"<WebElement tag={value.tag_name} text={value.text[:30]!r}>"
        elif isinstance(value, list):
            return [self._sanitize(v) for v in value]
        elif isinstance(value, dict):
            return {k: self._sanitize(v) for k, v in value.items()}
        else:
            return value

if __name__ == "__main__":
    lib = SeleniumLibraryMCP(run_on_failure="Capture Page Screenshot")
    server = lib.to_mcp()
    server.run(transport="stdio")
