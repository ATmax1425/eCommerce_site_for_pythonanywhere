from django.shortcuts import render, redirect
from .forms import RegisterForm, ProductForm, CartForm, OrderForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required, user_passes_test
from .models import Product, ProductInCart, UserOrder
import datetime
import os


def check_admin(user):
    return user.is_superuser


def get_cart_products(request, add_it=None):
    if request.user.is_authenticated:
        models_cart_data = ProductInCart.objects.all().filter(owner=request.user).all()
        cart_data = [[Product.objects.get(pk=i.product_id), i.quantity] for i in models_cart_data]
        grand_total = round(sum([i[0].price * i[1] for i in cart_data]), 2)
        cart_item_count = sum([i[1] for i in cart_data])
        return [cart_data, grand_total, cart_item_count]
    if add_it:
        cart_data = add_it
    else:
        cart_data = request.COOKIES.get('product_detail')
    if cart_data:
        cart_data = [[int(j) for j in i.split("|")] for i in cart_data.split(",")[:-1]]
        cart_data = [[Product.objects.get(pk=i[0]), i[1]] for i in cart_data]
        grand_total = round(sum([i[0].price * i[1] for i in cart_data]), 2)
        cart_item_count = sum([i[1] for i in cart_data])
        return [cart_data, grand_total, cart_item_count]
    else:
        return [None, 0]


def after_login(request):
    cookies_cart_data = request.COOKIES.get('product_detail')
    if cookies_cart_data:
        cookies_cart_data = cookies_cart_data.split(",")[-1]
        for product_det in cookies_cart_data:
            product, quantity = [int(i) for i in product_det.split("|")]
            add_cart = ProductInCart()
            add_cart.owner = request.user
            add_cart.product_id = product
            add_cart.quantity = quantity
            add_cart.save()
        response = redirect('/')
        response.delete_cookie('product_detail')
        return response
    return redirect('/')


@staff_member_required()
@user_passes_test(check_admin)
def delete_product(request, product):
    img_list = []
    for i in [product.img_url, product.img_url2, product.img_url3, product.img_url4, product.img_url5]:
        if i:
            img_list.append(i)
    product.delete()
    for i in img_list:
        if os.path.isfile(i.path):
            os.remove(i.path)


# Create your views here.
def home(request):
    products = Product.objects.all()
    active = "all"
    if request.method == "POST":
        product_id = request.POST.get("product-id")
        product = Product.objects.filter(id=product_id).first()
        if product and request.user.is_staff:
            delete_product(request, product)
    return render(request, 'main_app/home.html',
                  {"products": products, "active": active, "cart_products": get_cart_products(request)})


def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/after-login')
    else:
        form = RegisterForm()
    return render(request, 'registration/sign_up.html', {'form': form, "cart_products": get_cart_products(request)})


def cart(request, item_id=None):
    if request.method == "POST":
        if request.user.is_authenticated:
            cart_items = ProductInCart.objects.all().filter(owner=request.user).all()
            item = cart_items.filter(product_id=item_id).first()
            item.delete()
        else:
            cart_data = request.COOKIES.get('product_detail')
            cart_check = [[j for j in i.split("|")] for i in cart_data.split(",")[:-1]]
            for i, item in enumerate(cart_check):
                if item[0] == item_id:
                    cart_check.pop(i)
                    break
            cart_data = ""
            for i, j in cart_check:
                cart_data += "|".join([i, j]) + ","
            response = redirect("/cart")
            response.set_cookie("product_detail", cart_data,
                                expires=datetime.datetime.now() + datetime.timedelta(days=30))
            return response
    return render(request, 'main_app/cart.html',
                  {"cart_products": get_cart_products(request)})


def grinding_wheels(request):
    products = Product.objects.all().filter(type="GW")
    active = "GW"
    return render(request, 'main_app/home.html',
                  {"products": products, "active": active, "cart_products": get_cart_products(request)})


