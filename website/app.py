from flask import Flask, render_template, url_for

app = Flask(__name__)

posts = [
    {
    'author': "Joe Smow",
    'title': 'Blog Post 1',
    'content': 'sample data',
    'date': "April 21, 2018"
    },
    {
    'author': "Joe slow",
    'title': 'Blog Post 2',
    'content': 'sample data1',
    'date': "April 21, 2022"
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

if __name__ == '__main__':
    app.run(debug=True)
