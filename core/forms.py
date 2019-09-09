from django import forms


PAYMENT_CHOICES = (
    ('B','Bikash'), #key /name = B. value = Bikash
    ('C','Cash on delevery')
)

# name,phone,street,home
class CheckoutForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control','placeholder':'Jhon'}
    ),max_length=30,required=False)

    phone = forms.IntegerField(widget=forms.TextInput(
        attrs={'class':'form-control','placeholder':'+88 01...'}
    ),required=False)

    street_address = forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control','placeholder':'paris road'}
    ),max_length=120,required=False)

    home_address = forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control','placeholder':'5A Beautyladge'}
    ),max_length=120, required=False)

    use_default_address = forms.BooleanField(required=False)

    save_as_default_address = forms.BooleanField(required=False)

    payment_option = forms.ChoiceField(widget=forms.RadioSelect,choices=PAYMENT_CHOICES)



class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control',
        'placeholder':'Promo code',
        'aria-label':'Recipient\'s username',
        'aria-describedby' : 'basic-addon2'}
    ),max_length=30,required=True)

class RefundForm(forms.Form):
    ref_code = forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control',
        'placeholder':'Referrence code',
        'aria-label':'Recipient\'s username'}
    ),max_length=30,required=True)

    message = forms.CharField(widget=forms.Textarea(
        attrs={'class':'form-control',
        'placeholder':'Type your message here',
        'rows':4}
    ),max_length=30,required=True)

    email = forms.EmailField(widget= forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'Your email address',
    }))
