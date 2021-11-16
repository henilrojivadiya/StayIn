from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import cache_control
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView
from .models import Property, Property_Type, Property_For, Amenities, Property_Wise_Amenities, Popular_Location, Policies, Property_Image, Property_Wise_Policies, Property_Category, College, Landmark, Area
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import Property_Form, Property_Amenities, Property_Image_Form
from django.urls import reverse_lazy
from account.models import User
from owner.models import Owner
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from admin_panel.forms import Property_Form
import re
import mysql.connector

from django.core import serializers
from django.core.cache import cache
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.

def check_view(request):

    rooms = Property.objects.filter(is_verify=True, is_active=True) #.order_by('?')
    total_room_count = len(list(rooms))
    property_images = Property_Image.objects.values_list('property', flat=True)

    property_images = set(property_images)

    img_list = []
    for i in property_images:
        img = Property_Image.objects.filter(property=i)[:1]
        img_list.extend(list(img))

    # --------------POST request from rooms.html(Ajax)--------------
    if request.method == 'POST':

        # --------------Get Valuse from Ajax--------------
        property_type_query_var = request.POST.get('p_type_check')
        property_for_query_var = request.POST.get('p_for_check')
        p_category_check = request.POST.get('p_category_check')
        amenity_query_var = request.POST.get('amenity_check')
        search_area_var = request.POST.get('search_area')
        search_text_var = request.POST.get('fetch_search_text')
        availble_var = request.POST.get('availlabel')
        ddl_selected_data = request.POST.get('ddl_selected_data')
        price = request.POST.get('price').split('-')
        min_price_var = price[0].strip()
        max_price_var = price[1].strip()
        
        if min_price_var == '500' and max_price_var == '10000':
            min_max = False
        else:
            min_max = True


        # --------------Remove ',' from the values--------------
        property_type_query_var = property_type_query_var[:(len(property_type_query_var)-1)]
        property_for_query_var = property_for_query_var[:(len(property_for_query_var)-1)]
        amenity_query_var = amenity_query_var[:(len(amenity_query_var)-1)]
        p_category_check = p_category_check[:(len(p_category_check)-1)]

        search_text_landmark = Landmark.objects.filter(name__icontains = search_text_var)
        search_text_college = College.objects.filter(name__icontains = search_text_var)


        cache.delete('cache_property_type_checked')
        cache.set('cache_property_type_checked', property_type_query_var)
        print(cache.get('cache_property_type_checked'))

        cache.delete('cache_property_for_checked')
        cache.set('cache_property_for_checked', property_for_query_var)
        print(cache.get('cache_property_for_checked'))

        cache.delete('cache_property_amenities_checked')
        cache.set('cache_property_amenities_checked', amenity_query_var)
        print(cache.get('cache_property_amenities_checked'))

        cache.delete('cache_ddl_selected_data')
        cache.set('cache_ddl_selected_data', ddl_selected_data)
        print(cache.get('cache_ddl_selected_data'))

        # cache.delete('cache_search_text')
        # cache.set('cache_search_text', search_text_var)
        # print(cache.get('cache_search_text'))
        
        # --------------Query for Data Filtering in rooms.html page--------------
        query = 'SELECT * FROM properties.property_property'

        # --------------Logic for filter and fetch data from database--------------

        # ---------------Search-----------------------
        if(search_text_var != 'None' and len(search_area_var) == 0):
            if(len(property_type_query_var) != 0 or len(property_for_query_var) != 0 or len(search_text_var) != 0 and 'Where' not in query):
                query += ' Where '

            if(len(property_type_query_var) != 0 and 'Where' in query):
                query += ' property_type_id IN (' +property_type_query_var+') and '

            if(len(property_for_query_var) != 0 and len(property_type_query_var) == 0 and 'Where' in query):
                query += ' property_for_id IN (' +property_for_query_var+') and '

            if(len(property_for_query_var) != 0 and len(property_type_query_var) != 0 and 'Where' in query):
                query += ' property_for_id IN (' +property_for_query_var+') and '

            if(min_max == True and 'Where' in query ):
                query += 'price between '+min_price_var+' and '+max_price_var+' and '

            if(len(p_category_check) != 0 and len(property_for_query_var) == 0 and len(property_type_query_var) == 0):
                query += ' property_category_id IN ('+p_category_check+') and '
            
            if(len(p_category_check) != 0 and (len(property_for_query_var) != 0 or len(property_type_query_var) != 0)):
                query += ' property_category_id IN ('+p_category_check+') and '

            if(len(amenity_query_var) != 0 and 'Where' in query):
                query += ' id in (select `property_id` from properties.property_property_wise_amenities where `property_property_wise_amenities`.`amenities_id` in ('+amenity_query_var+')) and '

            if(len(search_text_landmark)!=0):
                if(len(search_text_var) != 0):
                    query += 'landmark_id in (SELECT id FROM properties.property_landmark where name = "' + \
                        search_text_var+'") and available_space >="'+availble_var+'" '

            if(len(search_text_college)!=0):
                if(len(search_text_var) != 0):
                    query += 'college_id in (SELECT id FROM properties.property_college where name = "' + \
                        search_text_var+'") and available_space >="'+availble_var+'" '
        # -----------------------popular-----------------------
        # if(len(search_area_var) != 0):
        #     if(len(property_type_query_var) != 0 or len(property_for_query_var) != 0 or len(search_area_var) != 0 and 'where' not in query):
        #         query += ' Where '
        #     if(len(property_type_query_var) != 0 and 'Where' in query):
        #         query += ' property_type_id IN (' + \
        #             property_type_query_var+') and '
        #     if(len(property_for_query_var) != 0 and len(property_type_query_var) == 0 and 'Where' in query):
        #         query += ' property_for_id IN (' + \
        #             property_for_query_var+') and '
        #     if(len(property_for_query_var) != 0 and len(property_type_query_var) != 0 and 'Where' in query):
        #         query += ' property_for_id IN (' + \
        #             property_for_query_var+') and '
            # if(len(search_area_var) != 0 and min_max == True):
            #     query += ' price between '+min_price_var+' and '+max_price_var+' and '

            # if(len(amenity_query_var) != 0 and 'Where' in query):
            #     query += ' id in (select `property_id` from properties.property_property_wise_amenities where `property_property_wise_amenities`.`amenities_id` in ('+amenity_query_var+')) and '
            # if(len(search_area_var) != 0):
            #     query += 'popular_location_id in (SELECT `property_popular_location`.`id` FROM properties.property_popular_location where `property_popular_location`.`name` = "'+search_area_var+'")'

        # -----------------------price-----------------------
        if(min_max == True and len(search_area_var) == 0 and search_text_var == 'None'):

            if(min_max == True and 'Where' not in query):
                query += ' Where '
            if(len(property_type_query_var) != 0):
                query += 'property_type_id IN ('+property_type_query_var+') and '

            if(len(property_for_query_var) != 0 and len(property_type_query_var) != 0):
                query += 'property_for_id IN ('+property_for_query_var+') and '

            if(len(property_for_query_var) != 0 and len(property_type_query_var) == 0):
                query += 'property_for_id IN ('+property_for_query_var+') and '

            if(len(amenity_query_var) != 0 and 'Where' in query):
                query += 'id in (select `property_id` from properties.property_property_wise_amenities where `property_property_wise_amenities`.`amenities_id` in ('+amenity_query_var+')) and '

            if(min_price_var != 0 or max_price_var !=10000):
                query += ' price between '+min_price_var+' and '+max_price_var+''

        # -----------------------testing-----------------------
        if(len(search_area_var) == 0 and search_text_var == 'None' and min_max == False):
            if(len(property_type_query_var) != 0 or len(property_for_query_var) != 0 or len(p_category_check) != 0 and 'Where' not in query):
                query += ' Where '
            if(len(property_type_query_var) != 0):
                query += 'property_type_id IN ('+property_type_query_var+') '
            if(len(property_for_query_var) != 0 and len(property_type_query_var) != 0):
                query += ' and property_for_id IN ('+property_for_query_var+')'
            if(len(property_for_query_var) != 0 and len(property_type_query_var) == 0):
                query += ' property_for_id IN ('+property_for_query_var+')'
            # if(len(property_for_query_var) != 0 and len(property_type_query_var) == 0):
            #     query += 'property_for_id IN ('+property_for_query_var+') and'

            if(len(p_category_check) != 0 and len(property_for_query_var) == 0 and len(property_type_query_var) == 0):
                query += ' property_category_id IN ('+p_category_check+') '
            
            if(len(p_category_check) != 0 and (len(property_for_query_var) != 0 or len(property_type_query_var) != 0)):
                query += ' and property_category_id IN ('+p_category_check+') '

            if(len(amenity_query_var) != 0 and 'Where' in query):
                query += ' and id in (select `property_id` from properties.property_property_wise_amenities where `property_property_wise_amenities`.`amenities_id` in ('+amenity_query_var+'))'
            elif(len(amenity_query_var) != 0):
                query += ' where id in (select `property_id` from properties.property_property_wise_amenities where `property_property_wise_amenities`.`amenities_id` in ('+amenity_query_var+'))'

        # --------------Get queryset using raw query--------------
        
        if ddl_selected_data == '0':
            query += ' ORDER BY `property_property`.`created_at` DESC'
        if ddl_selected_data == '1':
            query += ' ORDER BY `property_property`.`created_at` ASC'
        if ddl_selected_data == '2':
            query += ' ORDER BY `property_property`.`price` ASC'
        if ddl_selected_data == '3':
            query += ' ORDER BY `property_property`.`price` DESC'

        print('')
        print(query)
        print('')

        data = Property.objects.raw(query)
        search_room_count = len(list(data))

        cache.set('cache_check_data', list(data))
        print(cache.get('cache_check_data'))
        print('')
                
        paginator = Paginator(data,6)
        page_number = request.GET.get('page', 1)
        try:
            pages = paginator.page(page_number)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)

        # --------------Passing Context into fronuend--------------
        context = {
            'rooms': pages,
            'property_images': img_list,
            # 'page_obj' : pages,
            'total_room_count' : total_room_count,
            'search_room_count' : search_room_count,
        }

        # --------------Render Data on check page--------------
        return render(request, 'check.html', context)

