from django.contrib import admin
from .models import Property, Property_Type, Property_Image, Property_Wise_Amenities, Amenities, Popular_Location, Property_For,Policies, Property_Wise_Policies, Property_Category, Landmark, College, Area

# Register your models here.

class InLine_Property_wise_Amenities(admin.StackedInline):
    model = Property_Wise_Amenities
    extra = 0

class InLine_Property_wise_policies(admin.StackedInline):
    model = Property_Wise_Policies
    fields = (('property', 'policy'))
    extra = 0
    # max_num = 3

class InLine_Property_wise_Images(admin.StackedInline):
    model = Property_Image
    extra = 0
    fields = ('property', 'image', 'is_featured','property_images')
    list_display = ['property_images']
    readonly_fields = ('property_images',)

class PropertyAdmin(admin.ModelAdmin):
    inlines = [InLine_Property_wise_Amenities, InLine_Property_wise_policies, InLine_Property_wise_Images]
    fields = ('owner',('property_type', 'property_for', 'property_category'), ('name', 'address', 'popular_location', 'area', 'college', 'landmark'),('price', 'deposite'),('total_space', 'available_space', 'total_room','avail_space_per_room', 'total_bathroom'),('description'),('is_active', 'is_verify'))
    list_display_links = ('owner','name',)
    list_display = ('id','owner', 'name', 'price', 'is_active', 'is_verify', 'landmark')
    # list_editable = ('is_verify',)
    # list_per_page = 5
    search_fields = ('name','owner__phoneNumber', 'price')
    list_filter = ('is_verify', 'is_active', 'property_category', 'property_type','property_for')

    # filter_horizontal = ('name','price',)
    # fieldsets = ()


admin.site.register(Property, PropertyAdmin)
admin.site.register(Property_Type)
admin.site.register(Amenities)
admin.site.register(Property_Wise_Amenities)
admin.site.register(Popular_Location)
admin.site.register(Property_Image)
admin.site.register(Property_For)
admin.site.register(Policies)
admin.site.register(Property_Wise_Policies)
admin.site.register(Property_Category)
admin.site.register(Landmark)
admin.site.register(College)
admin.site.register(Area)