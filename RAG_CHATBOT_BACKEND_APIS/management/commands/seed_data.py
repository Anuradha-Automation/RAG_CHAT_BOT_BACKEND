import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from RAG_CHATBOT_BACKEND_APIS.models import Country, State


class Command(BaseCommand):
    help = 'Seeds data into the database'

    def handle(self, *args, **kwargs):
        countries_file = 'storage/data/countries.csv'
        states_file = 'storage/data/states.csv'
        try:
            # Load and Seed Countries
            countries_data = pd.read_csv(countries_file)
            countries_instances = []
            country_fields = {field.name for field in Country._meta.get_fields()}

            for _, row in countries_data.iterrows():
                row_dict = row.to_dict()
                filtered_row = {key: value for key, value in row_dict.items() if key in country_fields}
                country_instance = Country(**filtered_row)
                countries_instances.append(country_instance)

            Country.objects.bulk_create(countries_instances, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(f"Successfully seeded {len(countries_instances)} countries."))

            # Load and Seed States
            state_data = pd.read_csv(states_file)
            state_instances = []
            state_fields = {field.name for field in State._meta.get_fields()}

            for _, row in state_data.iterrows():
                row_dict = row.to_dict()
                country_name = row_dict.get('country_name')

                if not country_name:
                    self.stdout.write(self.style.WARNING(f"Missing country_name in row {row}. Skipping."))
                    continue

                try:
                    country_instance = Country.objects.get(name=country_name)
                except ObjectDoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Country '{country_name}' not found. Skipping row {row}."))
                    continue

                filtered_row = {key: value for key, value in row_dict.items() if key in state_fields and key != 'country_name'}
                state_instance = State(**filtered_row, country=country_instance)
                state_instances.append(state_instance)

            State.objects.bulk_create(state_instances, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(f"Successfully seeded {len(state_instances)} states."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error seeding database: {str(e)}"))

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully.'))
