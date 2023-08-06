from django.utils.translation import ugettext_lazy as _

from buildblock.settings import is_dev_environment

BUILDBLOCK_NAME = "BuildBlock"
BUILDBLOCK_ID = "buildblock"
BUILDBLOCK_ROLE = "Company"
BUILDBLOCK_EMAIL = "dev-test@buildblock.io" if is_dev_environment() else "info@buildblock.io"

BUILDBLOCK_BANK_NAME = "우리은행"
BUILDBLOCK_BANK_ACCOUNT_NUMBER = "1005103584730"
BUILDBLOCK_ACCOUNT_HOLDER_NAME = "(주)빌드블록"

# Language
ENGLISH = 'en'
KOREAN = 'ko'

LANGUAGE_CHOICES = (
    (ENGLISH, _('English')),
    (KOREAN, _('Korean')),
)

MSG_WRONG_APPROACH = _('잘못된 접근입니다.')

PENDING = 'PENDING'
ACTIVE = 'ACTIVE'
INACTIVE = 'INACTIVE'
COMPLETE = 'COMPLETE'
CANCELED = 'CANCELED'
FINISHED = 'FINISHED'
IN_PROGRESS = 'IN_PROGRESS'
INVESTMENT = 'INVESTMENT'
DONE = 'DONE'
WONT_FIX = 'WONT_FIX'
ACH_DEBIT = 'ACH_DEBIT'
UNKNOWN = 'UNKNOWN'
RENT = 'rent'
DEPOSIT = 'deposit'
UTILITY = 'utility'
OVERDUE = 'overdue'
FAILED = 'FAILED'
FAILED_NO_DESTINATION_ACCOUNT = 'FAILED_NO_DESTINATION_ACCOUNT'
FAILED_OTHER_REASON = 'FAILED_OTHER_REASON'
CREATED = 'CREATED'
STATUS_CHANGE = 'STATUS_CHANGE'
COMMENT_ADD = 'COMMENT_ADD'
COMMENT_DELETE = 'COMMENT_DELETE'
FIX_AND_FLIP = 'FIX_AND_FLIP'
ADU = 'ADU'
DIRECT_MANAGEMENT = 'DIRECT_MANAGEMENT'
SEPARATE_ORDER = 'SEPARATE_ORDER'
INTEGRATED_ORDER = 'INTEGRATED_ORDER'
ATTACHMENT = 'ATTACHMENT'
SIGNATURE = 'SIGNATURE'
BEFORE = 'BEFORE'
AFTER = 'AFTER'
NORMAL_WORKER = 'NORMAL_WORKER'
DEMOLITION_WORKER = 'DEMOLITION_WORKER'
ELECTRIC_WORKER = 'ELECTRIC_WORKER'
PAINTER = 'PAINTER'
PLUMBER = 'PLUMBER'
CARPENTER = 'CARPENTER'
CLEANER = 'CLEANER'
SPECIAL_WORKER = 'SPECIAL_WORKER'
WORKER = 'WORKER'
LEADER = 'LEADER'
CONTRACTOR = 'CONTRACTOR'
MATERIAL = 'MATERIAL'
TOOL = 'TOOL'
RENTAL = 'RENTAL'
FURNITURE = 'FURNITURE'
FOOD = 'FOOD'
ACCOMMODATION_FEE = 'ACCOMMODATION_FEE'
STORAGE_COST = 'STORAGE_COST'
FUEL_COST = 'FUEL_COST'
LABOR = 'LABOR'
ETC = 'ETC'
DAILY = 'DAILY'
WEEKLY = 'WEEKLY'
FINAL = 'FINAL'
ACCOUNT = 'ACCOUNT'
MANAGEMENT = 'MANAGEMENT'
MARKETING = 'MARKETING'
SUPPORT = 'SUPPORT'
PROPERTY = 'PROPERTY'
PAYMENT_REQUEST = "PAYMENT_REQUEST"
PAYMENT_REPORT = "PAYMENT_REPORT"
PAYMENT_OVERDUE = "PAYMENT_OVERDUE"

