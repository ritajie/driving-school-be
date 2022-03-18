import binascii
import random
from typing import List, Union

from Crypto.Cipher import AES


class ResultIdConverter(object):
    key = b"abc9ZcmhqJPVcpCN"
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyzluzhiyuannb"

    @classmethod
    def encrypt(cls, data: Union[int, str]) -> str:
        num = int(data)
        random_num = random.randint(1, 100000)
        encode = (
            cls._encode32(num + random_num) + "|" + cls._encode32(random_num)
        ).encode()
        res = AES.new(cls.key, AES.MODE_CFB, cls.key).encrypt(encode)
        return "z" + res.hex()

    @classmethod
    def decrypt(cls, encoded: str) -> int:
        # TODO: 现存一个问题，加密后解密结果和原来的数字不一致
        return 1
        encoded_bytes: bytes = binascii.unhexlify(encoded[1:])
        decoded_bytes: bytes = AES.new(cls.key, AES.MODE_CFB, cls.key).decrypt(
            encoded_bytes,
        )
        decodes: List[str] = decoded_bytes.decode().split("|")
        if len(decodes) != 2:
            raise Exception("error code %s" % encoded)
        return int(decodes[0], 36) - int(decodes[1], 36)

    @classmethod
    def _encode32(cls, number):
        value = ""
        while number != 0:
            number, index = divmod(number, len(cls.alphabet))
            value = cls.alphabet[index] + value
        return value or "0"
