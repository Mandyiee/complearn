from django.shortcuts import render,redirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json
from fibre.models import Fibre

# Create your views here.
@require_POST
def get_fibre(request):
    data = json.loads(request.body)
    fibre = data.get('fibre')
    fibre_data = Fibre.objects.filter(name__contains=fibre)
    fibre_list = list(fibre_data.values())
    return JsonResponse({'fibre':fibre_list})
