from flask import Flask, render_template, request, session, redirect
from functions import *
import datetime
import pandas
import numpy as np

app = Flask(__name__)
app.secret_key = "Dummy Key For Debugging Purposes"

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title="Home")

#Routes for the guided calculator suite
@app.route('/guided')
def guided():
    return render_template('guided.html',title='Guided')

#Page 1, loans
@app.route('/guided/loans', methods=['GET','POST'])
def loans():
    #Stores all input into session for extraction by other pages
    if request.method == "POST":
        session['principals'] = request.form.getlist('principal[]')
        session['interests'] = request.form.getlist('interest[]')
        session['loan_types'] = request.form.getlist('loan_type[]')
        return redirect('/guided/terms')
    
    return render_template('guided_loans.html',title='Guided Loans')

#Page 2, term costs
@app.route('/guided/terms', methods=['GET','POST'])
def terms():
    #Stores all input into session for extraction by other pages
    if request.method == "POST":
        session['year_grad'] = request.form['year_grad']
        session['term_cost'] = request.form['term_cost']
        return redirect('/guided/estimates')
    
    return render_template('guided_terms.html',title='Guided Terms')

#Page 3, estimates
@app.route('/guided/estimates', methods=['GET','POST'])
def estimates():
    #Stores all input into session for extraction by other pages
    if request.method == "POST":
        session['month_pay'] = request.form['month_pay']
        session['duration'] = request.form['duration']
        return redirect('/report')
    
    return render_template('guided_estimates.html',title='Guided Estimates')

@app.route('/unguided', methods=['GET','POST'])
def unguided():
    #Stores all input into session for extraction by other pages
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
    
@app.route('/report', methods=['GET','POST'])
def report():
    #Collects all calculator input from session for computation and display
    #numeric values are typecasted from string to float
    principal = [float(principal) for principal in session['principals']]
    interest = [float(interest) for interest in session['interests']]
    loantype = session['loan_types']
    monthly = float(session['month_pay'])
    grad = float(session['year_grad']) * 12
    term = float(session['term_cost'])   
    duration = float(session['duration']) * 12
    

    """Standardizations and revisions needed for the report"""
    #Calculate Total Debt Upon Graduation
    (grad_debt, grad_interest) = debt_upon_graduation(principal, interest, loantype, grad, term)

    repayment_duration = []
    monthly_rate = []
    for i in range(len(principal)):
        #Calculate Duration to Pay back the loan at the monthly rate
        repayment_duration.append(find_num_months(principal[i], interest[i], monthly))

        #Calculate monthly rate needed to pay back loan at ideal repayment time
        monthly_rate.append(find_monthly_payment(principal[i], interest[i], duration))

    #Calculate the total cost and interest for both ideals for comparison
    (ID_total, ID_int) = find_cost(principal, interest, monthly_rate, [duration])
    (IP_total, IP_int) = find_cost(principal, interest, [monthly], repayment_duration)

    #Calculate the percentage of payments going towards the principal for each ideal
    ID_per = prin_to_int_ratio(ID_total, ID_int)
    IP_per = prin_to_int_ratio(IP_total, IP_int)

    #Calculate the recommended salary for each ideal scenario
    ID_salary = minimum_salary(sum(monthly_rate))
    IP_salary = minimum_salary(monthly*len(principal))

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


@app.route('/log', methods=['GET','POST'])
def log_menu():
    return render_template('log.html',title='Log Menu')

@app.route('/log/repay', methods=['GET','POST'])
def repay_log():
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

@app.route('/log/loan', methods=['GET','POST'])
def loan_log():
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

@app.route('/milestone', methods=['GET','POST'])
def milestone():
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

    return render_template('milestone.html',
                           title='Milestones',
                           amount=amount,
                           pay_date=pay_date,
                           choice=loan_choice,
                           pay_note=pay_note,
                           num_pay_logs = len(pay_date),
                           loan_principal=adj_loan_principal,
                           loan_int_rate=loan_int_rate,
                           loan_date=loan_date,
                           loan_fees=adj_loan_fees,
                           loan_bal=[principal + fees for principal, fees in zip(adj_loan_principal, adj_loan_fees)],
                           loan_note=loan_note,
                           num_loan_logs = len(loan_date),
                           dates=dates,
                           balances=balances,
                           csv=csv
                           )

@app.route('/milestone/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('user_csv')

        df = pandas.read_csv(file, encoding='unicode_escape')

        session['amount'] = [x for x in df['Amount'].tolist() if pandas.notna(x)]
        session['pay_date'] = [datetime.datetime.strptime(str(x), '%m/%d/%Y %H:%M').strftime('%Y-%m-%d') for x in df['Date'].tolist() if pandas.notna(x)]
        session['pay_note'] = [x for x in df['Notes'].tolist() if pandas.notna(x)]
        session['loan_choice'] = [x for x in df['Loan Choice'].tolist() if pandas.notna(x)]
        session['loan_principal'] = [x for x in df['Principal'].tolist() if pandas.notna(x)]
        session['loan_int_rate'] = [x for x in df['Interest Rate'].tolist() if pandas.notna(x)]
        session['loan_date'] = [datetime.datetime.strptime(str(x), '%m/%d/%Y %H:%M').strftime('%Y-%m-%d') for x in df['Date of Disbursement'].tolist() if pandas.notna(x)]
        session['loan_fees'] = [x for x in df['Outstanding Interest/Fees'].tolist() if pandas.notna(x)]
        session['loan_note'] = [x for x in df['Loan Notes'].tolist() if pandas.notna(x)]

    return redirect('/milestone')

@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html', title='Login')

@app.route('/login/register', methods=['GET','POST'])
def register():
    return render_template('register.html', title='Register')

if __name__ == '__main__':
    app.run(debug=True)
