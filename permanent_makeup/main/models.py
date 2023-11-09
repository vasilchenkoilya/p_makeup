from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    customers = models.ManyToManyField(User, through='Reservation')
    image = models.ImageField(upload_to='service_image', null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Service, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Treatment'
        verbose_name_plural = 'Treatments'


class WorkGalllery(models.Model):
    image = models.ImageField(upload_to='work_gallery', null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    title = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.title} at {self.created_at}"
    
class Review(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.author.username} on {self.created_at.strftime('%Y-%m-%d')}"
    

class TimeSlot(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_available = models.BooleanField(default=True)




class Reservation(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, default=None)
    
