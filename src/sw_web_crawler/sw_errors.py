

class HeaderError(Exception):
    """
    Raised when there's a problem deciphering returned HTTP headers.
    """
    pass


class SizeError(Exception):
    """
    Raised when a file is too large to download in an acceptable time.
    """
    pass