def index_view(request):

    property_types = Property_Type.objects.all()
    pro_tuple = tuple(property_types)
    property_for = Property_For.objects.all()

    index = True

    property_images = Property_Image.objects.filter(is_featured=True)

    properties_count = [len((list(Property.objects.filter(property_type=i)))) for i in property_types ]
    properties_count_tuple = tuple(properties_count)
    property_types = dict(zip(pro_tuple,properties_count_tuple))

    recent_properties = Property.objects.all().order_by('-created_at')[:3]
    # print(recent_properties)

    try:
        if request.method == 'POST':
            firstName = request.POST.get('firstName')
            lastName =  request.POST.get('lastName')
            address =   request.POST.get('address')
            property_type =   request.POST.get('property_type')
            property_for =   request.POST.get('property_for')
            
            request.session['session_property_type'] = property_type
            request.session['session_property_for'] = property_for

            user = request.user
            if user.is_owner == False:
                user.first_name = firstName
                user.last_name = lastName
                user.is_owner = True
                user.save()
        
                try:
                    owner = Owner(firstName=firstName, lastName=lastName, phoneNumber=user.phone_number, email=user.email, address=address)
                    owner.save()
                except:
                    owner = Owner.objects.get(email=user.email)
                    owner.firstName = firstName
                    owner.lastName = lastName
                    owner.address = address
                    owner.save()

            return redirect('add_listing')
    except:
        return redirect('login')


    if 'term' in request.GET:
        query_original = request.GET.get('term')
        queryset = Landmark.objects.filter(name__icontains=query_original) or College.objects.filter(name__icontains=query_original) 
        search_list = []
        search_list += [i.name for i in queryset]
        return JsonResponse(search_list[:10], safe=False)

    context = {
        'property_types' : property_types,
        'properties_count' : properties_count,
        'recent_properties' : recent_properties,
        'property_images' : property_images,
        'property_for' : property_for,
        'index' : index,
    }
    return render(request, 'index.html', context)

