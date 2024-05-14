"""
Websites Referenced:
[1] https://www.geeksforgeeks.org/how-to-use-flask-session-in-python-flask/
[2] https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH
[3] https://github.com/CoreyMSchafer/code_snippets/blob/master/Python/Flask_Blog/02-Templates/templates/layout.html
[4] https://www.w3schools.com/html/html_forms.asp
[5] https://www.geeksforgeeks.org/how-to-create-a-form-dynamically-with-the-javascript/?ref=ml_lbp
[6] https://www.w3schools.com/jsref/jsref_toisostring.asp
[7] https://www.programiz.com/python-programming/datetime/strptime
[8] https://www.geeksforgeeks.org/saving-a-pandas-dataframe-as-a-csv/
[9] https://www.w3schools.com/html/html_tables.asp
[10] https://www.chartjs.org/docs/latest/general/accessibility.html
[11] https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/file
[12] https://www.mongodb.com/docs/manual/reference/method/db.collection.find/
[13] https://brightdata.com/blog/how-tos/web-scraping-with-python
[14] https://umbc.academicworks.com/
[15] https://smartasset.com/student-loans/student-loan-calculator
[16] https://www.calculator.net/student-loan-calculator.html
[17] https://studentaid.gov/understand-aid/types/loans/interest-rates
[18] https://money.stackexchange.com/questions/64639/how-to-calculate-the-number-of-months-until-a-loan-is-paid-off-given-principal
[19] https://www.investopedia.com/terms/e/equated_monthly_installment.asp
"""

from flask import Flask, render_template, request, session, redirect
from functions import *
from database import *
import datetime
import pandas
import numpy as np
from scraper import *

app = Flask(__name__)
app.secret_key = "Adjust the key as needed"


#<------------------------COMPONENT 1 CALCULATOR SUITE------------------------>
"""
References Applicable to Section:
[1] https://www.geeksforgeeks.org/how-to-use-flask-session-in-python-flask/
[2] https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH
[3] https://github.com/CoreyMSchafer/code_snippets/blob/master/Python/Flask_Blog/02-Templates/templates/layout.html
[4] https://www.w3schools.com/html/html_forms.asp
[5] https://www.geeksforgeeks.org/how-to-create-a-form-dynamically-with-the-javascript/?ref=ml_lbp
[15] https://smartasset.com/student-loans/student-loan-calculator
[16] https://www.calculator.net/student-loan-calculator.html
[17] https://studentaid.gov/understand-aid/types/loans/interest-rates
[18] https://money.stackexchange.com/questions/64639/how-to-calculate-the-number-of-months-until-a-loan-is-paid-off-given-principal
[19] https://www.investopedia.com/terms/e/equated_monthly_installment.asp
"""

#GUIDED CALCULATOR MENU
@app.route('/guided')
@app.route('/')
def guided():
    """
    Description: Displays the start menu for the guided calculator suite
    using guided.html
    """

    return render_template('guided.html',title='Guided')

#PAGE 1 of GUIDED CALCULATOR SUITE: LOANS PAGE
@app.route('/guided/loans', methods=['GET','POST'])
def loans():
    """
    Description: Extracts the list of existing loans from the user and sets
    them in the session for calculations, then sends them to the next page
    """

    if request.method == "POST":
        session['principals'] = request.form.getlist('principal[]')
        session['interests'] = request.form.getlist('interest[]')
        session['loan_types'] = request.form.getlist('loan_type[]')
        return redirect('/guided/terms')
    
    return render_template('guided_loans.html',title='Guided Loans')

#PAGE 2 of GUIDED CALCULATOR SUITE: TERMS PAGE
@app.route('/guided/terms', methods=['GET','POST'])
def terms():
    """
    Description: Extracts the years until graduation and cost per year 
    from the user and sets them in the session for calculations, 
    then sends them to the next page
    """

    if request.method == "POST":
        session['year_grad'] = request.form['year_grad']
        session['term_cost'] = request.form['term_cost']
        return redirect('/guided/estimates')
    
    return render_template('guided_terms.html',title='Guided Terms')

