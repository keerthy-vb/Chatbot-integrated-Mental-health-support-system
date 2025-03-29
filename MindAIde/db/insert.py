from models import User


user = User(name="Alice", age=25)
user.save()

print("User inserted successfully!")