def about_view(request):
    return render(request, 'about.html', {})

# def send_mail_view(request):
#     # form = SubscribeForm()
#     if request.method == 'POST':
#         # form = SubscribeForm(request.POST)
#         # if form.is_valid():
#         subject = 'Code Band'
#         message = 'Sending Email through Gmail'
#         recipient = form.cleaned_data.get('email')
#         send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
#         messages.success(request, 'Success!')
#         return redirect('index')

#     return render(request, 'subscriptions/home.html', {'form': form})

def contact_view(request):

    if request.method == 'POST':
        name =  request.POST.get('name')
        comment =   request.POST.get('comment')

        print(name)
        print(comment)

        subject = str(name)
        message = str(comment)
        recipient = request.POST.get('email')
        
        send_mail(subject, message, recipient, [settings.EMAIL_HOST_USER], fail_silently=False)

        return redirect('index')

    return render(request, 'contact.html')

@login_required
def add_listing_view(request):
    get_property_type = ''
    property_type = Property_Type.objects.all()
    property_for = Property_For.objects.all()
    amenities = Amenities.objects.all()
    policies = Policies.objects.all()
    colleges = College.objects.all().order_by('name')
    landmarks = Landmark.objects.all().order_by('name')
    areas = Area.objects.all().order_by('name')

    
    if 'session_property_type' in request.session:
        get_property_type = request.session.get('session_property_type')
        # print(f'get_property_type : {get_property_type}')
        get_property_type = int(get_property_type)
    
    if 'session_property_for' in request.session:
        get_property_for = request.session.get('session_property_for')
        # print(f'get_property_for : {get_property_for}')
        # get_property_for = int(get_property_for)
        

    if request.method == 'POST':
        form = Property_Form(request.POST)
        name = request.POST.get('name')
        address = request.POST.get('address')
        price = request.POST.get('price')
        deposite = request.POST.get('deposite')
        total_room = request.POST.get('total_bedrooms')
        avail_space_per_room = request.POST.get('avail_space_per_room')
        total_space = request.POST.get('total_space')
        total_bathroom = request.POST.get('total_bathroom')
        available_space = request.POST.get('available_space')
        # popular_location = request.POST.get('popular_location')
        property_category = request.POST.get('property_category')
        # property_type = request.POST.get('property_type')
        # property_for = request.POST.get('property_for')
        property_images = request.FILES.getlist('property_images')
        property_main_image = request.FILES.getlist('property_main_image')
        amenity_id = request.POST.get('amenity_check')
        amenity_id = amenity_id[:len(amenity_id)-1]
        policy_id = request.POST.get('policies_check')
        policy_id = policy_id[:len(policy_id)-1]
        clg_name = request.POST.get('clg_name')
        landmark = request.POST.get('landmark')
        area = request.POST.get('area')

        # popular_location = Popular_Location.objects.get(id=popular_location)
        property_type = Property_Type.objects.get(id=get_property_type)
        property_for = Property_For.objects.get(id=get_property_for)
        college = College.objects.get(name=clg_name)
        landmark = Landmark.objects.get(name=landmark)
        area = Area.objects.get(name=area)
        

        print(f'total_room : {total_room}')
        print(f'avail_space_per_room : {avail_space_per_room}')
        print(f'total_space : {total_space}')
        print(f'total_bathroom : {total_bathroom}')
        print(f'available_space : {available_space}')

        try:
            property_category = Property_Category.objects.get(id=property_category)
        except:
            pass

        same_property_add = False
        try:
            same_property_add = Property.objects.get(address=address)
            same_property_add = True
        except ObjectDoesNotExist:
            pass
    
        if same_property_add == False:
            user = request.user
            owner = Owner.objects.get(phoneNumber=user.phone_number, email=user.email)
            
            if total_room == None and avail_space_per_room == None and total_space == None and total_bathroom == None and available_space == None:
                property_obj = Property(owner=owner, property_type=property_type, property_for=property_for, name=name, address=address, price=price, deposite=deposite, landmark=landmark, college=college, area=area)
            else:
                property_obj = Property(owner=owner, property_type=property_type, property_category=property_category, property_for=property_for, name=name, address=address, price=price, deposite=deposite, total_room=total_room, avail_space_per_room=avail_space_per_room,total_space=total_space, available_space=available_space, total_bathroom=total_bathroom, landmark=landmark, college=college, area=area)

            property_obj.is_active = False
            property_obj.save()
            form = Property_Form()

            property_id = Property.objects.get(address=address, property_type=get_property_type, property_for=get_property_for)

            if property_id:
                if amenity_id != '':
                    new = amenity_id.split(",")
                    amenity_list = [int(i) for i in new]
                    for i in amenity_list:
                        a = Amenities.objects.get(id=i)
                        amenity = Property_Wise_Amenities(
                            property=property_id, amenities=a)
                        amenity.save()

                if policy_id != '':
                    new_policy = policy_id.split(",")
                    policy_list = [int(i) for i in new_policy]
                    for i in policy_list:
                        a = Policies.objects.get(id=i)
                        policies_of_property = Property_Wise_Policies(
                            property=property_id, policy=a)
                        policies_of_property.save()

                for i in property_main_image:
                    main_image = Property_Image(property=property_id, image=i)
                    main_image.is_featured=True
                    main_image.save()

                for i in property_images:
                    images = Property_Image(property=property_id, image=i)
                    images.save()

            request.session['add_listing'] = True
        
            return redirect('dashboard')
        
        form = Property_Form()
        request.session['same_address'] = True
        return redirect('dashboard')
        # else:
        #     pass
    else:
        form = Property_Form()

    context = {
        'property_type' : property_type,
        'property_for' : property_for,
        'amenities': amenities,
        'policies': policies,
        'form': form,
        'get_property_type' : get_property_type,
        'details_range' : range(1,7),
        'colleges' : colleges,
        'landmarks' : landmarks,
        'areas' : areas,
    }
    return render(request, 'add_listing.html', context)

