from currency_symbols import CurrencySymbols


def amount_calculation(first_price, second_price):
    if second_price is not None:
        format_price = float(first_price) + float(second_price)
    else:
        format_price = float(first_price)

    return format_price


def price_conversion(first_ticket_price, second_ticket_price, currency_code):

    formatted_price = amount_calculation(first_ticket_price, second_ticket_price)
    converted_currency_symbol = CurrencySymbols.get_symbol(currency_code)

    if len(converted_currency_symbol) == 1:
        return converted_currency_symbol + str(formatted_price)
    else:
        return converted_currency_symbol + ' ' + str(formatted_price)



