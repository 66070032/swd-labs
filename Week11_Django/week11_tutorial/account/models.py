from django.db import models, transaction
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.
class Account(models.Model):
    owner = models.CharField(max_length=100)
    account_no = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def transfer_funds(self, to_account_no, amount):
        try:
            with transaction.atomic():
                from_account = self
                if from_account.balance < amount:
                    raise ValueError("Insufficient funds in the source account.")
                # Debit the amount from the source account
                from_account.balance = from_account.balance - amount
                from_account.save()

                to_account = Account.objects.get(account_no=to_account_no)
                # Credit the amount to the destination account
                to_account.balance = to_account.balance + amount
                to_account.save()
        except ObjectDoesNotExist:
            print("Account does not exist.")

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)