#PAGE 3 of GUIDED CALCULATOR SUITE: IDEAL ESIMATES PAGE
@app.route('/guided/estimates', methods=['GET','POST'])
def estimates():
    """
    Description: Extracts how much the user wants to pay per month
    towards loans and how quickly the user want to pay off their loans 
    and sets them in the session for calculations, 
    then sends them to the report page where the result is diplayed
    """

    if request.method == "POST":
        session['month_pay'] = request.form['month_pay']
        session['duration'] = request.form['duration']
        return redirect('/report')
    
    return render_template('guided_estimates.html',title='Guided Estimates')

#UNGUIDED CALCULATOR SUITE
@app.route('/unguided', methods=['GET','POST'])
def unguided():
    """
    Description: Extracts all variables needed for the guided calculation
    in a single page for simplicity in the event the user is familiar with
    the process already, then sends the user to the report once information
    is submitted
    """

    if request.method == "POST":
        session['principals'] = request.form.getlist('principal[]')
        session['interests'] = request.form.getlist('interest[]')
        session['loan_types'] = request.form.getlist('loan_type[]')
        session['year_grad'] = request.form['year_grad']
        session['term_cost'] = request.form['term_cost']
        session['month_pay'] = request.form['month_pay']
        session['duration'] = request.form['duration']
        return redirect('/report')
    
    return render_template("unguided.html",title='Unguided')

#REPORT PAGE   
@app.route('/report', methods=['GET','POST'])
def report():
    """
    Description: Calculates the results of the report then displays then to the
    user. The results collected are described below
    """
    
    #Collects all calculator input from session for computation and display
    #numeric values are typecasted from string to float
    principal = [float(principal) for principal in session['principals']]
    interest = [float(interest) for interest in session['interests']]
    loantype = session['loan_types']
    monthly = float(session['month_pay'])
    grad = float(session['year_grad']) * 12
    term = float(session['term_cost'])   
    duration = float(session['duration']) * 12
    
    #Calculates Total Debt Upon Graduation
    (grad_debt, grad_interest) = debt_upon_graduation(principal, interest, loantype, grad, term)

    #The number of months to pay off each loan assuming a flat user 
    #provided rate (monthly)
    repayment_duration = []

    #The monthly payment to pay off each loan assuming all have to be paid off 
    #by the same deadline (duration)
    monthly_rate = []
    for i in range(len(principal)):
        #Calculate Duration to Pay back the given loan at the monthly rate
        repayment_duration.append(find_num_months(principal[i], interest[i], monthly))

        #Calculate monthly rate needed to pay back loan at ideal repayment time
        monthly_rate.append(find_monthly_payment(principal[i], interest[i], duration))

    #Calculate the total cost and interest given an ideal repayment deadline
    #ID stands for Ideal Duration
    (ID_total, ID_int) = find_cost(principal, interest, monthly_rate, [duration])

    #Calculate the total cost and interest given an ideal monthly rate
    #IP stands for Ideal Payment
    (IP_total, IP_int) = find_cost(principal, interest, [monthly], repayment_duration)

    #Calculate the percentage of payments going towards the principal for each ideal
    ID_per = prin_to_int_ratio(ID_total, ID_int)
    IP_per = prin_to_int_ratio(IP_total, IP_int)

    #Calculate the recommended salary for each ideal scenario
    ID_salary = minimum_salary(sum(monthly_rate))
    IP_salary = minimum_salary(monthly*len(principal))

    #Displays the results to the user
    return render_template('report.html', title='Report', 
                           principal=principal, 
                           interest=interest, 
                           loantype=loantype, 
                           monthly=monthly, 
                           grad=grad, 
                           term=term, 
                           duration=duration, 
                           grad_debt=grad_debt, 
                           grad_interest=grad_interest, 
                           repayment_duration=repayment_duration, 
                           monthly_rate=monthly_rate, 
                           ID_total=ID_total, 
                           ID_int=ID_int, 
                           IP_total=IP_total, 
                           IP_int=IP_int, 
                           ID_per=ID_per, 
                           IP_per=IP_per, 
                           ID_salary=ID_salary, 
                           IP_salary=IP_salary,
                           principal_length=len(principal),
                           total_EMI=sum(monthly_rate),
                           total_duration=max(repayment_duration))






