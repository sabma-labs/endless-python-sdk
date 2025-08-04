# Copyright © Endless Foundation
# Copyright © Aptos Foundation
# SPDX-License-Identifier: Apache-2.0

import asyncio

from endless_sdk.account import Account
from endless_sdk.account_address import AccountAddress
from endless_sdk.endless_token_client import EndlessTokenClient, Object, Property, PropertyMap
from endless_sdk.async_client import FaucetClient, RestClient
from endless_sdk.api_config import APIConfig , NetworkType


async def main():
    config_type = NetworkType.TESTNET  # Change to MAINNET or TESTNET as needed.
    api_config = APIConfig(config_type)
    rest_client = RestClient(api_config.NODE_URL,api_config.INDEXER_URL)
    token_client = EndlessTokenClient(rest_client)
    alice = Account.generate()
    bob = Account.generate()  
    # <:!:section_2

    collection_name = "Alice111"
    token_name = collection_name+"first token"

    print("\n=== Addresses ===")
    print(f"Alice: {alice.address()}")
    print(f"Bob: {bob.address()}")

    await rest_client.fund_account(alice)
    await rest_client.fund_account(bob)

    print("\n=== Initial Coin Balances ===")
    alice_balance = rest_client.account_balance(alice.address())
    bob_balance = rest_client.account_balance(bob.address())
    [alice_balance, bob_balance] = await asyncio.gather(*[alice_balance, bob_balance])
    print(f"Alice: {alice_balance}")
    print(f"Bob: {bob_balance}")

    print("\n=== Creating Collection and Token ===")

    txn_hash = await token_client.create_collection(
        alice,
        "Alice's simple collection",
        100,
        collection_name,
        "https://endless.dev",
        0,
        1,
    )
    await rest_client.wait_for_transaction(txn_hash)
    print("Done !!!@")

    await rest_client.close()


if __name__ == "__main__":
    asyncio.run(main())
