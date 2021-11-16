from django.urls import path
from .import views

urlpatterns = [
    path('', views.index_view, name="index"),
    path('about/', views.about_view, name="about"),
    path('contact/', views.contact_view, name="contact"),
    path('add_listing/', views.add_listing_view, name="add_listing"),
    path('check/',views.check_view,name="check"),
    path('property_left_sidebar/', views.property_left_sidebar_view, name="property_left_sidebar"),
    path('property_detail/<int:pk>/', views.property_detail_view, name="property_detail"),
    path('property_edit/', views.property_edit_view, name="property_edit"),
    
    path('dashboard/', views.dashboard_view, name="dashboard"),
    path('db_your_property/', views.db_your_property_view, name="db_your_property"),
    path('db_add_listing/', views.db_add_listing_view, name="db_add_listing"),
    path('db_my_profile/', views.db_my_profile_view, name="db_my_profile"),
    path('db_edit_profile/', views.db_edit_profile_view, name="db_edit_profile"),
    path('db_edit_your_property/<int:pk>/', views.db_edit_your_property_view, name="db_edit_your_property"),
    path('db_delete_your_property/<int:pk>/', views.db_delete_your_property_view, name="db_delete_your_property"),
    path('db_your_property_detail/<int:pk>/', views.db_your_property_detail_view, name="db_your_property_detail"),
]