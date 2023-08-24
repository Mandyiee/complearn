from django.shortcuts import render,redirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json
from material.models import Material
from .models import Matrix


# Create your views here.

@require_POST
def get_matrix(request):
    data = json.loads(request.body)
    matrix = data.get('matrix')
    matrix_data = Matrix.objects.filter(name__contains=matrix)
    matrix_list = list(matrix_data.values())
    return JsonResponse({'matrix':matrix_list})