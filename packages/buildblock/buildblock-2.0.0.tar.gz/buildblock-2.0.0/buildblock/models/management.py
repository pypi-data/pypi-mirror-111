from typing import List, NamedTuple, Optional, Union


class Lease(NamedTuple):
    id: int
    full_address: str
    room_num: Union[int, str]
    status: str
    owner_name: str
    tenant_name: str
    start_date: Optional[str]
    end_date: Optional[str]
    rent: int
    deposit: int
    payment_day: int
    tenant_phone_number: Optional[str] = None
    tenant_email: Optional[str] = None
    tenant_credit_score: Union[int, str] = 'N/A'
    num_paid_rents: Union[int, str] = 'N/A'
    created_at: Optional[str] = None
    is_auto_paid: bool = False


class Owner(NamedTuple):
    id: int
    name: str
    email: str
    phone_number: str
    nationality: str
    full_address: str
    products: List
    stripe_account: str
    total_balance_amount: Optional[int] = 0
    available_balance_amount: Optional[int] = 0
