from django.shortcuts import render, get_object_or_404
from . import models



def gallery_view(request):
    images = models.WorkGalllery.objects.all().order_by('-created_at')
    return render(request, 'main/gallery.html', {'images': images})

def index(request):
    services = models.Service.objects.all()
    return render(request, 'main/index.html', {'services': services})