# Copyright © Endless Foundation
# Copyright © Aptos Foundation
# SPDX-License-Identifier: Apache-2.0

"""
This example depends on the MoonCoin.move module having already been published to the destination blockchain.

One method to do so is to use the CLI:
    * Acquire the Endless CLI, see https://endless.dev/cli-tools/endless-cli/use-cli/install-endless-cli
    * `python -m examples.your-coin ~/endless-core/endless-move/move-examples/moon_coin`.
    * Open another terminal and `endless move compile --package-dir ~/endless-core/endless-move/move-examples/moon_coin --save-metadata --named-addresses MoonCoin=<Alice address from above step>`.
    * Return to the first terminal and press enter.
"""

import asyncio
import os
import sys

from endless_sdk.account import Account
from endless_sdk.account_address import AccountAddress
from endless_sdk.endless_cli_wrapper import EndlessCLIWrapper
from endless_sdk.async_client import FaucetClient, RestClient
from endless_sdk.bcs import Serializer
from endless_sdk.package_publisher import PackagePublisher
from endless_sdk.transactions import (
    EntryFunction,
    TransactionArgument,
    TransactionPayload,
)
from endless_sdk.type_tag import StructTag, TypeTag
from endless_sdk.api_config import APIConfig , NetworkType


class CoinClient(RestClient):
    async def register_coin(self, coin_address: AccountAddress, sender: Account) -> str:
        """Register the receiver account to receive transfers for the new coin."""

        payload = EntryFunction.natural(
            "0x1::managed_coin",
            "register",
            [TypeTag(StructTag.from_str(f"{coin_address}::moon_coin::MoonCoin"))],
            [],
        )
        signed_transaction = await self.create_bcs_signed_transaction(
            sender, TransactionPayload(payload)
        )
        return await self.submit_bcs_transaction(signed_transaction)

    async def mint_coin(
        self, minter: Account, receiver_address: AccountAddress, amount: int
    ) -> str:
        """Mints the newly created coin to a specified receiver address."""

        payload = EntryFunction.natural(
            "0x1::managed_coin",
            "mint",
            [TypeTag(StructTag.from_str(f"{minter.address()}::moon_coin::MoonCoin"))],
            [
                TransactionArgument(receiver_address, Serializer.struct),
                TransactionArgument(amount, Serializer.u64),
            ],
        )
        signed_transaction = await self.create_bcs_signed_transaction(
            minter, TransactionPayload(payload)
        )
        return await self.submit_bcs_transaction(signed_transaction)

    async def get_balance(
        self,
        coin_address: AccountAddress,
        account_address: AccountAddress,
    ) -> str:
        """Returns the coin balance of the given account"""

        balance = await self.account_resource(
            account_address,
            f"0x1::coin::CoinStore<{coin_address}::moon_coin::MoonCoin>",
        )
        return balance["data"]["coin"]["value"]


async def main(moon_coin_path: str):
    alice = Account.generate()
    bob = Account.generate()

    print("\n=== Addresses ===")
    print(f"Alice: {alice.address()}")
    print(f"Bob: {bob.address()}")

    config_type = NetworkType.LOCAL  # Change to MAINNET or TESTNET as needed.
    api_config = APIConfig(config_type)
    rest_client = RestClient(api_config.NODE_URL,api_config.INDEXER_URL)

    alice_fund = await rest_client.fund_account(alice.address(), 20_000_000)
    bob_fund = await rest_client.fund_account(bob.address(), 20_000_000)
    await asyncio.gather(*[alice_fund, bob_fund])

    if EndlessCLIWrapper.does_cli_exist():
        EndlessCLIWrapper.compile_package(moon_coin_path, {"MoonCoin": alice.address()})
    else:
        input("\nUpdate the module with Alice's address, compile, and press enter.")

    # :!:>publish
    module_path = os.path.join(
        moon_coin_path, "build", "Examples", "bytecode_modules", "moon_coin.mv"
    )
    with open(module_path, "rb") as f:
        module = f.read()

    metadata_path = os.path.join(
        moon_coin_path, "build", "Examples", "package-metadata.bcs"
    )
    with open(metadata_path, "rb") as f:
        metadata = f.read()

    print("\nPublishing MoonCoin package.")
    package_publisher = PackagePublisher(rest_client)
    txn_hash = await package_publisher.publish_package(alice, metadata, [module])
    await rest_client.wait_for_transaction(txn_hash)
    # <:!:publish

    print("\nBob registers the newly created coin so he can receive it from Alice.")
    txn_hash = await rest_client.register_coin(alice.address(), bob)
    await rest_client.wait_for_transaction(txn_hash)
    balance = await rest_client.get_balance(alice.address(), bob.address())
    print(f"Bob's initial MoonCoin balance: {balance}")

    print("Alice mints Bob some of the new coin.")
    txn_hash = await rest_client.mint_coin(alice, bob.address(), 100)
    await rest_client.wait_for_transaction(txn_hash)
    balance = await rest_client.get_balance(alice.address(), bob.address())
    print(f"Bob's updated MoonCoin balance: {balance}")

    try:
        maybe_balance = await rest_client.get_balance(alice.address(), alice.address())
    except Exception:
        maybe_balance = None
    print(f"Bob will transfer to Alice, her balance: {maybe_balance}")
    txn_hash = await rest_client.transfer_coins(
        bob, alice.address(), f"{alice.address()}::moon_coin::MoonCoin", 5
    )
    await rest_client.wait_for_transaction(txn_hash)
    balance = await rest_client.get_balance(alice.address(), alice.address())
    print(f"Alice's updated MoonCoin balance: {balance}")
    balance = await rest_client.get_balance(alice.address(), bob.address())
    print(f"Bob's updated MoonCoin balance: {balance}")


if __name__ == "__main__":
    assert (
        len(sys.argv) == 2
    ), "Expecting an argument that points to the moon_coin directory."

    asyncio.run(main(sys.argv[1]))
