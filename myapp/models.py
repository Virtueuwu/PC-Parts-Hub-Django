from django.db import models
from django.contrib.auth.models import User
from PIL import Image



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null= True)
    email = models.CharField(max_length=200, null= True)

    def __str__(self):
        return self.name if self.name else "Unnamed Customer"
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the product instance first

        if self.image:  # Check if an image is uploaded
            img = Image.open(self.image.path)  # Open the image using Pillow

            # Resize the image
            img = img.resize((300, 300), Image.Resampling.LANCZOS)

            # If the image is in "P" mode, convert it to "RGB" (JPEG format compatible)
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Save the resized and converted image back to the same path
            img.save(self.image.path, 'JPEG')  # Ensure saving as JPEG
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_oredered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length = 100, null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        return shipping
    
    #Calculate Total Price for Items
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
     #Calculate Total Quantity for Items
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default = 0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    # Calculate total price of items
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address