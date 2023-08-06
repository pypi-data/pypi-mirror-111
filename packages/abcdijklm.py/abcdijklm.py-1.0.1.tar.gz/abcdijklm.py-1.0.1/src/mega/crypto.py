from Crypto.Cipher import AES
import json
import base64
import struct
import binascii
import random
import sys

# Python3 compatibility
if sys.version_info < (3, ):

    async def makebyte(x):
        return x

    async def makestring(x):
        return x
else:
    import codecs

    async def makebyte(x):
        return codecs.latin_1_encode(x)[0]

    async def makestring(x):
        return codecs.latin_1_decode(x)[0]


async def aes_cbc_encrypt(data, key):
    aes_cipher = AES.new(key, AES.MODE_CBC, makebyte('\0' * 16))
    return aes_cipher.encrypt(data)


async def aes_cbc_decrypt(data, key):
    aes_cipher = AES.new(key, AES.MODE_CBC, makebyte('\0' * 16))
    return aes_cipher.decrypt(data)


async def aes_cbc_encrypt_a32(data, key):
    return await str_to_a32(await aes_cbc_encrypt(await a32_to_str(data), await a32_to_str(key)))


async def aes_cbc_decrypt_a32(data, key):
    return await str_to_a32(await aes_cbc_decrypt(await a32_to_str(data), await a32_to_str(key)))


async def stringhash(str, aeskey):
    s32 = await str_to_a32(str)
    h32 = [0, 0, 0, 0]
    for i in range(len(s32)):
        h32[i % 4] ^= s32[i]
    for r in range(0x4000):
        h32 = await aes_cbc_encrypt_a32(h32, aeskey)
    return await a32_to_base64((h32[0], h32[2]))


async def prepare_key(arr):
    pkey = [0x93C467E3, 0x7DB0C7A4, 0xD1BE3F81, 0x0152CB56]
    for r in range(0x10000):
        for j in range(0, len(arr), 4):
            key = [0, 0, 0, 0]
            for i in range(4):
                if i + j < len(arr):
                    key[i] = arr[i + j]
            pkey = await aes_cbc_encrypt_a32(pkey, key)
    return pkey


async def encrypt_key(a, key):
    return sum((await aes_cbc_encrypt_a32(a[i:i + 4], key)
                for i in range(0, len(a), 4)), ())


async def decrypt_key(a, key):
    return sum((await aes_cbc_decrypt_a32(a[i:i + 4], key)
                for i in range(0, len(a), 4)), ())


async def encrypt_attr(attr, key):
    attr = await makebyte('MEGA' + json.dumps(attr))
    if len(attr) % 16:
        attr += b'\0' * (16 - len(attr) % 16)
    return await aes_cbc_encrypt(attr, await a32_to_str(key))


async def decrypt_attr(attr, key):
    attr = await aes_cbc_decrypt(attr, await a32_to_str(key))
    attr = await makestring(attr)
    attr = attr.rstrip('\0')
    return json.loads(attr[4:]) if attr[:6] == 'MEGA{"' else False


async def a32_to_str(a):
    return struct.pack('>%dI' % len(a), *a)


async def str_to_a32(b):
    if isinstance(b, str):
        b = await makebyte(b)
    if len(b) % 4:
        # pad to multiple of 4
        b += b'\0' * (4 - len(b) % 4)
    return struct.unpack('>%dI' % (len(b) / 4), b)


async def mpi_to_int(s):
    """
    A Multi-precision integer is encoded as a series of bytes in big-endian
    order. The first two bytes are a header which tell the number of bits in
    the integer. The rest of the bytes are the integer.
    """
    return int(binascii.hexlify(s[2:]), 16)


async def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = await extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)


async def modular_inverse(a, m):
    g, x, y = await extended_gcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


async def base64_url_decode(data):
    data += '=='[(2 - len(data) * 3) % 4:]
    for search, replace in (('-', '+'), ('_', '/'), (',', '')):
        data = data.replace(search, replace)
    return base64.b64decode(data)


async def base64_to_a32(s):
    return await str_to_a32(await base64_url_decode(s))


async def base64_url_encode(data):
    data = base64.b64encode(data)
    data = await makestring(data)
    for search, replace in (('+', '-'), ('/', '_'), ('=', '')):
        data = data.replace(search, replace)
    return data


async def a32_to_base64(a):
    return await base64_url_encode(await a32_to_str(a))


async def get_chunks(size):
    p = 0
    s = 0x20000
    while p + s < size:
        yield (p, s)
        p += s
        if s < 0x100000:
            s += 0x20000
    yield (p, size - p)


def make_id(length):
    text = ''
    possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    for i in range(length):
        text += random.choice(possible)
    return text
