import datetime
from .models import Listing

def get_current_year_to_context(request):
    current_datetime = datetime.datetime.now()
    return {
        'current_year': current_datetime.year
    }

def get_listings_count_to_context(request):
    return {
        "listings_count": Listing.objects.all().count()
    }