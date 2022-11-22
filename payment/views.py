from decimal import Decimal
import imp
from django.http import HttpResponseNotFound, JsonResponse
import stripe
from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from orders.models import Order
from students.forms import CourseEnrollForm
from students.views import StudentEnrollCourseView
from orders.tasks import order_created
from cart.cart import Cart
from orders.forms import OrderCreateForm
from orders.models import OrderItem
from courses.models import Course
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import get_user_model
User = get_user_model()

# create the Stripe instance
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

def payment_process(request):
    cart = Cart(request)
    if request.method == 'POST':
        cancel_url = request.build_absolute_uri(reverse('cart_detail'))
        success_url = "http://127.0.0.1:8000/payment/success/?session_id={CHECKOUT_SESSION_ID}"
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                        course=item['course'],
                                        price=item['price'],
                                        quantity=item['quantity'])
            order = get_object_or_404(Order, id=order.id)
            session_data = {
            'customer_email': form.cleaned_data['email'],
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
            }
            for item in cart:
                session_data['line_items'].append({
                    'price_data': {
                        'unit_amount': int(item['price'] * Decimal('100')),
                        'currency': 'usd',
                        'product_data': {
                            'name': item['course'].title,
                        },
                    },
                    'quantity': item['quantity'],
                })
            if cart.coupon:
                stripe_coupon = stripe.Coupon.create(
                                    name=cart.coupon.code,
                                    percent_off=cart.discount,
                                    duration='once')
                session_data['discounts'] = [{
                    'coupon': stripe_coupon.id
                }]
            session = stripe.checkout.Session.create(**session_data)
            return redirect(session.url, code=303)
        else:
            print("ERROR : Form is invalid")
            print(form.errors)
    else:
        form = OrderCreateForm(instance=request.user,initial={'country': 'United States'})
    return render(request, 'payment/process.html', {'form': form,'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,})

def payment_completed(request, *args, **kwargs):
        #session = stripe.checkout.Session.retrieve('session_id')
        #customer = stripe.Customer.retrieve(session.customer)
        #session_id = request.GET.get('session_id')
        #if session_id is None:
            #return HttpResponseNotFound()  
        #session = stripe.checkout.Session.retrieve(session_id)

        cart = Cart(request)
        course_ids = cart.cart.keys()
        courses = Course.objects.filter(id__in=course_ids)
        for course in courses:
            course.students.add(request.user)
        cart.clear()
        return render(request, 'payment/completed.html',{'courses':courses})

def payment_canceled(request):
    return render(request, 'payment/canceled.html')