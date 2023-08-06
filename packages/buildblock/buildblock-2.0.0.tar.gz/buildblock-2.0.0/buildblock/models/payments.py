from typing import NamedTuple


class ActualPaymentAmount(NamedTuple):
    amount: float
    fee: float
    fee_rate: float


class Payments(NamedTuple):
    unpaid_amount: float
    payment_in_progress_amount: float
    card_payment: ActualPaymentAmount
    ach_debit_payment: ActualPaymentAmount
    rent_count: int