def property_left_sidebar_view(request):

    if 'term' in request.GET:
        query_original = request.GET.get('term')
        queryset = Landmark.objects.filter(name__icontains=query_original) or College.objects.filter(name__icontains=query_original) 
        search_list = []
        search_list += [i.name for i in queryset]
        return JsonResponse(search_list[:10], safe=False)

    property_type_id = '0'
    if request.method == 'POST':
        property_type_id = request.POST.get('property_type_id')
        rooms = Property.objects.filter(property_type=property_type_id)
        cache.set('cache_property_type_id', property_type_id)
        cache.delete('cache_index_search_text')
        
    else:
        rooms = Property.objects.filter(is_verify=True, is_active=True)

    
    if 'cache_property_type_id' in cache:
        property_type_id = cache.get('cache_property_type_id')
        rooms = Property.objects.filter(property_type=property_type_id)


    property_type = Property_Type.objects.all()
    property_for = Property_For.objects.all()
    amenities = Amenities.objects.all()
    popular_location = Popular_Location.objects.all()
    property_category = Property_Category.objects.all()
    property_images = Property_Image.objects.filter(is_featured=True)

    property_type_checked = []
    if 'cache_property_type_checked' in cache:
        property_type_checked = cache.get('cache_property_type_checked')
        property_type_checked = [int(i) for i in property_type_checked if i != ',']
    
    property_for_checked = []
    if 'cache_property_for_checked' in cache:
        property_for_checked = cache.get('cache_property_for_checked')
        property_for_checked = [int(i) for i in property_for_checked if i != ',']

    property_amenities_checked = []
    if 'cache_property_amenities_checked' in cache:
        property_amenities_checked = cache.get('cache_property_amenities_checked')
        property_amenities_checked = [int(i) for i in property_amenities_checked if i != ',']

    cache_ddl_selected_data = []
    if 'cache_ddl_selected_data' in cache:
        cache_ddl_selected_data = cache.get('cache_ddl_selected_data')
        cache_ddl_selected_data = [int(i) for i in cache_ddl_selected_data if i != ',']
    

    # --------------Get values from from end--------------
    query = request.GET.get('query')
    avail_count = request.GET.get('person_count')

    
    if query != None:
        cache.set('cache_index_search_text', query)
        request.session['session_index_search_text'] = query
        property_type_id = 0
    
    if 'cache_index_search_text' in cache:
        query = cache.get('cache_index_search_text')
        # print(f'query : {query}')

    # --------------Loginc for seraching--------------

    try:
        if query:
            search_result_college = College.objects.filter(name__icontains=query)
            search_result_landmark = Landmark.objects.filter(name__icontains=query)

            if len(search_result_landmark) != 0:
                for i in list(search_result_landmark):
                    query = i
                if avail_count:
                    q = 'SELECT * FROM properties.property_property where landmark_id in (SELECT id FROM properties.property_landmark where name = "{0}" )'.format(query) + ' and available_space >= "'+avail_count+'"'
                else:
                    q = 'SELECT * FROM properties.property_property where landmark_id in (SELECT id FROM properties.property_landmark where name = "{0}" )'.format(query)

            if len(search_result_college) != 0:
                for i in list(search_result_college):
                    query = i
                if avail_count:
                    q = 'SELECT * FROM properties.property_property where college_id in (SELECT id FROM properties.property_college where name = "{0}" )'.format(query) + ' and available_space >= "'+avail_count+'"'
                else:
                    q = 'SELECT * FROM properties.property_property where college_id in (SELECT id FROM properties.property_college where name = "{0}" )'.format(query)
                
            search_result = Property.objects.raw(q)
            rooms = search_result
    except:

        rooms = []

    if 'cache_check_data' in cache and len(property_type_checked) != 0 or len(property_for_checked) != 0 or len(property_amenities_checked) != 0 or len(cache_ddl_selected_data) != 0:
        rooms = cache.get('cache_check_data')

    print(rooms)

    total_room_count = len(list(rooms))
    search_room_count = len(list(rooms)) 

    paginator = Paginator(rooms,6)
    page_number = request.GET.get('page', 1)

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)


    # --------------Pass data into fromt end--------------
    context = {'rooms': page,
               'property_type': property_type,
               'property_for': property_for,
               'property_category' : property_category,
               'amenities': amenities,
               'popular_location': popular_location,
               'property_images': property_images,
               'query': query,
               'avail_count': avail_count,
            #    'page_obj': page,
               'total_room_count' : total_room_count,
               'search_room_count' : search_room_count,
               'property_type_id' : property_type_id,
               'property_type_checked' : property_type_checked,
               'property_for_checked' : property_for_checked,
               'amenity_checked' : property_amenities_checked,
               'cache_ddl_selected_data' : cache_ddl_selected_data,
               }

    return render(request, 'property_left_sidebar.html', context)

