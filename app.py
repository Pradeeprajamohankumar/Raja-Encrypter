from cryptography.fernet import Fernet
import os

SUPPORTED_FORMATS = ['.txt', '.pdf', '.ppt', '.docx', '.doc', '.jpg', '.png', '.jpeg', '.pptx', '.xlsm', '.xls', '.rtf','.HEIC']
ENCRYPTION_MARKER = b'ENCRYPTEDFILE'

def generate_key():
    return Fernet.generate_key()

def load_key(file_path):
    key_file = file_path + '.key'
    if os.path.exists(key_file):
        with open(key_file, 'rb') as f:
            return f.read()
    else:
        key = generate_key()
        with open(key_file, 'wb') as f:
            f.write(key)
        return key

def save_key(file_path, key):
    key_file = file_path + '.key'
    with open(key_file, 'wb') as f:
        f.write(key)

def is_encrypted(file_path):
    with open(file_path, 'rb') as file:
        file_data = file.read()
        return file_data.startswith(ENCRYPTION_MARKER)

def encrypt_file(key, file_path):
    if not is_encrypted(file_path):
        fernet = Fernet(key)
        with open(file_path, 'rb+') as file:
            file_data = file.read()
            encrypted_data = ENCRYPTION_MARKER + fernet.encrypt(file_data)
            file.seek(0)
            file.write(encrypted_data)
            file.truncate()
        print(f"File {file_path} encrypted successfully.")
        save_key(file_path, key)
    else:
        print(f"File {file_path} is already encrypted.")

def is_decrypted(file_path):
    with open(file_path, 'rb') as file:
        file_data = file.read()
        return not file_data.startswith(ENCRYPTION_MARKER)

def decrypt_file(key, file_path):
    if not is_decrypted(file_path):
        fernet = Fernet(key)
        with open(file_path, 'rb+') as file:
            file_data = file.read()
            if file_data.startswith(ENCRYPTION_MARKER):
                decrypted_data = fernet.decrypt(file_data[len(ENCRYPTION_MARKER):])
                file.seek(0)
                file.write(decrypted_data)
                file.truncate()
                key_file = file_path + '.key'
                if os.path.exists(key_file):
                    os.remove(key_file)
                print(f"File {file_path} decrypted successfully.")
            else:
                print(f"File {file_path} is not encrypted.")
    else:
        print(f"File {file_path} is already decrypted.")

def process_files(key, path, choice):
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file_path)[1]
                if file_ext in SUPPORTED_FORMATS:
                    if choice == 'e':
                        encrypt_file(key, file_path)
                    elif choice == 'd':
                        # Load the specific key for each file during decryption
                        key = load_key(file_path)
                        decrypt_file(key, file_path)
    else:
        file_ext = os.path.splitext(path)[1]
        if file_ext in SUPPORTED_FORMATS:
            if choice == 'e':
                encrypt_file(key, path)
            elif choice == 'd':
                key = load_key(path)
                decrypt_file(key, path)
        else:
            print(f"Unsupported file format for file {path}. Supported formats:", ", ".join(SUPPORTED_FORMATS))

def main():

    choice = input("Enter 'e' for encryption or 'd' for decryption: ").lower()
    if choice not in ['e', 'd']:
        print("Invalid choice. Please enter 'e' for encryption or 'd' for decryption.")
        return


    path = input("Enter the file or folder path: ")
    if not os.path.exists(path):
        print("Path not found.")
        return


    if choice == 'e':
        key = generate_key()
    else:
        key = None


    process_files(key, path, choice)

if __name__ == "__main__":
    main()
