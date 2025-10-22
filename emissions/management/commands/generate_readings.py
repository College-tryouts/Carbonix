from django.core.management.base import BaseCommand
from emissions.models import Sensor, SensorReading
from django.utils import timezone
import datetime, random

class Command(BaseCommand):
    help = "Generate sample readings for existing sensors"

    def handle(self, *args, **kwargs):
        sensors = Sensor.objects.all()
        if not sensors.exists():
            self.stdout.write(self.style.ERROR("No sensors found!"))
            return

        base_time = timezone.now()

        for sensor in sensors:
            for i in range(50):  # 50 readings per sensor
                if sensor.pollutant.name.lower() == "co2":
                    value = random.uniform(380, 450)
                    unit = "ppm"
                elif sensor.pollutant.name.lower() == "methane":
                    value = random.uniform(1.8, 2.5)
                    unit = "ppm"
                else:
                    value = random.uniform(10, 100)
                    unit = sensor.pollutant.unit or ""

                SensorReading.objects.create(
                    sensor=sensor,
                    timestamp=base_time - datetime.timedelta(hours=i),
                    value=value,
                    unit=unit,
                    quality_flag="OK"
                )

        self.stdout.write(self.style.SUCCESS("✅ Readings generated for all existing sensors!"))