@login_required
def property_detail_view(request, pk):
    # --------------Get data useing primery key--------------
    room = Property.objects.get(id=pk)
    property_wise_amenities = Property_Wise_Amenities.objects.filter(property=pk)
    property_wise_policies = Property_Wise_Policies.objects.filter(property=pk)    
    property_images = Property_Image.objects.filter(property=pk)
    

    room_landmark = room.landmark
    landmarks_wise_colleges = Property.objects.filter(landmark=room_landmark)
    landmarks_wise_colleges = [i.college for i in landmarks_wise_colleges]
    landmarks_wise_colleges = list(set(landmarks_wise_colleges))
    # print(landmarks_wise_colleges)

    user = User.objects.get(email=room.owner.email)
    print(user)
    profile_pic = user.profile_pic
    print(profile_pic)
    # --------------Get values from front end--------------
    price = request.POST.get('price')

    # --------------Fetch data from database--------------
    similar = Property.objects.filter(price=price).order_by('?')
    # for i in list(similar):
    #     print(i)
    # print(f'similar = {similar}')

    featured_images = [Property_Image.objects.filter(property=i, is_featured=True)[0] for i in similar]
    # print(f'featured_images : {featured_images}')

    # --------------Pass data into front end--------------
    context = {
        'room': room,
        'similar': similar[:3],
        'property_wise_amenities': property_wise_amenities,
        'property_images': property_images,
        'featured_images' : featured_images,
        'property_wise_policies':property_wise_policies,
        'landmarks_wise_colleges' : landmarks_wise_colleges,
        'profile_pic' : profile_pic,
    }
    return render(request, 'property_detail_page.html', context)

