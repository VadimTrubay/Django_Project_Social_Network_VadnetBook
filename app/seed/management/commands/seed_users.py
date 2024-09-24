import random
from django.core.management.base import BaseCommand
from faker import Faker
from authenticate.models import CustomUserModel  # Replace with your actual user model

fake = Faker()


class Command(BaseCommand):
    help = "Seed the database with 500 fake users"

    def handle(self, *args, **kwargs):
        NUM_USERS = 200

        for i in range(1, NUM_USERS + 1):
            username = f"test{i}"
            email = f"test{i}@gmail.com"
            password = f"test{i}"  # Password same as the username
            # status = random.choice(["active", "inactive", "passive"])
            # first_name = fake.first_name()
            # last_name = fake.last_name()
            # birth_date = fake.date_of_birth().strftime("%d.%m.%Y")
            # phone_number = fake.phone_number()
            # about_me = fake.text(max_nb_chars=20)
            # job_skills = random.choice(["django", "fastapi", "flask"])

            # Create user without a profile picture
            CustomUserModel.objects.create_user(
                username=username,
                email=email,
                password=password,
                # first_name=first_name,
                # last_name=last_name,
                # status=status,
                # birth_date=birth_date,
                # phone_number=phone_number,
                # job_skills=job_skills,
                # about_me=about_me,
                # profile_picture=None,
            )

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {NUM_USERS} users."))
