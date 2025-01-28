from django.shortcuts import render,redirect
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from tutionapp.models import Teacher
from tutionapp.models import Student
from tutionapp.models import CustomUser
from django.contrib import messages
from django.contrib.auth import login,authenticate
from django.contrib import auth
from django.db.models import Q
import random
from django.core.mail import send_mail
from django.conf import settings

from .import views

# Create your views here.

def home(request):
    return render(request,'home.html')

def loginpage(request):
    return render(request,'login.html')

def tsignup(request):
    return render(request,'tsignup.html')

def stsignup(request):
    return render(request,'stsignup.html')

def adminhome(request):
    return render(request,'admin_home.html')

def teacherhome(request):
    return render(request,'teacher_home.html')

def studenthome(request):
    return render(request,'student_home.html')


def add_techer(request):
    if request.method == 'POST':
        first_name= request.POST['first_name']
        last_name= request.POST['last_name']
        username= request.POST['username']
        age= request.POST['age']
        email= request.POST['email']
        contact= request.POST['contact']
        user_type= request.POST['text']
        sel= request.POST['sel']
        image= request.FILES.get('file')

        # checking username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.success(request, 'Username already exists; Please choose another.')
            return redirect('tsignup')
        
        # email checking
        if CustomUser.objects.filter(email=email).exists():
            messages.success(request, 'Email already exists; Please choose another.')
            return render(request,'tsignup.html')
        
        user= CustomUser.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            user_type=user_type
        )
        user.save()

        teacher= Teacher(
            user=user,
            course=sel,
            age=age,
            contact=contact,
            image=image
        )
        teacher.save()
        messages.success(request,' Registration Successful; Please wait for admin approval.')
        return redirect('tsignup')



def add_student(request):
    if request.method == 'POST':
        first_name= request.POST['first_name']
        last_name= request.POST['last_name']
        username= request.POST['username']
        age= request.POST['age']
        email= request.POST['email']
        contact= request.POST['contact']
        user_type= request.POST['text']
        sel= request.POST['sel']
        image= request.FILES.get('file')

        # checking username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.success(request, 'Username already exists; Please choose another.')
            return redirect('stsignup')
        
        # email checking
        if CustomUser.objects.filter(email=email).exists():
            messages.success(request, 'Email already exists; Please choose another.')
            return render(request,'stsignup.html')
        
        user= CustomUser.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            user_type=user_type
        )
        user.save()

        student= Student(
            user=user,
            course=sel,
            age=age,
            contact=contact,
            image=image
        )
        student.save()
        messages.success(request,' Registration Successful; Please wait for admin approval.')
        return redirect('stsignup')


def login1(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)

        if user is not None:
            if user.user_type=='1':
                login(request,user)
                return redirect('adminhome')
            elif user.user_type=='2':
                login(request,user)
                return redirect('teacherhome')
            elif user.user_type=='3':
                login(request,user)
                return redirect('studenthome')
            
        else:
            messages.info(request, "Invalid username or password!")
            return redirect('loginpage')
            



def admin_view(request):
    unapproved_count=CustomUser.objects.filter(status=0).count()
    count=unapproved_count - 1
    print(count)
    return render(request,'admin_home.html', {'unapproved_count':count})




def apv_dpv(request):
    users=CustomUser.objects.filter(~Q(user_type="1"))
    unapproved_count=CustomUser.objects.filter(status=0).count()
    count=unapproved_count - 1
    print(count)
    return render(request, 'apv_dpv.html', {'user_data': users, 'unapproved_count': count})



def approve(request,k):
    usr=CustomUser.objects.get(id=k)
    usr.status = 1
    usr.save()

    if usr.user_type == "2":
        tea=Teacher.objects.get(user=k)
        password =str(random.randint(100000, 999999))
        print(password)
        usr.set_password(password)
        usr.save()

        send_mail(
            'Admin approved!',
            f'Username: {tea.user.username}\n Password: {password}\n Email: {tea.user.email}',
            settings.EMAIL_HOST_USER,
            [tea.user.email]
        )
        messages.info(request, 'Teacher approved!')
    
    

    elif  usr.user_type == "3":
        stu=Student.objects.get(user=k)
        password =str(random.randint(100000, 999999))
        print(password)
        usr.set_password(password)
        usr.save()

        send_mail(
            'Admin approved!',
            f'Username: {stu.user.username}\n Password: {password}\n Email: {stu.user.email}',
            settings.EMAIL_HOST_USER,
            [stu.user.email]
        )
        messages.info(request, 'Student approved!')

    return redirect('apv_dpv')


def disapprove(request,k):
    usr=CustomUser.objects.get(id=k)
    if usr.user_type == "2":
        Teacher.objects.filter(user=k).delete()
        send_mail(
            subject='Admin Disapproval !',
            message='We regret to inform you that your account has been disapproved by the admin.',
                
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[usr.email],
             
         )
        messages.info(request, 'Teacher disapproved!')

    elif usr.user_type == "3":
        Student.objects.filter(user=k).delete()
        send_mail(
            subject='Admin Disapproval !',
            message='We regret to inform you that your account has been disapproved by the admin.',
             
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[usr.email],
         )
        messages.info(request, 'Student disapproved!')
        
    usr.delete()  
    return redirect('apv_dpv')  


def reset_pwd(request):
    return render(request,'reset.html')

def reset(request):
    if request.method=='POST':
        pas=request.POST['new_password']
        cpas=request.POST['confirm_password']
        if pas==cpas:
            if len(pas) < 6 or not any(char.isupper() for char in pas) \
            or not any(char.isdigit() for char in pas) \
            or not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?/~' for char in pas) :
                messages.error(request, 'Password must be at least 6 characters long and contain at least on uppercase letter, one digit and one special character.')
                return redirect('reset_pwd')
        

            else:
                usr=request.user.id
                tsr=CustomUser.objects.get(id=usr)
                tsr.password=pas
                tsr.set_password(pas)
                tsr.save()
                messages.info(request, "Password Changed!")
                return redirect('reset_pwd')






def logout(request):
    auth.logout(request)
    return render(request,'login.html')


