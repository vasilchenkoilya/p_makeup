from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Reservation, TimeSlot

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