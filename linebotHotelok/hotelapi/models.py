from django.db import models

class users(models.Model):
    uid = models.CharField(max_length=50, null=False)
    created_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.uid

class booking(models.Model):
    bid = models.CharField(max_length=50, default='0', null=False)
    user_name = models.CharField(max_length=20, null=False)
    educationtype = models.CharField(max_length=20, null=False)
    loan_datetime = models.CharField(max_length=20, null=False)
    loan_amnt = models.CharField(max_length=20, null=False)
    int_rate = models.CharField(max_length=20, null=False)
    installment = models.CharField(max_length=20, null=False)
    fico_range_low = models.CharField(max_length=20, null=False)
    total_pymnt = models.CharField(max_length=20, null=False)
    total_rec_prncp = models.CharField(max_length=20, null=False)
    last_pymnt_amnt = models.CharField(max_length=20, null=False)
    last_fico_range_high = models.CharField(max_length=20, null=False)
    last_fico_range_low = models.CharField(max_length=20, null=False)
    
    def __str__(self):
        return self.id
