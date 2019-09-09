from django import template
from core.models import Order

# now register out template tags to template library

register = template.Library()


@register.filter
def cart_item_count(user): # here cart_item_count will be our custome template tag
    if user.is_authenticated:
        # make a query to check if ther is any order of requested/current user
        qs = Order.objects.filter(user=user,ordered = False)
        if qs.exists():
            return qs[0].items.count()
    else:
        return 0

