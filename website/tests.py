from functions import *
import math

#Tests if the calculator can correctly calculate to answer the question
#How long does it take to repay a loan at a specified rate?
def simple():
    principal = [30000]
    interest_rates = [.07]
    categories = ['unsubsidized']
    misc_fees = 0
    graduation = 0
    payment = 348.33
    results = time_to_pay(principal, interest_rates, categories, misc_fees, graduation, payment)
    print("total: ",results[0])
    print("total interest: ",results[1])
    print("payment length in months: ",results[2])
    print("principal to interest ratios: ",results[3])

    return 0

if __name__ == '__main__':
    simple()