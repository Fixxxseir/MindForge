import stripe

from config.settings import STRIPE_API_KEY


class StripeService:
    stripe.api_key = STRIPE_API_KEY

    @staticmethod
    def create_stripe_product(name):
        """Создает продукт в stripe."""
        product = stripe.Product.create(name=name)

        return product

    @staticmethod
    def create_stripe_price(
        amount,
        product,
        currency="usd",
    ):
        """Создание цену в stripe."""
        price = stripe.Price.create(
            currency=currency,
            unit_amount=int(amount * 100),
            product_data={"name": product},
        )

        return price

    @staticmethod
    def create_stripe_session(success_url, price_id):
        """Создание сессию на оплату в stripe."""
        session = stripe.checkout.Session.create(
            success_url=success_url,
            line_items=[{"price": price_id, "quantity": 1}],
            mode="payment",
        )

        return session
