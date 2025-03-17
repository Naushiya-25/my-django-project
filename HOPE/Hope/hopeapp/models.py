# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    is_hospital = models.BooleanField(default=False)
    phone_regex = RegexValidator(regex=r'^\d{10}$', message="Phone number must be 10 digits")
    phone_number = models.CharField(validators=[phone_regex], max_length=10, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='hopeapp_user_set', 
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='hopeapp_user_permissions',  
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

class Hospital(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hospital_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.hospital_name

class AnimalReport(models.Model):
    rescuer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    animal_details = models.TextField()
    animal_image = models.ImageField(upload_to='animal_images/')
    token = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('IN_TREATMENT', 'In Treatment'),
        ('COMPLETED', 'Completed')
    ], default='PENDING')

class Treatment(models.Model):
    report = models.OneToOneField(AnimalReport, on_delete=models.CASCADE)
    treatment_details = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bill_image = models.ImageField(upload_to='bills/')
    payment_image = models.ImageField(upload_to='payment_proofs/')
    completed_at = models.DateTimeField(auto_now_add=True)

class Donation(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)