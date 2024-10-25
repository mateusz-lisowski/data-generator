import csv
import datetime
import random
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import astuple, dataclass
from decimal import Decimal
from pathlib import Path
from typing import Literal
from uuid import UUID, uuid4

from faker import Faker
from faker.providers import DynamicProvider


OUTPUT_DIR = Path('output')
CITES_QUANTITY = 100
SHOWS_QUANTITY = 100
TICKETS_QUANTITY = 1_000_000


fake = Faker()


PaymentType = Literal['cash', 'card']
ShowType = Literal['Acrobatic Troupe', 'Fire Jugglers', 'Animal Acts',
                     'Clown Comedy', 'Knife Throwing', 'Magician Illusions']

# Create custom faker providers
payment_type_provider = DynamicProvider(
    provider_name='payment_type',
    elements=list(PaymentType.__args__)
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


@dataclass
class Ticket:
    id: UUID
    price: Decimal
    payment_type: PaymentType
    seat_number: str
    show_id: UUID


def generate_cities(quantity: int, output_file: Path) -> list[UUID]:
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


def generate_shows(quantity: int, output_file: Path, possible_choices: list[UUID]) -> list[UUID]:
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


def generate_ticket_batch(quantity: int, possible_choices: list[UUID]) -> list[Ticket]:
    tickets = []
    for _ in range(quantity):
        ticket = Ticket(
            id=uuid4(),
            price=Decimal(random.randrange(100, 1000)) / 100,
            payment_type=fake.payment_type(),
            seat_number=fake.bothify(text='?-##', letters='ABCDEFG'),
            show_id=random.choice(possible_choices)
        )
        tickets.append(ticket)
    return tickets


def generate_tickets(quantity: int, output_file: Path, possible_choices: list[UUID], num_threads: int = 4) -> None:
    batch_size = quantity // num_threads
    remainder = quantity % num_threads
    tasks = [batch_size] * num_threads
    for i in range(remainder):
        tasks[i] += 1

    all_tickets = []
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(generate_ticket_batch, task, possible_choices) for task in tasks]
        for future in futures:
            all_tickets.extend(future.result())

    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for ticket in all_tickets:
            writer.writerow(astuple(ticket))


def main() -> None:
    start = time.perf_counter()

    OUTPUT_DIR.mkdir(exist_ok=True)

    cites_ids = generate_cities(CITES_QUANTITY, output_file=OUTPUT_DIR / 'cities.csv')
    show_ids = generate_shows(SHOWS_QUANTITY, possible_choices=cites_ids, output_file=OUTPUT_DIR / 'shows.csv')
    generate_tickets(TICKETS_QUANTITY, possible_choices=show_ids, output_file=OUTPUT_DIR / 'tickets.csv')

    end = time.perf_counter()
    elapsed_time = end - start

    print(f"Generated: {CITES_QUANTITY} cites, {SHOWS_QUANTITY} shows, {TICKETS_QUANTITY} tickets")
    print(f"Execution time: {elapsed_time:.5f} seconds")


if __name__ == '__main__':
    main()
