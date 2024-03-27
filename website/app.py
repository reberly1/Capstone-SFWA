from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title="Home")

@app.route('/calculator', methods=['GET','POST'])
def calculator():
    return render_template('calculator.html')

@app.route('/calculator/repayment', methods=['GET','POST'])
def repayment():
    return render_template('repayment.html')

@app.route('/calculator/adjustment', methods=['GET','POST'])
def adjustment():
    return render_template('adjustment.html')

@app.route('/calculator/unguided', methods=['GET','POST'])
def unguided():
    return render_template('unguided.html')

@app.route('/calculator/debt', methods=['GET','POST'])
def debt():
    return render_template("debt.html")
    
@app.route('/calculator/report', methods=['GET','POST'])
def report():
    if request.method == 'POST':
        principal = request.form.getlist('principal[]')
        interest = request.form.getlist('interest[]')
        sub = request.form.getlist('loantype[]')
        grad = request.form['grad']
        term = request.form['term']
        future = request.form['future']
        monthly = request.form['monthly']
        misc = request.form['misc']

        return render_template('report.html', title='Report', principal=principal, interest=interest, sub=sub, grad=grad, term=term,future=future, monthly=monthly, misc=misc)
    return render_template('report.html')

if __name__ == '__main__':
    app.run(debug=True)