#<------------------------COMPONENT 2 MILESTONE TRACKER------------------------>
"""
References Applicable to Section
[6] https://www.w3schools.com/jsref/jsref_toisostring.asp
[7] https://www.programiz.com/python-programming/datetime/strptime
[8] https://www.geeksforgeeks.org/saving-a-pandas-dataframe-as-a-csv/
[9] https://www.w3schools.com/html/html_tables.asp
[10] https://www.chartjs.org/docs/latest/general/accessibility.html
[11] https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/file
"""

#LOG MENU
@app.route('/log', methods=['GET','POST'])
def log_menu():
    """
    Description: Displays log menu to users
    """
    return render_template('log.html',title='Log Menu')

#REPAY LOGGING
@app.route('/log/repay', methods=['GET','POST'])
def repay_log():
    """
    Description: Logs all payments made/posted by the user through a series of inputs
    """

    #Initializes variables if they don't yet exist so that values can be added to them
    if 'amount' not in session:
        session['amount'] = []
    if 'pay_date' not in session:
        session['pay_date'] = []
    if 'pay_note' not in session:
        session['pay_note'] = []
    if 'loan_choice' not in session:
        session['loan_choice'] = []
    if 'loan_principal' not in session:
        session['loan_principal'] = []

    loans = session['loan_principal']

    if request.method == 'POST':
        #Extract current lists from session
        amount_list = session['amount']
        pay_date_list = session['pay_date']
        pay_note_list = session['pay_note']
        choice_list = session['loan_choice']

        #Append to the lists
        amount_list.append(request.form['amount'])
        pay_date_list.append(request.form['date'])
        pay_note_list.append(request.form['note'])
        choice_list.append(request.form['loan_choice'])

        #Set the session variables to the new lists
        session['amount'] = amount_list
        session['pay_date'] = pay_date_list
        session['pay_note'] = pay_note_list
        session['loan_choice'] = choice_list

    #Confirmation string
    conf = "There are " + str(len(session['pay_date'])) + " Entries Currently"

    return render_template('repay_log.html',title='Repayment Log', conf=conf, loans=loans)

#LOAN LOGGING
@app.route('/log/loan', methods=['GET','POST'])
def loan_log():
    """
    Description: Logs all payments made/posted by the user through a series of inputs
    """
    
    #Initializes variables if they don't yet exist so that values can be added to them
    if 'loan_principal' not in session:
        session['loan_principal'] = []
    if 'loan_int_rate' not in session:
        session['loan_int_rate'] = []
    if 'loan_date' not in session:
        session['loan_date'] = []
    if 'loan_fees' not in session:
        session['loan_fees'] = []
    if 'loan_bal' not in session:
        session['loan_bal'] = []
    if 'loan_note' not in session:
        session['loan_note'] = []

    if request.method == 'POST':
        # Extract current lists from session
        loan_principal_list = session['loan_principal']
        loan_int_rate_list = session['loan_int_rate']
        loan_date_list = session['loan_date']
        loan_fees_list = session['loan_fees']
        loan_note_list = session['loan_note']

        # Append to the lists
        loan_principal_list.append(request.form['new_loan'])
        loan_int_rate_list.append(request.form['new_rate'])
        loan_date_list.append(request.form['loan_date'])
        loan_fees_list.append(request.form['existing_int'])
        loan_note_list.append(request.form['loan_note'])

        # Set the session variables to the new lists
        session['loan_principal'] = loan_principal_list
        session['loan_int_rate'] = loan_int_rate_list
        session['loan_date'] = loan_date_list
        session['loan_fees'] = loan_fees_list
        session['loan_note'] = loan_note_list

    #Confirmation string
    conf = "There are " + str(len(session['loan_date'])) + " Entries Currently"
    
    return render_template('loan_log.html',title='Loan Log', conf=conf)

