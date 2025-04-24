# Copyright © Endless Foundation
# Copyright © Aptos Foundation
# SPDX-License-Identifier: Apache-2.0

import asyncio

from endless_sdk import asymmetric_crypto_wrapper, ed25519, secp256k1_ecdsa
from endless_sdk.account import Account
from endless_sdk.account_address import AccountAddress
from endless_sdk.asymmetric_crypto_wrapper import MultiSignature, Signature
from endless_sdk.async_client import FaucetClient, IndexerClient, RestClient
from endless_sdk.authenticator import AccountAuthenticator, MultiKeyAuthenticator
from endless_sdk.bcs import Serializer
from endless_sdk.api_config import APIConfig , NetworkType
from endless_sdk.transactions import (
    EntryFunction,
    SignedTransaction,
    TransactionArgument,
    TransactionPayload,
)

from .common import FAUCET_AUTH_TOKEN, FAUCET_URL, INDEXER_URL, NODE_URL


async def main():
    # :!:>section_1
    config_type = NetworkType.TESTNET  # Change to MAINNET or TESTNET as needed.
    api_config = APIConfig(config_type)
    rest_client = RestClient(api_config.NODE_URL,api_config.INDEXER_URL)
    

    # :!:>section_2
    key1 = secp256k1_ecdsa.PrivateKey.random()
    key2 = ed25519.PrivateKey.random()
    key3 = secp256k1_ecdsa.PrivateKey.random()
    pubkey1 = key1.public_key()
    pubkey2 = key2.public_key()
    pubkey3 = key3.public_key()

    alice_pubkey = asymmetric_crypto_wrapper.MultiPublicKey(
        [pubkey1, pubkey2, pubkey3], 2
    )
    alice_address = AccountAddress.from_key(alice_pubkey)

    bob = Account.generate()

    print("\n=== Addresses ===")
    print(f"Multikey Alice: {alice_address}")
    print(f"Bob: {bob.address()}")

    # :!:>section_3
    alice_fund = await rest_client.fund_account(alice_address)
    bob_fund = await rest_client.fund_account(bob)  # <:!:section_3
    await asyncio.gather(*[alice_fund, bob_fund])

    print("\n=== Initial Balances ===")
    # :!:>section_4
    alice_balance = rest_client.account_balance(alice_address)
    bob_balance = rest_client.account_balance(bob.address())
    [alice_balance, bob_balance] = await asyncio.gather(*[alice_balance, bob_balance])
    print(f"Alice: {alice_balance}")
    print(f"Bob: {bob_balance}")  # <:!:section_4

    # Have Alice give Bob 1_000 coins
    # :!:>section_5

    # TODO: Rework SDK to support this without the extra work

    # Build Transaction to sign
    transaction_arguments = [
        TransactionArgument(bob.address(), Serializer.struct),
        TransactionArgument(1_000, Serializer.u64),
    ]

    payload = EntryFunction.natural(
        "0x1::endless_account",
        "transfer",
        [],
        transaction_arguments,
    )

    raw_transaction = await rest_client.create_bcs_transaction(
        alice_address, TransactionPayload(payload)
    )

    # Sign by multiple keys
    raw_txn_bytes = raw_transaction.keyed()
    sig1 = key1.sign(raw_txn_bytes)
    sig2 = key2.sign(raw_txn_bytes)

    # Combine them
    total_sig = MultiSignature([(0, Signature(sig1)), (1, Signature(sig2))])
    alice_auth = AccountAuthenticator(MultiKeyAuthenticator(alice_pubkey, total_sig))

    # Verify signatures
    assert key1.public_key().verify(raw_txn_bytes, sig1)
    assert key2.public_key().verify(raw_txn_bytes, sig2)
    assert alice_pubkey.verify(raw_txn_bytes, total_sig)
    assert alice_auth.verify(raw_txn_bytes)

    # Submit to network
    signed_txn = SignedTransaction(raw_transaction, alice_auth)
    txn_hash = await rest_client.submit_bcs_transaction(signed_txn)

    # :!:>section_6
    await rest_client.wait_for_transaction(txn_hash)  # <:!:section_6

    print("\n=== Final Balances ===")
    alice_balance = rest_client.account_balance(alice_address)
    bob_balance = rest_client.account_balance(bob.address())
    [alice_balance, bob_balance] = await asyncio.gather(*[alice_balance, bob_balance])
    print(f"Alice: {alice_balance}")
    print(f"Bob: {bob_balance}")  # <:!:section_4

    await rest_client.close()


if __name__ == "__main__":
    asyncio.run(main())
