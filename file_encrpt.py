from cryptography.fernet import Fernet, InvalidToken
import os

def normalize_path(path):
    """Normalize file path: strip quotes, expand user dir, resolve to absolute path."""
    if not path or not path.strip():
        raise ValueError("Path is empty.")
    path = path.strip().strip('"\'')
    path = os.path.expanduser(path)
    return os.path.abspath(path)

def generate_key(key_filename):
    """Generate a new key and save it to a .key file"""
    key = Fernet.generate_key()
    with open(key_filename, "wb") as key_file:
        key_file.write(key)
    return key

def load_key(key_filename):
    """Load key from a .key or .decryptkey file"""
    with open(key_filename, "rb") as key_file:
        return key_file.read()

def encrypt_file(filepath):
    """Encrypt file and automatically generate a separate .key file. Accepts any file path."""
    filepath = normalize_path(filepath)
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    # Encrypt key and decrypt key saved in same directory as the file
    key_filename = filepath + ".key"
    decrypt_key_filename = filepath + ".decryptkey"

    # Generate a new key and save it as encrypt key
    key = generate_key(key_filename)
    # Also save the same key as decrypt key (for use when decrypting later)
    with open(decrypt_key_filename, "wb") as decrypt_key_file:
        decrypt_key_file.write(key)

    fernet = Fernet(key)

    # Read original file
    with open(filepath, "rb") as file:
        original = file.read()

    # Encrypt the file
    encrypted = fernet.encrypt(original)

    # Write encrypted content back to file
    with open(filepath, "wb") as encrypted_file:
        encrypted_file.write(encrypted)

    print("File encrypted successfully")
    print(f"Encrypt key saved as: {key_filename}")
    print(f"Decrypt key saved as: {decrypt_key_filename}")

def decrypt_file(filepath):
    """Decrypt file using .key or .decryptkey file. Also saves a decrypt key file. Accepts any file path."""
    filepath = normalize_path(filepath)
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    # Try .key first, then .decryptkey (same directory as the file)
    key_filename = filepath + ".key"
    decrypt_key_filename = filepath + ".decryptkey"

    if os.path.isfile(key_filename):
        key = load_key(key_filename)
        print(f"Using key file: {key_filename}")
    elif os.path.isfile(decrypt_key_filename):
        key = load_key(decrypt_key_filename)
        print(f"Using key file: {decrypt_key_filename}")
    else:
        raise FileNotFoundError(
            f"No key file found. Need either:\n  {key_filename}\n  or\n  {decrypt_key_filename}"
        )

    fernet = Fernet(key)

    # Read encrypted file
    with open(filepath, "rb") as enc_file:
        encrypted = enc_file.read()

    # Decrypt the file
    try:
        decrypted = fernet.decrypt(encrypted)
    except InvalidToken:
        raise ValueError(
            "Decryption failed. Wrong key or file is not encrypted (or was encrypted with another program)."
        )
    except Exception as e:
        raise ValueError(f"Decryption failed: {e}") from e

    # Write decrypted content back to file
    with open(filepath, "wb") as dec_file:
        dec_file.write(decrypted)

    # Save a copy of the key as decrypt key for later use
    with open(decrypt_key_filename, "wb") as dkf:
        dkf.write(key)

    print("File decrypted successfully")
    print(f"Decrypt key saved as: {decrypt_key_filename}")

# -------- Main menu --------
def main():
    while True:
        print()
        print("1. Encrypt File (generates .key and .decryptkey)")
        print("2. Decrypt File (uses .key or .decryptkey)")
        print("3. Exit")
        choice = input("Choose an option (1/2/3): ").strip()

        if choice == "3":
            print("Bye.")
            break

        if choice == "1":
            file_path = input("Enter full path of file to encrypt: ").strip()
            if not file_path:
                print("No path entered.")
                continue
            try:
                encrypt_file(file_path)
            except FileNotFoundError as e:
                print(f"Error: {e}")
            except ValueError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Error: {type(e).__name__}: {e}")
            continue

        if choice == "2":
            file_path = input("Enter full path of encrypted file to decrypt: ").strip()
            if not file_path:
                print("No path entered.")
                continue
            try:
                decrypt_file(file_path)
            except FileNotFoundError as e:
                print(f"Error: {e}")
            except ValueError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Error: {type(e).__name__}: {e}")
            continue

        print("Invalid choice. Enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
