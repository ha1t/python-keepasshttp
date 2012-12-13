# -*- coding: utf-8 -*-

# @url http://jp2.php.net/manual/en/ref.mcrypt.php#69782

from Crypto.Cipher import AES

class KeePassCrypt(object):

    def __init__(self, key, iv):
        self.key = key
        self.iv = iv

    @property
    def aes(self):
        return AES.new(self.key, AES.MODE_CBC, self.iv)

    def addPadding(self, word):
        block_size = 16
        padding_number = block_size - (len(word) % block_size)
        return word + chr(padding_number) * padding_number

    def stripPadding(self, word):
        return word[:-ord(word[-1])]

    def encrypt(self, word):
        word = self.addPadding(word)
        return self.aes.encrypt(word)

    def decrypt(self, word):
        decrypted_word = self.aes.decrypt(word)
        return self.stripPadding(decrypted_word)

