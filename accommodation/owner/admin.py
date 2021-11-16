from django.contrib import admin
from .models import Owner
# from property.models import Property
# Register your models here.

# class InLine_Owner_wise_property(admin.StackedInline):
#     model = Property
#     extra = 0

class Owner_Admin(admin.ModelAdmin):
    # inlines = [InLine_Owner_wise_property]
    list_display = ('firstName', 'lastName', 'phoneNumber', 'address')
    search_fields = ('firstName', 'lastName', 'phoneNumber')

admin.site.register(Owner, Owner_Admin)