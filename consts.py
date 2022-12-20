class Templates:
    main_template = '{{"page_index": "{}"}}'
    error_template = '{{"error": "{}", "response": null, "data": null}}'
    success_template = '{{"error": null, "response": "{}", "data": {}}}'
    user_template = '{{"phone_number": "", "email": "{}", "signedIn": "{}"}}'

token_length = 16

error_codes = {\
    16: 'Wrong query to database',
    17: 'Invalid data passed to body',
    18: 'User is already registered',
    19: 'User is not registered',
    20: 'User is already logged in',
    21: 'Provided username does not exist'
}