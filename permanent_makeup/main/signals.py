from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .models import Reservation, TimeSlot

@receiver(pre_save, sender=Reservation)
def check_timeslot_availability(sender: Reservation, instance: Reservation, **kwargs) -> None:
    """
    Checks if the time slot is available before saving the Reservation.

    Args:
        sender (Reservation): The sender of the signal.
        instance (Reservation): The instance of the Reservation being saved.

    Raises:
        ValidationError: Raised if the time slot is not available.
    """
    if not instance.time_slot.is_available:
        raise ValidationError("This time slot is not available.")

@receiver(post_save, sender=Reservation)
def mark_timeslot_unavailable(sender: Reservation, instance: Reservation, created: bool, **kwargs) -> None:
    """
    Marks the time slot as unavailable after saving the Reservation.

    Args:
        sender (Reservation): The sender of the signal.
        instance (Reservation): The instance of the Reservation being saved.
        created (bool): Indicates if the Reservation was created.

    """
    if created:
        instance.time_slot.is_available = False
        instance.time_slot.save()

@receiver(post_delete, sender=Reservation)
def mark_timeslot_available(sender: Reservation, instance: Reservation, **kwargs) -> None:
    """
    Marks the time slot as available after deleting the Reservation.

    Args:
        sender (Reservation): The sender of the signal.
        instance (Reservation): The instance of the Reservation being deleted.

    """
    time_slot = TimeSlot.objects.filter(id=instance.time_slot.id).first()
    if time_slot:
        time_slot.is_available = True
        time_slot.save()