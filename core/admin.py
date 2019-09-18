from django.contrib import admin
from .models import Item,Order,Order_Item,BillingAddress,Payment,Coupon,Refund,Wishlist
# Register your models here.

# create a method which will change the field in the admin section
def make_refund_accepted(modeladmin,request,queryset):
    # now set a quesryset and update with perticular fieldset
    queryset.update(refund_requested=False,refund_granted=True)

make_refund_accepted.short_description = 'Update orders to refund granted'



class OrderAdmin(admin.ModelAdmin):
    list_display = ['user' , 'ordered','being_delivered','received','refund_requested','refund_granted','billing_address','payment','coupon']

    list_display_links = [ 'user','billing_address','payment','coupon']

    list_filter = ['being_delivered','received','refund_requested','refund_granted' ]

    search_fields = [ 'user__username','ref_code']
    actions = [make_refund_accepted]


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['user' , 'ordered' , 'item']


class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user']

admin.site.register(Item)
admin.site.register(Order, OrderAdmin)
admin.site.register(Order_Item,OrderItemAdmin)
admin.site.register(BillingAddress)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Wishlist,WishlistAdmin)




