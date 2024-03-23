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

@app.route('/calculator/debt', methods=['GET','POST'])
def about():
    if request.method == 'POST':
        principal = request.form['principal']
        interest = request.form['interest']
        grad = request.form['grad']
        term = request.form['term']
        future = request.form['future']
        return render_template('debt.html', principal=principal, interest=interest, grad=grad, term=term,future=future)
    else:
        return render_template("debt.html")
    
@app.route('/calculator/report', methods=['GET','POST'])
def report():
    if request.method == 'POST':
        principal = request.form['principal']
        interest = request.form['interest']
        grad = request.form['grad']
        term = request.form['term']
        future = request.form['future']
        # Process the data (you can do whatever you want with it)
        print('Principal:', principal)
        print('Interest:', interest)
        print('Graduation Date:', grad)
        print('Term Cost:', term)
        print('Future Interest:', future)
        return render_template('report.html', title='Report', principal=principal, interest=interest, grad=grad, term=term,future=future)
    return render_template('report.html')

if __name__ == '__main__':
    app.run(debug=True)
