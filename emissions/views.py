from django.shortcuts import render, get_object_or_404, redirect
from .models import Mine, EmissionCalculation, Pollutant

import requests
from django.conf import settings
from django.http import JsonResponse

# inside your existing company view (emissions/views.py)
from .models import Mine, Pollutant, Sensor, Company

def company_dashboard(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    mines = Mine.objects.filter(company=company)
    pollutants = Pollutant.objects.all()
    sensor_models = list(Sensor.objects.values_list('model', flat=True).distinct())
    return render(request, 'emissions/company_dashboard.html', {
        'company': company, 'mines': mines, 'pollutants': pollutants, 'sensor_models': sensor_models
    })


import json
from django.core.serializers.json import DjangoJSONEncoder



# ICON_MAP = {
#         'CO2': 'https://cdn-icons-png.flaticon.com/512/2913/2913126.png',
#         'CH4': 'https://cdn-icons-png.flaticon.com/512/2913/2913153.png',
#         'SO2': 'https://cdn-icons-png.flaticon.com/512/2913/2913161.png',
#         'Dust': 'https://cdn-icons-png.flaticon.com/512/2913/2913174.png',
#         'NOx': 'https://cdn-icons-png.flaticon.com/512/2913/2913186.png',
#         'PM2.5': 'https://cdn-icons-png.flaticon.com/512/2913/2913199.png',
#         'PM10': 'https://cdn-icons-png.flaticon.com/512/2913/2913210.png' 
# }

ICON_MAP = {
    'CO2': 'https://cdn-icons-png.flaticon.com/512/2913/2913126.png',
    'CH4': 'https://cdn-icons-png.flaticon.com/512/2913/2913153.png',
    'SO2': 'https://cdn-icons-png.flaticon.com/512/2913/2913161.png',
    'Dust': 'https://cdn-icons-png.flaticon.com/512/2913/2913174.png',
    'NOx': 'https://cdn-icons-png.flaticon.com/512/2913/2913186.png',
    'PM2.5': 'https://cdn-icons-png.flaticon.com/512/2913/2913199.png',
    'PM10': 'https://cdn-icons-png.flaticon.com/512/2913/2913210.png',
    'CO': 'https://cdn-icons-png.flaticon.com/512/1822/1822552.png',        # Carbon monoxide
    'VOC': 'https://cdn-icons-png.flaticon.com/512/2913/2913225.png',       # Volatile organic compounds (example)
    'N2O': 'https://static.thenounproject.com/png/nitrous-oxide-icon-5705934-512.png',        # Nitric Oxide (if used)
    'O2': 'https://cdn-icons-png.flaticon.com/512/2913/2913118.png',
    'O3': 'https://static.thenounproject.com/png/ozone-icon-4809751-512.png'        # Oxygen (if needed)
}


def mine_detail(request, mine_id):
    mine = get_object_or_404(Mine, id=mine_id)
    pollutants = Pollutant.objects.all()

    # Pollutant-wise sensor readings
    pollutant_sensor_data = {}
    for pollutant in pollutants:
        readings_list = []
        sensors = Sensor.objects.filter(mine=mine, pollutant=pollutant).prefetch_related('readings')
        for sensor in sensors:
            for r in sensor.readings.all().order_by('timestamp'):
                readings_list.append({
                    "timestamp": r.timestamp.isoformat(),
                    "value": r.value,
                    "sensor": sensor.name,
                    "unit": r.unit
                })
        # ensure chronological order
        readings_list.sort(key=lambda x: x['timestamp'])
        pollutant_sensor_data[str(pollutant.id)] = readings_list  # ✅ string keys

    return render(
        request,
        "emissions/mine_detail.html",
        {
            "mine": mine,
            "pollutants": pollutants,
            "pollutant_sensor_data": json.dumps(pollutant_sensor_data, cls=DjangoJSONEncoder),
            "icon_map": ICON_MAP,
            "icon_map_json": json.dumps(ICON_MAP),
        },
    )


from django.http import JsonResponse
from django.conf import settings
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.DEEPSEEK_API_KEY  # your OpenRouter API key
)

import markdown
import re
from django.http import JsonResponse

def chatbot_response(request):
    message = request.GET.get("message", "")
    mine_name = request.GET.get("mine", "")

    if not message:
        return JsonResponse({"response": "Please type a message."})

    system_prompt = (
        "You are a friendly assistant for coal mine emissions. "
        "Reply casually, short and actionable in 3-5 bullet points. "
        "Focus only on what the user asks. "
        "If greeting or small talk, reply casually but briefly."
    )

    try:
        completion = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3.1:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Mine context: {mine_name}\nUser query: {message}"}
            ]
        )

        answer = completion.choices[0].message.content

    except Exception as e:
        answer = f"Bot: Sorry, error occurred. {e}"

    answer = re.sub(r"<.*?▁.*?>", "", answer)
    answer = answer.replace("▁", " ")
    answer = answer.strip()
    answer_html = markdown.markdown(answer)

    return JsonResponse({"response": answer_html})



from django.shortcuts import redirect
from django.utils import timezone

# create placeholder sensor for a pollutant (used as "add pollutant to mine")
def add_pollutant(request, mine_id):
    if request.method == 'POST' and request.user.is_authenticated:
        mine = get_object_or_404(Mine, pk=mine_id)
        pollutant_id = request.POST.get('pollutant_id')
        pollutant = get_object_or_404(Pollutant, pk=pollutant_id)
        # create a placeholder sensor so pollutant appears for this mine
        Sensor.objects.create(
            mine=mine,
            pollutant=pollutant,
            name=f"{pollutant.code} sensor (auto)",
            model='AutoModel',
            installation_date=timezone.now().date()
        )
    return redirect('emissions:company_dashboard', company_id=mine.company.id)

# add explicit sensor
def add_sensor(request, mine_id):
    if request.method == 'POST' and request.user.is_authenticated:
        mine = get_object_or_404(Mine, pk=mine_id)
        name = request.POST.get('name')
        pollutant_id = request.POST.get('pollutant_id')
        model = request.POST.get('model') or 'Unknown'
        installation_date = request.POST.get('installation_date') or timezone.now().date()
        pollutant = get_object_or_404(Pollutant, pk=pollutant_id)
        Sensor.objects.create(
            mine=mine, pollutant=pollutant, name=name, model=model, installation_date=installation_date
        )
    return redirect('emissions:mine_detail', mine_id=mine.id)


from django.contrib import messages
from .models import Company, Mine
from django.contrib.auth.decorators import login_required

@login_required
def add_mine(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    if request.method == "POST":
        name = request.POST.get("mine_name")
        location = request.POST.get("location")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")

        # Create new Mine linked to the company
        Mine.objects.create(
            company=company,
            name=name,
            location=location,
            latitude=latitude if latitude else None,
            longitude=longitude if longitude else None
        )
        messages.success(request, f"Mine '{name}' added successfully!")
        # Redirect back to the same company dashboard page
        return redirect('emissions:company_dashboard', company_id=company.id)

    # fallback, although form should be POST
    return redirect('emissions:company_dashboard', company_id=company.id)




