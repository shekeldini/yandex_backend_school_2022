import random

from django.core.management.base import BaseCommand, CommandError
from factories.users import CompanyFactory, JobFactory, UserFactory
from fake import provider

from enterprise.users.models import User, Job, Company


class Command(BaseCommand):
    help = 'Генерация пользователей'

    def handle(self, *args, **options):

        for locale in provider.LOCALES:
            try:
                fake = provider.fake(locale)

                companies = Company.objects.bulk_create(
                    Company(title=fake.company(), address=fake.address())
                    for _ in range(200)
                )
                jobs = Job.objects.bulk_create(Job(title=fake.job()) for _ in range(100))

                if hasattr(fake, "middle_name"):
                    middle_name = fake.middle_name()
                else:
                    middle_name = ""

                users = User.objects.bulk_create(
                    [
                        User(
                            first_name=fake.first_name(),
                            second_name=middle_name,
                            last_name=fake.last_name(),
                            email=fake.email(),
                            address=fake.address(),
                            phone_number=fake.phone_number(),
                            company=random.choice(companies),
                            job=random.choice(jobs),
                        )
                        for _ in range(30000)
                    ],
                )
                self.stdout.write(self.style.SUCCESS(locale))
            except Exception as err:
                self.stdout.write(self.style.ERROR(locale))
                self.stdout.write(str(err))

        self.stdout.write(self.style.SUCCESS('Successfully'))
