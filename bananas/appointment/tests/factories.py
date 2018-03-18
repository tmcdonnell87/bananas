import factory

from django.utils import timezone

from bananas.user.tests.factories import UserFactory


class AppointmentTypeFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('bs')

    class Meta:
        model = 'appointment.AppointmentType'


class AppointmentFactory(factory.django.DjangoModelFactory):
    client_first_name = factory.Faker('first_name')
    client_last_name = factory.Faker('last_name')
    client_email = factory.Sequence(lambda n: 'client-{0}@example.com'.format(n))
    client_phone = factory.Sequence(lambda n: '1800{num:07d}'.format(num=n))
    time = factory.Faker('date_time_this_year', after_now=True,
                         tzinfo=timezone.get_current_timezone())
    counselor = factory.SubFactory(UserFactory)
    appointment_type = factory.SubFactory(AppointmentTypeFactory)

    class Meta:
        model = 'appointment.Appointment'
