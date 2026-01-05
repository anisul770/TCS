import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transparent_cleaning_service.settings')
django.setup()

import itertools
import random
from reviews.models import Review
from services.models import Service
from users.models import User

def generate_bulk_reviews(total_needed=200):
    users = list(User.objects.all())
    services = list(Service.objects.all())

    all_possible_combos = list(itertools.product(users, services))
    random.shuffle(all_possible_combos)

    created_count = 0
    for user, service in all_possible_combos:
        if created_count >= total_needed:
            break
            
        obj, created = Review.objects.get_or_create(
            service=service,
            user=user,
            defaults={
                'rating': random.choice([3, 4, 4, 5, 5]),
                'comment': "Excellent service!"
            }
        )
        
        if created:
            created_count += 1
            if created_count % 20 == 0:
                print(f"Progress: {created_count}/{total_needed}")

    print(f"Created {created_count} reviews.")

if __name__ == '__main__':
    generate_bulk_reviews(200)