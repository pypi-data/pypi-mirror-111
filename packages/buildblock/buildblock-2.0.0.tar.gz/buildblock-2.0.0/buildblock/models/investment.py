from typing import NamedTuple


class InvestorModel(NamedTuple):
    id: int
    name: str
    email: str
    phone: str
    address: str
    num_investment: int


class InvestmentProductModel(NamedTuple):
    id: int
    title: str
    manager_id: int
    manager_name: str
    manager_email: str
    start_date: str
    end_date: str
    plan_file_name: str
    plan_file_url: str
    description: str


class InvestmentModel(NamedTuple):
    id: int
    amount: float
    investor: InvestorModel
    investment_product: InvestmentProductModel


class InvestmentContractModel(NamedTuple):
    id: int
    investment_id: int
    investment_product_id: int
    investment_product_title: str
    investor_id: int
    investor_name: str
    title: str
    envelope_id: str
    document_name: str
    records: dict
    status: str
    created_at: str
    due_date: str
    template_type: str
    template_title: str


class InvestmentStageModel(NamedTuple):
    id: str
    status: str
    title: str
    description: str
    progress_percentage: int
    steps: list


class InvestmentTransactionEntityModel(NamedTuple):
    id: str
    type: str
    name: str
    bank_name: str
    bank_account_number: str
