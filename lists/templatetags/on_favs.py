from django import template
from lists import models as list_models

register = template.Library()


@register.simple_tag(takes_context=True)
def on_favs(context, event):
    user = context.request.user
    # print(user)
    try:
        the_list = list_models.List.objects.get(
            user=user, name="My Favourite Event")
    except list_models.List.DoesNotExist:
        the_list = None
        # print(event in the_list.event.all())
        # return event in the_list.event.all()
    if the_list is not None:
        return event in the_list.event.all()
    else:
        return the_list