def hand_gloves(request):
    products = Product.objects.all().filter(type="HG")
    active = "HG"
    return render(request, 'main_app/home.html',
                  {"products": products, "active": active, "cart_products": get_cart_products(request)})


def safety_equipment(request):
    products = Product.objects.all().filter(type="SE")
    active = "SE"
    return render(request, 'main_app/home.html',
                  {"products": products, "active": active, "cart_products": get_cart_products(request)})


def contact(request):
    if request.user.is_authenticated:
        if UserOrder.objects.filter(owner=request.user).exists():
            return render(request, 'main_app/contact.html')
        if request.method == "POST":
            form = OrderForm(request.POST)
            if form.is_valid():
                cart_form = form.save(commit=False)
                cart_form.owner = request.user
                cart_form.save()
                return render(request, 'main_app/contact.html')
        else:
            form = OrderForm()
        return render(request, 'main_app/contact.html', {'form': form})
    return render(request, 'main_app/contact.html')
    # cart_item = form.save(commit=False)
    # cart_item.owner = request.user
    # cart_item.product_id = product_id
    # cart_item.save()
    # if request.user.is_authenticated:
    #     user_order = UserOrders()
    #     user_order.owner = request.user
    #     user_order.save()
    #     cart_data = get_cart_products(request)
    #     cart_data[3].ordered_at = datetime.datetime.now()
    # return render(request, 'main_app/contact.html')


def product_detail(request, product_name):
    product = Product.objects.all().filter(name=product_name).first()
    img_list = []
    for i in [product.img_url2, product.img_url3, product.img_url4, product.img_url5]:
        if i:
            img_list.append(i)
    description = [des.split(":") for des in product.description.split("\r\n")]
    if request.method == "POST":
        form = CartForm(request.POST)
        product_id = str(product.id)
        if form.is_valid():
            if request.user.is_authenticated:
                cart_item = ProductInCart.objects.all().filter(product_id=product_id).first()
                if cart_item:
                    cart_item.quantity += int(form.data['quantity'])
                    cart_item.save()
                else:
                    cart_item = form.save(commit=False)
                    cart_item.owner = request.user
                    cart_item.product_id = product_id
                    cart_item.save()
                return render(request, 'main_app/product_detail.html',
                              {"product": product, "description": description, "form": form,
                               "img_list": (range(1, len(img_list)+1), img_list),
                               "cart_products": get_cart_products(request)})

            cart_data = request.COOKIES.get('product_detail')
            if cart_data:
                cart_check = [[j for j in i.split("|")] for i in cart_data.split(",")[:-1]]
                if product_id in [i[0] for i in cart_check]:
                    for i, item in enumerate(cart_check):
                        if item[0] == product_id:
                            item[1] = str(int(item[1]) + int(form.data['quantity']))
                            cart_check[i] = item
                            break
                    cart_data = ""
                    for i, j in cart_check:
                        cart_data += "|".join([i, j]) + ","
                else:
                    cart_data += "|".join([product_id, form.data['quantity']]) + ","
            else:
                cart_data = "|".join([product_id, form.data['quantity']]) + ","

            response = render(request, 'main_app/product_detail.html',
                              {"product": product, "description": description, "form": form,
                               "img_list": (range(1, len(img_list)+1), img_list),
                               "cart_products": get_cart_products(request, add_it=cart_data)})
            response.set_cookie("product_detail", cart_data,
                                expires=datetime.datetime.now() + datetime.timedelta(days=10))
            return response
    else:
        form = CartForm()
    return render(request, 'main_app/product_detail.html',
                  {"product": product, "description": description, "form": form,
                   "img_list": (range(1, len(img_list)+1), img_list), "cart_products": get_cart_products(request)})


@login_required(login_url="/login")
@staff_member_required()
@user_passes_test(check_admin)
def create_products(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            # product.img_url = convert_to_url(product.img_url)
            # print("is_google_link", product.img_url)
            product.save()
            return redirect("/")
    else:
        form = ProductForm()
    return render(request, "main_app/create_products.html", {"form": form})