CASH = 'CASH'
CHECKS = 'CHECKS'
CREDIT_CARD = 'CREDIT_CARD'
DEBIT_CARD = 'DEBIT_CARD'

CREDIT_CARD_CHARGE_RATE = 0.03

# Wallet & Contract
BB_MAIN_WALLET = '0x01AFA212245f97F5C0f7433B1b08d08fCFca77a8'
POCKET_WALLET = '0x7590AA2F82e4072932F4909D08860356F007E261'

KRW_BB_MAIN_CONTRACT = '0x9d6aDEb02b9A24cCEF1a4032c9571b0a2b9970DC'
USD_BB_MAIN_CONTRACT = '0xf889E4C8F7B14D47a3577772d692cff657a8dbf3'
KLAYTN_KRW_BB_MAIN_CONTRACT = '0x327A795746E6377F1F65658Fa96327cc46D65308'
KLAYTN_USD_BB_MAIN_CONTRACT = '0x47d9b3a6DB0514b756C177275742EEEa236c9671'

MAIN_CONTRACTS = frozenset([
    KRW_BB_MAIN_CONTRACT,
    USD_BB_MAIN_CONTRACT,
    KLAYTN_KRW_BB_MAIN_CONTRACT,
    KLAYTN_USD_BB_MAIN_CONTRACT,
])

INVESTMENT_APP_NAME = "investment"
MANAGEMENT_APP_NAME = "management"
CONSTRUCTION_APP_NAME = "construction"

# Service Type
SERVICE_TYPE = (
    (INVESTMENT_APP_NAME, _("Management Service")),
    (MANAGEMENT_APP_NAME, _("Investment Service")),
    (CONSTRUCTION_APP_NAME, _("Construction Service")),
)

# User
TELECOM_CHOICES = (
    ("", _("선택")),
    ("KOR", _("한국 +82")),
    ("USA", _("미국 +1")),
)

COUNTRY_KOREA = "KR"
COUNTRY_UNITED_STATES = "US"

COUNTRY_CHOICES = (
    (COUNTRY_UNITED_STATES, _("미국")),
    (COUNTRY_KOREA, _("한국")),
    ("VIE", _("베트남")),
    ("ETC", _("그 외")),
)

US_STATE_CHOICES = (
    ("AL", _("Alabama")),
    ("AK", _("Alaska")),
    ("AZ", _("Arizona")),
    ("AR", _("Arkansas")),
    ("CA", _("California")),
    ("CO", _("Colorado")),
    ("CT", _("Connecticut")),
    ("DE", _("Delaware")),
    ("DC", _("District of Columbia")),
    ("FL", _("Florida")),
    ("GA", _("Georgia")),
    ("HI", _("Hawaii")),
    ("ID", _("Idaho")),
    ("IL", _("Illinois")),
    ("IN", _("Indiana")),
    ("IA", _("Iowa")),
    ("KS", _("Kansas")),
    ("KY", _("Kentucky")),
    ("LA", _("Louisiana")),
    ("ME", _("Maine")),
    ("MD", _("Maryland")),
    ("MA", _("Massachusetts")),
    ("MI", _("Michigan")),
    ("MN", _("Minnesota")),
    ("MS", _("Mississippi")),
    ("MO", _("Missouri")),
    ("MT", _("Montana")),
    ("NE", _("Nebraska")),
    ("NV", _("Nevada")),
    ("NH", _("New Hampshire")),
    ("NJ", _("New Jersey")),
    ("NM", _("New Mexico")),
    ("NY", _("New York")),
    ("NC", _("North Carolina")),
    ("ND", _("North Dakota")),
    ("OH", _("Ohio")),
    ("OK", _("Oklahoma")),
    ("OR", _("Oregon")),
    ("PA", _("Pennsylvania")),
    ("RI", _("Rhode Island")),
    ("SC", _("South Carolina")),
    ("SD", _("South Dakota")),
    ("TN", _("Tennessee")),
    ("TX", _("Texas")),
    ("UT", _("Utah")),
    ("VT", _("Vermont")),
    ("VA", _("Virginia")),
    ("WA", _("Washington")),
    ("WV", _("West Virginia")),
    ("WI", _("Wisconsin")),
    ("WY", _("Wyoming")),
)

