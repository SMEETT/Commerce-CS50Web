from django import forms
from .models import Listing, Category, Bid

class CreateListingForm(forms.ModelForm):
    # populate the CATEGORY dropdown with all available categories
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    
    class Meta:
        model = Listing
        fields = ('title', 'description', 'imgurl', 'category', 'price')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter a Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Please add a description here.'}),
            'imgurl': forms.TextInput(attrs={'class': 'form-control', 'label': 'Image URL', 'placeholder': 'Please provide an Image URL'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Please set a starting price'})
        }
        # Adjust LABELS where necessary
        labels = {
            'imgurl': "Image URL",
            'price': 'Starting Bid',
        }


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ('bid',)
        widgets = {
            'bid': forms.NumberInput(attrs={'placeholder': 'Place your Bid'})
        }
        labels = {
            'bid': "",
        }