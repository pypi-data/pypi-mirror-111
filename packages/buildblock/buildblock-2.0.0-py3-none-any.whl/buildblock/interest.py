import datetime
import math

from dateutil.relativedelta import relativedelta

LATE_INTEREST_RATE = 0.24
INCOMETAX_RATE = 0.25
LOCALTAX_RATE = 0.1
TRIGGER_CLAUSE_RATE = 0.24


def _convert_date(input_date):
    if isinstance(input_date, datetime.date):
        converted_date = input_date
        input_date = str(input_date.year) + "-" + str(input_date.month) + "-" + str(input_date.day)

    converted_date = datetime.datetime.strptime(input_date, '%Y-%m-%d')
    return converted_date.year, converted_date.month, converted_date.day


def _calculate_all_taxes(
    monthly_pretax_interest, index, days_in_year, days_in_month, input_date, lateTF=False
):
    multiplier = (1 + LATE_INTEREST_RATE / days_in_year) if lateTF else 1
    cumulative_input_date = \
        math.ceil(monthly_pretax_interest / days_in_month * index * multiplier)
    # This value will be 0 anyways if index == 1
    cumulative_prev_input_date = \
        math.ceil(monthly_pretax_interest / days_in_month * (index - 1) * multiplier)

    # pre-tax (round up to the nearest whole number)
    dailyPreTaxInterest = cumulative_input_date - cumulative_prev_input_date
    # income and local tax (round down to the nearest 10)
    dailyIncomeTax = \
        cumulative_input_date * INCOMETAX_RATE // 10 * 10 \
        - cumulative_prev_input_date * INCOMETAX_RATE // 10 * 10
    dailyLocalTax = \
        cumulative_input_date * INCOMETAX_RATE * LOCALTAX_RATE // 10 * 10 \
        - cumulative_prev_input_date * INCOMETAX_RATE * LOCALTAX_RATE // 10 * 10
    # daily tax
    dailyTax = dailyIncomeTax + dailyLocalTax
    # after-tax
    dailyAfterTaxInterest = dailyPreTaxInterest - dailyTax

    return dailyPreTaxInterest, dailyTax, dailyAfterTaxInterest, input_date


def normal_and_late_interest(investment, input_date, lateTF):
    input_date_year, input_date_month, input_date_day = _convert_date(input_date)
    first_date_year, first_date_month, first_date_day = _convert_date(investment.first_date)
    days_in_year = (datetime.datetime(input_date_year+1, 1, 1) - datetime.datetime(input_date_year, 1, 1)).days

    date_modified = datetime.datetime.strptime(input_date, '%Y-%m-%d') - datetime.timedelta(days=first_date_day-1)
    last_date_modified = (datetime.datetime.strptime(investment.last_date, '%Y-%m-%d')
                          - datetime.timedelta(days=first_date_day-1))

    if date_modified.year == last_date_modified.year and date_modified.month == last_date_modified.month:
        days_in_month = last_date_modified.day
    else:
        # before December
        if date_modified.month < 12:
            days_in_month = (
                datetime.datetime(date_modified.year, date_modified.month+1, 1)
                - datetime.datetime(date_modified.year, date_modified.month, 1)
            ).days
        else:
            days_in_month = 31   # only for December

    index = date_modified.day

    # pre-tax interest, interest income tax, local tax
    # round up to the nearest whole number
    monthly_pretax_interest = math.ceil(
        investment.principal * investment.interest_rate / days_in_year * days_in_month
    )
    return _calculate_all_taxes(monthly_pretax_interest, index, days_in_year, days_in_month, input_date, lateTF)


# USE FOR NEXT PRODUCT
# def trigger_clause(investment, input_date):
#     input_date_year, input_date_month, input_date_day = _convert_date(input_date)
#     last_date_year, last_date_month, last_date_day = _convert_date(investment.last_date)
#     days_in_year = (datetime.datetime(input_date_year+1, 1, 1) - datetime.datetime(input_date_year, 1, 1)).days
#     if input_date_year == last_date_year and input_date_month == last_date_month:
#         days_in_month = last_date_day
#     else:
#         if input_date_month < 12:   # before December
#             days_in_month = (
#                 datetime.datetime(input_date_year, input_date_month+1, 1) \
#                 - datetime.datetime(input_date_year, input_date_month, 1)
#             ).days
#         else:
#             days_in_month = 31   # only for December
#     index = input_date_day
#     monthly_pretax_interest = math.ceil(
#         investment.principal * TRIGGER_CLAUSE_RATE / days_in_year * days_in_month
#     )
#     return _calculate_all_taxes(monthly_pretax_interest, index, days_in_year, days_in_month)


