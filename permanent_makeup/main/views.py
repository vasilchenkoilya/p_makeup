from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import  CreateView
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from . import models
from .forms import ReviewForm , BookingForm
from django.contrib.auth.decorators import login_required



def gallery_view(request):
    images = models.WorkGalllery.objects.all().order_by('-created_at')
    return render(request, 'main/gallery.html', {'images': images})

def index(request):
    services = models.Service.objects.all()
    return render(request, 'main/index.html', {'services': services})

def service_detail(request, service_slug):
    service = get_object_or_404(models.Service, slug=service_slug)
    return render(request, 'main/service_detail.html', {'service': service})

def reviews_page(request):
    reviews = models.Review.objects.all().order_by('-created_at')
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            review = form.save(commit=False)
            review.author = request.user
            review.save()
            return redirect('reviews_page')
    context = {
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'reviews/reviews.html', context)

@login_required
def reservation_view(request):
    template_name = 'reservation/reservation.html'
    success_url = 'reservation_success' 

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.customer = request.user
            reservation.save()
            return redirect(success_url)
    else:
        form = BookingForm()

    return render(request, template_name, {'form': form})

def reservation_success(request):
    return render(request, 'reservation/reservation_success.html')


#class ReservationView(LoginRequiredMixin, CreateView):
#     template_name = 'reservation/reservation.html'
#     form_class = BookingForm
#     success_url = 'reservation_success' 

#     def form_valid(self, form):
#         reservation = form.save(commit=False)
#         reservation.customer = self.request.user
#         reservation.save()
#         return redirect(self.success_url)