from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from .models import * 
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import random
from django.http import HttpResponseRedirect,HttpResponse
from django.core.files.storage import FileSystemStorage
from django.utils.timezone import now
from django.http import JsonResponse
from django.conf import settings  
import uuid
import razorpay

class LandingPage(View):
    def get(self, request):
        return render(request, 'index.html')

class HomePage(View):
    def get(self, request):
        return render(request, 'home.html')

class About(View):
    def get(self, request):
        return render(request, 'about.html')

class Contact(View):
    def get(self, request):
        return render(request, 'contact.html')

class Approach(View):
    def get(self, request):
        return render(request, 'approach.html')

class Donate(View):
    def get(self, request):
        return render(request, 'donate.html')

class Wedo(View):
    def get(self, request):
        return render(request, 'wedo.html')
    
class Thankyou(View):
    def get(self, request, *args, **kwargs):
        # Render the thank you page
        return render(request, 'thank.html')

    def post(self, request, *args, **kwargs):
        # Check if the user is a hospital
        if request.user.is_authenticated and hasattr(request.user, 'is_hospital') and request.user.is_hospital:
            return redirect('vetdashboard')  # Redirect to vet dashboard
        else:
            return redirect('dashboard')


class LoginType(View):
    def get(self, request):
        return render(request, 'logintype.html')

class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, 'Please provide both email and password.')
            return render(request, 'login.html')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                if user.is_hospital:
                    messages.error(request,'Hospital id cannot login here ') 
                return redirect('dashboard')  
            else:
                messages.error(request, 'Your account is not active.')
        else:
            messages.error(request, 'Invalid email or password.')

        return render(request, 'login.html')

class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        full_name = request.POST.get('Fname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        try:
            if User.objects.filter(email=email).exists():
                messages.error(request, "An account with this email already exists.")
                return redirect('signup')

            user = User.objects.create_user(
                username=email,
                email=email,
                first_name=full_name,
                password=password
            )
            user.is_hospital = False 
            user.save()
            messages.success(request, "Signup successful. Please login.")
            return redirect('login')  

        except Exception as e:
            messages.error(request, f"Error during signup: {str(e)}")
            return redirect('signup') 

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('home')

class Dashboard(View):
    @method_decorator(login_required)
    def get(self, request):
        user_name = request.user.first_name 
        if request.user.is_hospital:
            return render(request, 'hospital_dashboard.html', {'user_name': user_name})
        return render(request, 'dashboard.html', {'user_name': user_name})
    

class AnimalReportView(View):
    @method_decorator(login_required)
    def get(self, request):
        user_name = request.user.first_name 
        hospitals = Hospital.objects.all()
        
        return render(request, 'report_animal.html', {
            'hospitals': hospitals,
            'user_name': user_name
        })

    @method_decorator(login_required)
    def post(self, request):
        rescuer = request.POST.get('rescuer')
        phone_number = request.POST.get('phone')
        hospital_id = request.POST.get('hospital')
        animal_details = request.POST.get('details')
        animal_image = request.FILES.get('image')  

        hospital = Hospital.objects.get(id=hospital_id)

        token = random.randint(10000000, 99999999)   
        AnimalReport.objects.create(
            rescuer_name= rescuer,
            phone_number=phone_number,
            hospital=hospital,
            animal_details=animal_details,
            animal_image=animal_image,
            token=token,
            status='PENDING'
        )

        return HttpResponseRedirect('thankyou') 
    
class Myreports(View):
    def get(self, request):
        user_name = request.user.first_name         
        reports = AnimalReport.objects.all().order_by('-created_at')   
        return render(request,'myreports.html', {'reports': reports,'user_name': user_name})


    
class HospitalLogin(View):
    def get(self, request):
        return render(request, 'hospital/hlogin.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, 'Please provide both email and password.')
            return render(request, 'hospital/hlogin.html')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if user.is_active:
                if user.is_hospital:
                    login(request, user)
                    return redirect('vetdashboard')  
                else:
                    messages.error(request, 'This account is not a hospital account.')
            else:
                messages.error(request, 'Your account is not active.')
        else:
            messages.error(request, 'Invalid email or password.')

        return render(request, 'hospital/hlogin.html')
    
class HospitalSignup(View):
    def get(self, request):
        return render(request, 'hospital/hsignup.html')

    def post(self, request):
        try:
            hospital_name = request.POST.get('hospital_name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm-password')

            if password != confirm_password:
                messages.error(request, "Passwords do not match!")
                return redirect('hospital_signup') 

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered!")
                return redirect('hospital_signup') 
            
            user = User.objects.create_user(
                username=email,  
                email=email,
                password=password 
            )

            user.is_hospital = True
            user.save()

            hospital = Hospital.objects.create(
                user=user,
                hospital_name=hospital_name
            )

            login(request, user)

            messages.success(request, 'Hospital signup successful. You are now logged in.')
            return redirect('vetlogin')  

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('hospital_signup')

class HospitalDashboard(View):
    @method_decorator(login_required)
    def get(self, request):
        
        if request.user.is_hospital:
            hospital = request.user.hospital 
            reports = AnimalReport.objects.filter(hospital=hospital)
            return render(request, 'hospital/hdashboard.html', {
                'reports': reports
            })
        return render(request, 'hospital/hdashboard.html')

    @method_decorator(login_required)
    def post(self, request):
        if request.user.is_hospital:
            report_token = request.POST.get('report_token')
            new_status = request.POST.get('status')

            if new_status in ['PENDING', 'IN_TREATMENT', 'COMPLETED']:
                try:
                    report = AnimalReport.objects.get(token=report_token, hospital=request.user.hospital)
                    report.status = new_status
                    report.save()
                    return redirect('vetdashboard') 
                except AnimalReport.DoesNotExist:
                    return redirect('vetdashboard')
        
        return redirect('vetdashboard')
    


class TreatmentCreateView(View):
    def get(self, request, token):
        report = get_object_or_404(AnimalReport, token=token)

        return render(request, 'hospital/treatment.html', {'report': report})
    def post(self, request, token):
        try:
            report = get_object_or_404(AnimalReport, token=token)
            treatment_details = request.POST.get('treatment')
            total_amount = request.POST.get('amount')
            bill_image = request.FILES.get('bill')
            payment_image = request.FILES.get('bankdetails')

            if not treatment_details or not total_amount or not bill_image or not payment_image:
                return HttpResponse("All fields are required", status=400)

            fs = FileSystemStorage()

            bill_image_path = fs.save(bill_image.name, bill_image)
            payment_image_path = fs.save(payment_image.name, payment_image)

            treatment = Treatment(
                report=report,
                treatment_details=treatment_details,
                total_amount=total_amount,
                bill_image=bill_image_path,
                payment_image=payment_image_path,
                completed_at=now()
            )
            treatment.save()

            report.status = 'COMPLETED'
            report.save()



            return redirect('thankyou') 

        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=500)



class DonationCreateView(View):
    def get(self, request):
        return render(request, 'donation_form.html')

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment-method')
        transaction_id = str(uuid.uuid4())

        donation = Donation(
            name=name,
            email=email,
            phone_number=phone_number,
            amount=amount,
            payment_method=payment_method,
            transaction_id=transaction_id
        )
        donation.save()

        razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        order_data = {
            'amount': float(amount) * 100, 
            'currency': 'INR',
            'payment_capture': '1'
        }
        
        try:
            order = razorpay_client.order.create(data=order_data)
            order_id = order['id']

            return JsonResponse({
                'status': 'success',
                'order_id': order_id,
                'razorpay_key': settings.RAZORPAY_KEY_ID,
                'transaction_id': transaction_id,
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)