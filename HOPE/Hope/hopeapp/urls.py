from django.urls import path
from .views import *


urlpatterns = [
    path('', LandingPage.as_view(),name='index'),
    path('home/', HomePage.as_view(),name='home'),
    path('about/', About.as_view(),name='about'),
    path('contact/', Contact.as_view(),name='contact'),
    path('approach/', Approach.as_view(),name='approach'),
    path('donate/', Donate.as_view(),name='donate'),
    path('whatwedo/', Wedo.as_view(),name='whatwedo'),
    path('report-animal/thankyou/', Thankyou.as_view(),name='thankyou'),
    path('myreport/', Myreports.as_view(), name='myreport'),
    path('logintype/', LoginType.as_view(),name='logintype'),
    path('login/', Login.as_view(),name='login'),
    path('signup/', Signup.as_view(),name='signup'),
    path('dashboard/', Dashboard.as_view(),name='dashboard'),
    path('logout/', Logout.as_view(),name='logout'),
    path('report-animal/', AnimalReportView.as_view(), name='animal_report'),
    path('vetlogin/', HospitalLogin.as_view(), name='vetlogin'),
    path('hospital_signup/', HospitalSignup.as_view(), name='hospital_signup'),
    path('vetdashboard/', HospitalDashboard.as_view(), name='vetdashboard'),
    path('treatment/create/<str:token>/', TreatmentCreateView.as_view(), name='treatment_create'),
    path('donate/', DonationCreateView.as_view(), name='donate'),

]