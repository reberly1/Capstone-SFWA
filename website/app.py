from flask import Flask, render_template, url_for, request
from functions import *
import math

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title="Home")

#Routes for the guided calculator suite
@app.route('/guided')
def guided():
    return render_template('guided.html',title='Guided')

#Page 1, loans
@app.route('/guided/loans')
def loans():
    return render_template('guided_loans.html',title='Guided Loans')

#Page 2, misc interest and fees
@app.route('/guided/misc')
def misc():
    return render_template('guided_misc.html',title='Guided Misc')

#Page 3, term costs
@app.route('/guided/terms')
def terms():
    return render_template('guided_terms.html',title='Guided Terms')

#Page 4, estimates
@app.route('/guided/estimates')
def estimates():
    return render_template('guided_estimates.html',title='Guided Estimates')

@app.route('/calculator', methods=['GET','POST'])
def calculator():
    return render_template('calculator.html')

@app.route('/unguided', methods=['GET','POST'])
def unguided():
    return render_template("unguided.html")
    
@app.route('/report', methods=['GET','POST'])
def report():
    if request.method == 'POST':
        principal = [float(x) for x in request.form.getlist('principal[]')]
        interest = [float(x) / 100 for x in request.form.getlist('interest[]')]
        sub = request.form.getlist('loantype[]')
        grad = float(request.form['grad'])
        term = float(request.form['term'])
        monthly = float(request.form['monthly'])
        misc = float(request.form['misc'])
        duration = float(request.form['duration'])

        repayment = pay_rate(interest, misc, principal, grad*term, duration*12)
        total = total_debt(principal, interest, sub, term, misc, grad*term)
        total_int = 0
        span = math.floor(misc/monthly)
        for i in range(len(principal)):
            span += repayment_time(monthly, interest[i], 0, principal[i], grad*term)[0]
            total_int += repayment_time(monthly, interest[i], 0, principal[i], grad*term)[1]
        return render_template('report.html', title='Report', principal=principal, interest=interest, sub=sub, grad=grad, term=term, monthly=monthly, misc=misc, total=total, span=span, total_int=total_int,repayment=repayment)
    return render_template('report.html')

if __name__ == '__main__':
    app.run(debug=True)
