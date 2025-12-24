import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(payment):
    """Создание продукта в Stripe."""

    return stripe.Product.create(
        name=payment.course.title if payment.course else payment.lesson.title,
    )


def create_stripe_price(*, product, unit_amount):
    """Создание цены в Stripe (в копейках)."""

    return stripe.Price.create(
        currency="usd",
        unit_amount=unit_amount,
        product=product.id,
    )


def create_stripe_session(*, price_id):
    """Создание checkout-сессии."""

    return stripe.checkout.Session.create(
        success_url="http://localhost:8000/success/",
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
    )
