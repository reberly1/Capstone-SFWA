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

@app.route('/about')
def about():
    return render_template('about.html', title='About')

if __name__ == '__main__':
    app.run(debug=True)
