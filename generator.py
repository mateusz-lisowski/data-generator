import csv
import random
from decimal import Decimal
from uuid import UUID, uuid4
from dataclasses import dataclass, astuple

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


@dataclass
class City:
    id: UUID
    name: str
    population: int


def generate_cities(quantity: int, output_file: str) -> list[UUID]:
    cites_ids = []
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for _ in range(quantity):
            city = City(
                id=uuid4(),
                name=fake.unique.city(),
                population=random.randrange(100_000, 10_000_000)
            )
            writer.writerow(astuple(city))
            cites_ids.append(city.id)
    return cites_ids


def main():
    cites_ids = generate_cities(100, 'cities.csv')
    print(cites_ids)

if __name__ == '__main__':
    main()
