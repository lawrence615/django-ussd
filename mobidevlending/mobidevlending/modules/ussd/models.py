from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

"""
This is used to store all the ussd user's details
"""


class Users(models.Model):
    phone = models.CharField(max_length=255)
    name = models.CharField(max_length=255, null=True)
    gender = models.SmallIntegerField(default=0)
    email = models.EmailField(max_length=254, null=True)
    session = models.IntegerField(default=0)
    progress = models.IntegerField(default=0)
    confirm_from = models.IntegerField(default=0)
    menu_id = models.IntegerField(default=0)
    menu_item_id = models.IntegerField(default=0)
    is_registration_done = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)

    def is_user_registered(self, phone):
        user = Users.objects.get(phone=phone)

        if user.is_registration_done == 0:
            return False
        else:
            return True


class Menus(models.Model):
    title = models.CharField(max_length=100)
    has_precondition = models.IntegerField()
    type = models.IntegerField(default=1)
    is_parent = models.BooleanField(default=0)
    confirmation_message = models.CharField(max_length=200, null=True)
    created_date = models.DateTimeField(default=timezone.now)


class MenuItems(models.Model):
    menu_id = models.ForeignKey("Menus", null=True, related_name='menus')
    description = models.CharField(max_length=255)
    next_menu_id = models.IntegerField()
    step = models.IntegerField()
    confirmation_phrase = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)

    @classmethod
    def get_menu_and_items(cls, menu_id):
        for items in MenuItems.objects.get(menu_id):
            response = items.description
        return response

    # @staticmethod
    def get_menu_item_given_menu_id_and_step(self, menu_id, step):
        menu_item = self.queryset.filter(menu_id=menu_id, step=step)

        return menu_item


class Logs(models.Model):
    service_code = models.CharField(max_length=100)
    session_id = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    text = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)


class Responses(models.Model):
    phone = models.CharField(max_length=50)
    menu_id = models.IntegerField()
    menu_item_id = models.IntegerField()
    user_input = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now)


    # def save_response(self, user_id, menu_id, menu_item_id, response):
