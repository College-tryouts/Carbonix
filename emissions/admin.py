from django.contrib import admin
from .models import Company, Mine, Pollutant, Sensor, SensorReading, EmissionCalculation, Report

# Company
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_email', 'industry_type')
    search_fields = ('name', 'industry_type')


# Mine
@admin.register(Mine)
class MineAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'location', 'latitude', 'longitude')
    list_filter = ('company',)
    search_fields = ('name', 'company__name', 'location')


# Pollutant
@admin.register(Pollutant)
class PollutantAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'unit', 'gwp')
    search_fields = ('name', 'code')


# Sensor
@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('name', 'mine', 'pollutant', 'model', 'installation_date', 'last_calibrated')
    list_filter = ('mine', 'pollutant')
    search_fields = ('name', 'model', 'mine__name')


# Sensor Reading
@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ('sensor', 'timestamp', 'value', 'unit', 'quality_flag')
    list_filter = ('sensor', 'timestamp')
    search_fields = ('sensor__name',)


# Emission Calculation
@admin.register(EmissionCalculation)
class EmissionCalculationAdmin(admin.ModelAdmin):
    list_display = ('mine', 'pollutant', 'period_start', 'period_end', 'emission_value', 'co2_equivalent')
    list_filter = ('mine', 'pollutant')
    search_fields = ('mine__name', 'pollutant__name')


# Report
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'mine', 'period_start', 'period_end', 'submitted_to', 'status', 'submitted_at')
    list_filter = ('company', 'mine', 'status')
    search_fields = ('company__name', 'mine__name', 'submitted_to')
