from django.db import models 
from django.utils.text import slugify
from django.conf import settings
from django.shortcuts import reverse,get_object_or_404



# Create a tuple for category choiches --
# left entry will store in the  database and right entry will displayed 

CATEGORY_CHOICES = (
    ('S','Shirt'),
    ('SW','Sport sWear'),
    ('OW','Out Wear')
    )

# create a tuple for choiching the label like bestselling, new etc

LABEL_CHOICES = (
    ('P' , 'primary'),
    ('S' , 'secondary'),
    ('D' , 'danger')
)
 

class Item(models.Model):
    title = models.CharField(max_length=32,null=True,blank=True)
    price = models.FloatField()
    discount_price = models.FloatField(null=True,blank=True)
    category = models.CharField(choices = CATEGORY_CHOICES,max_length = 2,default='S') # get_fieldname_display - to select choiches from template - get_category_display
    #{{object.get_label_display}} in the template will invoke the associated lebel of the item 
    label = models.CharField(choices = LABEL_CHOICES,max_length = 1,default='P') # get_label_display
    slug = models.SlugField()
    description = models.TextField(default='description here')
    image = models.ImageField(null=True,blank=True)
    
    


    def __str__(self):
        return  self.title

    #{{ item.get_absolute_url }} this method belongs to Item model and its feild and objects. 
    def get_absolute_url(self): 
        return reverse("core:product_detail", kwargs={"slug": self.slug})

    # {{object.get_add_to_cart_url}} 
    # object is the default context variable in the detail view. And call the variable with this method will perform an action of add_to_cart and provide the url add-to-cart
    # with a slug  
    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={"slug": self.slug})

    # {{object.get_remove_from_cart_url}}
    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={"slug": self.slug})
    

# when an user simply add an item to cart,this Order_Item model will hold or store the associate info.This is like the primary steps to buy- imagine you have a cartwheel and you carry it and store the item in it.
 
class Order_Item(models.Model): # like a cart you carry during shopping in the super shop
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)# initialy false because you didn't pay for this item                      
    item = models.ForeignKey(Item,on_delete=models.CASCADE) # the product you put in the cart
    quantity = models.IntegerField(default=1) # quantity of the item in the single cart, an item would have > 1 .


    def __str__(self):
        return '{0.quantity} pieces {0.item.title} by {0.user.username}'.format(self)

    # now create some methods associated with this model and model field to calculate some data based on users activity
    #${{order_item.get_total_item_price}} - order_item is the iterator associated with items and default model manager objects 

    # this all method belong to the objects created by this model class order_item = Order_Item.objects.all
    #now order_item (objects of Order_Item )can invoke this methods

    # {{order_item.get_total_item_price}}
    def get_total_item_price(self): # calculate and return total price when invoke
        return self.quantity * self.item.price
    
    # {{order_item.get_total_discount_item_price}}
    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price()- self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price: # discount_price field  belongs to Item model and item is the foreign key of this model,thus we can access both field
            return self.get_total_discount_item_price()
        else:
            return self.get_total_item_price()


# Imagine the real life experiens in super shop-you give the cartwheel and the salesman input all the detail in the software and return a cash memo to you. This model is like that. we need user info,their items,the time(start_date),
#ordered_date(because its e-com),billing_address,payment info,and at the end if everything ok , then the status which is ordered here.(a Boolean field)

class Order(models.Model): # store users final cart by users items on parchase time
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(Order_Item)
    ref_code = models.CharField(max_length=20)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey("BillingAddress",on_delete=models.SET_NULL,blank=True,null=True)
    payment = models.ForeignKey("Payment",on_delete=models.SET_NULL,blank=True,null=True)
    coupon = models.ForeignKey("Coupon",on_delete=models.SET_NULL,blank=True,null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    

    def __str__(self):
        return '{0.user.username}  at  {0.ordered_date}'.format(self)

    # {{order.get_total}}
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=21,null=True)
    street_address = models.CharField(max_length=50)
    home_address = models.CharField(max_length=50)
    default = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.user.username

class Coupon(models.Model):
    code = models.CharField(max_length = 15)
    amount = models.FloatField(default=5.0)
    

    def __str__(self):
        return self.code

class Refund(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    reason = models.TextField()
    email = models.EmailField()
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return 'pk'.format(self)
    
    

            







