from functions import *
import math
import unittest

class TestGeneralScenario(unittest.TestCase):
    def test_TDUG(self):   
        principal = [30000]
        interest = [7]
        loantype = ['unsubsidized']
        grad = 2 * 12
        term = 10000 
        TDUG = debt_upon_graduation(principal, interest, loantype, grad, term)[0]
        self.assertEqual(TDUG, 54200)

    def test_duration_calc(self):
        principal = 30000
        interest = 7
        monthly = 500
        duration = find_num_months(principal, interest, monthly)
        self.assertEqual(duration, 74)

    def test_month_pay_calc(self):
        principal = 30000
        interest = 7
        duration = 74
        month_pay = find_monthly_payment(principal, interest, duration)
        self.assertAlmostEqual(month_pay, 500, 0)

        """
        #Calculate the total cost and interest for both ideals for comparison
        (ID_total, ID_int) = find_cost(principal, monthly_rate, [duration])
        (IP_total, IP_int) = find_cost(principal, [monthly], repayment_duration)
        print('ID',ID_total, ID_int)
        print('IP',IP_total, IP_int)

        #Calculate the percentage of payments going towards the principal for each ideal
        ID_per = prin_to_int_ratio(ID_total, ID_int)
        IP_per = prin_to_int_ratio(IP_total, IP_int)

        #Calculate the recommended salary for each ideal scenario
        ID_salary = minimum_salary(monthly*len(principal))
        IP_salary = minimum_salary(sum(monthly_rate))
        """

if __name__ == '__main__':
    unittest.main()