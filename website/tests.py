from functions import *
import math

def again():
    principal = 30000
    interest_rates = 7
    payment = 348
    print(find_num_months(principal, interest_rates, payment))
    print(find_monthly_payment(principal,interest_rates,10))
    print(debt_upon_graduation([principal,principal],[interest_rates,interest_rates],['unsubsidized','subsidized'],2,10000))
if __name__ == '__main__':
    again()