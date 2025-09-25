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



ICON_MAP = {
        'CO2': 'https://cdn-icons-png.flaticon.com/512/2913/2913126.png',
        'CH4': 'https://cdn-icons-png.flaticon.com/512/2913/2913153.png',
        'SO2': 'https://cdn-icons-png.flaticon.com/512/2913/2913161.png',
        'Dust': 'https://cdn-icons-png.flaticon.com/512/2913/2913174.png',
        'NOx': 'https://cdn-icons-png.flaticon.com/512/2913/2913186.png',
        'PM2.5': 'https://cdn-icons-png.flaticon.com/512/2913/2913199.png',
        'PM10': 'https://cdn-icons-png.flaticon.com/512/2913/2913210.png' 
}

def mine_detail(request, mine_id):
    mine = get_object_or_404(Mine, id=mine_id)
    pollutants = Pollutant.objects.all()

    emissions_data = {}
    for pollutant in pollutants:
        emissions = (
            EmissionCalculation.objects.filter(mine=mine, pollutant=pollutant)
            .order_by("period_start")
            .values("period_start", "emission_value")
        )
        emissions_data[str(pollutant.id)] = list(emissions)  # ✅ string keys

    return render(
    request,
    "emissions/mine_detail.html",
    {
        "mine": mine,
        "pollutants": pollutants,
        "emissions_data": json.dumps(emissions_data, cls=DjangoJSONEncoder),
        "icon_map": ICON_MAP,  # keep dict for template
        "icon_map_json": json.dumps(ICON_MAP),  # extra copy for JS
    },
)

import requests
from django.http import JsonResponse
from django.conf import settings

def chatbot_response(request):
    message = request.GET.get("message", "")
    mine_name = request.GET.get("mine", "")

    if not message:
        return JsonResponse({"response": "Please type a message."})

    # prompt = f"Mine: {mine_name}\nUser: {message}\nSuggest simple ways to reduce emissions."

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    system_prompt = (
        "You are a friendly assistant for coal mine emissions. "
        "Reply casually, short and actionable in 3-5 bullet points. "
        "Focus only on what the user asks. "
        "If greeting or small talk, reply casually but briefly."
    )
    
    payload = {
        "model": "deepseek/deepseek-chat-v3.1:free",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Mine context: {mine_name}\nUser query: {message}"}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        # Get bot reply
        answer = data.get("choices", [{}])[0].get("message", {}).get("content", "Sorry, no response.")

    except Exception as e:
        answer = f"Error: {e}"

    return JsonResponse({"response": answer})



    try:
        data = response.json()
        answer = data[0]['generated_text'].replace(prompt, '').strip()
    except Exception:
        answer = "Sorry, I couldn't process that. Try again."

    return JsonResponse({"response": answer})


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
