from django.shortcuts import render
from django.views.generic.base import TemplateView 

import stripe 
from django.conf import settings 

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
class PaymentPageView(TemplateView):
    template_name = 'payment.html'

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        g = self.kwargs['g']
        t = self.kwargs['t']
        rtype = self.kwargs['rtype']
        count = self.kwargs['count']
        return render(request, 'payment.html', {'key' : context['key'], 'g':g, 't':t, 'rtype':rtype, 'count':count})
