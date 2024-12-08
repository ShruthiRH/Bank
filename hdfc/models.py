from django.db import models

class bank_hdfc(models.Model):
    user_name = models.TextField(max_length=100, unique=True)
    user_type = models.TextField()
    card_number = models.PositiveBigIntegerField(unique=True)
    cvv = models.PositiveIntegerField(max_length=3, unique=True)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return self.user_name

