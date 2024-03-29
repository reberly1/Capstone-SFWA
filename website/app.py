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

    return render_template("unguided.html",title='Unguided')
    
@app.route('/report', methods=['GET','POST'])
def report():
    #Collects all calculator input from session for computation and display
    principal = session.get('principal[]')
    interest = session.get('interest[]')
    loantype = session.get('loantype')
    grad = float(session.get('grad'))
    term = float(session.get('term'))
    monthly = float(session.get('monthly'))
    misc = float(session.get('misc'))
    duration = float(session.get('duration'))
    
    repayment = pay_rate(interest, misc, principal, grad*term, duration*12)

    total = total_debt(principal, interest, loantype, term, misc, grad*term)

    total_int = 0
    span = math.floor(misc/monthly)
    for i in range(len(principal)):
        span += repayment_time(monthly, interest[i], 0, principal[i], grad*term)[0]
        total_int += repayment_time(monthly, interest[i], 0, principal[i], grad*term)[1]
    
    return render_template('report.html', title='Report', principal=principal, interest=interest, sub=loantype, grad=grad, term=term, monthly=monthly, misc=misc, total=total, span=span, total_int=total_int,repayment=repayment)

if __name__ == '__main__':
    app.run(debug=True)
