from django.db import models
from accounts.models import Account
from store.models import Product, Variation
from django.db.models import Avg, Count


class Payment(models.Model):
    user            = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id      = models.CharField(max_length=100)
    payment_method  = models.CharField(max_length=100)
    amount_paid     = models.CharField(max_length=100)
    status          = models.CharField(max_length=100)
    created_at      = models.DateTimeField(auto_now_add=True)
    modified_at     = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.payment_id
    
class Order(models.Model):
    status = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        )

    user            = models.ForeignKey(Account,on_delete=models.SET_NULL, null=True)
    payment         = models.ForeignKey(Payment,on_delete=models.SET_NULL, null=True, blank=True)
    order_number    = models.CharField(max_length=20)
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    phone_number    = models.CharField(max_length=15)
    email           = models.EmailField(max_length=50)
    address_line_1  = models.CharField(max_length=50)
    address_line_2  = models.CharField(max_length=50, blank=True)
    country         = models.CharField(max_length=50)
    state           = models.CharField(max_length=50)
    city            = models.CharField(max_length=50)
    order_note      = models.CharField(max_length=100, blank=True)
    order_total     = models.FloatField()
    tax             = models.FloatField()
    status          = models.CharField(max_length=10, choices=status, default='New')
    ip              = models.CharField(max_length=20, blank=True)
    is_ordered      = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    modified_at     = models.DateTimeField(auto_now=True)

    def full_name(self):
        return self.first_name + ' ' + self.last_name
    
    def full_address(self):
        return self.address_line_1 + ' ' + self.address_line_2

    def __str__(self):
        return self.first_name
    

class OrderProduct(models.Model):
    order          = models.ForeignKey(Order,on_delete=models.CASCADE)            
    payment        = models.ForeignKey(Payment,on_delete=models.SET_NULL, blank=True, null=True)             
    user           = models.ForeignKey(Account,on_delete=models.CASCADE) 
    product        = models.ForeignKey(Product,on_delete=models.CASCADE) 
    variations     = models.ManyToManyField(Variation, blank=True)   
    quantity       = models.IntegerField()
    product_price  = models.FloatField()
    ordered        = models.BooleanField(default=False)
    created_at     = models.DateTimeField(auto_now_add=True)
    modified_at    = models.DateTimeField(auto_now=True) 

    def __str__(self) -> str:
        return self.product.product_name
    
    def save(self, *args, **kwargs):
        self.product_price = round(self.product_price, 2)
        super(OrderProduct, self).save(*args, **kwargs)

class ReviewRating(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    user        = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject     = models.CharField(max_length=100, blank=True)
    review      = models.TextField(max_length=500,blank=True)
    rating      = models.FloatField()
    ip          = models.CharField(max_length=20,blank=True)
    status      = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name
    
    def average_review(self):
        reviews = ReviewRating.objects.filter(product=self,status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
    
    def count_review(self):
        reviews = ReviewRating.objects.filter(product=self,status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count


    