#MILESTONE PAGE
@app.route('/milestone', methods=['GET','POST'])
def milestone():
    """
    Description: Calculates/Displays user's logs and progress through graph projection.
    Processes data to be storable as a csv.
    """
    
    #Initializes variables if they don't yet exist so that values can be added to them
    if 'amount' not in session:
        session['amount'] = []
    if 'pay_date' not in session:
        session['pay_date'] = []
    if 'pay_note' not in session:
        session['pay_note'] = []
    if 'loan_choice' not in session:
        session['loan_choice'] = []
    if 'loan_principal' not in session:
        session['loan_principal'] = []
    if 'loan_int_rate' not in session:
        session['loan_int_rate'] = []
    if 'loan_date' not in session:
        session['loan_date'] = []
    if 'loan_fees' not in session:
        session['loan_fees'] = []
    if 'loan_bal' not in session:
        session['loan_bal'] = []
    if 'loan_note' not in session:
        session['loan_note'] = []
    if 'validation' not in session:
        session['validation'] = ""

    #Extract Variables from session and convert data types
    amount = [float(amount) for amount in session['amount']]
    pay_date = [datetime.datetime.strptime(str(day), '%Y-%m-%d') for day in session['pay_date']]
    pay_note = session['pay_note']
    loan_choice = [int(choice) for choice in session['loan_choice']]
    loan_principal = [float(principal) for principal in session['loan_principal']]
    loan_int_rate = [float(rate) for rate in session['loan_int_rate']]
    loan_date = [datetime.datetime.strptime(str(day), '%Y-%m-%d') for day in session['loan_date']]
    loan_fees = [float(fee) for fee in session['loan_fees']]
    loan_note = session['loan_note']

    (adj_loan_principal, adj_loan_fees) = (loan_principal.copy(), loan_fees.copy())
    #If there is sufficient data to plot
    if (len(loan_principal) > 0 and len(amount) > 0):
        #Calculates adjustment from loans being repayed and interest accrued based on today's date
        int_accrued = int_since(loan_date, loan_int_rate, loan_principal)
        (adj_loan_principal, adj_loan_fees) = apply_adjustments(loan_principal.copy(), loan_fees.copy(), int_accrued, amount, loan_choice)

    #Filters payments that pertain to the current month for projection purposes
    current_payments = [(amount[i], loan_choice[i]) for i, date in enumerate(pay_date) if date.month == datetime.datetime.now().month]

    temp_prin = adj_loan_principal.copy()
    temp_fees = adj_loan_fees.copy()
    balances = [] 
    #Creates the balances for the 10 year projection while accounting for interest.
    for i in range(len(temp_prin)):
        bal_i = []
        monthly_payment = sum(amount for amount, choice in current_payments if choice == i)
        for j in range(120):

            #Calculate interest for current month
            temp_fees[i] += (30.437 * (loan_int_rate[i]/36500) * temp_prin[i])
            
            #Pay off the interest/fees first
            temp_fees[i] -= monthly_payment

            #Contribute the remaining payment to the principal
            if (temp_fees[i] <= 0):
                temp_prin[i] += temp_fees[i]
                temp_fees[i] = 0

            #If loan has been completely paid off
            if (temp_prin[i] < 0):
                temp_prin[i] = 0

            #Add the current balance to the plot data
            bal_i.append(temp_prin[i] + temp_fees[i]) 
        
        balances.append(bal_i)

    #Produces a list of months from today to 10 years from now for graph projection
    dates = [(datetime.date.today() + datetime.timedelta(days=30.437 * i)).strftime('%Y') for i in range(120)]

    #Produces the log csv that is downloaded at the user's request
    headers = ["Amount", "Date", "Loan Choice", "Notes", "Principal", "Interest Rate", "Date of Disbursement", "Outstanding Interest/Fees", "Loan Notes"]
    csv_data = [amount,pay_date,loan_choice,pay_note,loan_principal,loan_int_rate,loan_date,loan_fees,loan_note]
    df = pandas.DataFrame(csv_data).T
    df.columns = headers
    csv = df.to_csv(index=False)

    session['file'] = csv_data
    
    return render_template('milestone.html',
                           title='Milestones',
                           amount=amount,
                           pay_date=[date.strftime("%m/%d/%Y") for date in pay_date],
                           choice=loan_choice,
                           pay_note=pay_note,
                           num_pay_logs = len(pay_date),
                           loan_principal=[round(prin,2) for prin in adj_loan_principal],
                           loan_int_rate=loan_int_rate,
                           loan_date=[date.strftime("%m/%d/%Y") for date in loan_date],
                           loan_fees=[round(fees,2) for fees in adj_loan_fees],
                           loan_bal=[round(principal + fees,2) for principal, fees in zip(adj_loan_principal, adj_loan_fees)],
                           loan_note=loan_note,
                           num_loan_logs = len(loan_date),
                           dates=dates,
                           balances=balances,
                           csv=csv,
                           validation=session['validation']
                           )

