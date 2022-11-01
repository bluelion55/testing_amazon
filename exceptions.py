
# Exceptions encountered by generic scraper class
class BrowserNotInstantiated(Exception):
    """Raised when failed to initialise browser instance"""
    pass


class BodyNotFound(Exception):
    """Raised when the HTML body failed to load"""
    pass
