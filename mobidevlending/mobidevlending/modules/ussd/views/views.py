from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def ussd(request):
    params = request.POST if request.method == 'POST' else request.GET

    session = params.get('sessionId')
    service_code = params.get('serviceCode')
    phone = params.get('phoneNumber')
    text = params.get('text')

    user_input = capture_input(text)

    if user_input['level'] == 0:
        output = get_main_menu()
    elif user_input['level'] == 1:
        output = level_one_process(user_input)

    return send_response(output, 1)


def get_main_menu():
    return "Welcome to Mobidev Lending:" + "\n 1.Request Loan" + "\n 2.Pay Loan" + "\n 3.Check Loan Limit"


def level_one_process(user_input):
    if user_input.get('message') == "1":
        output = get_request_loan_menu()
    elif user_input.get('message') == "2":
        output = get_pay_loan_menu()
    elif user_input.get('message') == "3":
        output = get_check_loan_limit_menu()
    else:
        output = "Invalid input"

    return output


def level_two_process(user_input):
    if user_input.get('message') == "1":
        output = "Hello"

    return output


def get_request_loan_menu():
    return "Enter amount"


def get_pay_loan_menu():
    return "Pay Loan" + "\n 1.From M-PESA" + "\n 2.From M-Shwari"


def get_check_loan_limit_menu():
    return "Enter M-PESA PIN"


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


@csrf_exempt
def dynamic_ussd(request):
    params = request.POST if request.method == 'POST' else request.GET

    session = params.get('sessionId')
    service_code = params.get('serviceCode')
    phone = params.get('phoneNumber')
    text = params.get('text')




def capture_input(text):
    captured_text = text.replace(" ", "")
    if len(text) <= 0:
        user_input = {
            'level': 0,
            'message': captured_text
        }

    else:
        split_text = captured_text.split('*')
        user_input = {
            'split_text': split_text,
            'level': len(split_text),
            'message': captured_text
        }

    return user_input
