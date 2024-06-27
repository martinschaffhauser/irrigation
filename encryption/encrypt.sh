#!/bin/bash

# Prompt for the file to encrypt
echo "Which file to encrypt?"
read file_to_encrypt

# Prompt for the AGE public key
echo "Enter the AGE public key:"
read age_public_key

# Define the output name for the encrypted file
encrypted_file_name="${file_to_encrypt}.encrypted"

# Encrypt the file as binary data
sops --encrypt --input-type binary --output-type binary --age "$age_public_key" "$file_to_encrypt" > "$encrypted_file_name"

# Confirm encryption
if [ $? -eq 0 ]; then
    echo "File encrypted as $encrypted_file_name"
else
    echo "Encryption failed"
    exit 1
fi