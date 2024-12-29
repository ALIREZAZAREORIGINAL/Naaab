from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Prodocts, Category
from .forms import SignUpForm
from .forms import SearchForm
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from .models import Orders
from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now


def helloworld(request):
    all_prodoct = Prodocts.objects.all()
    all_category = Category.objects.all()
    return render(request, 'index.html', {'prodocts': all_prodoct, 'categories': all_category})


def about(request):
    return render(request, 'about.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "با موفقیت وارد شدید")
            return redirect("home")
        else:
            messages.error(request, "اطلاعات نادرست است!")
            return redirect("login")
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, "با موفقیت خارج شدید")
    return redirect("home")


def signup_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, ":) حساب کاربری با موفقیت ایجاد شد . خوش آمدید")
            return redirect("home")
        else:
            messages.error(request, 'متاسفانه مشکلی در ثبت نام شما پیش آمده ):')
            return redirect("signup")
    return render(request, 'signup.html', {'form': form})


def product(request, pk):
    product = get_object_or_404(Prodocts, pk=pk)
    return render(request, 'product.html', {'product': product})


def category_products(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products_list = Prodocts.objects.filter(category=category)
    paginator = Paginator(products_list, 6)  # نمایش 6 محصول در هر صفحه
    page = request.GET.get('page')
    products = paginator.get_page(page)
    return render(request, 'category_products.html', {'products': products, 'category': category})


def add_to_cart(request, product_id):
    product = get_object_or_404(Prodocts, pk=product_id)
    cart = request.session.get('cart', {})

    if product.QuantityInStock > 0:
        cart[str(product_id)] = cart.get(str(product_id), 0) + 1
        product.QuantityInStock -= 1
        product.save()
        request.session['cart'] = cart
        messages.success(request, f"محصول {product.Name} با موفقیت به سبد خرید اضافه شد!")
    else:
        messages.error(request, "محصول انتخابی شما در دسترس نیست.")
    
    return redirect('category_products', pk=product.category.id)



def cart(request):
    cart = request.session.get('cart', {})
    products = Prodocts.objects.filter(id__in=cart.keys())
    cart_items = [
        {
            'product': product,
            'quantity': cart[str(product.id)],
            'total_price': product.Price * cart[str(product.id)],
        }
        for product in products
    ]
    total_price = sum(item['total_price'] for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Prodocts, pk=product_id)

    if str(product_id) in cart:
        product.QuantityInStock += cart[str(product_id)]
        del cart[str(product_id)]
        product.save()
    
    request.session['cart'] = cart
    messages.success(request, "محصول از سبد خرید حذف شد.")
    return redirect('cart')


def update_cart(request, product_id):
    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Prodocts, pk=product_id)
        cart = request.session.get('cart', {})

        if quantity <= product.QuantityInStock + cart.get(str(product_id), 0):
            product.QuantityInStock += cart.get(str(product_id), 0) - quantity
            cart[str(product_id)] = quantity
            product.save()
            request.session['cart'] = cart
            messages.success(request, "سبد خرید بروزرسانی شد.")
        else:
            messages.error(request, "موجودی کافی برای این محصول وجود ندارد.")
    
    return redirect('cart')


def search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Prodocts.objects.filter(Name__icontains=query)

    return render(request, 'search_results.html', {'form': form, 'query': query, 'results': results})





@staff_member_required
def order_report(request):
    orders = Orders.objects.all()  # تمام سفارش‌ها را از مدل Orders بگیرید
    html = render_to_string('order_report.html', {'orders': orders})  # قالب HTML برای گزارش
    return HttpResponse(html)


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Prodocts, Orders, Customers

@login_required
def checkout(request):
    # گرفتن مشتری مرتبط با کاربر فعلی
    try:
        customer = Customers.objects.get(Email=request.user.email)
    except Customers.DoesNotExist:
        messages.error(request, "ابتدا باید اطلاعات مشتری را ثبت کنید.")
        return redirect('profile')  # یک مسیر برای ثبت اطلاعات مشتری ایجاد کنید

    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "سبد خرید شما خالی است!")
        return redirect('cart')

    products = Prodocts.objects.filter(id__in=cart.keys())
    total_price = 0

    # ثبت سفارش‌ها در جدول Orders
    for product in products:
        quantity = cart[str(product.id)]
        if quantity > product.QuantityInStock:
            messages.error(request, f"محصول {product.Name} موجودی کافی ندارد.")
            return redirect('cart')

        # کاهش موجودی محصول
        product.QuantityInStock -= quantity
        product.save()

        # محاسبه قیمت کل
        total_price += product.Price * quantity

        # ذخیره سفارش در جدول Orders
        Orders.objects.create(
            product=product,
            customers=customer,
            quantity=quantity,
            address=request.POST.get('address', ''),  # آدرس مشتری از فرم
            phone=customer.PhoneNumber,  # شماره تلفن مشتری
            status=True  # فرض پرداخت موفق
        )

    # پاک کردن سبد خرید
    request.session['cart'] = {}
    messages.success(request, f"پرداخت با موفقیت انجام شد! مبلغ کل: {total_price} تومان")

    return redirect('home')




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Customers
from django.contrib import messages

@login_required
def profile(request):
    try:
        customer = Customers.objects.get(Email=request.user.email)
    except Customers.DoesNotExist:
        customer = None

    if request.method == "POST":
        # ثبت یا ویرایش اطلاعات مشتری
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
       # address = request.POST['address']

        if customer:
            # به‌روزرسانی اطلاعات موجود
            customer.FirstName = first_name
            customer.LasttName = last_name
            customer.PhoneNumber = phone
            customer.save()
            messages.success(request, "اطلاعات شما با موفقیت به‌روزرسانی شد.")
        else:
            # ایجاد اطلاعات جدید
            Customers.objects.create(
                FirstName=first_name,
                LasttName=last_name,
                PhoneNumber=phone,
                Email=request.user.email,
                Password=request.user.password  # توجه: این به دلایل امنیتی مناسب نیست
            )
            messages.success(request, "اطلاعات شما با موفقیت ذخیره شد.")
        return redirect('checkout')

    return render(request, 'profile.html', {'customer': customer})
