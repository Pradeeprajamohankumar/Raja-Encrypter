from cryptography.fernet import Fernet
import os

SUPPORTED_FORMATS = ['.txt', '.pdf', '.ppt', '.docx', '.doc', '.jpg', '.png', '.jpeg', '.pptx', '.xlsm', '.xls', '.rtf', '.heic', '.mov']
ENCRYPTION_MARKER = b'ENCRYPTEDFILE'

def generate_key():
    return Fernet.generate_key()

def get_key(file_path):
    key_file = f"{file_path}.key"
    if os.path.exists(key_file):
        with open(key_file, 'rb') as f:
            return f.read()
    else:
        key = generate_key()
        save_key(file_path, key)
        return key

def save_key(file_path, key):
    with open(f"{file_path}.key", 'wb') as f:
        f.write(key)

def is_encrypted(file_path):
    try:
        with open(file_path, 'rb') as file:
            return file.read(len(ENCRYPTION_MARKER)) == ENCRYPTION_MARKER
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return False

def encrypt_file(key, file_path):
    if not is_encrypted(file_path):
        try:
            fernet = Fernet(key)
            with open(file_path, 'rb') as file:
                file_data = file.read()
            encrypted_data = ENCRYPTION_MARKER + fernet.encrypt(file_data)
            with open(file_path, 'wb') as file:
                file.write(encrypted_data)
            print(f"File {file_path} encrypted successfully.")
        except Exception as e:
            print(f"Error encrypting file {file_path}: {e}")
    else:
        print(f"File {file_path} is already encrypted.")

def is_decrypted(file_path):
    return not is_encrypted(file_path)

def decrypt_file(key, file_path):
    if not is_decrypted(file_path):
        try:
            fernet = Fernet(key)
            with open(file_path, 'rb') as file:
                file_data = file.read()
            if file_data.startswith(ENCRYPTION_MARKER):
                decrypted_data = fernet.decrypt(file_data[len(ENCRYPTION_MARKER):])
                with open(file_path, 'wb') as file:
                    file.write(decrypted_data)
                key_file = f"{file_path}.key"
                if os.path.exists(key_file):
                    os.remove(key_file)
                print(f"File {file_path} decrypted successfully.")
            else:
                print(f"File {file_path} does not have the correct encryption marker.")
        except Exception as e:
            print(f"Error decrypting file {file_path}: {e}")
    else:
        print(f"File {file_path} is already decrypted.")

def process_files(path, choice):
    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file_path)[1].lower()
                if file_ext in SUPPORTED_FORMATS:
                    key = get_key(file_path)
                    if choice == 'e':
                        encrypt_file(key, file_path)
                    elif choice == 'd':
                        decrypt_file(key, file_path)
    else:
        file_ext = os.path.splitext(path)[1].lower()
        if file_ext in SUPPORTED_FORMATS:
            key = get_key(path)
            if choice == 'e':
                encrypt_file(key, path)
            elif choice == 'd':
                decrypt_file(key, path)
        else:
            print(f"Unsupported file format for file {path}. Supported formats: {', '.join(SUPPORTED_FORMATS)}")

def main():
    choice = input("Enter 'e' for encryption or 'd' for decryption: ").lower()
    if choice not in ['e', 'd']:
        print("Invalid choice. Please enter 'e' for encryption or 'd' for decryption.")
        return

    path = input("Enter the file or folder path: ")
    if not os.path.exists(path):
        print("Path not found.")
        return

    process_files(path, choice)

if __name__ == "__main__":
    main()
