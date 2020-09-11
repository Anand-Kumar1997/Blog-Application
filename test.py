# from cryptography.fernet import Fernet
# key1 = Fernet.generate_key()
# key = b'wrbcK7TU_S8mPA-YYO5ZoqIh90huixAHE_oI0n33cKw='
# password = b'soni@1234'

# f = Fernet(key)
# enc_pwd = f.encrypt(password)
# dec_pwd = (f.decrypt(enc_pwd))

# print(dec_pwd)

#--------------------------------------------------------------

from cryptography.fernet import Fernet
key = b'pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY='
cipher_suite = Fernet(key)
ciphered_text = cipher_suite.encrypt(b'SuperSecretpassword')
# with open('E:\\Python\\Python Flask Apps\\Simple Flask Apps\\BlogApp\\mssqltip_bytes.bin', 'wb') as file_object:  file_object.write(ciphered_text)

# with open('E:\\Python\\Python Flask Apps\\Simple Flask Apps\\BlogApp\\mssqltip_bytes.bin', 'rb') as file_object:
#     for line in file_object:
#         encryptedpwd = line
# # print(encryptedpwd)
# uncipher_text = (cipher_suite.decrypt(encryptedpwd))
# plain_text_encryptedpassword = uncipher_text.decode()
# print(plain_text_encryptedpassword)
cipher_suite.encrypt(base64.encodestring(bytes(s, encoding="ascii")))
