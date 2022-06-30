import json
from cryptography.fernet import Fernet


def encrypt(string, key):
    return Fernet(key).encrypt(string.encode())


def decrypt(string, key):
    return Fernet(key).decrypt(string).decode()


to_encrypt = '{"name":"John", "age":30, "city":"New York"}'
to_file = f'dump.ky'
key = Fernet.generate_key()

enctex = encrypt(to_encrypt, key)
n1 = enctex.decode('UTF-8')

with open(to_file, 'w') as f:
    f.write(n1)
    f.close()

with open(to_file, 'r') as f:
    file_data = f.read()

n2 = file_data.encode('UTF-8')
dectex = decrypt(n2, key)

completed = json.loads(dectex)
print(f'\n\n{completed}')
