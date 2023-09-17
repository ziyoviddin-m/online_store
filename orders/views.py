import uuid
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from orders.forms import OrderForm
from django.views.generic import TemplateView, CreateView, DetailView
from common.mixin import TitleMixin
from products.models import Basket
from yookassa import Configuration, Payment
from orders.models import Order


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'ZIYOVIDDIN - Спасибо за заказ'

class Success(TemplateView):
    template_name = 'orders/success.html'

    def get(self, request, *args, **kwargs):
        super(Success, self).get(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=request.user)
        
        basket_history_data = []
        basket_item = {
            'purchased_items': [basket.de_json() for basket in baskets],
            'total_sum': float(baskets.total_sum())
        }
        basket_history_data.append(basket_item)

        order = Order.objects.filter(initiator=request.user).last()
        order.basket_history = basket_history_data
        order.status = order.PAID
        order.save()
        baskets.delete()
        return redirect('orders:order-success')


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order-create')
    title = 'ZIYOVIDDIN - Оформление заказа'

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)

        Configuration.account_id = '244417'
        Configuration.secret_key = 'test_LddCestGJrNmrUdK_4f_I-jXc9eNmdsMGGIXMWCXJQw'
        
        baskets = Basket.objects.filter(user=request.user)

        payment = Payment.create({
            "amount": {
                "value": f"{float(baskets.total_sum())}",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "http://127.0.0.1:8000/orders/success/"
            },
            "capture": True,
            "description": "Заказ №1"
        }, uuid.uuid4())
        return HttpResponseRedirect(payment.confirmation.confirmation_url)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)
    
    
class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Order
    
    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = f'ZIYOVIDDIN - Заказ #{self.object.id}'
        return context


    


