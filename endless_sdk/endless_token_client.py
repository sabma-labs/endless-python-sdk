# Copyright © Endless Foundation
# Copyright © Aptos Foundation
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any, List, Tuple , Optional
import pdb
from .account import Account
from .account_address import AccountAddress
from .async_client import RestClient
from .bcs import Deserializer, Serializer ,Serializable
from .transactions import EntryFunction, TransactionArgument, TransactionPayload
from .type_tag import StructTag, TypeTag


class Object:
    allow_ungated_transfer: bool
    owner: AccountAddress

    struct_tag: str = "0x1::object::ObjectCore"

    def __init__(self, allow_ungated_transfer, owner):
        self.allow_ungated_transfer = allow_ungated_transfer
        self.owner = owner

    @staticmethod
    def parse(resource: dict[str, Any]) -> Object:
        return Object(
            resource["allow_ungated_transfer"],
            AccountAddress.from_str_relaxed(resource["owner"]),
        )

    def __str__(self) -> str:
        return f"Object[allow_ungated_transfer: {self.allow_ungated_transfer}, owner: {self.owner}]"


class Collection:
    creator: AccountAddress
    description: str
    name: str
    uri: str

    struct_tag: str = "0x4::collection::Collection"

    def __init__(self, creator, description, name, uri):
        self.creator = creator
        self.description = description
        self.name = name
        self.uri = uri

    def __str__(self) -> str:
        return f"AccountAddress[creator: {self.creator}, description: {self.description}, name: {self.name}, ur: {self.uri}]"

    @staticmethod
    def parse(resource: dict[str, Any]) -> Collection:
        return Collection(
            AccountAddress.from_str_relaxed(resource["creator"]),
            resource["description"],
            resource["name"],
            resource["uri"],
        )

# class Option(Serializable):
#     """
#     An optional wrapper for Move types, similar to Rust's Option<T>.
#     Holds either zero or one element of type T.
#     """
#     def __init__(self, value = None) -> None:
#         super().__init__()
#         if value is not None:
#             self._vec = [value]
#         else:
#             self._vec = []
#         # Expose the single value or None
#         self.value  = self._vec.values[0] if self._vec.values else None

#     def unwrap(self) -> T:
#         """
#         Retrieve the inner value, or raise if empty.

#         Raises:
#             ValueError: if the option is empty.

#         Returns:
#             The contained T value.
#         """
#         if not self.is_some():
#             raise ValueError("Called unwrap on an empty MoveOption")
#         # At this point, _vec.values has exactly one element
#         return self._vec.values[0]

#     def is_some(self) -> bool:
#         """
#         Returns True if the option contains a value.
#         """
#         return len(self._vec.values) == 1

#     def serialize(self, serializer: Serializer) -> None:
#         """
#         Serialize the option (0 or 1, followed by the value if present) in BCS.
#         """
#         self._vec.serialize(serializer)

class Royalty(Serializable):
    numerator: int
    denominator: int
    payee_address: AccountAddress

    struct_tag: str = "0x4::royalty::Royalty"

    def __init__(self, numerator, denominator, payee_address):
        self.numerator = numerator
        self.denominator = denominator
        self.payee_address = payee_address

    def __str__(self) -> str:
        return f"Royalty[numerator: {self.numerator}, denominator: {self.denominator}, payee_address: {self.payee_address}]"

    @staticmethod
    def parse(resource: dict[str, Any]) -> Royalty:
        return Royalty(
            resource["numerator"],
            resource["denominator"],
            AccountAddress.from_str_relaxed(resource["payee_address"]),
        )
    def serialize(self,serializer: Serializer):
        serializer.u64(self.numerator)
        serializer.u64(self.denominator)
        serializer.address(str(self.payee_address))  # or .hex() / .address_str


