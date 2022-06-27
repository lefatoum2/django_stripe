
import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView

from stripapp.models import Price

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(View):

    def post(self, request, *args, **kwargs):
        price = Price.objects.get(id=self.kwargs["pk"])
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price.stripe_price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=settings.BASE_URL + '/payments/success/',
            cancel_url=settings.BASE_URL + '/payments/cancel/',
        )
        return redirect(checkout_session.url)


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        product = Product.objects.get(name="Basic Plan")
        prices = Price.objects.filter(product=product)
        context = super(HomePageView, self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "prices": prices
        })
        return context