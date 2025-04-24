# Copyright © Endless Foundation
# Copyright © Aptos Foundation
# SPDX-License-Identifier: Apache-2.0

import asyncio
import json 
from endless_sdk.account import Account
from endless_sdk.async_client import FaucetClient, IndexerClient, RestClient
from endless_sdk.api_config import APIConfig , NetworkType

async def main():
    # :!:>section_1
    config_type = NetworkType.TESTNET  # Change to MAINNET or TESTNET as needed.
    api_config = APIConfig(config_type)
    rest_client = RestClient(api_config.NODE_URL,api_config.INDEXER_URL) # <:!:section_1

    # :!:>section_2
    alice = Account.generate()
    bob = Account.generate()  # <:!:section_2
    
    print("\n=== Addresses ===")
    print(f"Alice: {alice.address()}")
    print(f"Bob: {bob.address()}")

    # :!:>section_3
    print("\n=== Fund Accounts ===")
    await rest_client.fund_account(alice)
    await rest_client.fund_account(bob)  # <:!:section_3


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
    print(f"Bob: {bob_balance}")  
    
    

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
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
