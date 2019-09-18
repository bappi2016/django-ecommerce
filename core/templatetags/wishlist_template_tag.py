from django import template
from core.models import Wishlist

# now register out template tags to template library

register = template.Library()


@register.filter
def wishlist_item_count(user): # here cart_item_count will be our custome template tag
    if user.is_authenticated:
        # make a query to check if ther is any order of requested/current user
        qs = Wishlist.objects.filter(user=user)
        if qs.exists():
            return qs.count()
    else:
        return 0

