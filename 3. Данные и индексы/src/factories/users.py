import factory


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'users.Company'
        django_get_or_create = ('title',)

class JobFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'users.Job'
        django_get_or_create = ('title',)

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'users.User'
