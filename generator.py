import csv
import random
import datetime
from decimal import Decimal
from uuid import UUID, uuid4
from dataclasses import dataclass, astuple
from typing import Literal

from faker import Faker
from faker.providers import DynamicProvider


fake = Faker()


Payment = Literal['cash', 'card']
ShowType = Literal['Acrobatic Troupe', 'Fire Jugglers', 'Animal Acts',
                     'Clown Comedy', 'Knife Throwing', 'Magician Illusions']

# Create custom faker providers
payment_type_provider = DynamicProvider(
    provider_name='payment_type',
    elements=list(Payment.__args__)
)

show_type_provider = DynamicProvider(
    provider_name='show_type',
    elements=list(ShowType.__args__)
)

# Register custom faker providers
fake.add_provider(show_type_provider)
fake.add_provider(payment_type_provider)


@dataclass
class City:
    id: UUID
    name: str
    population: int


@dataclass
class Show:
    id: UUID
    show_type: ShowType
    date: datetime.datetime
    city_id: UUID


def generate_cities(quantity: int, output_file: str) -> list[UUID]:
    cites_ids: list[UUID] = []
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


def generate_shows(quantity: int, output_file: str, possible_choices: list[UUID]) -> list[UUID]:
    shows_ids: list[UUID] = []
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for _ in range(quantity):
            show = Show(
                id=uuid4(),
                show_type=fake.show_type(),
                date=fake.date_time(),
                city_id=random.choice(possible_choices)
            )
            writer.writerow(astuple(show))
            shows_ids.append(show.id)
    return shows_ids


def main():
    cites_ids = generate_cities(100, output_file='cities.csv')
    show_ids = generate_shows(100, possible_choices=cites_ids, output_file='shows.csv')
    print(cites_ids)
    print(show_ids)

if __name__ == '__main__':
    main()
