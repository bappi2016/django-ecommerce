from __future__ import absolute_import, unicode_literals
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect,get_object_or_404
from .models import Item,Order,Order_Item,BillingAddress,Payment,Coupon,Refund,Wishlist
from django.views.generic import ListView,DetailView,View
from django.utils import timezone
from .tasks import send_feedback_email_task
from django.contrib.auth.decorators import login_required
from .forms import CheckoutForm,CouponForm,RefundForm
from django.core import mail
from django.core.mail import EmailMessage
from django.template.loader import get_template
import random
from random import choice
import string


from django.contrib.auth.models import User




# Create your views here.
class HomeView(ListView): # for displaying listview the default context variable is object_list
    model = Item
    paginate_by = 4
    template_name = "index.html"

class OrderSummaryView(LoginRequiredMixin,View):
    def get(self, *args , **kwargs):
        try:
            #from the Order model get the requested user,whose ordered =False, means order not yet delevered and store the value in the order
            order = Order.objects.get(user=self.request.user,ordered=False)
            context = { # set the default context variable object to order
                'object':order
            }
            return render(self.request,"order_summary.html",context)
        except ObjectDoesNotExist:# if user didn't have any item in the cart,but request the cart view
            messages.warning(self.request,"You do not have an active order")
            return redirect('/')
        


class ProductDetailView(DetailView): 
    model = Item
    template_name = "product_page.html"



# 1 -  Take the item,
# 2 - Create an order item, just like put the item in cart
# 3 - Assign the order item to the order if the user hasn't already ordered the item,if not, create the order item on the spot- like pass the cart to the salesman for entry and checkout and payment 
# 
#  

@login_required
def add_to_cart(request, slug): # pass the slug as the kwargs as a single item 
    # 1 -  Take the item,
    # at first get the item by its slug field from the Item model, 
    item = get_object_or_404(Item,slug=slug)
  
    # 2 - Create an order item,
    # by taking the item in the model Order_Item/cart
    # create an object and assign it to the variable order_item, take three field as arguments- a single item,requested user,and check the item not yet delevered 
    order_item,created = Order_Item.objects.get_or_create(item=item,
    user = request.user,
    ordered = False
    )# uses orm (get_or_create) to create the item in the Model

    # check if the user has the item in Order or not, for this we need to grab the users Order model,now make a qs

    # Take the current users Order models and filter ordered field and assign the result in order_qs
    order_qs = Order.objects.filter(user=request.user,ordered = False) # ordered = False,means user can now add new item to cart and order_qs has exists
    if order_qs.exists(): # if there is any model found
        #order = Order.objects.create(user=request.user,ordered_date=ordered_date)- create an object of the Order class and named it order
        order = order_qs[0] # grab the first cart/order of the list and assign it to order, now order has the percase item of user, 

        # Finally assign this order object to the Order model
        # In Order model there is items(ManyToManyField) field of Order-Item,that means we can store an Order item multiple times and it will store in the items field
        # items = models.ManyToManyField(Order_Item)
        # grab the first carts (order) in the items field and check if it maches any item when perchesing 
        if order.items.filter(item__slug=item.slug).exists():
            #it means this item in already in the cart
            # now just simply increase the quantity of it order_item.
            order_item.quantity += 1
            order_item.save()
            messages.info(request,'The item quantity was updated')
            return redirect('core:order-summary') 

        else: # if the item is new ... simply add the order_item to order.items
            # order = Order.objects.create(user=request.user,ordered_date=ordered_date)
            # thus order is the object of Order class, it can access all the class field like items -just like
            # order.items, order.billing_address etc
            order.items.add(order_item) # get the order_item and add it as an items[order_item]
            messages.info(request,"This item was added to your cart")
            return redirect('core:order-summary') 

        
    else: # if the perchase item is new
        ordered_date = timezone.now()  # grab the current time

        # take the current user field of the Order model and, other required field assign it to order, the  object of the Order model
        order = Order.objects.create(user=request.user,ordered_date=ordered_date)
        # add the order_item to the order.items field
        # order_item = Order_Item.objects.create(item=item)
        order.items.add(order_item)
        messages.info(request,'This item was added to your cart')
            

        # after successfully add an item
        return redirect('core:order-summary')