#UPLOAD FEATURE FOR MILESTONE PAGE
@app.route('/milestone/upload', methods=['GET','POST'])
def upload():
    """
    Description: Checks a provided file uploaded by the user,
    if the file is valid it will loaded into the milestone page.
    else an error message will be shown the to the user
    """

    if request.method == 'POST':
        file = request.files.get('user_csv')

        #Checks file extension
        if (file.filename.endswith('.csv') == False):
            validation = "Incompatible File, Please submit files with extension .csv"
            session['validation'] = validation
            return redirect('/milestone')

        df = pd.read_csv(file, encoding='unicode_escape')
        
        #Checks csv headers formatting
        headers = ["Amount", "Date", "Loan Choice", "Notes", "Principal", "Interest Rate", "Date of Disbursement", "Outstanding Interest/Fees", "Loan Notes"]
        for names in headers:
            if names not in df.columns:
                validation = "Incompatible File, Missing Column Header " + names
                session['validation'] = validation
                return redirect('/milestone')

        #Check the validity of the Date column by checking if a value error occurs
        try:
            test = [datetime.datetime.strptime(str(x), '%m/%d/%Y %H:%M').strftime('%Y-%m-%d') for x in df['Date'].tolist() if pandas.notna(x)]
        except ValueError:
            validation = "Incompatible File, Invalid Date Column Data"
            session['validation'] = validation
            return redirect('/milestone')
        
        #Check the validity of the Date of Disbursement column by checking if a value error occurs
        try:
            test = [datetime.datetime.strptime(str(x), '%m/%d/%Y %H:%M').strftime('%Y-%m-%d') for x in df['Date of Disbursement'].tolist() if pandas.notna(x)]
        except ValueError:
            validation = "Incompatible File, Invalid Date of Disbursement Column Data"
            session['validation'] = validation
            return redirect('/milestone')

        #Applies filtering to data including type conversion and removal of nan values
        amount = [x for x in df['Amount'].tolist() if pandas.notna(x)]
        date = [datetime.datetime.strptime(str(x), '%m/%d/%Y %H:%M').strftime('%Y-%m-%d') for x in df['Date'].tolist() if pandas.notna(x)]
        notes = [x if pandas.notna(x) else "" for x in df['Notes'].tolist() ]
        choice = [x for x in df['Loan Choice'].tolist() if pandas.notna(x)]
        principal = [x for x in df['Principal'].tolist() if pandas.notna(x)]
        int_rate = [x for x in df['Interest Rate'].tolist() if pandas.notna(x)]
        dod = [datetime.datetime.strptime(str(x), '%m/%d/%Y %H:%M').strftime('%Y-%m-%d') for x in df['Date of Disbursement'].tolist() if pandas.notna(x)]
        fees = [x for x in df['Outstanding Interest/Fees'].tolist() if pandas.notna(x)]
        loan_note = [x if pandas.notna(x) else "" for x in df['Loan Notes'].tolist()]

         #If the lengths of one of the columns is different reject the file
        if (len(amount) != len(date) or len(date) != len(choice)):
            validation = "Incompatible File, Misaligned Payment Data"
            session['validation'] = validation
            return redirect('/milestone')
        
        #If the lengths of one of the columns is different reject the file
        if (len(principal) != len(int_rate) or len(int_rate) != len(dod) or len(dod) != len(fees)):
            validation = "Incompatible File, Misaligned Loan Data"
            session['validation'] = validation
            return redirect('/milestone')
        
        #Check the validity of the amount column
        for i in amount:
            #If the amount is not a number
            if not ((isinstance(i, int)) or (isinstance(i, float))):
                validation = "Incompatible File, Invalid amount data " + i
                session['validation'] = validation
                return redirect('/milestone')
            #If the amount is less than 1
            if (i < 1):
                validation = "Incompatible File, Invalid amount data " + i
                session['validation'] = validation
                return redirect('/milestone')

        #Check the validity of the choice column
        for i in choice:
            #If the choice is not an integer    
            if not ((isinstance(i, int)) or (isinstance(i, float))):
                validation = "Incompatible File, Invalid choice data " + str(i)
                session['validation'] = validation
                return redirect('/milestone')
            
            #If choice does not exist
            if i > len(principal) - 1  or i < 0 or i % 1 != 0:
                validation = "Incompatible File, Invalid choice data " + str(i)
                session['validation'] = validation
                return redirect('/milestone')
        
        #Check the validity of the principal column
        for i in principal:
            #If the amount is not a number
            if not ((isinstance(i, int)) or (isinstance(i, float))):
                validation = "Incompatible File, Invalid principal data " + i
                session['validation'] = validation
                return redirect('/milestone')
            #If the amount is less than 1
            if (i < 1):
                validation = "Incompatible File, Invalid principal data " + i
                session['validation'] = validation
                return redirect('/milestone')

        #Check the validity of the Interest Rate column
        for i in int_rate:
            #If the amount is not a number
            if not ((isinstance(i, int)) or (isinstance(i, float))):
                validation = "Incompatible File, Invalid interest rate data " + i
                session['validation'] = validation
                return redirect('/milestone')
            #If the amount is less than 1
            if (i < 1):
                validation = "Incompatible File, Invalid interest rate data " + i
                session['validation'] = validation
                return redirect('/milestone')
            
        #Check the validity of the fees column
        for i in fees:
            #If the amount is not a number
            if not ((isinstance(i, int)) or (isinstance(i, float))):
                validation = "Incompatible File, Invalid fees data " + i
                session['validation'] = validation
                return redirect('/milestone')
            #If the amount is less than 0
            if (i < 0):
                validation = "Incompatible File, Invalid fees data " + i
                session['validation'] = validation
                return redirect('/milestone')

        session['amount'] = amount
        session['pay_date'] = date
        session['pay_note'] = notes
        session['loan_choice'] = choice
        session['loan_principal'] = principal
        session['loan_int_rate'] = int_rate
        session['loan_date'] = dod
        session['loan_fees'] = fees
        session['loan_note'] = loan_note
        session['validation'] = ""
        
    return redirect('/milestone')

