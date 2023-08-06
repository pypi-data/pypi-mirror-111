from enum import Enum

from django.utils.translation import ugettext_lazy as _


class ModelChoicesEnum(Enum):
    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]


class BankEnum(ModelChoicesEnum):
    CHASE = _("Chase Bank")
    BOA = _("Bank of America")
    WELLS_FARGO = _("Wells Fargo")
    US_BANK = _("U.S. Bank")
    BBVA_COMPASS = _("BBVA Compass")
    CAPITAL_ONE = _("Capital One Bank")
    BOW = _("Bank of the west")
    SANTANDER_CONSUMER = _("Santander Consumer Bank")
    CITI = _("Citi Bank")
    HUNTINGTON = _("Huntington Bank")
    MT = _("M&T Bank")
    WOODFOREST = _("Woodforest National Bank")
    CITIZENS = _("Citizens Bank")
    FIFTH_THIRD = _("Fifth Third Bank")
    KEY = _("Key Bank")
    TD = _("TD Bank")
    SUN_TRUST = _("Sun Trust Bank")
    REGIONS = _("Regions Bank")
    PNC = _("PNC Bank")
    BBT = _("BB&T Bank")
    FIRST_NATIONAL = _("First National Bank")
    BMO_HARRIS = _("BMO Harris Bank")
    FIRST_CITIZENS = _("First Citizens Bank")
    COMERICA = _("Comerica Bank")
    PEOPLES_UNITED = _("People's United Bank")
    UMPQUA = _("Umpqua Bank")
    OZK = _("Bank of the Ozarks")
    HSBC = _("HSBC")
    MUFG = _("MUFG Union Bank")
    ARVEST = _("Arvest Bank")
    CHEMICAL = _("Chemical Bank")
    TCF = _("TCF Bank")
    SYNOVUS = _("Synovus Bank")
    BANCORP_SOUTH = _("Bancorp South Bank")
    WASHINTON_FEDERAL = _("Washington Federal")
    ASSICIATED = _("Assiciated Bank")
    IBERIA = _("Iberiabank")
    VALLEY = _("Valley National Bank")
    WHITNEY = _("Whitney Bank")
    TRUST_MARK = _("Trust Mark National Bank")
    GREAT_WESTERN = _("Great Western Bank")
    COLUMBIA_STATE = _("Columbia State Bank")
    CENTENNIAL = _("Centennial Bank")
    OLD_NATIONAL = _("Old National Bank")
    SOUTH_STATE = _("South State Bank")
    FIRST_TENNESSEE = _("First Tennessee Bank")
    NBT = _("NBT Bank")
    RENASANT = _("Renasant Bank")
    BANNER = _("Banner Bank")
    WEBSTER = _("Webster Bank")
    SIMMONS = _("Simmons Bank")
    UNITED = _("United Bank")
    FROST = _("Frost Bank")
    WESBANCO = _("WesBanco Bank")
    COMMERCE = _("Commerce Bank")
    INVESTORS = _("Investors Bank")
    TRUSTCO = _("TrustCo Bank")
    FIRST_COMMONWEALTH = _("First Commonwealth Bank")
    STERLING = _("Sterling National Bank")
    CARTER = _("Carter Bank And Trust")
    FIRST_MIDWEST = _("First Midwest Bank")
    FIRST = _("First Bank")
    PARK_NATIONAL = _("Park National Bank")
    PINNACLE = _("Pinnacle Bank")
    GLACIER = _("Glacier Bank")
    FULTON = _("Fulton Bank")
    RABO = _("Rabobank")
    ZIONS = _("Zions Bank")
    FIRST_MERCHANTS = _("First Merchants Bank")
    EAST_WEST = _("East West Bank")
    FIRST_INTERSTATE = _("First Interstate Bank")
    UNION = _("Union Bank and Trust")
    GREAT_SOUTHERN = _("Great Southern Bank")
    FLAGSTER = _("Flagster Bank")


class AccountTransactionCategoryEnum(ModelChoicesEnum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    RETURN = "return"
    INVEST = "invest"


class AccountTransactionEntityTypeEnum(ModelChoicesEnum):
    UNKNOWN = "Unknown"
    USER = "User"
    COMPANY = "Company"


class TeamMemberDepartment(ModelChoicesEnum):
    EXECUTIVE = "Executive"
    ADVISOR = "Advisor"
    TECH_ENGINEERING = "Tech Engineering"
    MARKETING = "Biz Dev / Marketing"
    CONSTRUCTION = "Construction"
