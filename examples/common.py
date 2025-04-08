# Copyright © Endless Foundation
# Copyright © Aptos Foundation
# SPDX-License-Identifier: Apache-2.0

import os
import os.path

ENDLESS_CORE_PATH = os.getenv(
    "ENDLESS_CORE_PATH",
    os.path.abspath("./endless-framework"),
)
# :!:>section_1
FAUCET_URL = os.getenv(
    "ENDLESS_FAUCET_URL",
    "http://bridge.endless.link/faucet",
)
FAUCET_AUTH_TOKEN = os.getenv("FAUCET_AUTH_TOKEN", "AHpEpNrqVvZyFzV6fMfSb3RvLznZnfnK7MpksAnAgUfE")
INDEXER_URL = os.getenv(
    "ENDLESS_INDEXER_URL",
    "https://idx-test.endless.link/api/v1",
)
NODE_URL = os.getenv("ENDLESS_NODE_URL", "https://rpc-test.endless.link/v1")
# <:!:section_1