class Token:
    collection: AccountAddress
    index: int
    description: str
    name: str
    uri: str

    struct_tag: str = "0x4::token::Token"

    def __init__(
        self,
        collection: AccountAddress,
        index: int,
        description: str,
        name: str,
        uri: str,
    ):
        self.collection = collection
        self.index = index
        self.description = description
        self.name = name
        self.uri = uri

    def __str__(self) -> str:
        return f"Token[collection: {self.collection}, index: {self.index}, description: {self.description}, name: {self.name}, uri: {self.uri}]"

    @staticmethod
    def parse(resource: dict[str, Any]):
        return Token(
            AccountAddress.from_str_relaxed(resource["collection"]["inner"]),
            int(resource["index"]),
            resource["description"],
            resource["name"],
            resource["uri"],
        )


class InvalidPropertyType(Exception):
    """Invalid property type"""

    property_type: Any

    def __init__(self, property_type: Any):
        message = f"Unknown property type: {property_type}"
        super().__init__(message)
        self.property_type = property_type


class Property:
    name: str
    property_type: str
    value: Any

    BOOL: int = 0
    U8: int = 1
    U16: int = 2
    U32: int = 3
    U64: int = 4
    U128: int = 5
    U256: int = 6
    ADDRESS: int = 7
    BYTE_VECTOR: int = 8
    STRING: int = 9

    def __init__(self, name: str, property_type: str, value: Any):
        self.name = name
        self.property_type = property_type
        self.value = value

    def __str__(self) -> str:
        return f"Property[{self.name}, {self.property_type}, {self.value}]"

    def serialize_value(self) -> bytes:
        ser = Serializer()
        if self.property_type == "bool":
            Serializer.bool(ser, self.value)
        elif self.property_type == "u8":
            Serializer.u8(ser, self.value)
        elif self.property_type == "u16":
            Serializer.u16(ser, self.value)
        elif self.property_type == "u32":
            Serializer.u32(ser, self.value)
        elif self.property_type == "u64":
            Serializer.u64(ser, self.value)
        elif self.property_type == "u128":
            Serializer.u128(ser, self.value)
        elif self.property_type == "u256":
            Serializer.u256(ser, self.value)
        elif self.property_type == "address":
            Serializer.struct(ser, self.value)
        elif self.property_type == "0x1::string::String":
            Serializer.str(ser, self.value)
        elif self.property_type == "vector<u8>":
            Serializer.to_bytes(ser, self.value)
        else:
            raise InvalidPropertyType(self.property_type)
        return ser.output()

    def to_transaction_arguments(self) -> List[TransactionArgument]:
        return [
            TransactionArgument(self.name, Serializer.str),
            TransactionArgument(self.property_type, Serializer.str),
            TransactionArgument(self.serialize_value(), Serializer.to_bytes),
        ]

    @staticmethod
    def parse(name: str, property_type: int, value: bytes) -> Property:
        deserializer = Deserializer(value)

        if property_type == Property.BOOL:
            return Property(name, "bool", deserializer.bool())
        elif property_type == Property.U8:
            return Property(name, "u8", deserializer.u8())
        elif property_type == Property.U16:
            return Property(name, "u16", deserializer.u16())
        elif property_type == Property.U32:
            return Property(name, "u32", deserializer.u32())
        elif property_type == Property.U64:
            return Property(name, "u64", deserializer.u64())
        elif property_type == Property.U128:
            return Property(name, "u128", deserializer.u128())
        elif property_type == Property.U256:
            return Property(name, "u256", deserializer.u256())
        elif property_type == Property.ADDRESS:
            return Property(name, "address", AccountAddress.deserialize(deserializer))
        elif property_type == Property.STRING:
            return Property(name, "0x1::string::String", deserializer.str())
        elif property_type == Property.BYTE_VECTOR:
            return Property(name, "vector<u8>", deserializer.to_bytes())
        raise InvalidPropertyType(property_type)

    @staticmethod
    def bool(name: str, value: bool) -> Property:
        return Property(name, "bool", value)

    @staticmethod
    def u8(name: str, value: int) -> Property:
        return Property(name, "u8", value)

    @staticmethod
    def u16(name: str, value: int) -> Property:
        return Property(name, "u16", value)

    @staticmethod
    def u32(name: str, value: int) -> Property:
        return Property(name, "u32", value)

    @staticmethod
    def u64(name: str, value: int) -> Property:
        return Property(name, "u64", value)

    @staticmethod
    def u128(name: str, value: int) -> Property:
        return Property(name, "u128", value)

    @staticmethod
    def u256(name: str, value: int) -> Property:
        return Property(name, "u256", value)

    @staticmethod
    def string(name: str, value: str) -> Property:
        return Property(name, "0x1::string::String", value)

    @staticmethod
    def bytes(name: str, value: bytes) -> Property:
        return Property(name, "vector<u8>", value)


