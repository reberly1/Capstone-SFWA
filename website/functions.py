import datetime
import math

#Calculates the number of months to pay for a loan with a given monthly payment
def time_to_pay(principals, interest_rates, categories, misc_fees, graduation, payment):
    total = sum(principals)
    total_int = misc_fees
    ext_fees = misc_fees
    current_principals = principals
    payment_duration = 0
    months_in_year = 12
    prin_int_ratios = []

    #While any fees, interest, or loans are unpaid
    while sum(current_principals) > 0 or ext_fees > 0:
        
        #Assumption that while the student has not graduated they are not accruing interest on subsidized loans 
        #They are also not contributing payments to unsubsidized loans.
        graduated = False
        if (graduation * months_in_year) <= payment_duration:
            graduated = True

        monthly_int = monthly_interest(current_principals, interest_rates, categories, graduated)

        ext_fees += monthly_int
        total_int += monthly_int
        payment_duration += 1

        current_payment = payment
        ext_fees -= current_payment

        if (ext_fees < 0):
            current_payment = ext_fees * -1
            ext_fees = 0
        else:
            current_payment = 0

        #Adds the percentage of the current payment left after fees and interest
        prin_int_ratios.append(current_payment/payment)

        current_principals, current_payment = deduct_principal(current_principals, current_payment)

    total_int += current_payment
    total += total_int
    return [total, total_int, payment_duration, prin_int_ratios]

#Calculates the minimum monthly payment to pay for a loan for a given length in years
def pay_for_time(principals, interest_rates, categories, misc_fees, graduation, payment_duration):
    return 0

def monthly_interest(principals, interest_rates, categories, graduated):
    interest = 0
    days_in_year = 365
    days_in_month = 30

    for i in range(len(principals)):

        #If the loan is unsubsidized or the student has graduated from college accrue interest
        if (categories[i] == 'unsubsidized' or graduated == True):
            simple_daily_rate = (interest_rates[i] / days_in_year) * principals[i]
            daily_to_monthly = (simple_daily_rate * days_in_month)
            interest += daily_to_monthly
    
    return interest

def deduct_principal(principals, current_payment):
    minimum = principals[0]
    min_index = 0

    #While there are current payments to deduct and principals to deduct from
    while current_payment != 0 and sum(principals) != 0:
        for i in range(len(principals)):
            #If there exists a smaller non-zero value than the minimum
            #Or if the minimum itself is zero, set a new minimum to the current value
            if (minimum > principals[i] and principals[i] > 0) or minimum == 0:
                minimum = principals[i]
                min_index = i
        
        #Deduct the smallest loan by the current payment
        principals[min_index] -= current_payment

        #If the current_payment is larger than the principal
        #Set the current_payment to the difference
        if principals[min_index] <= 0:
            current_payment = (principals[min_index] * -1)
            principals[min_index] = 0
        else:
            current_payment = 0

    return principals, current_payment