# IN_PROGRESS: 공사 중 / ACTIVE: 렌탈 가능 상태 / PENDING: 등록 검토중
PRODUCT_STATUS_CHOICES = (
    (IN_PROGRESS, _("Construction")),
    (ACTIVE, _("Available")),
    (PENDING, _('Under Review')),
    (INVESTMENT, _('Investment')),
)

CONSTRUCTION_STATUS_CHOICES = (
    (PENDING, _('Ready')),
    (IN_PROGRESS, _("In Progress")),
    (COMPLETE, _("Complete")),
)

CONSTRUCTION_TYPE_CHOICES = (
    (FIX_AND_FLIP, _("Fix and Flip")),
    (ADU, _("ADU")),
)

CONSTRUCTION_METHOD_CHOICES = (
    (DIRECT_MANAGEMENT, _("Direct Management")),
    (SEPARATE_ORDER, _("Separate Order")),
    (INTEGRATED_ORDER, _("Integrated Order")),
)

CONSTRUCTION_PICTURE_STATUS_CHOICES = (
    (BEFORE, _("Before")),
    (IN_PROGRESS, _("In Progress")),
    (AFTER, _("After")),
)

REPORT_TYPE_CHOICES = (
    (DAILY, _("Daily")),
    (WEEKLY, _("Weekly")),
    (FINAL, _("Final")),
)

# 인부전공분류  NORMAL:일반인부
WORKER_SPECIALITY_CHOICES = (
    (NORMAL_WORKER, _("Normal Worker")),            # 잡부
    (DEMOLITION_WORKER, _("Demolition Worker")),    # 철거공
    (ELECTRIC_WORKER, _("Electric Worker")),        # 전기공
    (PAINTER, _("Painter")),                        # 페인트 인부
    (PLUMBER, _("Plumber")),                        # 배관공
    (CARPENTER, _("Carpenter")),                    # 목공
    (CLEANER, _("Cleaner")),                        # 청소부
    (SPECIAL_WORKER, _("Special Worker")),          # 특수인부
)

# 인부역할분류
WORKER_ROLE_CHOICES = (
    (WORKER, _("Worker")),          # 일반인부
    (LEADER, _("Leader")),          # 다른 인부들을 중개해줄 수 있는 인부
    (CONTRACTOR, _("Contractor")),  # 외주작업시 중개인
)

# 공사비용 카테고리
EXPENSE_CATEGORY_CHOICES = (
    (MATERIAL, _("Material")),                     # 자재
    (TOOL, _("Tool")),                             # 공구
    (RENTAL, _("Rental")),                         # 대여비
    (FURNITURE, _("Furniture")),                   # 가구
    (FOOD, _("Food")),                             # 식비
    (ACCOMMODATION_FEE, _("Accommodation Fee")),   # 숙박비
    (STORAGE_COST, _("Storage Cost")),             # 보관비
    (FUEL_COST, _("Fuel Cost")),                   # 유류비
    (ETC, _("Etc.")),                              # 기타
)

# 외주비 포함내역
OUTSOURCING_INCLUDED_CHOICES = (
    (LABOR, _("Labor")),                           # 인건비
    (MATERIAL, _("Material")),                     # 자재
    (ETC, _("Etc.")),                              # 기타
)

PRODUCT_PROPERTY_TYPE_CHOICES = (
    ("single_family ", _("Single Family")),
    ("multi_family", _("Multi Family")),
    ("condominium", _("Condominium")),
    ("townhouse", _("Townhouse")),
    ("co_op", _("Co-op")),
    ("land", _("Land")),
)

