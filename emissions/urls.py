from django.urls import path
from . import views

app_name = 'emissions'
urlpatterns = [
    path("dashboard/<int:company_id>/", views.company_dashboard, name="company_dashboard"),
    path("mine/<int:mine_id>/", views.mine_detail, name="mine_detail"),
    path("chatbot/", views.chatbot_response, name="chatbot_response"),
    path('company/<int:company_id>/add_mine/', views.add_mine, name='add_mine'),
    path('mine/<int:mine_id>/add-pollutant/', views.add_pollutant, name='add_pollutant'),
    path('mine/<int:mine_id>/add-sensor/', views.add_sensor, name='add_sensor'),

]
