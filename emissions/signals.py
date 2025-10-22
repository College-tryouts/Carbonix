from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import SensorReading, EmissionCalculation

@receiver(post_save, sender=SensorReading)
def create_or_update_emission(sender, instance, created, **kwargs):
    """
    Automatically update EmissionCalculation whenever a new sensor reading is added.
    """
    if created:
        pollutant = instance.sensor.pollutant
        mine = instance.sensor.mine

        emission_value = instance.value
        co2_eq = emission_value * (pollutant.gwp if pollutant and pollutant.gwp else 1)

        EmissionCalculation.objects.create(
            mine=mine,
            pollutant=pollutant,
            period_start=instance.timestamp,
            period_end=instance.timestamp,
            emission_value=emission_value,
            unit=instance.unit,
            co2_equivalent=co2_eq,
            method_notes=f"Auto-calculated from sensor: {instance.sensor.name}"
        )