class PropertyMap:
    properties: List[Property]

    struct_tag: str = "0x4::property_map::PropertyMap"

    def __init__(self, properties: List[Property]):
        self.properties = properties

    def __str__(self) -> str:
        response = "PropertyMap["
        for prop in self.properties:
            response += f"{prop}, "
        if len(self.properties) > 0:
            response = response[:-2]
        response += "]"
        return response

    def to_tuple(self) -> Tuple[List[str], List[str], List[bytes]]:
        names = []
        types = []
        values = []

        for prop in self.properties:
            names.append(prop.name)
            types.append(prop.property_type)
            values.append(prop.serialize_value())

        return (names, types, values)

    @staticmethod
    def parse(resource: dict[str, Any]) -> PropertyMap:
        props = resource["inner"]["data"]
        properties = []
        for prop in props:
            properties.append(
                Property.parse(
                    prop["key"],
                    prop["value"]["type"],
                    bytes.fromhex(prop["value"]["value"][2:]),
                )
            )

        return PropertyMap(properties)


class ReadObject:
    resource_map: dict[str, Any] = {
        Collection.struct_tag: Collection,
        Object.struct_tag: Object,
        PropertyMap.struct_tag: PropertyMap,
        Royalty.struct_tag: Royalty,
        Token.struct_tag: Token,
    }

    resources: dict[Any, Any]

    def __init__(self, resources: dict[Any, Any]):
        self.resources = resources

    def __str__(self) -> str:
        response = "ReadObject"
        for resource_obj, value in self.resources.items():
            response += f"\n\t{resource_obj.struct_tag}: {value}"

        return response


