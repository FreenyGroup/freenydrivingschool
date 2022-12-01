from decimal import Decimal
from django.conf import settings
from courses.models import Course
from coupons.models import Coupon
import json

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

class Cart:
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')
    def __iter__(self):
        """
        Iterate over the items in the cart and get the courses
        from the database.
        """
        course_ids = self.cart.keys()
        courses = Course.objects.filter(id__in=course_ids)
        cart = self.cart.copy()
        for course in courses:
            cart[str(course.id)]['course'] = course
        for item in cart.values():
            item['price'] = item['price']
            item['total_price'] = item['price'] * item['quantity']
            yield item
    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())
    def add(self, course, quantity=1, override_quantity=False):
        """
        Add a course to the cart or update its quantity.
        """
        course_id = str(course.id)
        if course_id not in self.cart:
            self.cart[course_id] = {'quantity': 0,
                                     'price': str(course.price)}
        if override_quantity:
            self.cart[course_id]['quantity'] = quantity
        else:
            self.cart[course_id]['quantity'] += quantity
        self.save()
    def save(self):
        self.session.modified = True
    def remove(self, course):
        """
        Remove a course from the cart.
        """
        course_id = str(course.id)
        if course_id in self.cart:
            del self.cart[course_id]
            self.save()
    def clear(self):
        del self.cart
        self.save()
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) \
                * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()