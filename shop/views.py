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
import urllib.request

# from .forms import CreateUserForm
# from django.contrib.auth.forms import UserCreationForm


from datetime import date, timedelta

# Create your views here.
from django.views.decorators.csrf import csrf_protect
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializer import UserSerializer, RegisterSerializer
from django.contrib.auth import login
from .forms import UserRegistrationForm,CreateOrderForm
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from .models import ProductImageModel,ProductModel,OrderModel, AvailabilityModel
from .filters import ProductFilter,OrderFilter,AvailabilityFilter

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
    # my_filter2 = OrderFilter2(request.GET, queryset=orders)
    orders = my_filter.qs
    for res in orders:
        product = OrderModel.objects.get(id=res.id).product
        # res.product = ProductModel.objects.get(id=product.id)
        res.price_of_order = res.amount * product.product_price
        total_days = res.date_of_order + timedelta(days=7)
        if res.date_of_order == date.today():
            res.status = f'Pending - order date: {res.date_of_order.strftime("%d.%m.%Y.")}'
        elif res.date_of_order >= total_days:
            res.status = f'Delivered {res.date_of_order.strftime("%d.%m.%Y.")}'
        elif res.date_of_order < date.today():
            res.status = f'Sent {res.date_of_order.strftime("%d.%m.%Y.")}'
        else:
            res.status = f'Unknown {res.date_of_order.strftime("%d.%m.%Y.")}'
    current_user = request.user
    context = {"orders": orders, "values": curr_vals, "currencies": currencies,
               "current_user": current_user,"my_filter":my_filter}
    # context = {}
    # ,"my_filter": my_filter
    return render(request, 'profile.html', context)

def homepage(request):
    key = '3537610c7a9346338cdca02d0b4e1047'
    key = '1cf038b92a748c3271a76ede2fcd7f0c'


    novi_sad_data = requests.get(
        "http://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}&units={2}".format('Novi Sad',
                                                                                          '3537610c7a9346338cdca02d0b4e1047',
                                                                                          'metric'))
    novi_sad_json = novi_sad_data.json()
    novi_sad_temp = novi_sad_json['main']['temp']
    novi_sad_temp_min = novi_sad_json['main']['temp_min']
    novi_sad_temp_max = novi_sad_json['main']['temp_max']
    novi_sad_humidity = novi_sad_json['main']['humidity']
    novi_sad = {'temp': novi_sad_temp, 'temp_min': novi_sad_temp_min, 'temp_max': novi_sad_temp_max,
              'humidity': novi_sad_humidity}

    belgrade_data = requests.get(
        "http://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}&units={2}".format('Belgrade',
                                                                                          '3537610c7a9346338cdca02d0b4e1047',
                                                                                          'metric'))

    belgrade_json = belgrade_data.json()
    belgrade_temp = belgrade_json['main']['temp']
    belgrade_temp_min = belgrade_json['main']['temp_min']
    belgrade_temp_max = belgrade_json['main']['temp_max']
    belgrade_humidity = belgrade_json['main']['humidity']
    belgrade = {'temp': belgrade_temp, 'temp_min': belgrade_temp_min, 'temp_max': belgrade_temp_max,
                'humidity': belgrade_humidity}


    nis_data = requests.get(
        "http://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}&units={2}".format('Nis',
                                                                                          '3537610c7a9346338cdca02d0b4e1047',
                                                                                          'metric'))
    nis_json = nis_data.json()
    nis_temp = nis_json['main']['temp']
    nis_temp_min = nis_json['main']['temp_min']
    nis_temp_max = nis_json['main']['temp_max']
    nis_humidity = nis_json['main']['humidity']
    nis = {'temp': nis_temp, 'temp_min': nis_temp_min, 'temp_max': nis_temp_max,
                'humidity': nis_humidity}

    context = {'belgrade': belgrade, 'novi_sad':novi_sad, 'nis':nis}
    return render(request, 'home.html',context)

def products(request):
    products = ProductModel.objects.all()
    my_filter = ProductFilter(request.GET, queryset=products)
    products = my_filter.qs

    paginator = Paginator(products, 4)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    context = {"products": products, "my_filter": my_filter}
    return render(request, 'products.html', context)

def product_page(request, pk):
    product = ProductModel.objects.get(id=pk)
    images = ProductImageModel.objects.filter(product=pk)
    stores = AvailabilityModel.objects.filter(product=pk)
    my_filter = AvailabilityFilter(request.GET, queryset=stores)
    stores = my_filter.qs

    # WEB SERVIS ZA KONVERZIJU VALUTA
    url = "https://api.exchangeratesapi.io/latest?symbols=USD,GBP"
    response = requests.get(url)
    data = response.text
    parsed = json.loads(data)

    base = parsed['base']
    currencies = [base] + list(parsed['rates'])
    curr_vals = [1] + list(parsed["rates"].values())

    context = {"product": product, "images": images, "stores": stores, "currencies": currencies, "values": curr_vals,
               "my_filter": my_filter}
    return render(request, 'product-details.html', context)

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


@login_required(login_url='login')
def view_as_pdf(request, pk):
    current_user = request.user
    # check = CheckModel.objects.get(id=pk)
    order = OrderModel.objects.get(id=pk)
    available = AvailabilityModel.objects.get(id=order.available.id)
    product = ProductModel.objects.get(id=order.product.id)
    order.price_of_order = order.amount * product.product_price
    total_days = order.date_of_order + timedelta(days=7)
    context = {"user": current_user, "order":order, "available": available, "product": product,
               "total_days": total_days}
    pdf = render_to_pdf('pdf-template.html', context)
    return HttpResponse(pdf, content_type='application/pdf')

def charts(request):

    return render(request, 'charts.html')