class EndlessTokenClient:
    """A wrapper around reading and mutating Digital Assets also known as Token Objects"""

    client: RestClient

    def __init__(self, client: RestClient):
        self.client = client

    async def read_object(self, address: AccountAddress) -> ReadObject:
        resources = {}

        read_resources = await self.client.account_resources(address)
        for resource in read_resources:
            if resource["type"] in ReadObject.resource_map:
                resource_obj = ReadObject.resource_map[resource["type"]]
                resources[resource_obj] = resource_obj.parse(resource["data"])
        return ReadObject(resources)

    # @staticmethod
    # def create_collection_payload(
    #     description: str,
    #     max_supply: int,
    #     name: str,
    #     royalty: Optional[Royalty],
    #     uri: str,
    # ) -> TransactionPayload:
    #     s = Serializer()
    #     opt_royalty_ser = Serializer.option_serializer(Serializer.struct)
    #     opt_royalty_ser(s, royalty)
    #     raw = s.output()
    #     print(raw)
    #     transaction_arguments = [
    #         TransactionArgument(description, Serializer.str),
    #         TransactionArgument(max_supply, Serializer.u64),
    #         TransactionArgument(name, Serializer.str),
    #         TransactionArgument(raw,Serializer.fixed_bytes),
    #         TransactionArgument(uri, Serializer.str),
    #     ]
        
    #     for i, arg in enumerate(transaction_arguments):
    #         b = arg.encode()
    #         print(f"arg#{i} ({type(arg.value).__name__}): {b.hex()} len={len(b)}")

    #     payload = EntryFunction.natural(
    #         "0x4::collection",
    #         "create_fixed_collection",
    #         [],
    #         transaction_arguments,
    #     )

    #     return TransactionPayload(payload)
    @staticmethod
    def create_collection_payload(
        description: str,
        max_supply: int,
        name: str,
        royalty: Optional[Royalty],
        uri: str,
    ) -> TransactionPayload:
        # Build args with the right serializers:
        args = [
            TransactionArgument(description, Serializer.str),
            TransactionArgument(max_supply,    Serializer.u64),
            TransactionArgument(name,          Serializer.str),
            TransactionArgument(royalty,       Serializer.option_serializer(Serializer.struct)),
            TransactionArgument(uri,           Serializer.str),
        ]
        payload = EntryFunction.natural(
            "0x4::collection",
            "create_fixed_collection",
            [],      # no type parameters
            args,
        )
        return TransactionPayload(payload)
    # :!:>create_collection
    async def create_collection(
        self,
        creator: Account,
        description: str,
        max_supply: int, 
        name: str,
        uri: str,
        royalty_numerator: int,
        royalty_denominator: int,
    ) -> str:  # <:!:create_collection
        royalty =  Royalty(royalty_numerator,royalty_denominator, creator.address())
        
        payload = EndlessTokenClient.create_collection_payload(
            description,
            max_supply,
            name,
            royalty,
            uri,
        )
        
        print("JSON args:", payload.__str__())

        signed_transaction = await self.client.create_bcs_signed_transaction(
            creator, payload
        )
        return await self.client.submit_bcs_transaction(signed_transaction)

    @staticmethod
    def mint_token_payload(
        collection: str,
        description: str,
        name: str,
        uri: str,
        properties: PropertyMap,
    ) -> TransactionPayload:
        (property_names, property_types, property_values) = properties.to_tuple()
        transaction_arguments = [
            TransactionArgument(collection, Serializer.str),
            TransactionArgument(description, Serializer.str),
            TransactionArgument(name, Serializer.str),
            TransactionArgument(uri, Serializer.str),
            TransactionArgument(
                property_names, Serializer.sequence_serializer(Serializer.str)
            ),
            TransactionArgument(
                property_types, Serializer.sequence_serializer(Serializer.str)
            ),
            TransactionArgument(
                property_values, Serializer.sequence_serializer(Serializer.to_bytes)
            ),
        ]

        payload = EntryFunction.natural(
            "0x4::endless_token",
            "mint",
            [],
            transaction_arguments,
        )

        return TransactionPayload(payload)

    # :!:>mint_token
    async def mint_token(
        self,
        creator: Account,
        collection: str,
        description: str,
        name: str,
        uri: str,
        properties: PropertyMap,
    ) -> str:  # <:!:mint_token
        payload = EndlessTokenClient.mint_token_payload(
            collection, description, name, uri, properties
        )
        signed_transaction = await self.client.create_bcs_signed_transaction(
            creator, payload
        )
        return await self.client.submit_bcs_transaction(signed_transaction)

    async def mint_soul_bound_token(
        self,
        creator: Account,
        collection: str,
        description: str,
        name: str,
        uri: str,
        properties: PropertyMap,
        soul_bound_to: AccountAddress,
    ):
        (property_names, property_types, property_values) = properties.to_tuple()
        transaction_arguments = [
            TransactionArgument(collection, Serializer.str),
            TransactionArgument(description, Serializer.str),
            TransactionArgument(name, Serializer.str),
            TransactionArgument(uri, Serializer.str),
            TransactionArgument(
                property_names, Serializer.sequence_serializer(Serializer.str)
            ),
            TransactionArgument(
                property_types, Serializer.sequence_serializer(Serializer.str)
            ),
            TransactionArgument(
                property_values, Serializer.sequence_serializer(Serializer.to_bytes)
            ),
            TransactionArgument(soul_bound_to, Serializer.struct),
        ]

        payload = EntryFunction.natural(
            "0x4::endless_token",
            "mint_soul_bound",
            [],
            transaction_arguments,
        )

        signed_transaction = await self.client.create_bcs_signed_transaction(
            creator, TransactionPayload(payload)
        )
        return await self.client.submit_bcs_transaction(signed_transaction)

    # :!:>transfer_token
    async def transfer_token(
        self, owner: Account, token: AccountAddress, to: AccountAddress
    ) -> str:
        return await self.client.transfer_object(owner, token, to)  # <:!:transfer_token

    async def burn_token(self, creator: Account, token: AccountAddress) -> str:
        payload = EntryFunction.natural(
            "0x4::endless_token",
            "burn",
            [TypeTag(StructTag.from_str("0x4::token::Token"))],
            [TransactionArgument(token, Serializer.struct)],
        )

        signed_transaction = await self.client.create_bcs_signed_transaction(
            creator, TransactionPayload(payload)
        )
        return await self.client.submit_bcs_transaction(signed_transaction)

    async def freeze_token(self, creator: Account, token: AccountAddress) -> str:
        payload = EntryFunction.natural(
            "0x4::endless_token",
            "freeze_transfer",
            [TypeTag(StructTag.from_str("0x4::token::Token"))],
            [TransactionArgument(token, Serializer.struct)],
        )

        signed_transaction = await self.client.create_bcs_signed_transaction(
            creator, TransactionPayload(payload)
        )
        return await self.client.submit_bcs_transaction(signed_transaction)

    async def unfreeze_token(self, creator: Account, token: AccountAddress) -> str:
        payload = EntryFunction.natural(
            "0x4::endless_token",
            "unfreeze_transfer",
            [TypeTag(StructTag.from_str("0x4::token::Token"))],
            [TransactionArgument(token, Serializer.struct)],
        )

        signed_transaction = await self.client.create_bcs_signed_transaction(
            creator, TransactionPayload(payload)
        )
        return await self.client.submit_bcs_transaction(signed_transaction)

    async def add_token_property(
        self, creator: Account, token: AccountAddress, prop: Property
    ) -> str:
        transaction_arguments = [TransactionArgument(token, Serializer.struct)]
        transaction_arguments.extend(prop.to_transaction_arguments())

        payload = EntryFunction.natural(
            "0x4::endless_token",
            "add_property",
            [TypeTag(StructTag.from_str("0x4::token::Token"))],
            transaction_arguments,
        )

        signed_transaction = await self.client.create_bcs_signed_transaction(
            creator, TransactionPayload(payload)
        )
        return await self.client.submit_bcs_transaction(signed_transaction)

    async def remove_token_property(
        self, creator: Account, token: AccountAddress, name: str
    ) -> str:
        transaction_arguments = [
            TransactionArgument(token, Serializer.struct),
            TransactionArgument(name, Serializer.str),
        ]

        payload = EntryFunction.natural(
            "0x4::endless_token",
            "remove_property",
            [TypeTag(StructTag.from_str("0x4::token::Token"))],
            transaction_arguments,
        )

        signed_transaction = await self.client.create_bcs_signed_transaction(
            creator, TransactionPayload(payload)
        )
        return await self.client.submit_bcs_transaction(signed_transaction)

    async def update_token_property(
        self, creator: Account, token: AccountAddress, prop: Property
    ) -> str:
        transaction_arguments = [TransactionArgument(token, Serializer.struct)]
        transaction_arguments.extend(prop.to_transaction_arguments())

        payload = EntryFunction.natural(
            "0x4::endless_token",
            "update_property",
            [TypeTag(StructTag.from_str("0x4::token::Token"))],
            transaction_arguments,
        )

        signed_transaction = await self.client.create_bcs_signed_transaction(
            creator, TransactionPayload(payload)
        )
        return await self.client.submit_bcs_transaction(signed_transaction)

    async def tokens_minted_from_transaction(
        self, txn_hash: str
    ) -> List[AccountAddress]:
        output = await self.client.transaction_by_hash(txn_hash)
        mints = []
        for event in output["events"]:
            if event["type"] not in (
                "0x4::collection::MintEvent",
                "0x4::collection::Mint",
            ):
                continue
            mints.append(AccountAddress.from_str_relaxed(event["data"]["token"]))
        return mints
