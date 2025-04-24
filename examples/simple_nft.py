# Copyright © Endless Foundation
# Copyright © Aptos Foundation
# SPDX-License-Identifier: Apache-2.0

import asyncio
import json
import pdb
import base58
from endless_sdk.account import Account
from endless_sdk.account_address import AccountAddress
from endless_sdk.endless_tokenv1_client import EndlessTokenV1Client
from endless_sdk.async_client import RestClient
from endless_sdk.api_config import APIConfig , NetworkType


async def main():
    config_type = NetworkType.TESTNET  # Change to MAINNET or TESTNET as needed.
    api_config = APIConfig(config_type)
    rest_client = RestClient(api_config.NODE_URL,api_config.INDEXER_URL)
    token_client = EndlessTokenV1Client(rest_client)

    collection_name = "niraj 040733"
    token_name = collection_name + " first token"
    property_version = 0
    
    # :!:>section_2
    #add your wallet private key
    alice = Account.generate()
    bob = Account.generate()  # <:!:section_2
    print("\n=== Addresses ===")
    print(f"Alice: {alice.address()}")
    print(f"Bob: {bob.address()}")
    
    print("\n=== Fund Accounts ===")
    
    
    await rest_client.fund_account(alice)
    await rest_client.fund_account(bob)
    
    
    

    

    print("\n=== Initial Coin Balances ===")
    alice_balance = rest_client.account_balance(alice.address())
    bob_balance = rest_client.account_balance(bob.address())
    [alice_balance, bob_balance] = await asyncio.gather(*[alice_balance, bob_balance])
    print(f"Alice: {alice_balance}")
    print(f"Bob: {bob_balance}")

    print("\n=== Creating Collection and Token ===")
    
    # :!:>section_4
    txn_hash = await token_client.create_collection(
        alice, collection_name, collection_name +  " simple collection", "https://endless.dev"
    )  # <:!:section_4
    await rest_client.wait_for_transaction(txn_hash)
    await rest_client.transaction_by_hash(txn_hash)

    # collection_address = alice.address()

    # for tx in tx_info["changes"]:
    #     if tx["data"]["type"] == "0x4::collection::Collection":
    #         collection_address = tx["address"]
    #         break

    # :!:>section_5
    # token_address = alice.address()
    txn_hash = await token_client.create_token(
        alice,
        collection_name,
        token_name,
        collection_name + " simple token",
        "https://aptos.dev/img/nyan.jpeg",
    )  # <:!:section_5
    await rest_client.wait_for_transaction(txn_hash)

    await rest_client.transaction_by_hash(txn_hash)

    # for tx in tx_info["changes"]:
    #     if tx["data"]["type"] == "0x4::token::Token":
    #         token_address = tx["address"]
    #         break

    # :!:>section_6
    collection_data = await token_client.get_collection(
        alice.address(), collection_name
    )
    print(
        f"Alice's collection: {json.dumps(collection_data, indent=4, sort_keys=True)}"
    )  # <:!:section_6
    # # :!:>section_7
    # balance = await token_client.get_token_balance(
    #     collection_address, alice.address(), collection_name, token_name, property_version
    # )
    # print(f"Alice's token balance: {balance}")  # <:!:section_7
    # :!:>section_8
    token_data = await token_client.get_token_data(
        alice.address(), collection_name, token_name, property_version
    )
    print(
        f"Alice's token data: {json.dumps(token_data, indent=4, sort_keys=True)}"
    )  # <:!:section_8

    print("\n=== Transferring the token to Bob ===")
    token_address = token_data.get("token").get("id")
    token_address_hex = f"0x{base58.b58decode(token_address).hex()}"

    # :!:>section_9
    txn_hash = await token_client.offer_token(
        alice,
        bob.address(),
        alice.address(),
        collection_name,
        token_name,
        property_version,
        1,
        AccountAddress.from_str(token_address_hex),
    )  # <:!:section_9
    await rest_client.wait_for_transaction(txn_hash)

    # :!:>section_10
    # txn_hash = await token_client.claim_token(
    #     bob,
    #     alice.address(),
    #     alice.address(),
    #     collection_name,
    #     token_name,
    #     property_version,
    # )  # <:!:section_10
    # await rest_client.wait_for_transaction(txn_hash)

    # alice_balance = token_client.get_token_balance(
    #     collection_address, alice.address(), collection_name, token_name, property_version
    # )
    # bob_balance = token_client.get_token_balance(
    #     bob.address(), alice.address(), collection_name, token_name, property_version
    # )
    # [alice_balance, bob_balance] = await asyncio.gather(*[alice_balance, bob_balance])
    # print(f"Alice's token balance: {alice_balance}")
    # print(f"Bob's token balance: {bob_balance}")

    # print("\n=== Transferring the token back to Alice using MultiAgent ===")
    # txn_hash = await token_client.direct_transfer_token(
    #     bob, alice, alice.address(), collection_name, token_name, 0, 1
    # )
    # await rest_client.wait_for_transaction(txn_hash)

    # alice_balance = token_client.get_token_balance(
    #     alice.address(), alice.address(), collection_name, token_name, property_version
    # )
    # bob_balance = token_client.get_token_balance(
    #     bob.address(), alice.address(), collection_name, token_name, property_version
    # )
    # [alice_balance, bob_balance] = await asyncio.gather(*[alice_balance, bob_balance])
    # print(f"Alice's token balance: {alice_balance}")
    # print(f"Bob's token balance: {bob_balance}")

    await rest_client.close()


if __name__ == "__main__":
    asyncio.run(main())