@login_required
def remove_from_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_qs = Order.objects.filter(user=request.user,ordered = False) # ordered = False,means user can now add new item to cart and order_qs has exists
    if order_qs.exists(): # if there is any model found
        order = order_qs[0] # grab the first cart/order of the list and assign it to order, now order has the percase item of user, 

        # Finally assign this order object to the Order model
        # In Order model there is items(ManyToManyField) field of Order-Item,that means we can store an Order item multiple times and it will store in the items field
        # items = models.ManyToManyField(Order_Item)
        # grab the first carts (order) items field and check if it maches any item when perchesing 
        if order.items.filter(item__slug=item.slug).exists():
            order_item = Order_Item.objects.filter(
                item=item,
                user = request.user,
                ordered = False
            )[0] # the last item that matches the filter
            order.items.remove(order_item)
            messages.info(request,'This item was removed from your cart')
            return redirect('core:order-summary')
        else:
            messages.info(request,'This item was not in your cart')
            return redirect('core:product_detail',slug=slug)
    else:
        messages.error(request,'You do not have an active order')# add a message saying the user doesn't have an order
        return redirect('core:product_detail',slug = slug)


@login_required
def remove_single_item_from_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_qs = Order.objects.filter(user=request.user,ordered = False) # ordered = False,means user can now add new item to cart and order_qs has exists
    if order_qs.exists(): # if there is any model found
        order = order_qs[0] # grab the first cart/order of the list and assign it to order, now order has the percase item of user, 

        # Finally assign this order object to the Order model
        # In Order model there is items(ManyToManyField) field of Order-Item,that means we can store an Order item multiple times and it will store in the items field
        # items = models.ManyToManyField(Order_Item)
        # grab the first carts (order) items field and check if it maches any item when perchesing
        # item__slug=item.slug will filter the single item just like pk = pk 
        if order.items.filter(item__slug=item.slug).exists():
            order_item = Order_Item.objects.filter(
                item=item,
                user = request.user,
                ordered = False
            )[0] # grab the last matches item
            if order_item.quantity > 1: 
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request,'This item quantity was updated')
            return redirect('core:order-summary')
        else:
            messages.info(request,'This item was not in your cart')
            return redirect('core:order-summary')
    else:
        messages.warning(request,'You do not have an active order')# add a message saying the user doesn't have an order
        return redirect('core:order-summary')

def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

