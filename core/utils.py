from django.utils.text import slugify

'''
random_string_generator is located here:
http://joincfe.com/blog/random-string-generator-in-python/
'''
import random
import string

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists() # if the slug is present or not
    if qs_exists: # if a slug already exists create a new slug with random string
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug



def unique_order_id_generator(instance): # instance refer to the model instance
    new_order_id = random_string_generator()

    Klass = instance.__class__
    # here order_id is the model field attribute
    qs_exists = Klass.objects.filter(order_id=new_order_id).exists() # if the slug is present or not
    if qs_exists: # if an order id is  already exists create a new order_id with random string

        return unique_order_id_generator(instance)
    return new_order_id



