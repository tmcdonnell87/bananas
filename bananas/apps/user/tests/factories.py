import factory


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker('first_name')
    username = factory.Faker('last_name')
    email = factory.Sequence(lambda n: 'user-{0}@example.com'.format(n))
    phone = factory.Sequence(lambda n: '1800{num:07d}'.format(num=n))
    password = factory.PostGenerationMethodCall('set_password', 'password')

    class Meta:
        model = 'user.User'
