import requests
from django.core.management import BaseCommand

from site_module.models import Province, City


class Command(BaseCommand):
    help = "inserting dummy data"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        # self.fake = Faker()

    def handle(self, *args, **options):
        provinces_response = requests.get("https://iran-locations-api.vercel.app/api/v1/states")
        provinces_data = provinces_response.json()
        for province in provinces_data:
            created_province = Province.objects.create(name=province.get("name"))
            cities_response = requests.get(
                f"https://iran-locations-api.vercel.app/api/v1/cities?state={province.get('name')}")
            cities_data = cities_response.json()
            for city in cities_data["cities"]:
                City.objects.create(name=city.get("name"), province_id=created_province.id)
