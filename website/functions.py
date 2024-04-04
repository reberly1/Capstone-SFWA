import math

def find_cost(prin_list, month_pay, duration):
    """
    Description
    Calculates the total cost of a loan and total interest
    Parameters
    prin_list:    TYPE: Float[]
                  DESC: The principals/balances of all student loans taken
    month_pay:    TYPE: Float[]
                  DESC: A list stating how much is paid to each loan
    duration:     TYPE: Int[]
                  DESC: A list of how long each loan takes to repay in months
    Returns
    Float Tuple:  DESC: The total cost of the loan and total interest
    """
    total_int = 0
    print(prin_list, month_pay, duration)
    for i in range(len(prin_list)):
        if (len(month_pay) > 1):
            total_int += find_total_int(prin_list[i], month_pay[i], duration[0])
        elif (len(duration) > 1):
            total_int += find_total_int(prin_list[i], month_pay[0], duration[i])

        else:
            total_int += find_total_int(prin_list[i], month_pay[0], duration[0])
    total = total_int + sum(prin_list)
    return (total, total_int)

def find_num_months(principal, interest_rate, month_pay):
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
    """
    
    i = (interest_rate / 12)/100
    A = principal
    p = month_pay
    N = math.floor(-math.log(1 - (i*A)/p) / math.log(1 + i))
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

def debt_upon_graduation(prin_list, rates_list, types_list, months_grad, year_cost):
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
    months_grad:   TYPE: Int
                  DESC: The number of months a student has before graduation
    year_cost:    TYPE: Float
                  DESC: The user estimated cost of college per year

    Return
    Float Tuple:  DESC: The total cost and interest accrued upon graduation
    """

    #Calculates the estimated total debt upon graduation based on existing and future expenses
    total_int = 0
    for i in range(len(prin_list)):
        if (types_list[i] == 'unsubsidized'):
            total_int += (prin_list[i] * rates_list[i] * (math.floor(months_grad/12)))/100
    total = total_int + sum(prin_list) + ((math.floor(months_grad/12)) * year_cost)
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

def find_total_int(principal, month_pay, duration):
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

    Returns
    Float:        DESC: The total interest accrued across the loan's duration
    """

    return (month_pay * duration) - principal


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
