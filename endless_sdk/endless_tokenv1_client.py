# Copyright © Endless Foundation
# Copyright © Aptos Foundation
# SPDX-License-Identifier: Apache-2.0
import os 
from typing import Any
from .account import Account
from .account_address import AccountAddress
from .async_client import ApiError, RestClient
from .bcs import Serializer
from .transactions import EntryFunction, TransactionArgument, TransactionPayload
from .type_tag import TypeTag, StructTag
import pdb
import base58
import aiohttp
import json
U64_MAX = 18446744073709551615
INDEXER_URL = os.getenv(
    "ENDLESS_INDEXER_URL",
    "https://idx-test.endless.link/api/v1",
)


class NFTCollection:
    def __init__(self, json_data):
        self.id = json_data.get('id')
        self.creator = json_data.get('creator')
        self.description = json_data.get('description')
        self.name = json_data.get('name')
        self.uri = json_data.get('uri')
        self.current_supply = json_data.get('current_supply')
        self.total_minted = json_data.get('total_minted')
        self.max_supply = json_data.get('max_supply')
        self.royalty_percent = json_data.get('royalty', {}).get('percent')
        self.royalty_payee = json_data.get('royalty', {}).get('payee_address')
        self.last_transaction_version = json_data.get('last_transaction_version')
        self.last_transaction_hash = json_data.get('last_transaction_hash')
        self.holders = json_data.get('holders')
        self.created_at = json_data.get('created_at')
        self.transfers = json_data.get('transfers')
    
    # Getter functions
    def get_id(self):
        return self.id

    def get_creator(self):
        return self.creator

    def get_description(self):
        return self.description

    def get_name(self):
        return self.name

    def get_uri(self):
        return self.uri

    def get_current_supply(self):
        return self.current_supply

    def get_total_minted(self):
        return self.total_minted

    def get_max_supply(self):
        return self.max_supply

    def get_royalty_percent(self):
        return self.royalty_percent

    def get_royalty_payee(self):
        return self.royalty_payee

    def get_last_transaction_version(self):
        return self.last_transaction_version

    def get_last_transaction_hash(self):
        return self.last_transaction_hash

    def get_holders(self):
        return self.holders

    def get_created_at(self):
        return self.created_at

    def get_transfers(self):
        return self.transfers


