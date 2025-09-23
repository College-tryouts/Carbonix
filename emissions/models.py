# Create your models here.
from django.db import models

# Company
class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_email = models.EmailField()
    industry_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Mine / Site
class Mine(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='mines')
    name = models.CharField(max_length=255)
    location = models.TextField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.company.name})"


# Pollutant
class Pollutant(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)
    gwp = models.FloatField(help_text="Global Warming Potential")

    def __str__(self):
        return self.name


# Sensor
class Sensor(models.Model):
    mine = models.ForeignKey(Mine, on_delete=models.CASCADE, related_name='sensors')
    pollutant = models.ForeignKey(Pollutant, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=100)
    installation_date = models.DateField()
    last_calibrated = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.mine.name})"


# Sensor Reading (raw data)
class SensorReading(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='readings')
    timestamp = models.DateTimeField()
    value = models.FloatField()
    unit = models.CharField(max_length=50)
    quality_flag = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.sensor.name} reading at {self.timestamp}"


# Emission Calculation (aggregated results)
class EmissionCalculation(models.Model):
    mine = models.ForeignKey(Mine, on_delete=models.CASCADE, related_name='emissions')
    pollutant = models.ForeignKey(Pollutant, on_delete=models.CASCADE)
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    emission_value = models.FloatField()
    unit = models.CharField(max_length=50)
    co2_equivalent = models.FloatField()
    method_notes = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-period_end']

    def __str__(self):
        return f"{self.pollutant.name} emission for {self.mine.name}"


# Report (to government)
class Report(models.Model):
    mine = models.ForeignKey(Mine, on_delete=models.CASCADE, related_name='reports')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='reports')
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    submitted_to = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"Report {self.id} for {self.company.name}"
