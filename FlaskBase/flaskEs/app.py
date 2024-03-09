from flask import Flask, render_template

app = Flask(__name__)

# creo la struttura dati per i post
posts = [
        {'id':1,'title':'CSS', 'date':'2022-10-10', 'tag':'css', 'content':'CSS sta per Cascading Style Sheet e in questo post ne parleremo meglio.'},
        {'id':2,'title':'HTML', 'date':'2022-10-04', 'tag':'html', 'content':'HTML sta per HyperText Markup Language e in questo post ne parleremo meglio.'}
    ]

@app.route('/')
def index():
    return render_template('index.html', posts=posts)

@app.route('/posts/<int:id>')
def single_post(id):
    post = posts[id-1]
    return render_template('single.html', post=post)

@app.route('/about')
def about():
    return render_template('about.html')