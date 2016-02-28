__author__ = 'Lawrence'

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from mobidevlending.modules.ussd.models import Users, Menus, MenuItems, Responses


@csrf_exempt
def ussd(request):
    if request.method == "POST":
        params = request.POST

        session = params.get('sessionId')
        service_code = params.get('serviceCode')
        phone = params.get('phoneNumber')
        text = params.get('text')

        ussd_user = Users.objects.filter(phone=phone).exists()

        if not ussd_user:  # check if user exists, if not create him/her
            user = Users(phone=phone, menu_id=1)
            user.save()

        result = text.split('*')[-1]

        if len(result) <= 0:
            message = text
        else:
            message = result

        if user_is_starting(text) or message == '0':
            ussd_user_2 = Users.objects.get(phone=phone)
            reset_user(ussd_user_2)  # reset user

            if Users.is_user_registered(ussd_user_2, phone):
                menu = Menus.objects.get(pk=2)
            else:
                menu = Menus.objects.get(pk=1)

            response = next_menu_switch(ussd_user_2, message, menu)

            return send_response(response, 1)
        else:
            ussd_user_3 = Users.objects.get(phone=phone)

            if ussd_user_3.session == 1:
                response = continue_ussd_progress(ussd_user_3, message)

            elif ussd_user_3.session == 2:
                response = continue_ussd_progress(ussd_user_3, message)

            return send_response(response, 1)


def continue_ussd_progress(ussd_user, message):
    menu = Menus.objects.get(pk=ussd_user.menu_id)

    if menu.type == 1:
        response = continue_ussd_menu(ussd_user, message, menu)

    elif menu.type == 2:
        response = continue_single_process(ussd_user, message, menu)

    return response


def continue_ussd_menu(ussd_user, message, menu):
    menu_items = get_menu_items(ussd_user.menu_id)

    pass


def continue_single_process(ussd_user, message, menu):
    if menu.id == 1:
        if ussd_user.progress == 1:
            if validate_input(message):
                store_ussd_response(ussd_user, message)
            else:
                return "Please provide your two names"
        if ussd_user.progress == 2:
            store_ussd_response(ussd_user, message)
        if ussd_user.progress == 3:
            store_ussd_response(ussd_user, message)
            ussd_user.session = 2
            ussd_user.save()

    step = ussd_user.progress + 1
    menu_item = MenuItems.objects.get(menu_id=menu.id, step=step)

    if menu_item:
        ussd_user.menu_item_id = menu_item.id
        ussd_user.menu_id = menu.id
        ussd_user.progress = step
        ussd_user.save()

        return menu_item.description


def confirm_ussd_process(ussd_user, message):
    user_menu = ussd_user.objetcs.get(menu_id=ussd_user.menu_id)
    return


def validate_input(message):
    how_many = len(message.split(" "))
    if how_many > 1:
        return True
    else:
        return False


def store_ussd_response(ussd_user, response):
    ussd_response = Responses()
    ussd_response.user_id = ussd_user.id
    ussd_response.menu_id = ussd_user.menu_id
    ussd_response.menu_item_id = ussd_user.menu_item_id
    ussd_response.response = response

    ussd_response.save()


def next_menu_switch(ussd_user, message, menu):
    if menu.type == 1:
        menu_items = get_menu_items(menu.id)

        no = 1
        response = menu.title
        for menu_item in menu_items:
            response += no + ":" + menu_item.description
            no += 1

        ussd_user.session = 1
        ussd_user.menu_id = menu.id
        ussd_user.menu_item_id = 0
        ussd_user.progress = 0
        ussd_user.save()

        return response

    elif menu.type == 2:
        store_ussd_response(ussd_user, message)

        response = continue_single_process(ussd_user, message, menu)

        return response


def get_menu_items(menu_id):
    menu_items = MenuItems.objects.get(menu_id=menu_id)
    return menu_items


def reset_user(ussd_user):
    ussd_user.session = 1
    ussd_user.progress = 0
    ussd_user.menu_id = 1
    ussd_user.confirm_from = 0
    ussd_user.menu_item_id = 0
    ussd_user.save()


def user_is_starting(text):
    if len(text) > 0:
        return False
    else:
        return True


def send_response(response, response_type):
    if response_type == 1:
        output = "CON "

    elif response_type == 2:
        output = "CON "
        response = " 1. Back to main menu" + "\n 2. Log out"

    else:
        output = "END "

    output += response

    response = HttpResponse(output, content_type='text/plain')
    return response
