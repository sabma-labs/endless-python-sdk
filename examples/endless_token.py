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
    # # This is a hack, once we add support for reading events or indexer, this will be easier
    # resp = await rest_client.account_resource(alice.address(), "0x1::account::Account")
    # int(resp["data"]["guid_creation_num"])

    # txn_hash = await token_client.mint_token(
    #     alice,
    #     collection_name,
    #     "Alice's simple token",
    #     token_name,
    #     "https://aptos.dev/img/nyan.jpeg",
    #     PropertyMap([Property.string("string", "string value")]),
    # )
    # await rest_client.wait_for_transaction(txn_hash)

    # minted_tokens = await token_client.tokens_minted_from_transaction(txn_hash)
    # assert len(minted_tokens) == 1
    # token_addr = minted_tokens[0]

    # collection_addr = AccountAddress.for_named_collection(
    #     alice.address(), collection_name
    # )
    # collection_data = await token_client.read_object(collection_addr)
    # print(f"Alice's collection: {collection_data}")
    # token_data = await token_client.read_object(token_addr)
    # print(f"Alice's token: {token_data}")

    # txn_hash = await token_client.add_token_property(
    #     alice, token_addr, Property.bool("test", False)
    # )
    # await rest_client.wait_for_transaction(txn_hash)
    # token_data = await token_client.read_object(token_addr)
    # print(f"Alice's token: {token_data}")
    # txn_hash = await token_client.remove_token_property(alice, token_addr, "string")
    # await rest_client.wait_for_transaction(txn_hash)
    # token_data = await token_client.read_object(token_addr)
    # print(f"Alice's token: {token_data}")
    # txn_hash = await token_client.update_token_property(
    #     alice, token_addr, Property.bool("test", True)
    # )
    # await rest_client.wait_for_transaction(txn_hash)
    # token_data = await token_client.read_object(token_addr)
    # print(f"Alice's token: {token_data}")
    # txn_hash = await token_client.add_token_property(
    #     alice, token_addr, Property.bytes("bytes", b"\x00\x01")
    # )
    # await rest_client.wait_for_transaction(txn_hash)
    # token_data = await token_client.read_object(token_addr)
    # print(f"Alice's token: {token_data}")

    # print("\n=== Transferring the Token from Alice to Bob ===")
    # print(f"Alice: {alice.address()}")
    # print(f"Bob:   {bob.address()}")
    # print(f"Token: {token_addr}\n")
    # print(f"Owner: {token_data.resources[Object].owner}")
    # print("    ...transferring...    ")
    # txn_hash = await rest_client.transfer_object(alice, token_addr, bob.address())
    # await rest_client.wait_for_transaction(txn_hash)
    # token_data = await token_client.read_object(token_addr)
    # print(f"Owner: {token_data.resources[Object].owner}\n")

    await rest_client.close()


if __name__ == "__main__":
    asyncio.run(main())
