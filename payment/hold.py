def payment_process(request):
    cart = Cart(request)
    if request.method == 'POST':
        success_url=request.build_absolute_uri(
            reverse('completed')
        ) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url = request.build_absolute_uri(
                        reverse('cart_detail'))
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                        course=item['course'],
                                        price=item['price'],
                                        quantity=item['quantity'])
            
            # launch asynchronous task
            
            order = get_object_or_404(Order, id=order.id)
        # Stripe checkout session data
        session_data = {
            'customer_email': form['email'],
            'mode': 'payment',
            #'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }
        # add order items to the Stripe checkout session
        for item in order.items.all():
            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': int(item.price * Decimal('100')),
                    'currency': 'usd',
                    'product_data': {
                        'name': item.course.title,
                    },
                },
                'quantity': item.quantity,
            })
        # Stripe coupon
        if order.coupon:
            stripe_coupon = stripe.Coupon.create(
                                name=order.coupon.code,
                                percent_off=order.discount,
                                duration='once')
            session_data['discounts'] = [{
                'coupon': stripe_coupon.id
            }]

        # create Stripe checkout session
        session = stripe.checkout.Session.create(**session_data)
        return redirect(session.url, code=303)

    else:
        form = OrderCreateForm(instance=request.user)
    return render(request, 'payment/process.html', {'form': form,'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY})