from datetime import datetime, timedelta
import os
import django
from faker import Faker
import random
from events.models import Category, Event, Participant

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Event_Managemet.settings')
django.setup()

# Function to generate random dates
def generate_random_datetime():
    start_date = datetime.now() - timedelta(days=365)  # 1 year in the past
    end_date = datetime.now() + timedelta(days=365)  # 1 year in the future
    random_datetime = start_date + (end_date - start_date) * random.random()
    return random_datetime

# Populate the database
def populate_db():
    # Initialize Faker
    fake = Faker()

    # Create Categories
    categories = [Category.objects.create(
        name=fake.bs().capitalize(),
        description=fake.paragraph()
    ) for _ in range(1)]
    print(f"Created {len(categories)} categories.")

    # Create Events
    events = []
    for _ in range(20):
        random_datetime = generate_random_datetime()
        event = Event.objects.create(
            category=random.choice(categories),
            name=fake.sentence(),
            description=fake.paragraph(),
            date=random_datetime.date(),
            time=random_datetime.time(),
            location=fake.address(),
            start_time=random_datetime
        )
        events.append(event)
    print(f"Created {len(events)} events.")

    # Create Participants
    participants = [Participant.objects.create(
        name=fake.name(),
        email=fake.email()
    ) for _ in range(10)]
    print(f"Created {len(participants)} participants.")

    # Assign Participants to Events
    for event in events:
        event.participants.set(random.sample(participants, random.randint(1, 3)))
    print("Populated events with participants.")
    print("Database populated successfully!")

# Run the script
if __name__ == "__main__":
    populate_db()
