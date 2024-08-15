from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import CustomUsers, Staffs, Students, AdminHOD
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'home.html')

def contact(request):
    return render(request, 'contact.html')

def loginUser(request):
    return render(request, 'login_page.html')

def doLogin(request):
    
    print("here")
    email_id = request.GET.get('email')
    password = request.GET.get('password')
    
    # user_type = request.GET.get('user_type')
    print(email_id)
    print(password)
    print(request.user)
    if not (email_id and password):
        messages.error(request, 'Please provide all the details !!')
        return render(request, 'login_page.html')
    
    user = CustomUsers.objects.filter(email=email_id, password=password).last()
    if not user:
        messages.error(request, 'Invalid Login Credentials!!')
        return render(request, 'login_page.html')
    
    login(request, user)
    print(request.user)
    
    if user.user_type == CustomUsers.ESTUDENT:
        return redirect('student_home/')
    elif user.user_type == CustomUsers.STAFF:
        return redirect('staff_home/')
    elif user.user_type == CustomUsers.HOD:
        return redirect('admin_home/')
    
    return render(request, 'home.html')

def registration(request):
    return render(request, 'registration.html')

def doRegistration(request):
    firts_name = request.GET.get('firts_name')
    last_name = request.GET.get('last_name')
    email_id = request.GET.get('email')
    password = request.GET.get('password')
    confirm_password = request.GET.get('confirmPassword')
    
    print(email_id)
    print(password)
    print(confirm_password)
    print(firts_name)
    print(last_name)
    if not (email_id and password and confirm_password):
        messages.error(request, 'Please provide all the details')
        return render(request, 'registration.html')
    
    if password != confirm_password:
        messages.error(request, 'Both password should match!!')
        return render(request, 'registration.html')
    
    is_user_exist = CustomUsers.objects.filter(email=email_id).exists()
    if is_user_exist:
        messages.error(request, 'User with this email id already exits. Please proceed to login!!')
        return render(request, 'registration.html')
    
    user_type = get_user_type_from_email(email_id)
    
    if user_type is None:
        messages.error(request, "Please use valid format for the email id: '<username>.<staff|student|hod>@<college_domain>'")
        return render(request, 'registration.html')
    
    username = email_id.split('@')[0].split('.')[0]
    
    if CustomUsers.objects.filter(username=username).exists():
        messages.error(request, 'Username already exists. Please choose another one!!')
        return render(request, 'registration.html')
    
    user = CustomUsers()
    user.username = username
    user.email = email_id
    user.password = password
    user.user_type = user_type
    user.first_name = firts_name
    user.last_name = last_name
    user.save()
    
    if user_type == CustomUsers.STAFF: 
        Staffs.objects.create(admin=user)
    elif user_type == CustomUsers.STUDENT:
        Students.objects.create(admin=user)
    elif user_type == CustomUsers.HOD:
        AdminHOD.objects.create(admin=user)
    return render(request, 'login_page.html')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

def get_user_type_from_email(email_id):
    
      """ 
    Returns CustomUser.user_type corresponding to the given email address 
    email_id should be in following format: 
    '<username>.<staff|student|hod>@<college_domain>' 
    eg.: 'abhishek.staff@jecrc.com' 
    """
    try: 
        email_id = email_id.split('@')[0]  # type: ignore
        email_user_type = email_id.split('.')[1] 
        return CustomUsers.EMAIL_TO_USER_TYPE_MAP[email_user_type] 
    except: 
        return None


    

    
    
