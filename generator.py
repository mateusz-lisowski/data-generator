import random
from decimal import Decimal
from uuid import uuid4

from faker import Faker
from faker.providers import DynamicProvider


fake = Faker()


# Create custom faker providers
payment_type_provider = DynamicProvider(
    provider_name='payment_type',
    elements=['cash', 'card']
)

show_type_provider = DynamicProvider(
    provider_name='show_type',
    elements=[
        'Acrobatic Troupe', 'Fire Jugglers', 'Animal Acts', 'Clown Comedy', 'Knife Throwing', 'Magician Illusions'
    ]
)

# Register custom faker providers
fake.add_provider(show_type_provider)
fake.add_provider(payment_type_provider)
