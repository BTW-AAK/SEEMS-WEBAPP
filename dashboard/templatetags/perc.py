from django import template

register = template.Library()

@register.filter(name='percentage')
def percentage(value, arg):
    if arg ==0:
        return 0
    
    return (value / arg)*100

@register.filter(name='priceModifier')
def priceModifier(value):


    return round(value*6,4)