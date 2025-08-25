# store/context_processors.py

def cart_context(request):
    cart = request.session.get('cart', [])
    cart_total_items = sum(item['quantity'] for item in cart)

    show_cart_badge = cart_total_items > 0 and not request.session.get('cart_seen', False)

    return {
        'cart': cart,
        'cart_total_items': cart_total_items,
        'show_cart_badge': show_cart_badge
    }