class EndlessTokenV1Client:
    """A wrapper around reading and mutating EndlessTokens also known as Token Objects"""

    _client: RestClient

    def __init__(self, client: RestClient):
        self._client = client

    async def create_collection(
        self, account: Account, name: str, description: str, uri: str
    ) -> str:
        """Creates a new collection within the specified account"""

        transaction_arguments = [
            TransactionArgument(description, Serializer.str),
            TransactionArgument(U64_MAX, Serializer.u64),
            TransactionArgument(name, Serializer.str),
            TransactionArgument(uri, Serializer.str),
            TransactionArgument(True, Serializer.bool),
            TransactionArgument(True, Serializer.bool),
            TransactionArgument(True, Serializer.bool),
            TransactionArgument(True, Serializer.bool),
            TransactionArgument(True, Serializer.bool),
            TransactionArgument(True, Serializer.bool),
            TransactionArgument(True, Serializer.bool),
            TransactionArgument(True, Serializer.bool),
            TransactionArgument(True, Serializer.bool),
            TransactionArgument(0, Serializer.u64),
            TransactionArgument(990, Serializer.u64),
        ]

        # creator: & signer,
        # description: String,
        # max_supply: u64,
        # name: String,
        # uri: String,
        # mutable_description: bool,
        # mutable_royalty: bool,
        # mutable_uri: bool,
        # mutable_token_description: bool,
        # mutable_token_name: bool,
        # mutable_token_properties: bool,
        # mutable_token_uri: bool,
        # tokens_burnable_by_creator: bool,
        # tokens_freezable_by_creator: bool,
        # royalty_numerator: u64,
        # royalty_denominator: u64,

        payload = EntryFunction.natural(
            "0x4::nft",
            "create_collection",
            [],
            transaction_arguments,
        )

        signed_transaction = await self._client.create_bcs_signed_transaction(
            account, TransactionPayload(payload)
        )
        return await self._client.submit_bcs_transaction(signed_transaction)

    async def create_token(
        self,
        account: Account,
        collection_name: str,
        name: str,
        description: str,
        supply: int,
        uri: str,
        royalty_points_per_million: int,
    ) -> str:

        # collection: String,
        # description: String,
        # name: String,
        # uri: String,
        # property_keys: vector < String >,
        # property_types: vector < String >,
        # property_values: vector < vector < u8 >>,

        transaction_arguments = [
            TransactionArgument(collection_name, Serializer.str),
            TransactionArgument(description, Serializer.str),
            TransactionArgument(name, Serializer.str),
            TransactionArgument(uri, Serializer.str),
            TransactionArgument([], Serializer.sequence_serializer(Serializer.str)),
            TransactionArgument([], Serializer.sequence_serializer(Serializer.str)),
            TransactionArgument([], Serializer.sequence_serializer(Serializer.u8))


            # TransactionArgument(supply, Serializer.u64),
            # TransactionArgument(supply, Serializer.u64),

            # TransactionArgument(account.address(), Serializer.struct),
            # SDK assumes per million
            # TransactionArgument(1000000, Serializer.u64),
            # TransactionArgument(royalty_points_per_million, Serializer.u64),
            # TransactionArgument(
            #     [False, False, False, False, False],
            #     Serializer.sequence_serializer(Serializer.bool),
            # ),
            # TransactionArgument([], Serializer.sequence_serializer(Serializer.str)),
            # TransactionArgument(
            #     [], Serializer.sequence_serializer(Serializer.to_bytes)
            # ),
            # TransactionArgument([], Serializer.sequence_serializer(Serializer.str)),
        ]

        payload = EntryFunction.natural(
            "0x4::nft",
            "mint",
            [],
            transaction_arguments,
        )
        signed_transaction = await self._client.create_bcs_signed_transaction(
            account, TransactionPayload(payload)
        )
        return await self._client.submit_bcs_transaction(signed_transaction)

    async def offer_token(
        self,
        account: Account,
        receiver: AccountAddress,
        creator: AccountAddress,
        collection_name: str,
        token_name: str,
        property_version: int,
        amount: int,
        token_address: AccountAddress,
    ) -> str:
        transaction_arguments = [
            # TransactionArgument(creator, Serializer.struct),
            TransactionArgument(token_address, Serializer.struct),
            TransactionArgument(receiver, Serializer.struct),
            # TransactionArgument(creator, Serializer.struct),
            # TransactionArgument(collection_name, Serializer.str),
            # TransactionArgument(token_name, Serializer.str),
            # TransactionArgument(property_version, Serializer.u64),
            # TransactionArgument(amount, Serializer.u64),
        ]

        payload = EntryFunction.natural(
            "0x1::object",
            "transfer",
            [TypeTag(StructTag.from_str("0x4::token::Token"))],
            transaction_arguments,
        )
        signed_transaction = await self._client.create_bcs_signed_transaction(
            account, TransactionPayload(payload)
        )
        return await self._client.submit_bcs_transaction(signed_transaction)

    async def claim_token(
        self,
        account: Account,
        sender: AccountAddress,
        creator: AccountAddress,
        collection_name: str,
        token_name: str,
        property_version: int,
    ) -> str:
        transaction_arguments = [
            TransactionArgument(sender, Serializer.struct),
            TransactionArgument(creator, Serializer.struct),
            TransactionArgument(collection_name, Serializer.str),
            TransactionArgument(token_name, Serializer.str),
            TransactionArgument(property_version, Serializer.u64),
        ]

        payload = EntryFunction.natural(
            "0x3::token_transfers",
            "claim_script",
            [],
            transaction_arguments,
        )
        signed_transaction = await self._client.create_bcs_signed_transaction(
            account, TransactionPayload(payload)
        )
        return await self._client.submit_bcs_transaction(signed_transaction)

    async def direct_transfer_token(
        self,
        sender: Account,
        receiver: Account,
        creators_address: AccountAddress,
        collection_name: str,
        token_name: str,
        property_version: int,
        amount: int,
    ) -> str:
        transaction_arguments = [
            TransactionArgument(creators_address, Serializer.struct),
            TransactionArgument(collection_name, Serializer.str),
            TransactionArgument(token_name, Serializer.str),
            TransactionArgument(property_version, Serializer.u64),
            TransactionArgument(amount, Serializer.u64),
        ]

        payload = EntryFunction.natural(
            "0x3::token",
            "direct_transfer_script",
            [],
            transaction_arguments,
        )

        signed_transaction = await self._client.create_multi_agent_bcs_transaction(
            sender,
            [receiver],
            TransactionPayload(payload),
        )
        return await self._client.submit_bcs_transaction(signed_transaction)

    #
    # Token accessors
    #

    async def get_token(
        self,
        owner: AccountAddress,
        creator: AccountAddress,
        collection_name: str,
        token_name: str,
        property_version: int,
    ) -> Any:
        resource = await self._client.account_resource(owner, "0x4::collection::ConcurrentSupply")
        # resource = await self._client.account_resource(owner, "0x4::token::Token")
        return resource["data"]

        # token_store_handle = resource["data"]["tokens"]["handle"]

        # token_id = {
        #     "token_data_id": {
        #         "creator": str(creator),
        #         "collection": collection_name,
        #         "name": token_name,
        #     },
        #     "property_version": str(property_version),
        # }
        #
        # try:
        #     return await self._client.get_table_item(
        #         token_store_handle,
        #         "0x3::token::TokenId",
        #         "0x3::token::Token",
        #         token_id,
        #     )
        # except ApiError as e:
        #     if e.status_code == 404:
        #         return {
        #             "id": token_id,
        #             "amount": "0",
        #         }
        #     raise

    async def get_token_balance(
        self,
        owner: AccountAddress,
        creator: AccountAddress,
        collection_name: str,
        token_name: str,
        property_version: int,
    ) -> str:
        info = await self.get_token(
            owner, creator, collection_name, token_name, property_version
        )
        return info
        # return info["amount"]

    # async def get_token_data(
    #     self,
    #     creator: AccountAddress,
    #     collection_name: str,
    #     token_name: str,
    #     property_version: int,
    # ) -> Any:
    #     resource = await self._client.account_resource(
    #         creator, "0x4::token::Token"
    #     )
    #     return resource["data"]

    #     # token_data_handle = resource["data"]["token_data"]["handle"]
    #     #
    #     # token_data_id = {
    #     #     "creator": str(creator),
    #     #     "collection": collection_name,
    #     #     "name": token_name,
    #     # }
    #     #
    #     # return await self._client.get_table_item(
    #     #     token_data_handle,
    #     #     "0x3::token::TokenDataId",
    #     #     "0x3::token::TokenData",
    #     #     token_data_id,
    #     # )  # <:!:read_token_data_table
    
    async def get_token_data(
        self,
        creator: str,
        collection_name: str,
        token_name: str,
        property_version: int,
    ) -> Any:
        pdb.set_trace()
        try:
            # Step 1: Get collection data using the get_collection function
            collection = await self.get_collection(creator, collection_name)
            if not collection:
                print("Collection not found.")
                return None

            collection_id = collection.get("id")
            if not collection_id:
                print("Collection ID missing in collection data.")
                return None

            # Step 2: Paginated fetch from history endpoint
            page = 0
            total_count = 0
            while True:
                history_url = f"{INDEXER_URL}/collections/{collection_id}/history"
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(history_url, params={"page": page}, timeout=10) as response:
                            response.raise_for_status()
                            page_data = await response.json()
                except Exception as e:
                    print(f"Failed to fetch token history page {page} for collection {collection_id}: {e}")
                    return None

                # Step 3: Search for the matching token
                data = page_data.get("data", [])
                for token in data:
                    token_data = token.get("token")
                    if (
                        token_data.get("name") == token_name and
                        str(token_data.get("property_version", 0)) == str(property_version)
                    ):
                        return token

                total_count+=len(data)
                if page_data.get("total") < total_count:
                    page += 1
                else:
                    break

            print("Token not found in history.")
            return None

        except Exception as e:
            print(f"An error occurred while fetching token data: {e}")
            return None



    # async def get_collection(
    #     self, creator: AccountAddress, collection_name: str
    # ) -> Any:
    #     resource = await self._client.account_resource(
    #         creator, "0x4::collection::Collection"
    #     )
    #     return resource["data"]

    #     # token_data = resource["data"]["collection_data"]["handle"]
    #     #
    #     # return await self._client.get_table_item(
    #     #     token_data,
    #     #     "0x1::string::String",
    #     #     "0x3::token::CollectionData",
    #     #     collection_name,
    #     # )
    

    async def get_collection(self, creator: str, collection_name: str) -> Any:
        
        try:
            # Convert 0x address to base58 format
            creator_bytes = bytes.fromhex(str(creator).removeprefix("0x"))
            creator_b58 = base58.b58encode(creator_bytes).decode()

            page = 0
            base_url = f"{INDEXER_URL}/collections"
            total_count = 0
            async with aiohttp.ClientSession() as session:
                while True:
                    try:
                        async with session.get(base_url, params={'page': page}, timeout=10) as response:
                            response.raise_for_status()
                            json_data = await response.json()
                    except Exception as e:
                        print(f"Failed to fetch page {page}: {e}")
                        break

                    data = json_data.get("data", [])
                    for item in data:
                        if item.get("creator") == creator_b58 and item.get("name") == collection_name:
                            return item
                    total_count+= len(data)
                    if json_data.get("total") > total_count :
                        page += 1
                    else:
                        break

        except Exception as e:
            print(f"An error occurred while fetching collection: {e}")

        return None

    async def transfer_object(
        self, owner: Account, object: AccountAddress, to: AccountAddress
    ) -> str:
        transaction_arguments = [
            TransactionArgument(object, Serializer.struct),
            TransactionArgument(to, Serializer.struct),
        ]

        payload = EntryFunction.natural(
            "0x1::object",
            "transfer_call",
            [],
            transaction_arguments,
        )

        signed_transaction = await self._client.create_bcs_signed_transaction(
            owner,
            TransactionPayload(payload),
        )
        return await self._client.submit_bcs_transaction(signed_transaction)
