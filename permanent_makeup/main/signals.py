from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import Reservation, TimeSlot


@receiver(pre_save, sender=Reservation)
def check_timeslot_availability(sender, instance, **kwargs):
    if not instance.time_slot.is_available:
        raise ValidationError("This time slot is not available.")

@receiver(post_save, sender=Reservation)
def mark_timeslot_unavailable(sender, instance, created, **kwargs):
    if created:
        instance.time_slot.is_available = False
        instance.time_slot.save()

@receiver(post_delete, sender=Reservation)
def mark_timeslot_available(sender, instance, **kwargs):
    time_slot = TimeSlot.objects.filter(id=instance.time_slot.id).first()
    if time_slot:
        time_slot.is_available = True
        time_slot.save()