from django.urls import path
from .views import check_user, check_ngo, make_transactions

urlpatterns = [
    path('check-user/', check_user, name='check_user'),
    path('check-ngo/', check_ngo, name='check_ngo'),
    path('make-transaction/',make_transactions, name='make_transaction')
]
