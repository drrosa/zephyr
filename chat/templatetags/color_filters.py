from django import template
from django.utils.safestring import mark_safe
import hashlib

register = template.Library()


@register.filter(name="username_color")
def username_color(username):
    """Generate a unique color class based on the username."""
    hash_val = hashlib.md5(username.encode()).hexdigest()
    color_code = "#" + hash_val[:6]
    return mark_safe(f'style="color: {color_code};"')
