from decimal import Decimal
from django.core.validators import MinValueValidator, \
    MaxValueValidator
from django.db import models
from django.conf import settings
from courses.models import Course
from coupons.models import Coupon
from django.urls import reverse
from django.core.validators import RegexValidator


class Order(models.Model):
    id = models.BigAutoField(
        primary_key=True
    )
    first_name = models.CharField('first_name', max_length=50)
    last_name = models.CharField('last_name', max_length=50)
    email = models.EmailField('e-mail')
    ship_address = models.CharField('ship_address', max_length=250)
    address2 = models.CharField('address2', max_length=250)
    locality = models.CharField('locality', max_length=250)
    state = models.CharField('state', max_length=250)
    postcode = models.CharField('postcode', max_length=250)
    country = models.CharField('country', max_length=250)
    phone = models.CharField(validators=[
        RegexValidator(regex=r'^\+?1?\d{9,11}$', message='Phone number must be 9-11 characters',
                       code='invalid_phone_number')], max_length=11, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=250, blank=True)
    coupon = models.ForeignKey(Coupon,
                               related_name='orders',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Order {self.id}'

    def get_absolute_url(self):
        return reverse('process')

    def get_total_cost_before_discount(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_discount(self):
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost * (self.discount / Decimal(100))
        return Decimal(0)

    def get_total_cost(self):
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount()

    def get_stripe_url(self):
        if not self.stripe_id:
            return ''
        if '_test_' in settings.STRIPE_SECRET_KEY:
            path = '/test/'
        else:
            path = '/'
        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    course = models.ForeignKey(Course,
                               related_name='order_items',
                               on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