class CheckoutView(View):
    def get(self,*args,**kwargs): # here we will override the get method
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            form = CheckoutForm()
            context = {
                'form':form,
                'coupon_form':CouponForm(),
                'order':order
            }
            dafult_address_qs = BillingAddress.objects.filter(
                user = self.request.user,
                default = True
            )
            if dafult_address_qs.exists():
                context.update({'default_address':dafult_address_qs[0]})

            return render(self.request,"checkout.html",context)
        except ObjectDoesNotExist:
            messages.warning(self.request,"You do not have an active order")
            return redirect("core:checkout")
        
        
    def post(self,*args,**kwargs): # for continue checkout
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            if form.is_valid():
                use_default_address = form.cleaned_data.get(
                    'use_default_address')
                if use_default_address:
                    print("Using the defualt address")
                    address_qs = BillingAddress.objects.filter(
                        user=self.request.user,
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                        
                    else:
                        messages.info(
                            self.request,"No default shipping address available")
                        return redirect('core:checkout')
                
                else:
                    print("User is entering a new shipping address")
                    name = form.cleaned_data.get('name')
                    phone = form.cleaned_data.get('phone')
                    street_address = form.cleaned_data.get('street_address')
                    home_address = form.cleaned_data.get('home_address')
                    
                    
                    if is_valid_form([name,phone,street_address,home_address]):
                        billing_address = BillingAddress(
                            user = self.request.user,
                            name = name,
                            phone = phone,
                            street_address = street_address,
                            home_address = home_address
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()
                        
                        save_address = form.cleaned_data.get(
                                'save_as_default_address')
                        if save_address:
                            billing_address.default = True
                            billing_address.save()
                    else :
                        messages.info(self.request,"Please fill the required addresses fields")
                        return redirect('core:checkout')

                
                payment_option = form.cleaned_data.get('payment_option')
                if payment_option == 'C':
                    return redirect('core:payment',payment_option= 'Cash-on-delevery') 
            
        except ObjectDoesNotExist:
            messages.warning(self.request,"You do not have an active order")
            return redirect('core:order-summary')
      
# create a random referrence code when user complete a perchase       
def create_ref_code(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class PaymentView(View):
    def get(self,*args,**kwargs):
        #form = CheckoutForm()
        order = Order.objects.get(user=self.request.user,ordered=False)
        context = {
            'order':order
        }
        return render(self.request,"payment.html",context)
        
    def post(self,*args,**kwargs):
        order = Order.objects.get(user=self.request.user,ordered=False)
        amount  = int(order.get_total())
        

        # create the payment
        payment = Payment()
        payment.user = self.request.user
        payment.amount = amount
        payment.save()

        # in our order model , we need to set all the perchage item to True , that means ordered =True
        # first grab all the order items and asssign it to order_items
        order_items = order.items.all()
        # update all the items to ordered =True
        order_items.update(ordered=True)
        # and save their current status- by loop throug all the item
        for item in order_items:
            item.save() 

        # assign the payment to the order
        order.ordered = True
        order.payment = payment
        order.ref_code = create_ref_code()
        order.save()

        messages.success(self.request,"Your order has been received,We will notify you soon")
        return redirect('core:home')


# coupon funtinality 

def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request,'This coupon does not exists')
        return redirect('core:checkout')

# def add_coupon(request):
#     if request.method == "POST":
#         form = CouponForm(request.POST or None)
#         if form.is_valid():
#             try:
#                 code = form.cleaned_data.get('code')
#                 order = Order.objects.get(user=request.user,ordered = False) # 1st get the order
#                 order.coupon = get_coupon(request,code) # get the coupon
#                 order.save()
#                 messages.success(request,'The coupon has been successfully added to your cart')
#                 return redirect('core:checkout')
#             except ObjectDoesNotExist:
#                 messages.info(request,'You do not have an active cart')
#                 return redirect('core:checkout')
#     #TODO raise exception here             
#     return None
      

class AddCouponView(View):
    # this view will handle a form , so we need to override the post method
    def post(self, *args,**kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                # get the code from the form
                code = form.cleaned_data.get('code')
                # get the order
                order = Order.objects.get(user=self.request.user,ordered=False)
                order.coupon = get_coupon(self.request,code)
                order.save()
                messages.success(self.request,'The coupon has been successfully added to your cart')
                return redirect('core:checkout')
            except ObjectDoesNotExist:
                messages.warning(self.request,"You do not have an active order")
                return redirect('core:checkout')


class RequestRefundView(View):
    def get(self,*args,**kwargs):
        form = RefundForm()
        context = {
            'form':form
        }
        return render(self.request,"request_refund.html",context)
    def post(self,*args,**kwargs):
        form = RefundForm(self.request.POST or None)
        if form.is_valid():
            # get the ref code from the form
            ref_code = form.cleaned_data.get('ref_code')
            # get the messages from the form
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                #   store the rufun to the model
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()
                send_feedback_email_task.delay(message,email,ref_code)
 
                
                messages.info(self.request,'Your request has been submitted, we will notify you soon')
                return redirect('core:request-refund')

            except ObjectDoesNotExist:
                messages.info(self.request,"Your referrence code didn't match")
                return redirect('core:request-refund')

# add and remove wishlist funtionality


@login_required
def add_to_wishlist(request,slug):

    item = get_object_or_404(Item,slug=slug)

    wished_item,created = Wishlist.objects.get_or_create(wished_item=item,
    slug = item.slug,
    user = request.user,
    ) # creating or extracting the wished item
    if created:
        messages.info(request,'The item was added to your wishlist')
    # make a query to check if item requested item is exits or not
    else:
        messages.info(request,'The item was already in your wishlist')
    return redirect('core:product_detail',slug=slug)

    

    
    # if wish_list_qs.exists():
    #     messages.info(request,'The item was already in your wishlist')
    #     return redirect('core:product_detail',slug=slug)



class WishlistView(LoginRequiredMixin,View):
    def get(self, *args , **kwargs):
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            wishlist = Wishlist.objects.filter(user=self.request.user)
            context = { # set the default context variable object to order
            'object':order,
            'wishlist':wishlist
            }
            return render(self.request,"wishlist.html",context)
        except ObjectDoesNotExist:# if user didn't have any item in the cart,but request the cart view
            messages.warning(self.request,"You do not have any wishlist item")
            return redirect('/')









    

    

