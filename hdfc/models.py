from django.db import models

class Account(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('ngo', 'NGO'),
        ('user', 'User'),
    ]
    
    ACCOUNT_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('closed', 'Closed'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES)
    account_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    account_status = models.CharField(max_length=20, choices=ACCOUNT_STATUS_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True)

    # Add the new account_number field
    account_number = models.CharField(max_length=16, default='0000000000000000')  # New field for account number

    class Meta:
        db_table = 'accounts'
        constraints = [
            models.CheckConstraint(check=models.Q(account_type__in=['ngo', 'user']), name='account_type_check'),
            models.CheckConstraint(check=models.Q(account_status__in=['active', 'inactive', 'closed']), name='account_status_check'),
        ]
        
    def __str__(self):
        return f'{self.name} ({self.account_number})'



class Card(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('blocked', 'Blocked'),
        ('expired', 'Expired'),
    ]
    
    account = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='cards')
    card_number = models.CharField(max_length=128)
    expiry_date = models.CharField(max_length=5) 
    cvv = models.CharField(max_length=128)
    pin_code = models.CharField(max_length=128)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    date_issued = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cards'
        constraints = [
            models.CheckConstraint(check=models.Q(status__in=['active', 'blocked', 'expired']), name='status_check'),
        ]

    def __str__(self):
        return f'{self.card_number} - {self.status}'

from django.db import models

class Transaction(models.Model):
    TRANSACTION_STATUS_CHOICES = [
        ('successful', 'Successful'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    ]
    
    account = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='transactions')
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_status = models.CharField(max_length=20, choices=TRANSACTION_STATUS_CHOICES)

    class Meta:
        db_table = 'transactions'
        constraints = [
            models.CheckConstraint(check=models.Q(transaction_status__in=['successful', 'pending', 'failed']), name='transaction_status_check'),
        ]

    def __str__(self):
        return f'{self.transaction_amount} - {self.transaction_status}'

