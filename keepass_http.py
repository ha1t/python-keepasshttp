# -*- coding: utf-8 -*-
# @url http://stackoverflow.com/questions/7954661/aes-256-encryption-with-pycrypto-using-cbc-mode-any-weaknesses
# TODO: AddPadding, Trimが必要

import getpass
import os.path
import sys
import base64
import json
from Crypto.Cipher import AES
import socket
from kptool.keepassdb import keepassdb

if len(sys.argv) != 2 or not os.path.exists(sys.argv[1]):
  print "Usage: keepass_http.py KeePassDBPath"
  sys.exit()

#db_path = "/Users/halt/Dropbox/Private/KeePass/halt.kdb"
db_path = sys.argv[1]
print "KeePass DB v1 path:" + db_path

password = getpass.getpass("Enter Password: ")

def handle_request(request):
  header, body = request.split('\r\n\r\n')
  response = json.loads(body)

  print '-- start response ------'
  print response

  if response['RequestType'] == 'associate':
    response['Id'] = 'chromeipass'
    response['Success'] = True

    file_handle = open('keyfile.txt', 'w')
    file_handle.write(body)
    file_handle.close()

  elif response['RequestType'] == 'test-associate':
    response['Id'] = 'chromeipass'
    response['Success'] = True

  elif response['RequestType'] == 'get-logins':
    global db_path
    global password
    url = decrypt(response['Url'], response['Nonce'])
    k = keepassdb.KeepassDBv1(db_path, password)
    for e in k.find_entries():
      print e
      response['Name']     = e['title']
      response['Login']    = e['username']
      response['Uuid']     = e['id']
      response['Password'] = e['password']
      break;

  else:
    print '-- start unknown request type response ------'
    print response

  http_response = create_response(json.dumps(response))
  return http_response

def create_response(body):
  data = []
  data.append('HTTP/1.1 200 OK')
  data.append('Connection: close')
  data.append('Content-Type: application/json; charset=utf-8')
  data.append('')
  data.append(body)
  data.append('')

  response = "\r\n".join(data)

  print '-- start create_response'
  print response

  return response

class KeepassCrypt:

  def __init__(self, iv):

    keyfile = json.loads(open('keyfile.txt').read())
    key = keyfile['Key']
    key = base64.b64decode(key);

    self.aes = AES.new(key, AES.MODE_CBC, iv)

  def encrypt(self, word):
    return self.aes.encrypt(word)

  def decrypt(self, word):
    decrypted_word = self.aes.decrypt(word)
    return decrypted_word[0:-2]

raw_iv = 'jJqvS66N93xq6AHV9O45Jw=='
iv = base64.b64decode(raw_iv)
kpc = KeepassCrypt(iv)

raw_word = 'n+4SXVjeuoBBmsADfqwbOg=='
word = base64.b64decode(raw_word)
#word = 'http://mixi.jp'

word = kpc.decrypt(word)
print word
word = kpc.encrypt(word)
word = base64.b64encode(word)
print word

sys.exit()


host = 'localhost'
port = 19455

serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversock.bind((host,port))
serversock.listen(1)
print 'Waiting for connections...'
clientsock, client_address = serversock.accept()

while True:
  rcvmsg = clientsock.recv(4096)
  #print 'Received -> %s' % (rcvmsg)
  print 'Wait...'

  response = handle_request(rcvmsg)

  clientsock.sendall(response)
clientsock.close()

