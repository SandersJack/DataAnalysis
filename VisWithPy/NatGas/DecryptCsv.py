from cryptography.fernet import Fernet
import os
import Constants

fernet = Fernet(Constants.csv_key)
directory = "dataSets-Encrypt/"

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    
    with open(directory+filename, 'rb') as enc_file:
        encrypted = enc_file.read()

    decrypted = fernet.decrypt(encrypted)
    
    with open('dataSets/'+filename, 'wb') as dec_file:
        dec_file.write(decrypted)