#SAVE TO PROFILE FUNCTION FOR MILESTONE PAGE
@app.route('/milestone/save', methods=['GET','POST'])
def save():
    """
    Description: Saves the user's milestone log to their profile
    """

    if 'profile' not in session:
        validation = "Save Failed, User is not currently logged in" 
        session['validation'] = validation
        return redirect('/milestone')
   
    username = session['profile']['username']
    csv_data = session['file']

    #Saves data to profile in database
    if save_log(username, csv_data):
        validation = "Save Succeeded" 
        session['validation'] = validation
        session['profile']['logs'] = csv_data
        session.modified = True

    return redirect('/milestone')
    
#LOAD FROM PROFILE FUNCTION FOR MILESTONE PAGE
@app.route('/milestone/load', methods=['GET','POST'])
def load():
    """
    Description: Loads milestone data from user profile to 
    milestone page
    """

    #Checks if the profile exists and contains the log information
    if 'profile' not in session:
        validation = "Load Failed, User is not currently logged in" 
        session['validation'] = validation
        return redirect('/milestone')
    
    csv_data = session['profile']['logs']

    if csv_data == "Empty":
        validation = "Load Failed, User does not currently have a save file" 
        session['validation'] = validation
        return redirect('/milestone')
    
    #Produces the log csv that is downloaded at the user's request
    headers = ["Amount", "Date", "Loan Choice", "Notes", "Principal", "Interest Rate", "Date of Disbursement", "Outstanding Interest/Fees", "Loan Notes"]
    df = pandas.DataFrame(csv_data).T
    df.columns = headers
    
    #Format it for use in milestones page
    amount = [x for x in df['Amount'].tolist() if pandas.notna(x)]
    date = [datetime.datetime.fromisoformat(str(x)).strftime('%Y-%m-%d') for x in df['Date'].tolist() if pandas.notna(x)]
    notes = [x if pandas.notna(x) else "" for x in df['Notes'].tolist() ]
    choice = [x for x in df['Loan Choice'].tolist() if pandas.notna(x)]
    principal = [x for x in df['Principal'].tolist() if pandas.notna(x)]
    int_rate = [x for x in df['Interest Rate'].tolist() if pandas.notna(x)]
    dod = [datetime.datetime.fromisoformat(str(x)).strftime('%Y-%m-%d') for x in df['Date of Disbursement'].tolist() if pandas.notna(x)]
    fees = [x for x in df['Outstanding Interest/Fees'].tolist() if pandas.notna(x)]
    loan_note = [x if pandas.notna(x) else "" for x in df['Loan Notes'].tolist()]

    session['amount'] = amount
    session['pay_date'] = date
    session['pay_note'] = notes
    session['loan_choice'] = choice
    session['loan_principal'] = principal
    session['loan_int_rate'] = int_rate
    session['loan_date'] = dod
    session['loan_fees'] = fees
    session['loan_note'] = loan_note
    session['validation'] = ""

    validation = "Load Succeeded" 
    session['validation'] = validation
    return redirect('/milestone')





