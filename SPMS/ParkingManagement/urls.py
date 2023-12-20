from django.urls import path
from . import views
# from django.views import View



urlpatterns=[
    path('Delete/<int:pk>', views.Delete, name='Delete'),
    path('Display/', views.CategoryView.DisplayCRUD, name='Display'),
    path('ManageVehicles/', views.ManageVehicle, name= 'ManageVehicles'),
    path('Update/<int:pk>', views.Update, name='Update'),
    path('Deactive/<int:pk>',views.Deactive, name='Deactive'),
    path('Category/', views.CategoryView.AddCategory, name= 'AddCategory'),
    path('VehicleEntry/', views.AdVehicle, name= 'VehicleEntry'),
    path('',views.Login,name='Login'),
    path('Register/',views.Register,name='Register'),
    path('AccountSettings/',views.AccountSettings,name='AccountSettings'),
    path('Dashboard/',views.Dashboard,name='Dashboard'),
    path('Logout/', views.Logout, name='Logout'),
    path('Parked/<int:pk>', views.Parked, name='Parked'),
    path('Left/<int:pk>', views.Left, name='Left'),
    path('Activate/<int:pk>',views.Activate, name='Activate'),
    path('Search/', views.Search, name='Search'),
    path('ManageSearch/', views.ManageSearch, name='ManageSearch'),
    path('CategorySearch/', views.CategorySearch, name='CategorySearch'),
    path('Reports/', views.Reports,name='Reports'),
]