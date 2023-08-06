from buildblock.apps.core.views import TemplateView
from buildblock.apps.investment.views.base import InvestmentServiceMixin


class OverviewView(InvestmentServiceMixin, TemplateView):
    '''
    투자 종합적인 페이지
    - 현재 투자금
    - 누적 투자금 / 총 수익 / 투자 횟수
    - 현재 진행 중인 투자 상품
    '''
    pass