def get_interest(investment, input_date, lateTF=False, triggerClauseTF=False):
    if input_date > investment.last_date:
        return 'Something wrong'
    if not triggerClauseTF:
        return normal_and_late_interest(investment, input_date, lateTF)


class InvestmentCal(object):

    def __init__(self, first_date, last_date, interest_rate):
        # 날짜체크
        if isinstance(first_date, datetime.date):
            self.first_date_datetimeform = first_date
        else:
            if '-' in first_date:
                s_year, s_month, s_day = map(int, first_date.split('-'))
            elif ',' in first_date:
                s_year, s_month, s_day = map(int, first_date.split(','))
            elif '/' in first_date:
                s_year, s_month, s_day = map(int, first_date.split('/'))
            elif '.' in first_date:
                s_year, s_month, s_day = map(int, first_date.split('.'))
            self.first_date_datetimeform = datetime.date(s_year, s_month, s_day)  # 투자 시작일

        if isinstance(last_date, datetime.date):
            self.last_date_datetimeform = last_date
        else:
            if '-' in last_date:
                s_year, s_month, s_day = map(int, last_date.split('-'))
            elif ',' in last_date:
                s_year, s_month, s_day = map(int, last_date.split(','))
            elif '/' in last_date:
                s_year, s_month, s_day = map(int, last_date.split('/'))
            elif '.' in last_date:
                s_year, s_month, s_day = map(int, last_date.split('.'))
            self.last_date_datetimeform = datetime.date(s_year, s_month, s_day)  # 투자 시작일

        date_diff = self.last_date_datetimeform - self.first_date_datetimeform

        self.date_delta = date_diff.days
        self.date_list = []
        date_list = [self.first_date_datetimeform + datetime.timedelta(days=x) for x in range(0, self.date_delta)]
        for date_one in date_list:
            self.date_list.append(date_one.strftime("%Y-%m-%d"))

        self.interest_rate = interest_rate
        self.first_date = self.first_date_datetimeform.strftime("%Y-%m-%d")
        self.last_date = self.last_date_datetimeform.strftime("%Y-%m-%d")

    def InterestAllDayArray(self, principal):
        self.principal = principal
        dayArray = []
        for date_one in self.date_list:
            dayOne = get_interest(self, date_one)
            dayArray.append(dayOne)
        return dayArray

    def InterestAllDaySum(self, principal, ex_rate=1):
        ex_rate = float(ex_rate)
        self.principal = float(principal) / ex_rate if ex_rate > 0 else 0
        dayArray = []
        for date_one in self.date_list:
            dayOne = get_interest(self, date_one)
            dayArray.append(dayOne)
        daySum = [0, 0, 0]
        for dayOne in dayArray:
            daySum[0] += dayOne[0] * ex_rate
            daySum[1] += dayOne[1] * ex_rate
            daySum[2] += dayOne[2] * ex_rate
        return daySum

    def InterestSomeDaySum(self, principal, some_date):
        self.principal = principal
        dayArray = []
        for date_one in self.date_list:
            dayOne = get_interest(self, date_one)
            dayArray.append(dayOne)
        daySum = [0, 0, 0]
        for dayOne in dayArray:
            if dayOne[3] > some_date:
                break
            daySum[0] += dayOne[0]
            daySum[1] += dayOne[1]
            daySum[2] += dayOne[2]
        return daySum

    def InterestToDaySum(self, principal, ex_rate=1):
        ex_rate = float(ex_rate)
        self.principal = float(principal) / ex_rate if ex_rate > 0 else 0
        today_datetimeform = datetime.datetime.today()
        today = today_datetimeform.strftime("%Y-%m-%d")

        dayArray = []
        for date_one in self.date_list:
            dayOne = get_interest(self, date_one)
            dayArray.append(dayOne)
        daySum = [0, 0, 0]
        for dayOne in dayArray:
            if dayOne[3] > today:
                break
            daySum[0] += dayOne[0] * ex_rate
            daySum[1] += dayOne[1] * ex_rate
            daySum[2] += dayOne[2] * ex_rate
        return daySum

    def InterestNextMonthSum(self, principal, invest_month, ex_rate=1):
        ex_rate = float(ex_rate)
        self.principal = float(principal) / ex_rate if ex_rate > 0 else 0
        first_date_datetimeform = self.first_date_datetimeform
        today_datetimeform = datetime.datetime.today().date()
        start_month_date_datetimeform = first_date_datetimeform - relativedelta(days=1)
        end_month_date_datetimeform = first_date_datetimeform + relativedelta(months=1)

        for m in range(invest_month + 1):
            if start_month_date_datetimeform < today_datetimeform and end_month_date_datetimeform > today_datetimeform:
                break
            start_month_date_datetimeform = start_month_date_datetimeform + relativedelta(months=1)
            end_month_date_datetimeform = end_month_date_datetimeform + relativedelta(months=1)

        start_date = start_month_date_datetimeform.strftime("%Y-%m-%d")
        end_date = end_month_date_datetimeform.strftime("%Y-%m-%d")

        dayArray = []
        usedDay = 0
        for date_one in self.date_list:
            if start_date < date_one and end_date > date_one:
                usedDay += 1
                dayOne = get_interest(self, date_one)
                dayArray.append(dayOne)

        # 0: Before Tax interest amount
        # 1: Tax amount
        # 2: After Tax interest amount
        # 3: Interest Payment Date
        # 4: Used Day
        daySum = [0, 0, 0]
        for dayOne in dayArray:
            daySum[0] += dayOne[0] * ex_rate
            daySum[1] += dayOne[1] * ex_rate
            daySum[2] += dayOne[2] * ex_rate
        daySum.append(end_month_date_datetimeform)
        daySum.append(usedDay)
        return daySum

    def InterestAllMonthlySum(self, principal, invest_month, ex_rate=1):
        ex_rate = float(ex_rate)
        self.principal = float(principal) / ex_rate if ex_rate > 0 else 0
        first_date_datetimeform = self.first_date_datetimeform
        start_month_date_datetimeform = first_date_datetimeform - relativedelta(days=1)
        end_month_date_datetimeform = first_date_datetimeform + relativedelta(months=1)

        mounthSum = []
        for m in range(invest_month + 1):
            start_date = start_month_date_datetimeform.strftime("%Y-%m-%d")
            end_date = end_month_date_datetimeform.strftime("%Y-%m-%d")

            dayArray = []
            usedDay = 0
            for date_one in self.date_list:
                if start_date < date_one and end_date > date_one:
                    usedDay += 1
                    dayOne = get_interest(self, date_one)
                    dayArray.append(dayOne)

            # 0: Before Tax interest amount
            # 1: Tax amount
            # 2: After Tax interest amount
            # 3: Interest Payment Date
            # 4: Used Day
            daySum = [0, 0, 0]
            for dayOne in dayArray:
                daySum[0] += dayOne[0] * ex_rate
                daySum[1] += dayOne[1] * ex_rate
                daySum[2] += dayOne[2] * ex_rate
            if daySum[0] > 0:
                daySum.append(end_month_date_datetimeform)
                daySum.append(usedDay)
                mounthSum.append(daySum)
            # 한달 추가
            start_month_date_datetimeform = start_month_date_datetimeform + relativedelta(months=1)
            end_month_date_datetimeform = end_month_date_datetimeform + relativedelta(months=1)
        return mounthSum

    def InterestNextMonthSumToday(self, principal, invest_month):
        self.principal = principal
        first_date_datetimeform = self.first_date_datetimeform
        today_datetimeform = datetime.datetime.today().date() - relativedelta(days=1)
        start_month_date_datetimeform = first_date_datetimeform - relativedelta(days=1)
        end_month_date_datetimeform = first_date_datetimeform + relativedelta(months=1)

        for m in range(invest_month + 1):
            if start_month_date_datetimeform < today_datetimeform and end_month_date_datetimeform > today_datetimeform:
                break
            start_month_date_datetimeform = start_month_date_datetimeform + relativedelta(months=1)
            end_month_date_datetimeform = end_month_date_datetimeform + relativedelta(months=1)

        start_date = start_month_date_datetimeform.strftime("%Y-%m-%d")
        end_date = end_month_date_datetimeform.strftime("%Y-%m-%d")

        dayArray = []
        usedDay = 0
        for date_one in self.date_list:
            if start_date < date_one and end_date > date_one:
                usedDay += 1
                dayOne = get_interest(self, date_one)
                dayArray.append(dayOne)

        daySum = [0, 0, 0]
        for dayOne in dayArray:
            daySum[0] += dayOne[0]
            daySum[1] += dayOne[1]
            daySum[2] += dayOne[2]
        daySum.append(end_month_date_datetimeform)
        daySum.append(usedDay)
        return daySum
