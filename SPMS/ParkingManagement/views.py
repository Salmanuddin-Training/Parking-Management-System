from django.shortcuts import render, redirect
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.views.generic import View
# Create your views here.
from .models import Category
from .models import AddVehicle

from .forms import CategoryForm
from .forms import AddVehicleForm


def Register(request):
    if request.method=="POST":
        RUsername= request.POST['RUsername']
        REmail= request.POST['REmail']
        RPassword= request.POST['RPassword']
        RConfirmPassword=request.POST['RConfirmPassword']

        if RPassword==RConfirmPassword:
            if User.objects.filter(username=RUsername).exists():
                print("Username Already Exists, Try Another Username..!")
                return redirect("Register")
            else:
                if User.objects.filter(email=REmail).exists():
                    print("Email Is Already Taken, Try Another Email..!")
                    return redirect("Register")
                else:
                    UserRegistration= User.objects.create_user(username=RUsername,email=REmail,password=RPassword)
                    UserRegistration.save()
                    return redirect("Login")
        else:
            print("Password Didn't Matched..!")
            return redirect('Register')
    else:
        return render(request,'Register.html')

def Login(request):
    if request.method=="POST":
        Username=request.POST['Username']
        Password=request.POST['Password']
        UserLogin=auth.authenticate(username=Username,password=Password)
        if UserLogin is not None:
            auth.login(request,UserLogin)
            print("Successfully Logged In..!")
            return redirect("Dashboard")
        else:
            print("Invalid Details Or User Not Registered..!")
            return redirect("Login")
    else:
        return render(request,'Login.html')

@login_required(login_url="Login")
def Logout(request):
    if request.method =="POST":
        auth.logout(request)
        print("Logged Out Successfully..!")
        return redirect('Login')

@login_required(login_url="Login")      # Category
class CategoryView(View):
    def AddCategory(request):
        form = CategoryForm()

        if request.method == "POST":        # post == Post ==> True
            form = CategoryForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                return redirect('Display')

        context = {'form': form}
        return render(request, 'Category.html', context)

    def DisplayCRUD(request):       
        display= Category.objects.all()

        page_num= request.GET.get("page")  # Total Number Of Pages Required
        paginator= Paginator(display,5)

        try:
            display= paginator.page(page_num)  # Total No. Of Pages (Pages==5 Prdoduct's/Page)
        except PageNotAnInteger:
            display = paginator.page(1) # If No. Of Products<5 Then Set Pages To first page only which is 127.0.0.1:8000
        except EmptyPage:
            display = paginator.page(paginator.num_pages)
        
        context = { 'display':display}
        return render(request,"Category.html",context)

@login_required(login_url='Login')
def ManageVehicle(request):
    display = AddVehicle.objects.all()

    page_num = request.GET.get("page")  # Total number of pages required
    paginator = Paginator(display, 5)

    try:
        display = paginator.page(page_num)  # Total 5-+ Products load --> each page 3 =>2 pages(1,2)

    except PageNotAnInteger:
        display = paginator.page(1)  # its show first page only which is 127.0.0.1:8000

    except EmptyPage:  # If the page is empty (there is no product this except block will execute)
        display = paginator.page(paginator.num_pages)


    context = {'display': display}

    return render(request, 'ManageVehicles.html', context)


@login_required(login_url='login')
def AdVehicle(request):
    form = AddVehicleForm()

    if request.method == "POST":        # post == Post ==> True
        form = AddVehicleForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Manage')

    context = {'form': form}
    return render(request, 'VehicleEntry.html', context)


def Delete(request, pk):
    displey = Category.objects.get(id=pk)
    displey.delete()

    return redirect('Display')

def Update(request, pk):
    display = Category.objects.get(id=pk)
    form = CategoryForm(instance=display)

    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=display)
        if form.is_valid():
            form.save()

            return redirect('Display')

    context = {'form': form}

    return render(request, 'Category.html', context)

def Deactive(request,pk):
    category = Category.objects.get(id=pk)
    category.status = False
    category.save()
    return redirect('Display')

def Activate(request,pk):
    category = Category.objects.get(id=pk)
    category.status = True
    category.save()
    return redirect('Display')

def Left(request,pk):
    category1 = AddVehicle.objects.get(id=pk)
    category1.status = False
    category1.save()
    return redirect('ManageVehicles')

def Parked(request,pk):
    category1 = AddVehicle.objects.get(id=pk)
    category1.status = True
    category1.save()
    return redirect('ManageVehicles')

@login_required(login_url='Login')
def Search(request):
    if request.method == "GET":
        query = request.GET.get('query')
        if query: # condition is true
            display = AddVehicle.objects.filter(vehicle_no__contains = query)
            return render(request, 'Search.html',{'display':display})
        else:
             print("No Information Is Available Regarding Search..!")
             return render(request, 'Search.html',{})

def ManageSearch(request):
    if request.method == "GET":
        query = request.GET.get('query')
        if query: # condition is true
            display = AddVehicle.objects.filter(vehicle_no__contains = query)
            return render(request, 'ManageVehicles.html',{'display':display})
        else:
            print("No Information Is Available Regarding Search..!")
            return render(request, 'ManageVehicles.html',{})

def CategorySearch(request):
    if request.method == "GET":
        query = request.GET.get('query')
        if query: # condition is true
            display = Category.objects.filter(parking_area_no__contains = query)
            return render(request, 'Category.html',{'display': display})
        else:
            print("No Information Is Available Regarding Search..!")
            return render(request, 'Category.html',{})

@login_required(login_url='Login')
def Dashboard(request):

    parked_count = AddVehicle.objects.filter(status=True).count()
    departed_count = AddVehicle.objects.filter(status=False).count()
    category_count = Category.objects.filter(status=True).count()
    records_count = AddVehicle.objects.all().count()
    total_earnings = AddVehicle.objects.filter(status=True).aggregate(Sum('parking_charge'))["parking_charge__sum"]

    context = {'parked_count': parked_count,
               'departed_count': departed_count,
               'category_count': category_count,
               'records_count': records_count,
               'total_earnings': total_earnings,
               }
    return render(request, 'Dashboard.html', context)

@login_required(login_url='Login')
def Reports(request):
    return render(request, 'Reports.html')

@login_required(login_url='Login')
def AccountSettings(request):
    if request.method=="POST":
        OldPassword=request.POST['OldPassword']
        UserCheck=auth.authenticate(password=OldPassword)
        if UserCheck is not None:
            Password=request.POST['Password']
            ConfirmPassword=request.POST['ConfirmPassword']
            if Password==ConfirmPassword:
                User.objects.aupdate(password=Password)
                print("Password Updated..!")
                return redirect('Login')
            else:
                print("Paswword Doesn't Match..!")
                return render(request,'AccountSettings.html')
        else:
            print("Please Enter Current Password..!")
    return render(request, 'AccountSettings.html')