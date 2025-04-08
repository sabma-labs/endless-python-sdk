import importlib.metadata as metadata

# constants
PACKAGE_NAME = "endless-sdk"


class Metadata:
    ENDLESS_HEADER = "x-endless-client"

    @staticmethod
    def get_endless_header_val():
        version = metadata.version(PACKAGE_NAME)
        return f"endless-python-sdk/{version}"
