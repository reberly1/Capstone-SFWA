def total_debt(principals, rates, subsidized, num_months, misc):
    total = 0
    for i in range(len(principals)):
        if (subsidized[i]) == 'unsubsidized':
            total += (principals[i] + interest(principals[i], rates[i], num_months[i]))
        else:
            total += principals[i]
    return (total + misc)

def interest(principal, int_rate, num_months):
    days = num_months * 30
    daily = (int_rate * principal)/365
    return days * daily

def repayment_time(payment, int_rate, misc, principal):
    int_accrued = 0
    num_months = 0
    total_int = 0

    #Pay any outstanding fees or interest first
    while (misc != 0):
        int_accrued += interest(principal, int_rate, 1)
        num_months += 1
        misc -= payment
        if (misc <= 0):
            int_accrued += misc
            misc = 0
    
    while (principal != 0):
        int_accrued += interest(principal, int_rate, 1)
        num_months += 1
        while (int_accrued != 0): 
            int_accrued -= payment
            if (int_accrued < 0):
                principal += int_accrued
                int_accrued = 0

    return 0

def prin_ratio(payment, mon_int):
    return ((payment - mon_int)/payment)

def pay_rate(int_rate, misc, principal, num_months):
    return 0

def total_interest():
    return 0

def month_count(terms):
    return 0