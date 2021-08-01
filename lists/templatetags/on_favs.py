from django import template
from lists import models as list_models

register = template.Library()

@register.simple_tag(takes_context=True)
def on_favs(context,event):
    user = context.request.user
    # print(user)
    the_list = list_models.List.objects.get(user=user,name="My Favourite Event")
    # print(event in the_list.event.all())
    return event in the_list.event.all()