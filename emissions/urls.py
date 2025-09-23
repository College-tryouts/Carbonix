from django.urls import path
from . import views

app_name = 'emissions'
urlpatterns = [
    path("dashboard/", views.company_dashboard, name="company_dashboard"),
    path("mine/<int:mine_id>/", views.mine_detail, name="mine_detail"),
]
