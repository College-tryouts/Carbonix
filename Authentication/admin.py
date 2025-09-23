from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile

# Extend User admin
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'company', 'phone')
    list_filter = ('role', 'company')
    search_fields = ('user__username', 'user__email')
