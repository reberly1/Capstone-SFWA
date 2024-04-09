from flask import Flask, render_template, request, session, redirect
from functions import *
import math

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

    return render_template('report.html', title='Report', principal=principal, interest=interest, loantype=loantype, monthly=monthly, grad=grad, term=term, duration=duration, grad_debt=grad_debt, grad_interest=grad_interest, repayment_duration=repayment_duration, monthly_rate=monthly_rate, ID_total=ID_total, ID_int=ID_int, IP_total=IP_total, IP_int=IP_int, ID_per=ID_per, IP_per=IP_per, ID_salary=ID_salary, IP_salary=IP_salary,principal_length=len(principal),total_EMI=sum(monthly_rate),total_duration=max(repayment_duration))

@app.route('/log', methods=['GET','POST'])
def log():
    return render_template('log.html',title='Log')

@app.route('/milestone', methods=['GET','POST'])
def milestone():
    return render_template('milestone.html',title='Milestones')

if __name__ == '__main__':
    app.run(debug=True)
