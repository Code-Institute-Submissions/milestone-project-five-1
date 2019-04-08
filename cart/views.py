import stripe

from decimal import *
from django.conf import settings

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages

from tickets.models import Contribution
from tickets.views import Ticket

stripe.api_key = settings.STRIPE_SECRET_KEY


def view_cart(request):

    return render(request, 'cart/cart.html')


def addtocart(request, featureid):
    """
    Add an amount to the cart for contributions to check out at a later time
    """

    cart = request.session.get('cart', {})
    if featureid not in cart:

        cart[featureid] = {
            'id': featureid,
            'contrib_amount': request.POST['contribution_amount']
        }

    else:

        messages.error(
            request, 'You\'re already contributing to this feature.')
        return redirect('/tickets/feature/'+featureid)

    request.session['cart'] = cart

    return redirect("cart")


def removefromcart(request, featureid):
    """
    Delete a feature contribution from the cart
    """
    cart = request.session.get('cart', {})

    if featureid in cart:

        del cart[featureid]
        messages.success(request, "Feature removed")

    request.session['cart'] = cart

    return redirect(reverse('cart'))


def checkout(request):

    context = {
        'key': settings.STRIPE_PUBLISHABLE_KEY
    }

    return render(request, "cart/checkout.html", context)


def charge(request):

    if request.method == 'POST':

        cart = request.session.get('cart', {})
        total_charge = 0

        for item in cart.keys():

            amount = cart[item]['contrib_amount']
            total_charge += Decimal(amount)

        try:

            charge = stripe.Charge.create(
                amount=int(total_charge*100),
                currency='eur',
                description='UA Feature Contribution',
                source=request.POST['stripeToken']
            )

            if charge.paid:

                for item in cart.keys():

                    user = request.user
                    ticket = get_object_or_404(Ticket, pk=item)
                    amount = cart[item]['contrib_amount']

                    contribution = Contribution(
                        userid=user,
                        ticket=ticket,
                        amount=amount)

                    contribution.save()

                messages.success(
                    request,
                    'Thank you for your contribution, \
                    keep an eye on the features to see \
                    when they will begin development.')

                request.session['cart'] = {}
                return redirect(reverse('dashboard'))

            else:

                messages.error(
                    request, 'The payment gateway declined your card.')

        except stripe.error.CardError:
            messages.error(
                request, 'There was an error processing your payment.')

        return redirect('dashboard')


def updatecart(request, featureid):
    """
    Delete a feature contribution from the cart
    """
    cart = request.session.get('cart', {})

    if featureid in cart:

        cart[featureid]['contrib_amount'] = request.POST['contribution_amount']
        messages.success(request, "Cart Updated!")

    request.session['cart'] = cart

    return redirect(reverse('cart'))