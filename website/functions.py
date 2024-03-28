import datetime

def total_debt(principals, rates, subsidized, term, misc, future):
    total = 0
    num_months = month_count(term)

    #For each loan
    for i in range(len(principals)):
        #Calculate the amount of interest from unsubsidized loans and include with that loan's principal
        if (subsidized[i]) == 'unsubsidized':
            total += (principals[i] + interest(principals[i], rates[i], num_months))
        else:
            #If the loan is subsidized only include the principal
            total += principals[i]

    return (total + misc)

def interest(principal, int_rate, num_months):
    days = num_months * 30
    daily = (int_rate * principal)/365
    return days * daily

def repayment_time(payment, int_rate, misc, principal, future):
    int_accrued = 0
    num_months = 0
    total_int = 0

    #Pay any outstanding fees or interest first
    while (misc != 0):
        int_accrued += interest(principal, int_rate, 1)
        total_int += interest(principal, int_rate, 1)
        num_months += 1
        misc -= payment

        #Apply overpay to the interest accrued
        if (misc <= 0):
            int_accrued += misc
            misc = 0
    
    #Pay the principal and any ongoing accruing interest
    while (principal > 0):
        int_accrued += interest(principal, int_rate, 1)
        total_int += interest(principal, int_rate, 1)
        num_months += 1

        #Pay off any existing interest first
        if (int_accrued > 0): 
            int_accrued -= payment
            #If the interest is overpayed, apply the difference to the principal
            if (int_accrued < 0):
                principal += int_accrued
                int_accrued = 0
        
        #Pay to principal if there are no fees or interest to consider
        else:
            principal -= payment

    #Pay for any anticipated future loans
    while (future > 0):
        num_months += 1
        future -= payment

    #Return length in months to repay loan and interest accrued in that time frame
    return [num_months, total_int]

def prin_ratio(payment, mon_int):
    #Returns what percentage of a monthly payment goes to principal
    return ((payment - mon_int)/payment)

def pay_rate(rates, misc, principals, future, num_months):
    #Note does not yet factor in the adjusted interest for when the principal is being paid off
    total_interest = 0
    total_principal = 0
    for i in range(len(principals)):
        total_interest += interest(principals[i], rates[i], num_months)
        total_principal += principals[i]

    total = total_interest + misc + total_principal + future

    return total/num_months

def month_count(terms):
    current_month = datetime.datetime.now().month
    months = 0
    
    #Person not currently attending school
    if (terms == 0):
        return 0

    #For each school year add 12 months
    while (terms > 1):
        terms -= 2
        months += 12

    #Calculate the difference between the passing months and their graduate month
    if (current_month <= 5 and terms == 1):
        months += (5 - current_month)

    elif (current_month <= 5 and terms == 0):
        months -= current_month
    
    elif (current_month > 5 and terms == 0):
        months -= (current_month - 5)
    else:
        months += (12 - current_month)
    
    return months

