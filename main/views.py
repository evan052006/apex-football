import datetime
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from main.models import Product
from main.forms import ProductForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core import serializers


def show_products_by_xml(request):
    product_list = Product.objects.all()
    xml_data = serializers.serialize("xml", product_list)
    return HttpResponse(xml_data, content_type="application/xml")


def show_products_by_json(request):
    product_list = Product.objects.all()
    json_data = serializers.serialize("json", product_list)
    return HttpResponse(json_data, content_type="application/json")


def show_product_xml_by_id(request, id):
    product_item = get_object_or_404(Product, id=id)
    xml_data = serializers.serialize("xml", [product_item])
    return HttpResponse(xml_data, content_type="application/xml")


def show_product_json_by_id(request, id):
    product_item = get_object_or_404(Product, id=id)
    json_data = serializers.serialize("json", [product_item])
    return HttpResponse(json_data, content_type="application/json")


@login_required(login_url='/login')
def show_product(request, id):
    product = get_object_or_404(Product, id=id)
    return render(
        request,
        "product_detail.html",
        {
            "product": product
        }
    )


@login_required(login_url='/login')
def create_product(request):
    form = ProductForm(request.POST or None)
    if form.is_valid() and request.method == "POST":
        '''
        product_entry = form.save(commit=False)
        '''
        form.requester = request.user
        form.save()
        return redirect('main:show_index')

    context = {'form': form}
    return render(request, "create_product.html", context)


@login_required(login_url='/login')
def show_index(request):
    filter_type = request.GET.get("filter", "all")
    if filter_type == "all":
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(requester=request.user)
    return render(
        request,
        "index.html",
        {
            "nama": "Christopher Evan Tanuwidjaja",
            "kelas": "A",
            "app_name": "main",
            "product_list": product_list,
            "last_login": request.COOKIES.get('last_login', 'Never')
        }
    )


def register_user(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form': form}
    return render(request, 'register.html', context)


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_index"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    return redirect('main:login')
