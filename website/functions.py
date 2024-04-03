import math

def find_num_months(principal, interest_rate, payment):
    #Finds number of months N to repay a loan with
    #N = -log(1-iA/p)/log(1+i) where i is interest rate A is principal and p in monthly payment
    i = (interest_rate / 12)/100
    A = principal
    p = payment
    N = -math.log(1 - (i*A)/p) / math.log(1 + i)
    return math.floor(N)

def find_monthly_payment(principal, interest_rate, duration):
    #Finds the minimum monthly payment for a loan with
    #EMI = [p x r x (1+r)^n]/[(1+r)^n-1]
    r = (interest_rate / 12)/100
    n = duration * 12  # convert years to months
    EMI = (principal * r * (1 + r)**n) / ((1 + r)**n - 1)
    return math.floor(EMI)

def debt_upon_graduation(principal_list, rates_list, types_list, years, term_cost):
    #Calculates the estimated total debt upon graduation based on existing and future expenses
    total_int = 0
    for i in range(len(principal_list)):
        if (types_list[i] == 'unsubsidized'):
            total_int += (principal_list[i] * rates_list[i] * years)/100
    total = total_int + sum(principal_list) + (years * term_cost)
    return (total, total_int)

def prin_to_int_ratio(total, total_int):
    #Calculates what percentage of payments contributed goes towards the principal 
    return (total-total_int)/total

def find_total_int(principal, payment, duration):
    #Calculates total interest the borrower has to pay
    #Formula is total payments - principal
    return (payment*duration*12) - principal

def minimum_salary(payment):
    #For a comfortable loan to income ratio, your income should be 3 times your monthly debt payment
    comfort_ratio = 3
    yearly = 12
    #Returns the yearly and monthly income needed to have a debt to income ratio of ~33%
    return (payment*comfort_ratio*yearly, payment*comfort_ratio)
