from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http import HttpResponse
import csv
from .models import Category, Customers, Prodocts, Orders, Brand


# ثبت مدل‌ها در ادمین
admin.site.register(Category)
admin.site.register(Customers)
admin.site.register(Prodocts)
admin.site.register(Brand)


# کلاس برای سفارشی‌سازی ادمین کاربران
class CustomUserAdmin(BaseUserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'is_staff', 'is_active', 'is_superuser', 'date_joined', 'last_login'
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')


# حذف ثبت پیش‌فرض User و ثبت سفارشی
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# اکشن برای دانلود گزارش سفارش‌ها به فرمت CSV
@admin.action(description='دانلود گزارش سفارش‌ها')
def export_orders_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['شناسه سفارش', 'محصول', 'مشتری', 'تاریخ سفارش', 'وضعیت', 'تعداد', 'آدرس', 'تلفن'])

    for order in queryset:
        writer.writerow([
            order.id,
            order.product.Name,
            f'{order.customers.FirstName} {order.customers.LasttName}',
            order.OrderDate,
            'ارسال شده' if order.status else 'در انتظار',
            order.quantity,
            order.address,
            order.phone
        ])
    return response


# سفارشی‌سازی ادمین برای مدل Orders
@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'customers', 'OrderDate', 'status', 'quantity')
    list_filter = ('status', 'OrderDate')
    search_fields = ('product__Name', 'customers__FirstName', 'customers__LasttName')
    actions = [export_orders_csv]