@login_required
def property_edit_view(request):
    return render(request, 'property_edit_page.html', {})

@login_required
def dashboard_view(request):

    property_types = Property_Type.objects.all()
    property_for = Property_For.objects.all()    

    user = request.user
    owner = Owner.objects.get(email=user.email)

    total_pro = Property.objects.filter(owner=owner)
    request.session['owner_wise_total_property'] = total_pro = len(list(total_pro))

    request_pending = Property.objects.filter(owner=owner, is_verify=False).order_by('created_at')
    deactiveted = Property.objects.filter(owner=owner, is_active=False)
    properties = request_pending.union(deactiveted).order_by('-created_at')
    property_images = [Property_Image.objects.filter(property=i, is_featured=True)[0] for i in properties]

    properties_count = len(list(properties))
    request_pending_count = len(list(request_pending))
    
    deactivated_property = Property.objects.filter(owner=owner, is_active=False)
    deactivated_property_count = len(list(deactivated_property))
    activated_property = Property.objects.filter(owner=owner, is_verify=True)
    activated_property_count = len(list(activated_property))

    add_listing = False
    if 'add_listing' in request.session:
        add_listing = True
        del request.session['add_listing']
    
    same_property_address = False
    if 'same_address' in request.session:
        same_property_address = True
        del request.session['same_address']

    context = {
        'request_pending_count' : request_pending_count,
        'properties_count' : properties_count,
        'deactivated_property_count' : deactivated_property_count,
        'activated_property_count' : activated_property_count,
        'request_pending' : properties,
        'property_images' : property_images,
        'add_listing' : add_listing,
        'same_property_address' : same_property_address,
        'property_types':property_types,
        'property_for':property_for,
    }
    return render(request, 'db.html', context)

@login_required
def db_your_property_view(request):

    property_types = Property_Type.objects.all()
    property_for = Property_For.objects.all()    

    change_available_space_count = False
    available_space_count = -1
    updated_property_name = ''
    if request.method == 'POST':
        available_space_count = request.POST.get('available_space_count')    
        property_id = request.POST.get('pro_id')
        data = Property.objects.get(id=property_id)
        data.available_space = available_space_count
        updated_property_name = data.name
        print(updated_property_name)

        if(int(available_space_count) == 0):
            data.is_active = False
        else:
            data.is_active = True         
        data.save()

        change_available_space_count = True
        
    property_updated = False
    if 'property_updated' in request.session:
        property_updated = True
        del request.session['property_updated']
        
    
    if 'updated_property_name' in request.session:
        updated_property_name = request.session.get('updated_property_name')
        del request.session['updated_property_name']

    property_deleted = False
    if 'property_deleted' in request.session:
        property_deleted = True
        del request.session['property_deleted']
    
    # property_deactivated = False
    # if 'session_property_deactivated' in request.session:
    #     property_deleted = True
    #     del request.session['session_property_deactivated']

    user = request.user
    owner = Owner.objects.get(email=user.email)
    properties = Property.objects.filter(owner=owner).order_by('-created_at')

    property_images = [Property_Image.objects.filter(property=i, is_featured=True)[0] for i in properties]

    total_pro = Property.objects.filter(owner=owner)
    request.session['owner_wise_total_property'] = total_pro = len(list(total_pro))
    # properties_id_list = [i.id for i in properties]
    # property_images = []
    # for i in properties_id_list:
    #     property_of_img = Property_Image.objects.filter(property=i, is_featured=True)
    #     property_images.extend(property_of_img)

    context = {
        'properties': properties,
        'property_images': property_images,
        'available_space_count' : available_space_count,
        'change_available_space_count' : change_available_space_count,
        'property_updated' : property_updated,
        'property_deleted' : property_deleted,
        'updated_property_name' : updated_property_name,
        'property_types':property_types,
        'property_for':property_for,
        # 'property_deactivated' : property_deactivated,
    }
    return render(request, 'db_your_property.html', context)

