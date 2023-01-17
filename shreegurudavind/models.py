from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


TYPE_CHOICES = (
    ('GW', 'Grinding wheel'),
    ('HG', 'Hand gloves'),
    ('SE', 'Safety equipments'),
)


def user_directory_path(instance, filename):
    return f"product_{instance.user.id}/{filename}"


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50)
    # https://docs.djangoproject.com/en/4.1/ref/models/fields/#django.db.models.FileField.upload_to
    img_url = models.ImageField()
    img_url2 = models.ImageField(null=True, blank=True)
    img_url3 = models.ImageField(null=True, blank=True)
    img_url4 = models.ImageField(null=True, blank=True)
    img_url5 = models.ImageField(null=True, blank=True)
    short_description = models.TextField(default="add short_description")
    description = models.TextField(help_text="ex./n colour:red/n size:3 units ")
    price = models.FloatField()
    gst_price = models.FloatField()
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    in_stock = models.BooleanField(default=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('type',)

    def __str__(self):
        return f"{str(self.id)} || {str(self.name)} || {str(self.price)}"


class ProductInCart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.IntegerField()
    quantity = models.IntegerField(validators=[MinValueValidator(Decimal('0.01'))])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('owner',)

    def __str__(self):
        return " | ".join([str(self.owner), str(self.product_id), str(self.quantity)])


class UserOrder(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=50, null=True)
    phone_num = models.CharField(max_length=12, unique=True)
    Address_line1 = models.CharField(max_length=100)
    Address_line2 = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=6)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=20)
