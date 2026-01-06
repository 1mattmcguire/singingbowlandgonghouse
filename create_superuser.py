from django.contrib.auth import get_user_model

User = get_user_model()

username = "Zenish"
email = "1mattmcguire@gmail.com"
password = "1mattmcguire@"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created successfully!")
else:
    print("Superuser already exists.")
