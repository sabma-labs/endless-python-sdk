# Copyright © Endless Foundation
# Copyright © Aptos Foundation
# SPDX-License-Identifier: Apache-2.0

import asyncio

from endless_sdk.account import Account
from endless_sdk.async_client import FaucetClient, RestClient
from endless_sdk.api_config import APIConfig , NetworkType
from .common import FAUCET_AUTH_TOKEN, FAUCET_URL, NODE_URL


async def main():
    # :!:>section_1
    config_type = NetworkType.LOCAL  # Change to MAINNET or TESTNET as needed.
    api_config = APIConfig(config_type)
    rest_client = RestClient(api_config.NODE_URL,api_config.INDEXER_URL)  # <:!:section_1

    # :!:>section_2
    alice = Account.generate_secp256k1_ecdsa()
    bob = Account.generate_secp256k1_ecdsa()  # <:!:section_2

    print("\n=== Addresses ===")
    print(f"Alice: {alice.address()}")
    print(f"Bob: {bob.address()}")

    # :!:>section_3
    alice_fund = await rest_client.fund_account(alice.address(), 100_000_000)
    bob_fund = await rest_client.fund_account(bob.address(), 0)  # <:!:section_3
    await asyncio.gather(*[alice_fund, bob_fund])

    print("\n=== Initial Balances ===")
    # :!:>section_4
    alice_balance = rest_client.account_balance(alice.address())
    bob_balance = rest_client.account_balance(bob.address())
    [alice_balance, bob_balance] = await asyncio.gather(*[alice_balance, bob_balance])
    print(f"Alice: {alice_balance}")
    print(f"Bob: {bob_balance}")  # <:!:section_4

    # Have Alice give Bob 1_000 coins
    # :!:>section_5
    txn_hash = await rest_client.bcs_transfer(
        alice, bob.address(), 1_000
    )  # <:!:section_5
    # :!:>section_6
    await rest_client.wait_for_transaction(txn_hash)  # <:!:section_6

    print("\n=== Intermediate Balances ===")
    alice_balance = rest_client.account_balance(alice.address())
    bob_balance = rest_client.account_balance(bob.address())
    [alice_balance, bob_balance] = await asyncio.gather(*[alice_balance, bob_balance])
    print(f"Alice: {alice_balance}")
    print(f"Bob: {bob_balance}")  # <:!:section_4

    # Have Alice give Bob another 1_000 coins using BCS
    txn_hash = await rest_client.bcs_transfer(alice, bob.address(), 1_000)
    await rest_client.wait_for_transaction(txn_hash)

    print("\n=== Final Balances ===")
    alice_balance = rest_client.account_balance(alice.address())
    bob_balance = rest_client.account_balance(bob.address())
    [alice_balance, bob_balance] = await asyncio.gather(*[alice_balance, bob_balance])
    print(f"Alice: {alice_balance}")
    print(f"Bob: {bob_balance}")

    await rest_client.close()


if __name__ == "__main__":
    asyncio.run(main())
