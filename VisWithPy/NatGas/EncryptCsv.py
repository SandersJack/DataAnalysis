from cryptography.fernet import Fernet
import os
import Constants

fernet = Fernet(Constants.csv_key)

directory = "dataSets/"

for file in os.listdir(directory):
    filename = os.fsdecode(file)

    with open(directory+filename, 'rb') as file:
        original = file.read()


    encrypted = fernet.encrypt(original)
    
    with open('dataSets-Encrypt/'+filename, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)