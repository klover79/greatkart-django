from django.db import models
from django.urls import reverse
from category.models import Category

class Product(models.Model):
    product_name    = models.CharField(max_length=200,  unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    description     = models.TextField(max_length=500, blank=True)
    price           = models.IntegerField()
    images          = models.ImageField(upload_to='photos/products')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    create_date     = models.DateField(auto_now_add=True)
    modified_date   = models.DateField(auto_now=True)

    def get_url(self):
        return reverse('stores:product-detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name
    


    


variation_category_choice =(
    ('color', 'color'),
    ('size', 'size'),
)

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color', is_active=True)
    
    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size', is_active=True)
    
    def get_product_variation(self, p_product, p_variation_category, p_variation_value):
        return self.get(product=p_product, variation_category__iexact=p_variation_category, variation_value__iexact=p_variation_value)

class Variation(models.Model):
    product             = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category  = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value     = models.CharField(max_length=100)
    is_active           = models.BooleanField(default=True)
    created_date        = models.DateTimeField(auto_now_add=True)
    updated_date        = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):   
        return self.variation_value
    
 
