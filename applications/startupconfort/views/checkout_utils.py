import uuid
from random import randint
from django.utils import timezone

def get_total(amount):
    total = """
                <tr class="total">
                    <td></td>

                    <td>
                       Total: $ {0}
                    </td>
                </tr>
                <tr class="total">
                    <td></td>

                    <td>
                       Status: Successfully Paid by the you on {1}
                    </td>
                </tr>
            </table>
            <table>
                <tr>
                    <td>
                        <a href='/'>
                        <h3>
                        return to Startup Confort
                        <h3>
                        </a>
                    </td>
                </tr>
            </table>
        </div>
    """.format(amount, timezone.now().strftime('%Y-%m-%d'))
    return total


def shipping():
    content = """
            <tr class="item last">
                <td>
                    Shipping
                </td>

                <td>
                    $ 8 USD
                </td>
            </tr>
    """
    return content

def item_loop(item_name, price):
    content = """
            <tr class="item">
                <td>
                    {0}
                </td>

                <td>
                    $ {1} USD
                </td>
            </tr>
    """.format(item_name, price)
    return content

def get_footer():
    footer ="""
        </body>
        </html>
    """
    return footer


def get_body(email, username, address, country, confirmation_number, created):
    body ="""
    <body>
        <div class="invoice-box">
            <table cellpadding="0" cellspacing="0">
                <tr class="top">
                    <td colspan="2">
                        <table>
                            <tr>
                                <td class="title">
                                    <a href='/'>
                                    <img src="https://www.sparksuite.com/images/logo.png" style="width:100%; max-width:300px;">
                                    </a>
                                </td>

                                <td>
                                    Invoice #: {4}<br>
                                    Created: {5}<br>
                                    Status: <bold>Sucessfully paid</bold>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>

                <tr class="information">
                    <td colspan="2">
                        <table>
                            <tr>
                                <td>
                                    Startup Comfort <br>
                                    4798 Onondaga Blvd<br>
                                    Syracuse, New York
                                </td>

                                <td>
                                    {1}<br>
                                    {2}<br>
                                    {3}<br>
                                    {6}
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>

                <tr class="heading">
                    <td>
                        Payment Method
                    </td>

                    <td>
                        Confirmation #
                    </td>
                </tr>

                <tr class="details">
                    <td>
                        Online Payment
                    </td>

                    <td>
                        {0}
                    </td>
                </tr>

                <tr class="heading">
                    <td>
                        Item
                    </td>

                    <td>
                        Price
                    </td>
                </tr>
    """.format(confirmation_number, username, address, country, randint(150,2039), created.strftime('%Y-%m-%d') , email)
    return body


def get_header():
    header="""
    <!doctype html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>A simple, clean, and responsive HTML invoice template</title>

        <style>
        .invoice-box {
            max-width: 800px;
            margin: auto;
            padding: 30px;
            border: 1px solid #eee;
            box-shadow: 0 0 10px rgba(0, 0, 0, .15);
            font-size: 16px;
            line-height: 24px;
            font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;
            color: #555;
        }

        .invoice-box table {
            width: 100%;
            line-height: inherit;
            text-align: left;
        }

        .invoice-box table td {
            padding: 5px;
            vertical-align: top;
        }

        .invoice-box table tr td:nth-child(2) {
            text-align: right;
        }

        .invoice-box table tr.top table td {
            padding-bottom: 20px;
        }

        .invoice-box table tr.top table td.title {
            font-size: 45px;
            line-height: 45px;
            color: #333;
        }

        .invoice-box table tr.information table td {
            padding-bottom: 40px;
        }

        .invoice-box table tr.heading td {
            background: #eee;
            border-bottom: 1px solid #ddd;
            font-weight: bold;
        }

        .invoice-box table tr.details td {
            padding-bottom: 20px;
        }

        .invoice-box table tr.item td{
            border-bottom: 1px solid #eee;
        }

        .invoice-box table tr.item.last td {
            border-bottom: none;
        }

        .invoice-box table tr.total td:nth-child(2) {
            border-top: 2px solid #eee;
            font-weight: bold;
        }

        @media only screen and (max-width: 600px) {
            .invoice-box table tr.top table td {
                width: 100%;
                display: block;
                text-align: center;
            }

            .invoice-box table tr.information table td {
                width: 100%;
                display: block;
                text-align: center;
            }
        }

        /** RTL **/
        .rtl {
            direction: rtl;
            font-family: Tahoma, 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;
        }

        .rtl table {
            text-align: right;
        }

        .rtl table tr td:nth-child(2) {
            text-align: left;
        }
        </style>
    </head>
    """
    return header


def get_billing_template(cartitems, email, username, address, country, confirmation_number, created, amount):
    items_content = [item_loop(item.product.title, item.product.price) for item in cartitems]
    items_content = ''.join(items_content)
    content  = get_header() + get_body(email, username, address, country, confirmation_number, created) +  items_content +   shipping() + get_total(amount) + get_footer()
    return content
