from django.shortcuts import render, get_object_or_404
from .models import Mine, EmissionCalculation

def company_dashboard(request):
    # Get the company of the logged-in user
    company = request.user.profile.company  
    mines = Mine.objects.filter(company=company)
    return render(request, "emissions/company_dashboard.html", {"company": company, "mines": mines})

import json
from django.core.serializers.json import DjangoJSONEncoder

def mine_detail(request, mine_id):
    mine = get_object_or_404(Mine, id=mine_id)
    emissions = EmissionCalculation.objects.filter(mine=mine).order_by("-period_end")

    # Prepare JSON-safe data for charts
    emissions_data = list(
        emissions.values("period_start", "period_end", "emission_value", "pollutant__name")
    )
    emissions_json = json.dumps(emissions_data, cls=DjangoJSONEncoder)

    return render(
        request,
        "emissions/mine_detail.html",
        {"mine": mine, "emissions": emissions, "emissions_json": emissions_json},
    )