@login_required(login_url='login')
def create_order(request, pk):
    avb = AvailabilityModel.objects.get(id=pk)
    product = ProductModel.objects.get(id=avb.product.id)
    obj = OrderModel(product=product,available=avb)
    obj.available = avb
    obj.product = product
    obj.amount = 1
    total_price = product.product_price
    form = CreateOrderForm(instance=obj)
    if request.method == "POST":
        form = CreateOrderForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.date_of_order = date.today()
            if obj.date_of_order < date.today():
                messages.info(request, "Order date can not be in the past")
                return redirect('create-order', pk=pk)
            # orders = OrderModel.objects.filter(accommodation=obj.accommodation)
            # for res in reservations:
            if (obj.amount > avb.number_of_available_items):
                messages.info(request, "The amount you chose is not available in our online store.")
                return redirect('create_order', pk=pk)
            # avb.number_of_available_items = avb.number_of_available_items - obj.amount
            obj.user = request.user
            obj.date_of_order = date.today()
            obj.price_of_order = obj.amount * product.product_price
            total_price = obj.price_of_order
            if obj.price_of_order <= 0:
                messages.info(request, "There is no order!")
                return redirect('create_order', pk=pk)
            obj.available = avb
            obj.product = product
            obj.save()
            # return redirect('create_order',pk = pk)
            messages.success(request, "Your order is done!")
        else:
            messages.info(request, "You have to fill all the fields to make an order."
                                   )

    context = {"form": form, "obj":obj, "avb": avb, "product":product, 'total_price':total_price}
    return render(request, 'order.html', context)


# @login_required(login_url='login')
# def update_order2(request, pk):
#     order = OrderModel.objects.get(id=pk)
#     avb = AvailabilityModel.objects.get(id=order.available.id)
#     product = ProductModel.objects.get(id=order.product.id)
#     obj = OrderModel()
#     obj.product = product
#     obj.available = avb
#     form = CreateOrderForm(instance=order)
#     total_price = product.product_price
#
#     if request.method == "POST":
#         form = CreateOrderForm(request.POST, instance=order)
#         if form.is_valid():
#             obj = form.save(commit=False)
#             if obj.amount < 1:
#                 messages.info(request, "Amount must be positive number.")
#                 return redirect('update_order', pk=order.id)
#             # if str.__len__(obj.address) <= 5:
#             #     messages.info(request, "Address must be valid!")
#             #     return redirect('update_order', pk=order.id)
#             obj.date_of_order = date.today()
#
#             if (obj.amount > avb.number_of_available_items):
#                 messages.info(request, "The amount you chose is not available in our online store.")
#                 return redirect('update_order', pk=order.id)
#             obj.user = request.user
#             obj.date_of_order = date.today()
#             obj.price_of_order = obj.amount * product.product_price
#             total_price = obj.price_of_order
#             if obj.price_of_order <= 0:
#                 messages.info(request, "There is no order!")
#                 return redirect('update_order', pk=order.id)
#             obj.available = avb
#             obj.product = product
#             obj.save()
#             # return redirect('create_order',pk = pk)
#             messages.success(request, "Your order is updated!")
#         else:
#             messages.info(request, "You have to fill all the fields to update an order."
#                           )
#
#         context = {"form": form, "obj": obj, "avb": avb, "product": product, 'total_price': total_price}
#         return render(request, 'order.html', context)

@login_required(login_url='login')
def update_order(request, pk):
    order = OrderModel.objects.get(id=pk)
    available = AvailabilityModel.objects.get(id=order.available.id)
    product = ProductModel.objects.get(id=order.product.id)
    obj = OrderModel()
    obj.product = product
    obj.available = available
    total_price = order.amount * product.product_price
    form = CreateOrderForm(instance=order,
                                 initial={'Amount': order.amount,
                                          'Address': order.address,
                                          'Order type': order.order_type})

    if request.method == "POST":
        form = CreateOrderForm(request.POST, instance=order)
        if form.is_valid():
            obj = form.save(commit=False)
            if obj.amount < 1:
                messages.info(request, "Amount must be positive number.")
                return redirect('update_order', pk=order.id)
            if obj.address == "":
                messages.info(request, "Address must be valid!")
                return redirect('update_order', pk=order.id)
            obj.date_of_order = date.today()

            if (obj.amount > available.number_of_available_items):
                messages.info(request, "The amount you chose is not available in our online store.")
                return redirect('update_order', pk=order.id)

            obj.user = request.user
            obj.date_of_order = date.today()
            obj.price_of_order = obj.amount * product.product_price
            total_price = obj.price_of_order
            if obj.price_of_order <= 0:
                messages.info(request, "There is no order!")
                return redirect('update_order', pk=order.id)
            obj.available = available
            obj.product = product
            obj.save()
            # return redirect('create_order',pk = pk)
            messages.success(request, "Your order is updated!")
            return redirect('homepage')
        else:
            messages.info(request, "You have to fill all the fields to make a reservation."
                                   " Date format is DD.MM.YYYY.")

    context = {"form": form, "product": product, "available": available, 'total_price': total_price}
    return render(request, 'order.html', context)

@login_required(login_url='login')
def delete_order(request, pk):
    order = OrderModel.objects.get(id=pk)
    product = ProductModel.objects.get(id=order.product.id)
    total_days = order.date_of_order + timedelta(days=7)
    message = f"Are you sure you want to remove order {order} from the list?" if total_days > date.today() else f"Are you sure you want to cancel order {order}?"
    if request.method == "POST":
        order.delete()
        message = "Order is deleted."
        # context = {"message": message,}
        return redirect('homepage')
    context = {"message": message, "order": order, "product":product}
    return render(request,'delete_order.html', context)