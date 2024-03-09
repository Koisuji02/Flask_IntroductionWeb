from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import date
from flask_session import Session

app = Flask(__name__)
# La riga sotto posso toglierla perchè il flashing viene effettuato con la session
#app.secret_key = 'questa è una secret key'

# Queste 2 istruzioni mi fanno passare da client-side session (cookies)
# a server-side session; con config, configuro dove salvo la sessione
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False     # sessione non permanente
Session(app)

# creo la struttura dati per i post
posts = [
        {'id':1,'title':'CSS', 'date':'2022-10-10', 'tag':'css',
         'content':'CSS sta per Cascading Style Sheet e in questo post ne parleremo meglio.'},
        {'id':2,'title':'HTML', 'date':'2022-10-04', 'tag':'html',
         'content':'HTML sta per HyperText Markup Language e in questo post ne parleremo meglio.'}
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

@app.route('/posts/new', methods=['GET','POST'])
def new_post():
    if request.method == 'POST':
        post = request.form.to_dict() # rende request.form modificabile
        # gestire errore titolo
        if post['title'] == '':
            app.logger.error('Titolo non può essere vuoto!')
        # data default
        if post['date'] == '':
            post['date'] = date.today()
        # salvo immagine dal form se esiste (per questo aggiungo l'enctype)
        post_image = request.files['image']
        if post_image:
            post_image.save('static/' + post['title'] + '.jpg')
        #aggiungo id (metto in coda il nuovo post)
        post['id'] = posts[-1]['id'] + 1
        #aggiungo post all'array posts
        posts.append(post)
        # per visualizzare messaggio di successo
        flash('!!!Post creato correttamente!!!', 'success')
        return redirect(url_for('index'))
    else:
        return render_template('new-post.html')
    
@app.route('/amministratore')
def admin():
    # se viene premuto il bottone amministratore
    session['admin'] = True
    return redirect(url_for('index'))
