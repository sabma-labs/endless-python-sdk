import os
from enum import Enum

class NetworkType(Enum):
    MAINNET = "mainnet"
    TESTNET = "testnet"
    LOCAL = "local"

class APIConfig:
    """
    A configuration class that holds API URLs and related settings for different networks.
    """
    def __init__(self, network: NetworkType):
        self.network = network
        self._setup_config()

    def _setup_config(self):
        """
        Initializes configuration values based on the given network.
        """
        if self.network == NetworkType.MAINNET:
            # Mainnet configuration: reads environment variables with a specific suffix or falls back to provided defaults.
            self.ENDLESS_CORE_PATH = os.getenv(
                "ENDLESS_CORE_PATH_MAINNET",
                os.path.abspath("./endless-framework")
            )
            self.FAUCET_URL = os.getenv(
                "ENDLESS_FAUCET_URL_MAINNET",
                ""
            )
            self.FAUCET_AUTH_TOKEN = os.getenv(
                "FAUCET_AUTH_TOKEN_MAINNET",
                ""
            )
            self.INDEXER_URL = os.getenv(
                "ENDLESS_INDEXER_URL_MAINNET",
                "https://idx.endless.link/api/v1"
            )
            self.NODE_URL = os.getenv(
                "ENDLESS_NODE_URL_MAINNET",
                "https://rpc.endless.link/v1"
            )
        elif self.network == NetworkType.TESTNET:
            # Testnet configuration: adjust defaults as needed for your test network.
            self.ENDLESS_CORE_PATH = os.getenv(
                "ENDLESS_CORE_PATH_TESTNET",
                os.path.abspath("./endless-framework")
            )
            self.FAUCET_URL = os.getenv(
                "ENDLESS_FAUCET_URL_TESTNET",
                ""
            )
            self.FAUCET_AUTH_TOKEN = os.getenv(
                "FAUCET_AUTH_TOKEN_TESTNET",
                ""
            )
            self.INDEXER_URL = os.getenv(
                "ENDLESS_INDEXER_URL_TESTNET",
                "https://idx-test.endless.link/api/v1"
            )
            self.NODE_URL = os.getenv(
                "ENDLESS_NODE_URL_TESTNET",
                "https://rpc-test.endless.link/v1"
            )
        elif self.network == NetworkType.LOCAL:
            # Local configuration: use the base defaults or variables for local development.
            self.ENDLESS_CORE_PATH = os.getenv(
                "ENDLESS_CORE_PATH_LOCAL",
                os.path.abspath("./endless-framework")
            )
            self.FAUCET_URL = os.getenv(
                "ENDLESS_FAUCET_URL_LOCAL",
                "http://127.0.0.1:8081"
            )
            self.FAUCET_AUTH_TOKEN = os.getenv(
                "FAUCET_AUTH_TOKEN_LOCAL",
                ""
            )
            self.INDEXER_URL = os.getenv(
                "ENDLESS_INDEXER_URL_LOCAL",
                "http://127.0.0.1:8090/api/v1"
            )
            self.NODE_URL = os.getenv(
                "ENDLESS_NODE_URL_LOCAL",
                "http://127.0.0.1:8080/v1"
            )
        else:
            raise ValueError("Invalid network type provided.")

    def __str__(self):
        return f"APIConfig(network={self.network.value}, NODE_URL={self.NODE_URL})"

# # Example usage in another file:
# if __name__ == "__main__":
#     # Set the configuration type (choose from NetworkType.MAINNET, NetworkType.TESTNET, NetworkType.LOCAL)
#     config_type = NetworkType.LOCAL  # Change to MAINNET or TESTNET as needed.
#     config = APIConfig(config_type)

#     # Now you can access the API URLs and other settings via the config object:
#     print("Endless Core Path:", config.ENDLESS_CORE_PATH)
#     print("Faucet URL:", config.FAUCET_URL)
#     print("Indexer URL:", config.INDEXER_URL)
#     print("Node URL:", config.NODE_URL)
