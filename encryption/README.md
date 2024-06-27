# Encryption of platformio.ini

- install SOPS and AGE
- create AGE key that needs to be kept securely (definitely not within Github Project)
    - age-keygen -o key.txt
- dont forget to add files to .gitignore
- use encrypt and decrypt scripts to encrypt sensitive files before uploading
