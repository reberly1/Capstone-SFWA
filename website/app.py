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
        session['loantypes'] = request.form.getlist('loantype[]')
        return redirect('/guided/misc')
    
    return render_template('guided_loans.html',title='Guided Loans')

#Page 2, misc interest and fees
@app.route('/guided/misc', methods=['GET','POST'])
def misc():
    #Stores all input into session for extraction by other pages
    if request.method == "POST":
        session['misc'] = request.form['misc']
        return redirect('/guided/terms')
    
    return render_template('guided_misc.html',title='Guided Misc')

#Page 3, term costs
@app.route('/guided/terms', methods=['GET','POST'])
def terms():
    #Stores all input into session for extraction by other pages
    if request.method == "POST":
        session['grad'] = request.form['grad']
        session['term cost'] = request.form['term cost']
        return redirect('/guided/estimates')
    
    return render_template('guided_terms.html',title='Guided Terms')

#Page 4, estimates
@app.route('/guided/estimates', methods=['GET','POST'])
def estimates():
    #Stores all input into session for extraction by other pages
    if request.method == "POST":
        session['monthly'] = request.form['monthly']
        session['duration'] = request.form['duration']
        return redirect('/report')
    
    return render_template('guided_estimates.html',title='Guided Estimates')

@app.route('/unguided', methods=['GET','POST'])
def unguided():
    #Stores all input into session for extraction by other pages
    if request.method == "POST":
        session['principals'] = request.form.getlist('principal[]')
        session['interests'] = request.form.getlist('interest[]')
        session['loantypes'] = request.form.getlist('loantype[]')
        session['misc'] = request.form['misc']
        session['grad'] = request.form['grad']
        session['term cost'] = request.form['term cost']
        session['monthly'] = request.form['monthly']
        session['duration'] = request.form['duration']
        return redirect('/report')
    
    return render_template("unguided.html",title='Unguided')
    
@app.route('/report', methods=['GET','POST'])
def report():
    #Collects all calculator input from session for computation and display
    #numeric values are typecasted from string to float
    principal = [float(principal) for principal in session['principals']]
    interest = [float(interest) for interest in session['interests']]
    loantype = session['loantypes']
    monthly = float(session['monthly'])
    grad = float(session['grad'])
    term = float(session['term cost'])   
    duration = float(session['duration'])
    
    #Calculate Total Debt Upon Graduation
    (grad_debt, grad_interest) = debt_upon_graduation(principal, interest, loantype, grad, term)

    repayment = []
    monthly_rate = []
    for i in range(len(principal)):
        #Calculate Duration to Pay back the loan at the monthly rate
        repayment.append(find_num_months(principal[i], interest[i], monthly))

        #Calculate monthly rate needed to pay back loan at ideal repayment time
        monthly_rate.append(find_monthly_payment(principal[i], interest[i], duration))

    return render_template('report.html', title='Report')

@app.route('/log', methods=['GET','POST'])
def log():
    return render_template('log.html',title='Log')

if __name__ == '__main__':
    app.run(debug=True)
