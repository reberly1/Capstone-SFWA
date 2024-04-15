import math
import datetime

def find_cost(prin_list, rates_list, month_pay, duration):
    """
    Description
    Calculates the total cost of a loan and total interest
    Parameters
    prin_list:    TYPE: Float[]
                  DESC: The principals/balances of all student loans taken
    rates_list:   TYPE: Float[]
                  DESC: The interest rates of all student loans taken
    month_pay:    TYPE: Float[]
                  DESC: A list stating how much is paid to each loan
    duration:     TYPE: Int[]
                  DESC: A list of how long each loan takes to repay in months
    Returns
    Float Tuple:  DESC: The total cost of the loan and total interest
    """
    total_int = 0
    for i in range(len(prin_list)):
        if (len(month_pay) > 1):
            total_int += calc_int(prin_list[i], month_pay[i], duration[0], rates_list[i])
        elif (len(duration) > 1):
            total_int += calc_int(prin_list[i], month_pay[0], duration[i], rates_list[i])

        else:
            total_int += calc_int(prin_list[i], month_pay[0], duration[0], rates_list[i])
    total = total_int + sum(prin_list)
    return (total, total_int)

def find_num_months(principal, int_rate, month_pay):
    """
    Description
    Calculates the number of months N to repay a loan with
    N = -log(1-iA/p)/log(1+i) 
    where i is interest rate A is principal and p in monthly payment
    then converts the value to years

    Parameters
    principal:    TYPE: Float
                  DESC: Principal or balance of the loan
    int_rate:     TYPE: Float
                  DESC: Interest rate of the loan
    month_pay:    TYPE: Float
                  DESC: Monthly payment towards a given student loan

    Returns
    Int           DESC: The number of months needed to pay back the loan
                        or -12000 indicating it cannot be repaid
    """
    
    i = (int_rate / 12)/100
    A = principal
    p = month_pay
    if (1 > (i*A)/p):
        N = math.ceil(-math.log(1 - (i*A)/p) / math.log(1 + i))
    else:
        N = -12000
    return N

def find_monthly_payment(principal, int_rate, duration):
    """
    Description
    Calculates the monthly payment required to pay off the loan
    using the formula EMI = [p x r x (1+r)^n]/[(1+r)^n-1]

    Parameters
    principal:    TYPE: Float
                  DESC: Principal or balance of the loan
    int_rate:     TYPE: Float
                  DESC: Interest rate of the loan
    duration:     TYPE: INT
                  DESC: The lifespan of the loan in months

    Returns
    Float         DESC: The monthly payment required to afford the loan
    """
    
    r = (int_rate / 12)/100
    n = duration 
    EMI = (principal * r * (1 + r)**n) / ((1 + r)**n - 1)
    return EMI

def debt_upon_graduation(prin_list, rates_list, types_list, years_grad, year_cost):
    """
    Description
    Estimates the total loans accrued throughout college including interest

    Parameters
    prin_list:    TYPE: Float[]
                  DESC: The principals/balances of all student loans taken
    rates_list:   TYPE: Float[]
                  DESC: The interest rates of all student loans taken
    types_list:   TYPE: str[]
                  DESC: The unsubsidized or subsidized statuses of all loans
    years_grad:   TYPE: Int
                  DESC: The number of years a student has before graduation
    year_cost:    TYPE: Float
                  DESC: The user estimated cost of college per year

    Return
    Float Tuple:  DESC: The total cost and interest accrued upon graduation
    """

    #Calculates the estimated total debt upon graduation based on existing and future expenses
    total_int = 0
    for i in range(len(prin_list)):
        if (types_list[i] == 'unsubsidized'):
            total_int += (prin_list[i] * rates_list[i] * (math.ceil(years_grad/12)))/100
    total = total_int + sum(prin_list) + ((math.ceil(years_grad/12)) * year_cost)
    return (total, total_int)

def prin_to_int_ratio(total, total_int):
    """
    Description
    Calculates the percentage of payments contributed to the principal

    Parameters
    total:        TYPE: Float
                  DESC: The total cost of a loan, principal + interest
    total_int:    TYPE: Float
                  DESC: The total interest of a loan

    Returns
    Float:        DESC: The percentage of the loan that is the principal
    """

    #Calculates what percentage of payments contributed goes towards the principal 
    return (total-total_int)/total

def calc_int(principal, month_pay, duration, int_rate):
    """
    Description
    Calculates the total interest accrued over the duration of a loan
    using the formula, I = 

    Parameters
    principal:    TYPE: Float
                  DESC: Total loan balance or principal
    month_pay:     TYPE: Float
                  DESC: Monthly payment made towards loan
    duration:     TYPE: Float
                  DESC: Total time spent in months paying off the loan
    int_rate:     TYPE: Float
                  DESC: Interest rate of the loan

    Returns
    Float:        DESC: The total interest accrued across the loan's duration
    """
    temp_prin = principal
    true_rate = int_rate/100
    temp_monthly = 0
    interest = 0
    for i in range(int(duration)):
        temp_interest = (temp_prin * (true_rate/365) * 30.437)
        temp_monthly = (month_pay - temp_interest) 
        temp_prin -= temp_monthly
        interest += temp_interest

    return interest 

def minimum_salary(month_pay):
    """
    Description
    Calculates the yearly and monthly income required to have a DTI or
    debt to income ratio of 33% for a given monthly loan paymen

    Parameters
    month_pay:    TYPE: Float, 
                  DESC: monthly payment towards a given student loan

    Returns
    Float Tuple:  DESC: Contains the yearly/monthly income to have a DTI of 33%
    """

    comfort_ratio = 3
    yearly = 12
    return (month_pay*comfort_ratio*yearly, month_pay*comfort_ratio)

def int_since(loan_dates, loan_int_rates, loan_principals, last_pay_date):
    int_accrued = []

    for i in range(len(loan_dates)):
        days_since_disbursement = int((last_pay_date - loan_dates[i]).days)
        int_for_loan = (loan_int_rates[i]/36500) * days_since_disbursement * loan_principals[i]
        int_accrued.append(int_for_loan)

    return int_accrued

def apply_adjustments(loan_principals, loan_fees, int_accured, amounts, loan_choice):
    #Apply interest to outstanding fees and interest
    for i in range(len(int_accured)):
        loan_fees[i] += int_accured[i]

    for i in range(len(amounts)):
        payment = amounts[i]
        loan_index = loan_choice[i]

        #Pay off fees and interest first
        loan_fees[loan_index] -= payment

        #Applies the difference to the principal
        if loan_fees[loan_index] < 0:
            loan_principals[loan_index] += loan_fees[loan_index]
            loan_fees[loan_index] = 0

        #If the given loan was paid off set it to 0
        if loan_principals[loan_index] < 0:
            loan_principals[loan_index] = 0

    return (loan_principals, loan_fees)