# TODO: product forms 이용해 list & freetext 적용
PRODUCT_WASHER_DRYER_CHOICES = (
    ("no_data", _("No Data")),
    ("none", _("None")),
    ("unit", _("Unit")),
    ("building", _("Building")),
    ("building_coin", _("Building(coin)")),
)

# TODO: product forms 이용해 list & freetext 적용
PRODUCT_ALLOWED_PETS_CHOICES = (
    ("no_data", _("No Data")),
    ("none", _("None")),
    ("dog", _("Dog")),
    ("dog_cat", _("Dog&Cat")),
)

BASE_UNIT_CHOICES = (
    ("", ""),
    ("KRW", "KRW"),
    ("USD", "USD"),
)

DISPLAY_UNIT_SYMBOL = {
    "KRW": "￦",
    "USD": "＄",
}

INDIVIDUAL_INVESTOR = 'individual_investor'
INDIVIDUAL_INVESTOR_WITH_INCOME_REQUIREMENT = 'individual_investor_with_income_requirement'
PROFESSIONAL_INDIVIDUAL_INVESTOR = 'professional_individual_investor'
CORPORATE_INVESTOR = 'corporate_investor'

LAST_FIRST_NAME_LANGUAGES = frozenset(["ko"])

SUBSCRIPTION_INVEST_TYPE_SURVEY = (
    ("401k", _("401k")),
    ("IRA", _("IRA")),
    ("MutualFunds", _("Mutual Funds")),
    ("Government", _("Government bonds")),
    ("Stocks", _("Stocks")),
    ("ExchangeTraded", _("Exchange-traded fund")),
    ("PTP", _("Peer-to-peer lending")),
)

# User Role
OWNER_ROLE = 'owner_role'
TENANT_ROLE = 'tenant_role'
INVESTOR_ROLE = 'investor_role'
CONSTRUCTOR_ROLE = 'constructor_role'
MANAGER_ROLE = 'manager_role'
AGENT_ROLE = 'agent_role'

USER_ROLES = (
    (OWNER_ROLE, _('Owner')),
    (TENANT_ROLE, _('Tenant')),
    (INVESTOR_ROLE, _('Investor')),
    (CONSTRUCTOR_ROLE, _('Constructor')),
    (MANAGER_ROLE, _('Manager')),
    (AGENT_ROLE, _('Agent')),
)

MANAGER = 'manager'
AGENCY = 'agency'

GROUP_CATEGORIES = (
    (MANAGER, _('Manager')),    # Investment Manager
    (AGENCY, _('Agency')),      # Real Estate Agency
)

INVESTMENT_ROLES = (
    (INVESTOR_ROLE, _('Investor')),
    (MANAGER_ROLE, _('Manager')),
)

INVESTMENT_ROLE_SET = frozenset([x for x, y in INVESTMENT_ROLES])

MANAGEMENT_ROLES = (
    (OWNER_ROLE, _('Owner')),
    (TENANT_ROLE, _('Tenant')),
    (AGENT_ROLE, _('Agent')),
)

MANAGEMENT_ROLE_SET = frozenset([x for x, y in MANAGEMENT_ROLES])

# management
LEASE_STATUS_CHOICES = (
    (ACTIVE, _(ACTIVE)),
    (PENDING, _(PENDING)),
    (COMPLETE, _(COMPLETE)),
)

LIVE_LEASE_STATUS = [PENDING, ACTIVE]


MAINTENANCE_STATUS_CHOICES = (
    (PENDING, _('PENDING')),
    (IN_PROGRESS, _('IN PROGRESS')),
    (DONE, _('DONE')),
    (WONT_FIX, _('WONT_FIX')),
)

MAINTENANCE_STATUS_LIST = {
    'resolved': [DONE, WONT_FIX],
    'unresolved': [PENDING, IN_PROGRESS],
}

