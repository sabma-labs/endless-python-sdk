import unittest
from endless_sdk.ed25519 import PrivateKey, PublicKey, MultiPublicKey, Signature, MultiSignature
from endless_sdk.bcs import Serializer, Deserializer

class EDSTest(unittest.TestCase):

    # def test_create_public_key_from_hex(self):
    #     '''
    #     this test case is failing because Providing a hex private-key  
    #     into PrivateKey.from_str(…),  & deriving its corresponding Ed25519 public key, 
    #     and then  to expect the public key’s hex‐string to be exactly the same as the original hex string is wrong. 
    #     In Ed25519, the public key is a completely different 32-byte value, 
    #     derived (via the curve’s base‐point multiplication) from the private seed.
        
    #     '''
    #     hex_string = "0x0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
    #     private_key = PrivateKey.from_str(hex_string)
    #     public_key = private_key.public_key()
    #     self.assertEqual(public_key.__str__(), hex_string)

    def test_verify_correct_signature(self):
        message = b"test_message"
        private_key = PrivateKey.random()
        public_key = private_key.public_key()
        signature = private_key.sign(message)
        self.assertTrue(public_key.verify(message, signature))

    def test_private_key_serialization(self):
        private_key = PrivateKey.random()
        ser = Serializer()
        private_key.serialize(ser)
        deserializer = Deserializer(ser.output())
        ser_private_key = PrivateKey.deserialize(deserializer)
        self.assertEqual(private_key, ser_private_key)

    def test_public_key_serialization(self):
        private_key = PrivateKey.random()
        public_key = private_key.public_key()
        ser = Serializer()
        public_key.serialize(ser)
        deserializer = Deserializer(ser.output())
        ser_public_key = PublicKey.deserialize(deserializer)
        self.assertEqual(public_key, ser_public_key)

    def test_signature_serialization(self):
        private_key = PrivateKey.random()
        message = b"another_message"
        signature = private_key.sign(message)
        ser = Serializer()
        signature.serialize(ser)
        deserializer = Deserializer(ser.output())
        ser_signature = Signature.deserialize(deserializer)
        self.assertEqual(signature, ser_signature)

    def test_multisig(self):
        private_key_1 = PrivateKey.random()
        private_key_2 = PrivateKey.random()
        multisig_public_key = MultiPublicKey([private_key_1.public_key(), private_key_2.public_key()], 1)
        message = b"multisig"
        signature_1 = private_key_1.sign(message)
        multisig_signature = MultiSignature.from_key_map(multisig_public_key, [(private_key_1.public_key(), signature_1)])
        self.assertTrue(multisig_public_key.verify(message, multisig_signature))

    def test_multisig_serialization(self):
        private_key_1 = PrivateKey.random()
        private_key_2 = PrivateKey.random()
        multisig_public_key = MultiPublicKey([private_key_1.public_key(), private_key_2.public_key()], 1)
        ser = Serializer()
        multisig_public_key.serialize(ser)
        deserializer = Deserializer(ser.output())
        ser_multisig_public_key = MultiPublicKey.deserialize(deserializer)
        self.assertEqual(multisig_public_key, ser_multisig_public_key)

    def test_multisig_signature_serialization(self):
        private_key_1 = PrivateKey.random()
        private_key_2 = PrivateKey.random()
        message = b"multisig"
        signature_1 = private_key_1.sign(message)
        multisig_public_key = MultiPublicKey([private_key_1.public_key(), private_key_2.public_key()], 1)
        multisig_signature = MultiSignature.from_key_map(multisig_public_key, [(private_key_1.public_key(), signature_1)])
        ser = Serializer()
        multisig_signature.serialize(ser)
        deserializer = Deserializer(ser.output())
        ser_multisig_signature = MultiSignature.deserialize(deserializer)
        self.assertEqual(multisig_signature, ser_multisig_signature)

    def test_generate_random_private_key(self):
        private_key1 = PrivateKey.random()
        private_key2 = PrivateKey.random()
        self.assertNotEqual(private_key1, private_key2)

    def test_derive_public_key_from_private_key(self):
        private_key = PrivateKey.random()
        public_key = private_key.public_key()
        self.assertIsInstance(public_key, PublicKey)

if __name__ == '__main__':
    unittest.main()
