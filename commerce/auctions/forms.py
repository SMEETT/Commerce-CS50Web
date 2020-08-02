from django import forms
from .models import Listing, Category, Bid, Comment

class ListingForm(forms.ModelForm):
    # populate the CATEGORY dropdown with all available categories
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select)
    
    class Meta:
        model = Listing
        fields = ('title', 'description', 'imgurl', 'category', 'start_price')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Please enter a Title.'}),
            'description': forms.Textarea(attrs={'placeholder': 'Please add a description.'}),
            'imgurl': forms.TextInput(attrs={'placeholder': 'Please provide an Image URL.'}),
            'start_price': forms.NumberInput(attrs={'placeholder': 'Please set a starting price.'})
        }

        # Adjust LABELS where necessary
        labels = {
            'imgurl': "Image URL",
            'start_price': 'Start Price',
        }


# this form doesn't need any css-classes as attrs, since it uses CrispyForm 
# to be able to render it in a row

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ('bid_price',)
        widgets = {
            'bid_price': forms.NumberInput(attrs={'placeholder': 'Place your Bid'})
        }
        labels = {
            'bid_price': ""
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': 'Please feel free to comment on this listing.'})
        }
        labels = {
            'comment': "",
        }