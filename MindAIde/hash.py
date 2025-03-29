from hash_service import generate_password_hash, check_password_hash

password = "admin@123"  # Change to your desired password
hashed_password = generate_password_hash(password)

print("Hashed Password:", hashed_password)


print(check_password_hash("433fc6ad9c6c2d7105b1342a837be686c4c116c89b0605848303d03147cbe226", password))