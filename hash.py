from werkzeug.security import generate_password_hash

password = "23142173"
hashed_password = generate_password_hash(password, method='scrypt')

print("Copie este hash:")
print(hashed_password)