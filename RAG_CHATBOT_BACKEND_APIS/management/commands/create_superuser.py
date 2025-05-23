import string
import secrets
from django.core.management.base import BaseCommand
from RAG_CHATBOT_BACKEND_APIS.models import CustomUser
from django.conf import settings

class Command(BaseCommand):
    help = 'Create a superuser with custom details and display the login information'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='admin', help='Username of the superuser')
        parser.add_argument('--email', type=str, default='admin@gmail.com', help='Email of the superuser')
    def handle(self, *args, **kwargs):
        username = kwargs['username']
        email = kwargs['email']
        
        # Check if the user already exists
        user_exists = CustomUser.objects.filter(username=username).exists()

        if user_exists:
            self.stdout.write(self.style.SUCCESS(f'Superuser with username {username} already exists'))
            # Retrieve the user and show login details
            user = CustomUser.objects.get(username=username)
            password = 'ADmin123!'
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS('Here are the login details:'))
            self.stdout.write(self.style.SUCCESS(f'Username: {username}'))
            self.stdout.write(self.style.SUCCESS(f'Password: {password}'))

        else:
            # Generate a random secure password
            password = 'ADmin123!'
            
            # Create the superuser
            CustomUser.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser created successfully with username: {username}'))
            # Show the login details
            self.stdout.write(self.style.SUCCESS('Here are the login details:'))
            self.stdout.write(self.style.SUCCESS(f'Username: {username}'))
            self.stdout.write(self.style.SUCCESS(f'Password: {password}'))

    def generate_random_password(self, length=12):
        """Generate a secure random password with letters, digits, and symbols."""
        alphabet = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(alphabet) for i in range(length))
