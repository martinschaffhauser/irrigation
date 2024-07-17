#!/bin/bash

# Check if a file argument was provided
if [ -z "$1" ]; then
    echo "Usage: $0 <file_to_decrypt>"
    exit 1
fi

# Assign the first argument to the file_to_decrypt variable
file_to_decrypt="$1"

# Prompt for the AGE private key for decryption
echo "Enter the AGE private key for decryption:"
read -s age_private_key  # -s option hides the input for security

# Extract the directory and base name without the ".encrypted" suffix
file_dir=$(dirname "$file_to_decrypt")
file_base=$(basename "$file_to_decrypt" .encrypted)

# Define the output name for the decrypted file
decrypted_file_name="${file_dir}/${file_base}"

# Output the decrypted file name for confirmation
echo "Decrypted file will be saved as: $decrypted_file_name"

# Set the AGE key as an environment variable for sops
export SOPS_AGE_KEY="$age_private_key"

# Decrypt the file back to its original form
sops --decrypt --input-type binary --output-type binary "$file_to_decrypt" > "$decrypted_file_name"

# Unset the environment variable
unset SOPS_AGE_KEY

# Confirm decryption
if [ $? -eq 0 ]; then
    echo "File decrypted as ${decrypted_file_name}"
else
    echo "Decryption failed"
    exit 1
fi
