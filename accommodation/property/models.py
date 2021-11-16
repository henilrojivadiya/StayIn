from django.db import models
from owner.models import Owner
from account.models import User
import re
from django.template.defaultfilters import truncatechars
from django.utils.safestring import mark_safe
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.cache import cache
# Create your models here.

class Property_Type(models.Model):
    Type = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ("Property Type")
        verbose_name_plural = ("(6) Property Types")

    def __str__(self):
        return self.Type


class Popular_Location(models.Model):
    name = models.CharField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ("Popular Location")
        verbose_name_plural = ("(5) Popular Locations")

    def __str__(self):
        return self.name


class Property_For(models.Model):
    name = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = ("Property For")
        verbose_name_plural = ("(7) Property For")

    def __str__(self):
        return self.name

class Property_Category(models.Model):
    name = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = ("Property Category")
        verbose_name_plural = ("(11) Property Category")

    def __str__(self):
        return self.name

class Landmark(models.Model):
    name = models.CharField(max_length=300)
    
    class Meta:
        verbose_name = ("Landmark")
        verbose_name_plural = ("(12) Landmark")

    def __str__(self):
        return self.name

class College(models.Model):
    name = models.CharField(max_length=300)
    
    class Meta:
        verbose_name = ("College")
        verbose_name_plural = ("(10) College")

    def __str__(self):
        return self.name
    
class Area(models.Model):
    name = models.CharField(max_length=500)
    iframe_map_link = models.CharField(max_length=1000)

    class Meta:
        verbose_name = ("Area")
        verbose_name_plural = ("(13) Area")

    def __str__(self):
        return self.name

class Property(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, blank=True, null=True, related_name='owner')
    property_type = models.ForeignKey(Property_Type,  on_delete=models.CASCADE, blank=True, null=True, related_name='property_type')
    popular_location = models.ForeignKey(Popular_Location,  on_delete=models.CASCADE, blank=True, null=True, related_name='popular_location')
    property_for = models.ForeignKey(Property_For, on_delete=models.CASCADE, blank=True, null=True, related_name='property_for')
    property_category = models.ForeignKey(Property_Category, on_delete=models.CASCADE, blank=True, null=True, related_name='property_category')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, blank=True, null=True)
    
    college = models.ForeignKey(College, on_delete=models.CASCADE, blank=True, null=True)
    landmark = models.ForeignKey(Landmark, on_delete=models.CASCADE, blank=True, null=True)

    name = models.CharField(max_length=200)
    address = models.CharField(max_length=400)
    price = models.IntegerField()
    deposite = models.IntegerField()
    total_room = models.IntegerField(default=0)
    avail_space_per_room = models.IntegerField(default=0)
    total_bathroom = models.IntegerField(default=0)
    total_space = models.IntegerField(default=0)
    available_space = models.IntegerField(default=0)
    description = models.TextField(default='Text')
    # iframe_map_link = models.CharField(max_length=900, default='Link')
    is_verify = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ("Property")
        verbose_name_plural = ("(1) Properties")

    def __str__(self):
        return self.name

    # def policies_data(self):
    #     return self.policies.split('.')

    def discount(self):
        dis = 30
        return int((self.price * dis)/100)


    def total_price(self):
        dis = 30
        num = int((self.price * dis)/100)
        total = (self.price - num) + self.deposite
        return total

    def link_map(self):
        map_link = self.area.iframe_map_link
        if map_link == 'Not Found':
            # cache.set('session_map_link', True)
            return
            # map_link = '<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d118147.68202122551!2d70.75125604248163!3d22.273630792892693!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3959c98ac71cdf0f%3A0x76dd15cfbe93ad3b!2sRajkot%2C%20Gujarat!5e0!3m2!1sen!2sin!4v1608634511359!5m2!1sen!2sin" width="600" height="450" frameborder="0" style="border:0;" allowfullscreen="" aria-hidden="false" tabindex="0"></iframe>'

        return (re.findall(r'"([^"]*)"', map_link))[0]

class Amenities(models.Model):
    name = models.CharField(max_length=500)
    icon = models.ImageField(upload_to='icon/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ("Amenities")
        verbose_name_plural = ("(8) Amenities")

    def __str__(self):
        return self.name


class Property_Wise_Amenities(models.Model):
    amenities = models.ForeignKey(
        Amenities, on_delete=models.CASCADE, blank=True, null=True)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ("Property Wise Amenities")
        verbose_name_plural = ("(2) Properties Wise Amenities")

    def __str__(self):
        return self.property.name


class Property_Image(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, blank=True, null=True)
    image = models.FileField(upload_to='property_images/', blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ("Property Images")
        verbose_name_plural = ("(4) Property Wise Images")

    def __str__(self):
        return f"{str(self.id)} = {self.property.owner.firstName} {self.property.owner.lastName} ({self.property.name})"

    def property_images(self):
        return mark_safe('<img src="{}" width="30%" height="30%" />'.format(self.image.url))
    

    property_images.allow_tags = True

class Policies(models.Model):
    policy = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ("Policies")
        verbose_name_plural = ("(9) Policies")
    
    def __str__(self):
        return self.policy

class Property_Wise_Policies(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, blank=True, null=True)
    policy = models.ForeignKey(Policies, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ("Property Wise Policies")
        verbose_name_plural = ("(3) Property Wise Policies")

    def __str__(self):
        return f"{self.property.name} ({self.policy.id})"


