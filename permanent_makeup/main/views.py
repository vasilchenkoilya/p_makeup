from django.shortcuts import render, get_object_or_404, redirect
from . import models
from .forms import ReviewForm , BookingForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from permanent_makeup.local_settings import ADMMIN_EMAIL
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone


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

            mail_context = {
                'reservation': reservation,
                'user': request.user,
            }
            html_user_message = render_to_string('emails/user_reservation_email.html', context=mail_context )
            html_admin_message = render_to_string('emails/admin_reservation_email.html', context=mail_context)
            send_mail(
                "Reservation confirmation",
                "",
                "admin@megamakeup.com",                
                [request.user.email],
                html_message=html_user_message,
                fail_silently=False,
            )
            send_mail(
                "New reservation",
                "",
                "admin@megamakeup.com",
                [ADMMIN_EMAIL],
                html_message=html_admin_message,
                fail_silently=False,
            )
            return redirect(success_url)
    else:
        form = BookingForm()

    return render(request, template_name, {'form': form})

class MyReservationsView(LoginRequiredMixin, ListView):
    template_name = 'reservation/my_reservations.html'
    context_object_name = 'reservations'
    model = models.Reservation

    def get_queryset(self):
        queryset = super().get_queryset().filter(customer=self.request.user).order_by('time_slot__start_time')
        return queryset

    def get_visit_date(self, time_slot):
        local_start_time = timezone.localtime(time_slot.start_time)
        return local_start_time.strftime('%d.%m.%Y %H:%M')

    def get_date_time_today(self):
        today_time = timezone.localtime()
        return today_time
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formatted_reservations'] = [(reservation, self.get_visit_date(reservation.time_slot)) for reservation in context['reservations']]
        context['today_time'] = self.get_date_time_today()      
        return context
    
    def post(self, request, *args, **kwargs):
        reservation_id = request.POST.get('reservation_id')
        reservation = get_object_or_404(models.Reservation, id=reservation_id)
        if reservation.customer == request.user and reservation.time_slot.start_time > timezone.now():
            reservation.delete()
        return redirect('my_reservations')
   

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