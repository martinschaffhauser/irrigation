#!/bin/bash

# Check if a file argument was provided
if [ -z "$1" ]; then
    echo "Usage: $0 <file_to_encrypt>"
    exit 1
fi

# Assign the first argument to the file_to_encrypt variable
file_to_encrypt="$1"

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
