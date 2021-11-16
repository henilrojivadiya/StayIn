from django import forms
from .models import Property, Property_Wise_Amenities, Property_Image

class Property_Form(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['owner', 'property_type', 'property_for', 'property_category', 'name', 'address', 'price', 'deposite', 'total_space', 'total_room', 'total_bathroom', 'avail_space_per_room', 'available_space', 'description','is_active','is_verify']

        widgets = {
            'owner' : forms.Select(attrs={'class': 'form-control', 'id': 'ownerID'}),
            'property_type' : forms.Select(attrs={'class': 'form-control'}),
            # 'popular_location' : forms.Select(attrs={'class': 'form-control'}),
            'property_for' : forms.Select(attrs={'class': 'form-control'}),
            'property_category' : forms.Select(attrs={'class': 'form-control'}),
            'name' : forms.TextInput(attrs={'class': 'form-control'}),
            'address' : forms.TextInput(attrs={'class': 'form-control' }),
            'price' : forms.NumberInput(attrs={'class': 'form-control'}),
            'deposite' : forms.NumberInput(attrs={'class': 'form-control'}),
            'total_room' : forms.NumberInput(attrs={'class': 'form-control'}),
            'avail_space_per_room' : forms.NumberInput(attrs={'class': 'form-control'}),
            'total_bathroom' : forms.NumberInput(attrs={'class': 'form-control'}),
            'total_space' : forms.NumberInput(attrs={'class': 'form-control'}),
            'available_space' : forms.NumberInput(attrs={'class': 'form-control'}),
            # 'policies' : forms.Textarea(attrs={'class': 'form-control'}),
            'description' : forms.Textarea(attrs={'class': 'form-control'}),            
            # 'iframe_map_link' : forms.TextInput(attrs={'class': 'form-control'}),
        }

class Property_Amenities(forms.ModelForm):
    class Meta:
        model = Property_Wise_Amenities
        fields = ['property']

        widgets = {
            'property' : forms.Select(attrs={'class':'form-control'}),          
        }

class Property_Image_Form(forms.ModelForm):
    class Meta:
        model = Property_Image
        fields = ['property', 'image']