RENT_PAYMENT_STATUSES = (
    (PENDING, _('PENDING')),
    (IN_PROGRESS, _('IN PROGRESS')),
    (COMPLETE, _('COMPLETE')),
    (FAILED, _('FAILED')),
    (CANCELED, _('CANCELED')),
)

RENT_PAYMENT_TYPE = (
    (RENT, _('RENT')),
    (DEPOSIT, _('DEPOSIT')),
    (UTILITY, _('UTILITY')),
    (OVERDUE, _('OVERDUE FEE')),
)

RENT_PAYMENT_METHOD_TYPE = (
    (CREDIT_CARD, _('CREDIT CARD')),
    (DEBIT_CARD, _('DEBIT CARD')),
    (ACH_DEBIT, _('ACH DEBIT')),
    (CASH, _('CASH')),
    (CHECKS, _('CHECKS')),
    (UNKNOWN, _('UNKNOWN')),
)

AGREEMENTS_TYPE = (
    ("tos", _("Terms of Service")),
    ("pp", _("Privacy Policy")),
    ("pay", _("Payment Policy")),
)

PAYMENT_TRANSFER_DESTINATION_ACCOUNT_TYPES = (
    ("stripe", _("Stripe")),
)

PAYMENT_TRANSFER_STATUSES = (
    (PENDING, _('PENDING')),
    (COMPLETE, _('COMPLETE')),
    (FAILED_NO_DESTINATION_ACCOUNT, _('FAILED_NO_DESTINATION_ACCOUNT')),
    (FAILED_OTHER_REASON, _('FAILED_OTHER_REASON')),
)

PAYMENT_LINKED_REASON_TYPE = (
    (OVERDUE, _('OVERDUE')),
    (FAILED, _('FAILED')),
)

# Investment
CONTRACT_TEMPLATE_TYPE = (
    (ATTACHMENT, _('Attachment')),
    (SIGNATURE, _('Signature Contract')),
)

INVESTMENT_STEP_STATUS_TYPE = (
    (PENDING, _('Pending')),
    (IN_PROGRESS, _('In Progress')),
    (COMPLETE, _('Complete')),
)

# Investment Workflow
INVESTMENT_WORKFLOW_HOUSE_FLIP = 'INVESTMENT_WORKFLOW_HOUSE_FLIP'
INVESTMENT_WORKFLOW_TYPE = (
    (INVESTMENT_WORKFLOW_HOUSE_FLIP, _('House Flipping Investment')),
)

SIG_REQUIRED_WAITING = 'SIG_REQUIRED_WAITING'
SIG_REQUIRED_PENDING = 'SIG_REQUIRED_PENDING'
SIG_REQUIRED_COMPLETE = 'SIG_REQUIRED_COMPLETE'
SIG_NOT_REQUIRED_PENDING = 'SIG_NOT_REQUIRED_PENDING'
SIG_NOT_REQUIRED_COMPLETE = 'SIG_NOT_REQUIRED_COMPLETE'

CONTRACT_STATUS_TYPE = (
    (SIG_REQUIRED_WAITING, _('Waiting for Others')),
    (SIG_REQUIRED_PENDING, _('Need to Sign')),
    (SIG_REQUIRED_COMPLETE, _('Completed')),
    (SIG_NOT_REQUIRED_PENDING, _('Unread')),
    (SIG_NOT_REQUIRED_COMPLETE, _('Read')),
)

# Administrator Page
MESSAGING_TEMPLATE_CATEGORY_CHOICES = (
    (ACCOUNT, _("Account")),
    (INVESTMENT, _("Investment")),
    (MANAGEMENT, _("Management")),
    (MARKETING, _("Marketing")),
    (SUPPORT, _("Support")),
    (PROPERTY, _("Property")),
    (PAYMENT_REQUEST, _("Payment Request")),
    (PAYMENT_REPORT, _("Payment Reqort")),
    (PAYMENT_OVERDUE, _("Payment Overdue")),
    (ETC, _("Etc.")),
)

RECORD_DATETIME_FORMAT = "%d-%b-%Y %H:%M:%S"
