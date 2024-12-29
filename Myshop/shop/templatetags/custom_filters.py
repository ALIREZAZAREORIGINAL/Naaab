from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, None)


@register.filter
def number_format(value):
    try:
        value = int(value)  # تبدیل مقدار به عدد صحیح
        return "{:,}".format(value)  # جدا کردن سه رقم سه رقم
    except (ValueError, TypeError):
        return value