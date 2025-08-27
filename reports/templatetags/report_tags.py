from django import template
from savings.models import SavingAccount

register = template.Library()

@register.filter
def get_year_count(year):
    return SavingAccount.objects.filter(year=year).count()