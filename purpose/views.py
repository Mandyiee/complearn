from django.shortcuts import render,redirect
from purpose.forms import PurposeForm
# Create your views here.

def add_purpose(request):
    if request.method == 'POST':
        form = PurposeForm(request.POST)
        if form.is_valid():
            form.save()
    previous_page = request.META.get('HTTP_REFERER')
    if previous_page:
        return redirect(previous_page)
    return redirect('/')
            