from models import User

# Fetch all users
users = User.objects()
for user in users:
    print(f"Name: {user.name}, Age: {user.age}")
