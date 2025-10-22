from emissions.models import Pollutant, Sensor, SensorReading, Mine
from django.utils import timezone
import random

mine = Mine.objects.first()
if not mine:
    raise SystemExit("No Mine found. Create a Mine first.")

pollutant_codes = ["SO2", "NOx", "PM2.5", "CO"]

for code in pollutant_codes:
    pollutant = Pollutant.objects.filter(code=code).first()
    if not pollutant:
        print(f"Pollutant {code} not found — skipping.")
        continue

    sensor, created = Sensor.objects.get_or_create(
        name=f"{code} Sensor 1",
        model=f"{code}-M100",
        mine=mine,
        pollutant=pollutant,
        defaults={
            'installation_date': timezone.now().date(),
            'last_calibrated': timezone.now().date()
        }
    )

    if created:
        print(f"Created sensor: {sensor.name}")
    else:
        print(f"Using existing sensor: {sensor.name}")

    for i in range(10):
        ts = timezone.now() - timezone.timedelta(hours=(10 - i))
        value = round(random.uniform(5.0, 50.0), 2)
        SensorReading.objects.create(
            sensor=sensor,
            timestamp=ts,
            value=value,
            unit="ppm"
        )
    print(f"Added 10 readings for {sensor.name}")
