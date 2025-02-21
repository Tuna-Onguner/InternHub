from django import template

register = template.Library()


@register.filter
def can_make_announcement(user):
    return user.role not in ["STUDENT", "INSTRUCTOR"]


@register.filter
def can_submit_report(user):
    return user.role in ["STUDENT"]


@register.filter
def can_submit_feedback(user):
    return user.role in ["INSTRUCTOR"]


@register.filter
def can_submit(user):
    return user.role in ["INSTRUCTOR", "STUDENT"]


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
