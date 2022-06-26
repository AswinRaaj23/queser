from django.shortcuts import render
from .models import Question

# Create your views here.
def home(request):
    context = {
        'title':'hello there'
    }
    return render(request, 'stacquora/home.html', context)