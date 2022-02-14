from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db import transaction

from django.forms import inlineformset_factory

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from basketapp.models import Basket
from ordersapp.models import Order, OrderItem
from ordersapp.forms import OrderItemForm

from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete


class OrderList(ListView):
   model = Order
   template_name = "ordersapp/order_list.html"

   def get_queryset(self):
       return Order.objects.filter(user=self.request.user)

   def get_context_data(self, *, object_list=None, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Заказы'
    return context



class OrderItemsCreate(CreateView):
    model = Order
    template_name = "ordersapp/order_form.html"
    fields = []
    success_url = reverse_lazy('ordersapp:orders_list')

    def get_context_data(self, **kwargs):
        data = super(OrderItemsCreate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)


        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.get_items(self.request.user)
            if len(basket_items):
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(basket_items))
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price
                basket_items.delete()
            else:
                formset = OrderFormSet()

        data['orderitems'] = formset
        data['page_title'] = 'Создание заказа'
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderItemsCreate, self).form_valid(form)


class OrderItemsUpdate(UpdateView):
    model = Order
    template_name = "ordersapp/order_form.html"
    fields = []
    success_url = reverse_lazy('ordersapp:orders_list')

    def get_context_data(self, **kwargs):
        data = super(OrderItemsUpdate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            data['orderitems'] = OrderFormSet(self.request.POST, instance=self.object)
        else:
            #data['orderitems'] = OrderFormSet(instance=self.object)
            formset = OrderFormSet(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
            data['orderitems'] = formset
            data['page_title'] = 'Редактирование заказа'
        return data

    def get_item(self, *args, **kwargs):
        return self.objects.get(*args, **kwargs)

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderItemsUpdate, self).form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    template_name = "ordersapp/order_confirm_delete.html"
    success_url = reverse_lazy('ordersapp:orders_list')

    def get_context_data(self, **kwargs):
        context = super(OrderDelete, self).get_context_data(**kwargs)
        context['page_title'] = 'Удаление заказа'
        return context


class OrderRead(DetailView):
   model = Order

   def get_context_data(self, **kwargs):
       context = super(OrderRead, self).get_context_data(**kwargs)
       context['page_title'] = 'Просмотр заказа'
       return context


def order_forming_complete(request, pk):
   order = get_object_or_404(Order, pk=pk)
   order.status = Order.SENT_TO_PROCEED
   order.save()

   return HttpResponseRedirect(reverse('ordersapp:orders_list'))

# здесь вылетала ошибка с объектами потому, что в таком виде эта функция дёргает класс, а не непосредственно объект, но он-то не дёргается тем get_item, который с self.
# get_item с конкретным аргументом (pk) на это работал, потому что конкретный аргумент. чтобы это пофиксить, в строке 158 уточняем аргумент для get_item (instance, pk=instance.pk),
# и ещё вызываем метод __class__ у get_item
# (если опять запутаешься - спроси Киху, попроси ещё раз объяснить)

@receiver(pre_save, sender=OrderItem)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
   if update_fields is 'quantity' or 'product':
       if instance.pk:
           instance.product.quantity -= instance.quantity - \
                                        sender.get_item(instance, pk=instance.pk).quantity
       else:
           instance.product.quantity -= instance.quantity
       instance.product.save()


@receiver(pre_delete, sender=OrderItem)
def product_quantity_update_delete(sender, instance, **kwargs):
   instance.product.quantity += instance.quantity
   instance.product.save()


