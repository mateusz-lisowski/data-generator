import argparse
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

from dateutil import relativedelta
from faker import Faker
from faker.providers import DynamicProvider


parser = argparse.ArgumentParser(description='Generate random Circus data.')

parser.add_argument('-c', '--cities', type=int, default=100, help='Number of cities to generate.')
parser.add_argument('-s', '--shows', type=int, default=100, help='Number of shows to generate.')
parser.add_argument('-t', '--tickets', type=int, default=1000, help='Number of tickets to generate.')
parser.add_argument('-v', '--viewers', type=int, default=100, help='Number of viewers to generate.')

args = parser.parse_args()

OUTPUT_DIR = Path('output')

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
class Viewer:
    id: UUID
    name: str
    age: int


@dataclass
class City:
    id: UUID
    name: str
    population: int


@dataclass
class Show:
    id: UUID
    show_type: ShowType


@dataclass
class Ticket:
    id: UUID
    price: Decimal
    payment_type: PaymentType
    date: datetime.datetime
    show_id: UUID
    viewer_id: UUID
    city_id: UUID


def generate_viewers(quantity: int, output_file: Path) -> list[UUID]:
    viewers_ids: list[UUID] = []
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for _ in range(quantity):
            viewer = Viewer(
                id=uuid4(),
                name=fake.name(),
                age=random.randint(1, 100)
            )
            writer.writerow(astuple(viewer))
            viewers_ids.append(viewer.id)
    return viewers_ids


def generate_cities(quantity: int, output_file: Path) -> tuple[list[UUID], list[City]]:
    cites_ids: list[UUID] = []
    cities: list[City] = []
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
            cities.append(city)
    return cites_ids, cities


def modify_cities(cities: list[City], output_file: Path, mode: str = 'a') -> list[UUID]:
    cites_ids: list[UUID] = []
    with open(output_file, mode, newline='') as file:
        writer = csv.writer(file)
        for city in cities:
            city.id = uuid4()
            city.population = random.randrange(100_000, 10_000_000)
            cites_ids.append(city.id)
            writer.writerow(astuple(city))
    return cites_ids


def generate_shows(quantity: int, output_file: Path) -> list[UUID]:
    shows_ids: list[UUID] = []
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for _ in range(quantity):
            show = Show(
                id=uuid4(),
                show_type=fake.show_type(),
            )
            writer.writerow(astuple(show))
            shows_ids.append(show.id)
    return shows_ids


def generate_ticket_batch(quantity: int, shows: list[UUID], viewers: list[UUID], cities: list[UUID],
                          start_date: datetime.datetime, end_date: datetime.datetime) -> list[Ticket]:
    tickets = []
    for _ in range(quantity):
        ticket = Ticket(
            id=uuid4(),
            price=Decimal(random.randrange(100, 1000)) / 100,
            payment_type=fake.payment_type(),
            date=fake.date_time_between(start_date=start_date, end_date=end_date),
            show_id=random.choice(shows),
            viewer_id=random.choice(viewers),
            city_id=random.choice(cities),
        )
        tickets.append(ticket)
    return tickets


def generate_tickets(
        quantity: int,
        output_file: Path,
        shows: list[UUID],
        start_date: datetime.datetime,
        end_date: datetime.datetime,
        viewers: list[UUID],
        cities: list[UUID],
        num_threads: int = 4
) -> None:
    batch_size = quantity // num_threads
    remainder = quantity % num_threads
    tasks = [batch_size] * num_threads
    for i in range(remainder):
        tasks[i] += 1

    all_tickets = []
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(generate_ticket_batch, task, shows, viewers, cities, start_date, end_date)
                   for task in tasks]
        for future in futures:
            all_tickets.extend(future.result())

    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for ticket in all_tickets:
            writer.writerow(astuple(ticket))


def main() -> None:
    start = time.perf_counter()

    OUTPUT_DIR.mkdir(exist_ok=True)

    viewers_ids = generate_viewers(args.viewers, output_file=OUTPUT_DIR / 'viewers.csv')

    cites_ids_t1, cites_t1 = generate_cities(args.cities, output_file=OUTPUT_DIR / 'cities_t1.csv')
    show_ids_t1 = generate_shows(args.shows, output_file=OUTPUT_DIR / 'shows_t1.csv')
    generate_tickets(
        args.tickets,
        shows=show_ids_t1,
        viewers=viewers_ids,
        cities=cites_ids_t1,
        output_file=OUTPUT_DIR / 'tickets_t1.csv',
        start_date=datetime.datetime.now() - relativedelta.relativedelta(years=10),
        end_date=datetime.datetime.now() - relativedelta.relativedelta(years=1)
    )

    cites_ids_t2, cites_t2 = generate_cities(args.cities // 10, output_file=OUTPUT_DIR / 'cities_t2.csv')
    modify_cities(cites_t1[:args.cities // 10], output_file=OUTPUT_DIR / 'cities_t2.csv')
    show_ids_t2 = generate_shows(args.shows // 10, output_file=OUTPUT_DIR / 'shows_t2.csv')
    generate_tickets(
        args.tickets // 10,
        shows=show_ids_t2,
        viewers=viewers_ids,
        cities=cites_ids_t2,
        output_file=OUTPUT_DIR / 'tickets_t2.csv',
        start_date=datetime.datetime.now() - relativedelta.relativedelta(years=1),
        end_date=datetime.datetime.now()
    )

    end = time.perf_counter()
    elapsed_time = end - start

    print(f"Generated: {args.cities} cites, {args.shows} shows, {args.tickets} tickets, {args.viewers} viewers")
    print(f"Execution time: {elapsed_time:.5f} seconds")


if __name__ == '__main__':
    main()
