from decimal import Decimal
import json
from .cart import Cart
def cart(request):
    return {'cart': Cart(request)}
