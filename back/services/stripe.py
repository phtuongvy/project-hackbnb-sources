import os
import stripe
import requests
import re

def create_checkout(reference, name, unit_price, quantity, confirmation_secret):
    """
        Create Stripe checkout
        Documentation: https://docs.stripe.com/checkout/quickstart?client=react&lang=python
    """
    
    stripe.api_key = os.getenv('STRIPE_API_KEY')
    origin_host = os.getenv('APP_ORIGIN_HOST')
    return stripe.checkout.Session.create(
        mode='payment',
        success_url=f"{origin_host}/booking/{reference}?checkout_confirmation_secret={confirmation_secret}",
        cancel_url=origin_host,
        line_items=[
            {
                'quantity': quantity,
                'price_data': {
                    'currency': 'EUR',
                    'unit_amount': round(unit_price * 100),
                    'product_data': {
                        'name': name,
                    },
                },
            },
        ],
    )

def get_checkout_lines(checkout_session_id):
    # Fix D3 (SSRF) : on valide strictement le format de l'ID avant de construire l'URL,
    # pour empecher toute injection de caracteres (../, #, ?, /...) qui detournerait
    # la requete vers un autre endpoint de l'API Stripe.
    if not checkout_session_id or not re.fullmatch(r"^cs_[A-Za-z0-9_]+$", checkout_session_id):
        raise ValueError("Invalid checkout session ID")

    url = f"https://api.stripe.com/v1/checkout/sessions/{checkout_session_id}/line_items"

    session = requests.Session()
    session.auth = (os.getenv('STRIPE_API_KEY'), "")
    return session.get(url).json()["data"]
