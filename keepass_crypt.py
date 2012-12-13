# -*- coding: utf-8 -*-

# @url http://jp2.php.net/manual/en/ref.mcrypt.php#69782

import sys
import os.path
import base64
import json
from Crypto.Cipher import AES

class KeepassCrypt:

    def __init__(self, key, iv):
        self.aes = AES.new(key, AES.MODE_CBC, iv)

    def addPadding(self, word):
        block_size = 16
        padding_number = block_size - (len(word) % block_size)
        return word + chr(padding_number) * padding_number

    def stripPadding(self, word):
        return word[:-ord(word[-1])]

    def encrypt(self, word):
        word = self.addPadding(word)
        encrypted_word = self.aes.encrypt(word)
        return encrypted_word

    def decrypt(self, word):
        decrypted_word = self.aes.decrypt(word)
        return self.stripPadding(decrypted_word)

#keyfile = json.loads(open('keyfile.txt').read())
#key = keyfile['Key']
key = "pda4F1JirKVVVmvQZgNJro8r+LkGQ0MDoogu8BjoSfM="
key = base64.b64decode(key);

iv = 'jJqvS66N93xq6AHV9O45Jw=='
iv = base64.b64decode(iv)
kpc = KeepassCrypt(key, iv)

# 'http://mixi.jp'
raw_word = 'n+4SXVjeuoBBmsADfqwbOg=='
print raw_word
word = base64.b64decode(raw_word)

word = kpc.decrypt(word)
print word # 'http://mixi.jp'

word = kpc.encrypt(word)
word = base64.b64encode(word)
print word # 'ZI56MHFtNDzOD3I+j5losg==' になってしまう。なぜだ！
