from buildblock.apps.core.constants import OWNER_ROLE
from buildblock.models.investment import InvestmentContractModel, InvestmentProductModel, InvestorModel


class InvestmentContext:
    def _make_investment_contract_context(self, investment_contract):
        return InvestmentContractModel(
            id=investment_contract.id,
            investment_id=investment_contract.investment.id,
            investment_product_id=investment_contract.investment.investment_product.id,
            investment_product_title=investment_contract.investment.investment_product.title,
            investor_id=investment_contract.investment.user.id,
            investor_name=investment_contract.investment.user.name,
            title=investment_contract.title,
            envelope_id=investment_contract.identifier,
            document_name=investment_contract.document_file.name if investment_contract.document_file else None,
            records=investment_contract.records,
            status=investment_contract.status,
            created_at=investment_contract.created_at,
            due_date=investment_contract.due_date,
            template_type=investment_contract.template.type,
            template_title=investment_contract.template.title
        )

    def _make_investment_product_context(self, investment_product):
        return InvestmentProductModel(
            id=investment_product.id,
            title=investment_product.title,
            manager_id=investment_product.manager.id,
            manager_name=investment_product.manager.name,
            manager_email=investment_product.manager.email,
            start_date=investment_product.start_date,
            end_date=investment_product.end_date,
            plan_file_name=investment_product.plan.name if investment_product.plan else None,
            plan_file_url=investment_product.plan.url if investment_product.plan else None,
            description=investment_product.description,
        )

    def _make_investor_context(self, user):
        return InvestorModel(
            id=user.id,
            name=user.name,
            email=user.email,
            phone=user.phone_number,
            address=user.profile_owner.full_address if OWNER_ROLE in user.user_role else None,
            num_investment=user.investor_investments.count()
        )
