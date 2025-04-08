# Copyright © Endless Foundation
# Copyright © Aptos Foundation
# SPDX-License-Identifier: Apache-2.0

import asyncio
import json 
from endless_sdk.account import Account
from endless_sdk.async_client import FaucetClient, IndexerClient, RestClient

from .common import FAUCET_AUTH_TOKEN, FAUCET_URL, INDEXER_URL, NODE_URL
import pdb

async def main():
    # :!:>section_1
    rest_client = RestClient("https://rpc-test.endless.link/v1")
    # faucet_client = FaucetClient(
    #     FAUCET_URL, rest_client, FAUCET_AUTH_TOKEN
    # )  # <:!:section_1
    if INDEXER_URL and INDEXER_URL != "none":
        indexer_client = IndexerClient(INDEXER_URL)
    else:
        indexer_client = None

    # :!:>section_2
    # alice = Account.generate()
    bob = Account.generate()  # <:!:section_2
    alice =  Account.load_key("0x48ca3b85eaf1b2d6658d662a34a572f6eada8076f14e93d36e6291edff564086")
    # bob =  Account.load_key("0x7bdbb1a41263b886e8d1fe5f5299874310946e9ef4a2a9317c2c632bcb5641d9")
    print("\n=== Addresses ===")
    print(f"Alice: {alice.address()}")
    print(f"Bob: {bob.address()}")

    # :!:>section_3
    # alice_fund = faucet_client.fund_account(alice.address(), 100_000_000)
    # bob_fund = faucet_client.fund_account(bob.address(), 0)  # <:!:section_3
    # await asyncio.gather(*[alice_fund, bob_fund])

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

    if indexer_client:
        query = """
            query TransactionsQuery($account: String) {
              account_transactions(
                limit: 20
                where: {account_address: {_eq: $account}}
              ) {
                transaction_version
                coin_activities {
                  amount
                  activity_type
                  coin_type
                  entry_function_id_str
                  owner_address
                  transaction_timestamp
                }
              }
            }
        """

        variables = {"account": f"{bob.address()}"}
        data = await indexer_client.query(query, variables)
        assert len(data["data"]["account_transactions"]) > 0

    await rest_client.close()


if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
