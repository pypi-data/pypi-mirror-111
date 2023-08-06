import random
import string
from datetime import datetime


def construct_transfer_group(user_id, product_id, payment_identifier=None):
    if payment_identifier is None:
        payment_identifier = \
            ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    group_values = [
        str(user_id),
        str(product_id),
        str(int(datetime.utcnow().timestamp())),
        str(payment_identifier),
    ]
    return ':'.join(group_values)
