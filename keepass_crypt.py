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

    if (block_size > len(word)):
      fill_len = block_size - len(word)
    elif (len(word) % block_size == 0):
      fill_len = 0
    else:
      fill_len = block_size - (len(word) % block_size)

    pad_char = chr(fill_len)

    return word + pad_char * fill_len

  def stripPadding(self, word):
    pad_char = ord(word[-1:])

    if (pad_char > len(word)):
      return word

    return word.rstrip(chr(pad_char))

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
print word

word = kpc.encrypt("http://mixi.jp")
word = base64.b64encode(word)
print word

sys.exit()