@login_required
def db_add_listing_view(request):

    property_types = Property_Type.objects.all()
    property_for = Property_For.objects.all() 

    amenities = Amenities.objects.all()
    policies = Policies.objects.all()

    form = Property_Form()

    context = {
        'form': form,
        'amenities': amenities,
        'policies': policies,
        'property_types':property_types,
        'property_for':property_for,
    }
    return render(request, 'db_add_listing.html', context)

@login_required
def db_my_profile_view(request):

    property_types = Property_Type.objects.all()
    property_for = Property_For.objects.all() 

    user = request.user
    # name = user.first_name[0] + user.last_name[0]
    owner = 0
    if user.is_owner == True:
        owner = Owner.objects.get(email=user.email)

    context = {
        'owner' : owner,
        'property_types':property_types,
        'property_for':property_for,
        # 'name' : name
    }
    return render(request, 'db_my_profile.html', context)

@login_required
def db_edit_profile_view(request):
    property_types = Property_Type.objects.all()
    property_for = Property_For.objects.all() 

    user = request.user
    owner = 0
    if user.is_owner == True:
        owner = Owner.objects.get(email=user.email)

    if request.method == 'POST':
        first_name = request.POST.get('first_name').replace(' ','').strip()
        last_name = request.POST.get('last_name').replace(' ','').strip()
        phone_number = " ".join(request.POST.get('phone_number').split())
        email = " ".join(request.POST.get('email').split())
        user_id = request.POST.get('user_id')
        user_is_owner = request.POST.get('user_is_owner')
        profile_pic = request.FILES.getlist('profile_image')

        print(profile_pic)

        if user.is_owner == True:
            address = " ".join(request.POST.get('address').split())

        user = User.objects.get(id=user_id)
        user_email = User.objects.get(id=user_id).email

        if user_is_owner == 'True':
            owner = Owner.objects.get(email=user_email)
            owner.firstName = first_name
            owner.lastName = last_name
            owner.phoneNumber = phone_number
            owner.email = email
            if address != 0:
                owner.address = address
            owner.save()

        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        user.email = email
        for i in profile_pic:
            user.profile_pic = i
        user.save()

        return redirect('db_my_profile')


    context = {
        'owner' : owner,
        'property_types':property_types,
        'property_for':property_for,
    }
    return render(request, 'db_edit_profile.html', context)

@login_required
def db_your_property_detail_view(request, pk):
    property_types = Property_Type.objects.all()
    property_for = Property_For.objects.all() 
    user_email_loop = request.user
    user_email_loop = user_email_loop.email

    try:
        property_id_loop = Property.objects.get(id=pk)
        owner_loop = property_id_loop.owner
        owner_id_loop = property_id_loop.owner.id
        owner_email_loop = owner_loop.email
        property_id_loop = property_id_loop.owner.id

        property_wise_policies = Property_Wise_Policies.objects.filter(property=pk)

        property_images = Property_Image.objects.filter(property=pk)

        if request.method == 'POST':
            deactive_property = Property.objects.get(id=pk)
            if deactive_property.is_active == True:
                deactive_property.is_active = False
            else:
                deactive_property.is_active = True

            deactive_property.save()

            # request.session['session_property_deactivated'] = True
            # request.session['session_property_deactivated_name'] = deactive_property.name
            return redirect('db_your_property')

        pro = Property.objects.get(id=pk)
        property_wise_amenities = Property_Wise_Amenities.objects.filter(property=pk)
        

        context = {
            'property': pro,
            'property_wise_amenities': property_wise_amenities,
            'property_wise_policies' : property_wise_policies,
            'owner_email_loop': owner_email_loop,
            'user_email_loop': user_email_loop,
            'property_id_loop': property_id_loop,
            'owner_id_loop': owner_id_loop,
            'property_images': property_images,
            'property_types':property_types,
            'property_for':property_for,
        }
        return render(request, 'db_your_property_detail.html', context)
    except:
        return redirect('index')

