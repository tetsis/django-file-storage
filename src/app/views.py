from django.shortcuts import render
from django.http import HttpResponse
from model.models import File
 
def index(request):
    files = File.objects.all()

    context = {
        'files': files,
    }
    return render(request, 'index.html', context)

def upload(request):
    return render(request, 'upload.html')