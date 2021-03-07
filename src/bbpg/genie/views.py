from django.shortcuts import render

def sample(request):
    return render(request, 'genie/sample.html')

# Create your views here.
