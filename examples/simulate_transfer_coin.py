# Copyright © Endless Foundation
# Copyright © Aptos Foundation
# SPDX-License-Identifier: Apache-2.0

import asyncio
import json

from endless_sdk.account import Account
from endless_sdk.async_client import FaucetClient, RestClient
from endless_sdk.bcs import Serializer
from endless_sdk.transactions import (
    EntryFunction,
    TransactionArgument,
    TransactionPayload,
)
from endless_sdk.type_tag import StructTag, TypeTag

from .common import NODE_URL


async def main():
    rest_client = RestClient(NODE_URL)
    
    #add your wallet private key
    alice =  Account.load_key("")
    bob =  Account.generate()

    print("\n=== Addresses ===")
    print(f"Alice: {alice.address()}")
    print(f"Bob: {bob.address()}")


    payload = EntryFunction.natural(
        "0x1::endless_coin",
        "transfer",
        [],
        [   
            TransactionArgument(bob.address(), Serializer.struct),
            TransactionArgument(100_000, Serializer.u128),
        ],
    )
    transaction = await rest_client.create_bcs_transaction(
        alice, TransactionPayload(payload)
    )

    print("\n=== Simulate before creating Bob's Account ===")
    output = await rest_client.simulate_transaction(transaction, alice)
    if output[0]["vm_status"] == "Executed successfully":
        print("Warning: Transaction succeeded unexpectedly. Bob's account might already exist.")
    else:
        print("Transaction failed as expected. Bob's account is not created yet.")
    
    print("\n=== Simulate after creating Bob's Account ===")
    output = await rest_client.simulate_transaction(transaction, alice)
    assert output[0]["vm_status"] == "Executed successfully", "This should succeed"
    print(json.dumps(output, indent=4, sort_keys=True))

    await rest_client.close()


if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())