#<------------------------COMPONENT 3 PROFILES/SCHOLARSHIPS------------------------>
"""
References Applicable to Section
[12] https://www.mongodb.com/docs/manual/reference/method/db.collection.find/
[13] https://brightdata.com/blog/how-tos/web-scraping-with-python
[14] https://umbc.academicworks.com/
"""

#LOGIN PAGE
@app.route('/login', methods=['GET','POST'])
def login():
    """
    Description: Log user into their profile if they enter correct details
    """

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        profile = login_user(username, password)
        
        #If the database finds a profile log the user in else send error
        if (profile):
            session.clear()
            session['profile'] = profile
            return render_template('login.html', title='Login', message='Welcome ' + username)
        else:
            return render_template('login.html', title='Login', message='Authentication Failed, Try Again')
        
    return render_template('login.html', title='Login')

#REGISTRATION MENU
@app.route('/login/reg_menu', methods=['GET','POST'])
def reg_menu():
    """
    Description: Displays menu determining whether user want to log in as
    a normal user or a sponsor
    """
    return render_template('register_menu.html',title='Register Menu')

#REGISTER SPONSOR PAGE
@app.route('/login/reg_menu/reg_admin', methods=['GET','POST'])
def reg_admin():
    """
    Description: Registers sponsor accounts through verification of key
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin_key = request.form['key']

        #If the admin has the proper admin key register them else send error
        if (register_admin(username, password, admin_key)):
            return redirect('/login')
        else:
            return render_template('reg_admin.html',title='Register Menu', message="Credentials Not Accepted, Please revise")
        
    return render_template('reg_admin.html',title='Register Menu')

#REGISTER REGULAR USER
@app.route('/login/reg_menu/register', methods=['GET','POST'])
def register():
    """
    Description: Registers user accounts into the database
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        gpa = float(request.form['gpa'])
        status = request.form['status']
        hours = float(request.form['hours'])

        if (register_user(username, password, gpa, status, hours)):
            return redirect('/login')
        else:
            return render_template('register.html', title='Register', message="Username Already Taken, Please pick another username")
        
    return render_template('register.html', title='Register')