@login_required
def db_edit_your_property_view(request, pk):
    property_types = Property_Type.objects.all()
    property_for = Property_For.objects.all() 

    user_email_loop = request.user
    user_email_loop = user_email_loop.email

    property_id_loop = Property.objects.get(id=pk)
    owner_loop = property_id_loop.owner
    owner_id_loop = property_id_loop.owner.id
    owner_email_loop = owner_loop.email
    property_id_loop = property_id_loop.owner.id

    check_property_type = Property.objects.get(id=pk).property_type.id

    total_space = Property.objects.get(id=pk).total_space
    available_space = Property.objects.get(id=pk).available_space
    total_room = Property.objects.get(id=pk).total_room
    total_bathroom = Property.objects.get(id=pk).total_bathroom
    avail_space_per_room = Property.objects.get(id=pk).avail_space_per_room
    
    request.session['session_total_space'] = total_space
    request.session['session_available_space'] = available_space
    request.session['session_total_room'] = total_room
    request.session['session_avail_space_per_room'] = avail_space_per_room
    request.session['session_total_bathroom'] = total_bathroom

    amenities = Amenities.objects.all()
    policies = Policies.objects.all()

    property_wise_amenities = Property_Wise_Amenities.objects.filter(property=pk)
    property_wise_amenities = [i.amenities.id for i in property_wise_amenities]
    
    property_wise_policies = Property_Wise_Policies.objects.filter(property=pk)
    property_wise_policies = [i.policy.id for i in property_wise_policies]    

    property_images = Property_Image.objects.filter(property=pk, is_featured=False)
    main_property_images = Property_Image.objects.filter(property=pk, is_featured=True)

    if request.method == 'POST':
        data = Property.objects.get(id=pk)
        form = Property_Form(request.POST, instance=data)
    
        is_active = data.is_active
        is_verify = data.is_verify

        total_room = request.POST.get('total_room')
        avail_space_per_room = request.POST.get('avail_space_per_room')
        total_space = request.POST.get('total_space')
        total_bathroom = request.POST.get('total_bathroom')
        available_space = request.POST.get('available_space')
              
        data.total_room = total_room
        data.avail_space_per_room = avail_space_per_room
        data.total_space = total_space
        data.total_bathroom = total_bathroom
        data.available_space = available_space
        data.save()

        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            property_type = form.cleaned_data['property_type']
            property_for = form.cleaned_data['property_for']
            property_category = form.cleaned_data['property_category']
            
            amenity_id = request.POST.get('amenity_check')
            amenity_id = amenity_id[:len(amenity_id)-1]
            policy_id = request.POST.get('policies_check')
            policy_id = policy_id[:len(policy_id)-1]

            property_images = request.FILES.getlist('property_images')
            property_main_image = request.FILES.getlist('property_main_image')


            property_images_delete = request.POST.get('images_check')
            property_images_delete = property_images_delete[:len(property_images_delete)-1]

            user = request.user
            owner = Owner.objects.get(email=user)
            data.owner = owner
            # data.policies = policy_id
            if is_active == True:
                data.is_active = True
            if is_verify == True:
                data.is_verify = True
            data.save()
            form.save()

            property_id = Property.objects.get(address=address, property_type=property_type, property_for=property_for)
            property_wise_amenity_delete = Property_Wise_Amenities.objects.filter(property=property_id)
            property_wise_amenity_delete.delete()

            property_wise_policies_delete = Property_Wise_Policies.objects.filter(property=property_id)
            property_wise_policies_delete.delete()

            if property_id:
                if amenity_id != '':
                    new = amenity_id.split(",")
                    amenity_list = [int(i) for i in new]
                    for i in amenity_list:
                        a = Amenities.objects.get(id=i)
                        amenity = Property_Wise_Amenities(
                            property=property_id, amenities=a)
                        amenity.save()
                
                if policy_id != '':
                    policy_new = policy_id.split(",")
                    policies_list = [int(i) for i in policy_new]
                    for i in policies_list:
                        a = Policies.objects.get(id=i)
                        policy = Property_Wise_Policies(property=property_id, policy=a)
                        policy.save()

                if property_main_image:
                    property_of_image = Property_Image.objects.filter(property=property_id, is_featured=True)
                    property_of_image.delete()
                    for i in property_main_image:
                        main_image = Property_Image(property=property_id, image=i)
                        main_image.is_featured = True
                        main_image.save()

                if property_images_delete:
                    property_images_delete = property_images_delete.split(',')

                    for i in property_images_delete:
                        property_images_delete = Property_Image.objects.get(image=i)
                        property_images_delete.delete()

                if property_images:
                    for i in property_images:
                        images = Property_Image(property=property_id, image=i)
                        images.save()

            form = Property_Form()

            request.session['property_updated'] = True
            request.session['updated_property_name'] = name
            return redirect('db_your_property')

    else:
        data = Property.objects.get(id=pk)
        form = Property_Form(instance=data)

    context = {
        'form': form,
        'amenities': amenities,
        'policies': policies,
        'property_wise_amenities': property_wise_amenities,
        'property_wise_policies' : property_wise_policies,
        'owner_email_loop': owner_email_loop,
        'user_email_loop': user_email_loop,
        'property_id_loop': property_id_loop,
        'owner_id_loop': owner_id_loop,
        'property_images': property_images,
        'main_property_images': main_property_images,
        # 'policy_of_property': policy_of_property,
        # 'policies_new':policies_new,
        'details_range' : range(1,7),
        'check_property_type' : check_property_type,
        'property_types':property_types,
        'property_for':property_for,
    }
    return render(request, 'db_edit_your_property.html', context)

@login_required
def db_delete_your_property_view(request, pk):
    data = Property.objects.get(id=pk)
    data.delete()

    request.session['property_deleted'] = True

    return redirect('db_your_property')

def error_404_view(request, exception):
    return render(request, 'error_404_page.html')


