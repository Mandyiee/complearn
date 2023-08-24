from django.shortcuts import render,redirect
from .forms import CompositeForm
from calculations.calculations import Calculation
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json
from material.models import Material
from .models import Composite
from fibre.models import Fibre
from matrix.models import Matrix
from purpose.models import Purpose
from purpose.forms import PurposeForm
# Create your views here.

def home(request):
    
    purposes = Purpose.objects.all()
    form = PurposeForm()
    context = {
        'purposes':purposes,
        'form': form
    }
    return render(request,'home.html',context)

#         cal = Calculation(youngModulusFibre=form.cleaned_data['young_modulus'],youngModulusMatrix=form.cleaned_data['young_modulus_two'],tensileStrengthFibre=form.cleaned_data['tensile_strength'],tensileStrengthMatrix=form.cleaned_data['tensile_strength_two'])
    #         cal(youngModulusFibre=form.cleaned_data['young_modulus'],youngModulusMatrix=form.cleaned_data['young_modulus_two'],tensileStrengthFibre=form.cleaned_data['tensile_strength'],tensileStrengthMatrix=form.cleaned_data['tensile_strength_two'])
            
            
#fmr cant work because of the first
def get_purpose(request):
    data = json.loads(request.body)
    purpose = data.get('purpose')
    purpose_data = Purpose.objects.filter(usage__contains=purpose).first()
    
    if purpose_data:
        purpose_dict = {
            'id': purpose_data.id,
            'usage': purpose_data.usage,
            'tensile_strength': int(purpose_data.tensile_strength),  # Convert Decimal to string
            'young_modulus': int(purpose_data.young_modulus),        # Convert Decimal to string
        }
        return JsonResponse({'purpose': purpose_dict})
    else:
        return JsonResponse({'error': 'Purpose not found'}, status=404)
    

@require_POST
def make_composite(request):
    data = json.loads(request.body)
    print(data)
    try:
        fibre, created = Fibre.objects.get_or_create(name=data['fibre_name'],tensile_strength=data['fibre_tensile_strength'],young_modulus=data['fibre_young_modulus'])
        fibre.save()
        matrix,created = Matrix.objects.get_or_create(name=data['matrix_name'],tensile_strength=data['matrix_tensile_strength'],young_modulus=data['matrix_young_modulus'])
        matrix.save()
        purpose, created = Purpose.objects.get_or_create(usage=data['purpose_select'],tensile_strength=data['purpose_tensile_strength'],young_modulus=data['purpose_young_modulus'])
        purpose.save()
        composite = Composite.objects.create(fibre=fibre,matrix=matrix,purpose=purpose)
        cal = Calculation(youngModulusFibre=composite.fibre.young_modulus,
                   youngModulusMatrix=composite.matrix.young_modulus,
                   tensileStrengthFibre=composite.fibre.tensile_strength,
                   tensileStrengthMatrix=composite.matrix.tensile_strength,
                   desired_tensile_strength=composite.purpose.tensile_strength,
                   desired_young_modulus=composite.purpose.young_modulus,
                   opt=data['opt'],
                   comp_id=composite.id)
        cals = cal()
        print(cals)
        return JsonResponse({'url':f'/composite/{composite.id}'},safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({'url':f'/error'},safe=False)

def composite(request,id):
    composite = Composite.objects.get(id=id)
    context = {
        'composite':composite
    }
    return render(request,'composite.html',context)

def error(request):
    return render(request,'error.html')