#SCHOLARSHIP PAGE
@app.route('/scholarships', methods = ['GET', 'POST'])
def scholarships():
    """
    Description: Displays list of valid scholarships to the user
    """
    
    #if the user is not logged in
    if 'profile' not in session:
        scholarships = fetch_scholarships(None)
        return render_template('scholarships.html', scholarships=scholarships, length=len(scholarships), page=1)

    #if the user is logged in as an admin
    elif 'admin' in session['profile']:
        if request.method == 'POST':
            sponsor = session['profile']['username']
            name = request.form['name']
            gpa = float(request.form['gpa'])
            status = request.form['status']
            hours = float(request.form['hours'])
            desc = request.form['desc']
            award = request.form['award']
            
            #Upload the scholarship to the database
            document = post_scholarship(sponsor, name, gpa, status, hours, desc, award)
            
            #If the scholarship was posted
            if document:
                session['profile']['scholarships'].append(document)
                session.modified = True
                return render_template('scholarships.html', profile=session['profile'], admin=True, message="Scholarship Posted!", page=1)
            else:
                return render_template('scholarships.html', profile=session['profile'], admin=True, message="Scholarship Failed to be Posted!", page=1)
            
        return render_template('scholarships.html', profile=session['profile'], admin=True, page=1)
    
    #if the user is logged in as a normal user
    else:
        profile = session['profile']
        scholarships = fetch_scholarships(profile)
        return render_template('scholarships.html', profile=session['profile'], scholarships=scholarships, length=len(scholarships))

#PROFILE PAGE
@app.route('/profile', methods=["GET", "POST"])
def profile():
    """
    Description: Displays and edits user credentials
    """
    #if the user is not logged in
    if 'profile' not in session:
        return render_template('profile.html')

    #if the user is logged in as an admin
    elif 'admin' in session['profile']:
        scholarships=session['profile']['scholarships']
        return render_template('profile.html', profile=session['profile'],scholarships=scholarships, length=len(scholarships), admin=True)
    
    #if the user is logged in as a normal user
    else: 
        if request.method == "POST":
            gpa = float(request.form['gpa'])
            status = request.form['status']
            hours = float(request.form['hours'])
            username = session['profile']['username']
            password = session['profile']['password']
            
            #Update the old credentials with the new ones in the database
            edit_profile(gpa, status, hours, username)
            session.pop('profile')
            session['profile'] = login_user(username, password)
        
        return render_template('profile.html', profile=session['profile'])

#LOGOUT PAGE
@app.route('/login/logout')
def logout():
    """
    Description: Logs user out by clearing their session
    """
    session.clear() 
    return redirect('/login')
