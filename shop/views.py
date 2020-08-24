from django.contrib.auth import authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
import urllib
from django.db.models import QuerySet
import requests, json
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as dj_login
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa


# from .forms import CreateUserForm
# from django.contrib.auth.forms import UserCreationForm


from datetime import date

# Create your views here.
from django.views.decorators.csrf import csrf_protect
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializer import UserSerializer, RegisterSerializer
from django.contrib.auth import login
from .forms import UserRegistrationForm
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from .models import ProductImageModel,ProductModel,CheckModel,OrderModel
from .filters import ProductFilter,CheckFilter,OrderFilter

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })



class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

@csrf_protect
def login_user(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            dj_login(request, user)
            return redirect('homepage')
        else:
            messages.info(request, "Username or password is incorrect.")
    return render(request, 'login.html')
@csrf_protect
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
           form.save()
           username = form.cleaned_data.get('username')
           messages.success(request,f"Account created for {username}")
           return redirect('login')
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'register.html', context)

# @csrf_protect
# def register(request):
#     if request.user.is_authenticated:
#         return redirect('homepage')
#     else:
#         form = CreateUserForm()
#         if request.method == 'POST':
#             form = CreateUserForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 user = form.cleaned_data.get("username")
#                 messages.success(request, f"Account was created for {user} ")
#                 return redirect('login')
#             else:
#                 pass1 = form.cleaned_data.get("password")
#                 # pass2 = form.cleaned_data.get("password2")
#                 if pass1 is None:
#                     messages.info(request, "The password is not valid.")
#                 else:
#                     messages.info(request, "Username is taken.")
#
#         context = {'form': form}
#         return render(request, 'register.html', context)

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('homepage')


@login_required(login_url='login')
def user_profile(request):
    # WEB SERVIS ZA KONVERZIJU VALUTA
    url = "https://api.exchangeratesapi.io/latest?symbols=USD,GBP"
    response = requests.get(url)
    data = response.text
    parsed = json.loads(data)

    base = parsed['base']
    currencies = [base] + list(parsed['rates'])
    curr_vals = [1] + list(parsed["rates"].values())

    orders = OrderModel.objects.filter(user=request.user)
    my_filter = OrderFilter(request.GET, queryset=orders)
    orders = my_filter.qs
    for res in orders:
        product = OrderModel.objects.get(id=res.id).product
        res.product = ProductModel.objects.get(id=product.id)
        if res.date_of_order > date.today():
            res.status = f'Pending - start date: {res.date_of_order.strftime("%d.%m.%Y.")}'
        elif res.date_of_order < date.today():
            res.status = f'Checked out {res.date_of_order.strftime("%d.%m.%Y.")}'
        else:
            res.status = f'Checked in {res.date_of_order.strftime("%d.%m.%Y.")}'
    current_user = request.user
    context = {"orders": orders, "values": curr_vals, "currencies": currencies,
               "current_user": current_user,"my_filter": my_filter}
    # context = {}
    # ,"my_filter": my_filter
    return render(request, 'profile.html', context)

def homepage(request):
    # key = 'LQBJ8397PZR8L3UK'
    # london_data = requests.get(
    #     "http://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}&units={2}".format('London',
    #                                                                                       '1cf038b92a748c3271a76ede2fcd7f0c',
    #                                                                                       'metric'))
    #
    # london_json = london_data.json()
    # london_temp = london_json['main']['temp']
    # london_temp_min = london_json['main']['temp_min']
    # london_temp_max = london_json['main']['temp_max']
    # london_humidity = london_json['main']['humidity']
    # london = {'temp': london_temp, 'temp_min': london_temp_min, 'temp_max': london_temp_max,
    #           'humidity': london_humidity}
    #
    # #urllib.request.urlopen(f'https://api.thingspeak.com/update?api_key={key}&field1={london_temp}')
    #
    # belgrade_data = requests.get(
    #     "http://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}&units={2}".format('Belgrade',
    #                                                                                       '1cf038b92a748c3271a76ede2fcd7f0c',
    #                                                                                       'metric'))
    #
    # belgrade_json = belgrade_data.json()
    # belgrade_temp = belgrade_json['main']['temp']
    # belgrade_temp_min = belgrade_json['main']['temp_min']
    # belgrade_temp_max = belgrade_json['main']['temp_max']
    # belgrade_humidity = belgrade_json['main']['humidity']
    # belgrade = {'temp': belgrade_temp, 'temp_min': belgrade_temp_min, 'temp_max': belgrade_temp_max,
    #             'humidity': belgrade_humidity}
    # #urllib.request.urlopen(f'https://api.thingspeak.com/update?api_key={key}&field2={belgrade_temp}')
    #
    # paris_data = requests.get(
    #     "http://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}&units={2}".format('Paris',
    #                                                                                       '1cf038b92a748c3271a76ede2fcd7f0c',
    #                                                                                       'metric'))
    #
    # paris_json = paris_data.json()
    # paris_temp = paris_json['main']['temp']
    # paris_temp_min = paris_json['main']['temp_min']
    # paris_temp_max = paris_json['main']['temp_max']
    # paris_humidity = paris_json['main']['humidity']
    # paris = {'temp': paris_temp, 'temp_min': paris_temp_min, 'temp_max': paris_temp_max, 'humidity': paris_humidity}
    # urllib.request.urlopen(f'https://api.thingspeak.com/update?api_key={key}&field3={paris_temp}')

    # context = {}
    return render(request, 'home.html')

def products(request):
    products = ProductModel.objects.all()
    my_filter = ProductFilter(request.GET, queryset=products)
    products = my_filter.qs

    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    context = {"products": products, "my_filter": my_filter}
    return render(request, 'products.html', context)