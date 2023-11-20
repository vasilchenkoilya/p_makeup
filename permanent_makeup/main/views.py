from typing import Any
from datetime import datetime

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from . import models
from .forms import ReviewForm, BookingForm
from permanent_makeup.settings import ADMIN_EMAIL


def gallery_view(request: HttpRequest) -> HttpResponse:
    """
    View function for the gallery page.
    It retrieves all images from the WorkGallery model and renders them on the gallery page.
    """
    images = models.WorkGallery.objects.all().order_by('-created_at')
    return render(request, 'main/gallery.html', {'images': images})


def index(request: HttpRequest) -> HttpResponse:
    """
    View function for the index page.
    It retrieves all services from the Service model and renders them on the index page.
    """
    services = models.Service.objects.all()
    return render(request, 'main/index.html', {'services': services})


def service_detail(request: HttpRequest, service_slug: str) -> HttpResponse:
    """
    View function for the service detail page.
    It retrieves a specific service based on the provided slug and renders it on the service detail page.
    """
    service = get_object_or_404(models.Service, slug=service_slug)
    return render(request, 'main/service_split.html', {'service': service})


def leave_review(request: HttpRequest) -> HttpResponse:
    """
    View function for leaving a review.
    It saves the review form if it's valid and the user is authenticated.
    """
    form = ReviewForm(request.POST)
    if form.is_valid() and request.user.is_authenticated:
        review = form.save(commit=False)
        review.author = request.user
        review.save()
    return redirect('reviews_page')


def reviews_page(request: HttpRequest) -> HttpResponse:
    """
    View function for the reviews page.
    It retrieves all reviews from the Review model and renders them on the reviews page.
    """
    reviews = models.Review.objects.all().order_by('-created_at')
    form = ReviewForm()
    if request.method == 'POST':
        return leave_review(request)
    context = {
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'reviews/reviews.html', context)


@login_required
def reservation_view(request: HttpRequest) -> HttpResponse:
    """
    View function for the reservation page.
    It saves the booking form if it's valid and sends confirmation emails to the user and the admin.
    """
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
            html_user_message = render_to_string('emails/user_reservation_email.html', context=mail_context)
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
                [ADMIN_EMAIL],
                html_message=html_admin_message,
                fail_silently=False,
            )
            return redirect(success_url)
    else:
        form = BookingForm()

    return render(request, template_name, {'form': form})


class MyReservationsView(LoginRequiredMixin, ListView):
    """
    View for displaying the user's reservations.
    It inherits from Django's ListView and requires the user to be logged in.
    """
    template_name = 'reservation/my_reservations.html'
    context_object_name = 'reservations'
    model = models.Reservation

    def get_queryset(self) -> Any:
        """
        Overrides the get_queryset method to filter the reservations by the current user.
        """
        queryset = super().get_queryset().filter(customer=self.request.user).order_by('time_slot__start_time')
        return queryset

    def get_visit_date(self, time_slot: models.TimeSlot) -> str:
        """
        Returns the visit date in the format 'dd.mm.yyyy HH:MM'.
        """
        local_start_time = timezone.localtime(time_slot.start_time)
        return local_start_time.strftime('%d.%m.%Y %H:%M')

    def get_date_time_today(self) -> datetime:
        """
        Returns the current date and time.
        """
        today_time = timezone.localtime()
        return today_time
    
    def get_context_data(self, **kwargs: Any) -> dict:
        """
        Overrides the get_context_data method to add additional context.
        """
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()
        context['formatted_reservations'] = [(reservation, self.get_visit_date(reservation.time_slot)) for reservation in context['reservations']]
        context['today_time'] = self.get_date_time_today()      
        return context
    
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """
        Overrides the post method to handle different actions.
        """
        action = request.POST.get('action')
        if action == 'leave_review':
            return leave_review(request)
        else:
            reservation_id = request.POST.get('reservation_id')
            reservation = get_object_or_404(models.Reservation, id=reservation_id)
            if reservation.customer == request.user and reservation.time_slot.start_time > timezone.now():
                reservation.delete()
            return redirect('my_reservations')
   

def reservation_success(request: HttpRequest) -> HttpResponse:
    """
    View for the reservation success page.
    It renders the reservation success page and sets a refresh header.
    """
    response = render(request, 'reservation/reservation_success.html')
    response['Refresh'] = '2; url=/'
    return response

def contacts_view(request: HttpRequest) -> HttpResponse:
    """
    View for the contacts page.
    It renders the contacts page.
    """
    return render(request, 'main/contacts.html')
