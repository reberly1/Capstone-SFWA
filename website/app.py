from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
def home():
   if request.method == 'POST':
        # Get form data
        name = request.form['name']
        message = request.form['message']

        # Process the data (you can do whatever you want with it)
        print('Name:', name)
        print('Message:', message)
        return render_template('home.html', name=name, message=message)
   else:
        return render_template('home.html')

@app.route('/about', methods=['GET','POST'])
def about():
    if request.method == 'POST':
        principal = request.form['principal']
        interest = request.form['interest']
        grad = request.form['grad']
        term = request.form['term']
        # Process the data (you can do whatever you want with it)
        print('Principal:', principal)
        print('Interest:', interest)
        print('Graduation Date', grad)
        print('Term Cost', term)
        return render_template('about.html', title='About', principal=principal, interest=interest, grad=grad, term=term)
    else:
        return render_template("about.html")
if __name__ == '__main__':
    app.run(debug=True)
