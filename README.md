## File Encryption Tool
A Python-based file encryption and decryption tool designed to protect sensitive digital data using modern cryptographic techniques. The tool uses the Fernet symmetric encryption algorithm from the Python Cryptography Project library to ensure strong data confidentiality and integrity.

The application runs through a Command Line Interface (CLI) and allows users to securely encrypt files, generate encryption keys automatically, and decrypt files when needed.
 
## Objectives

```
Objectives
│
├── Develop a secure file encryption system for protecting sensitive data
├── Implement symmetric encryption using the Fernet algorithm
├── Automatically generate and manage encryption keys
├── Provide a simple command-line interface for encryption and decryption
└── Ensure confidentiality and integrity of digital files
```

## Features

```
Features
│
├── File encryption using Fernet symmetric encryption
├── Secure file decryption using stored encryption keys
├── Automatic key generation (.key and .decryptkey)
├── File path validation and normalization
├── Error handling for invalid paths or incorrect keys
└── CLI-based user interaction
```

## project structure 
```
file_encryption/
│
├── main.py
├── key.key
├── decryptkey.decryptkey
├── README.md
└── example_files/
```
## Installation

clone the repository:
```
git clone https://github.com/AashVortex/file_encryption.git
cd file_encryption
```
Install required dependencies:
```
pip install cryptography
```

## Usage
to run the program 

```
python file_encrpt.py
```
after you run the code you will see a menu like this

1. Encrypt File
2. Decrypt File
3. Exit

## Video link
```
https://youtu.be/HZ978FEvCnk
```
