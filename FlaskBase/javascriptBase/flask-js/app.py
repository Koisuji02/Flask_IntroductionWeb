from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import date
from flask_session import Session
# importo il file che ho creato per gestire il database (come da teoria)
import posts_dao


app = Flask(__name__)
# La riga sotto posso toglierla perchè il flashing viene effettuato con la session
#app.secret_key = 'questa è una secret key'

# Queste 2 istruzioni mi fanno passare da client-side session (cookies)
# a server-side session; con config, configuro dove salvo la sessione
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False     # sessione non permanente
Session(app)

# Sono passato dal dizionario posts al database

@app.route('/')
def index():
    posts = posts_dao.get_posts()
    return render_template('index.html', posts=posts)

@app.route('/posts/<int:id>')
def single_post(id):
    post = posts_dao.get_post(id)
    comments = posts_dao.get_comments(id)
    return render_template('single.html', post=post, comments=comments)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/posts/new', methods=['GET','POST'])
def new_post():
    if request.method == 'POST':
        post = request.form.to_dict()
        if post['title'] == '':
            app.logger.error('Titolo non può essere vuoto!')
        if post['date'] == '':
            post['date'] = date.today()
        post_image = request.files['image']
        if post_image:
            post_image.save('static/' + post['title'] + '.jpg')
        # uso la variabile success restituita dalla add per diversificare gli alert
        success = posts_dao.add(post)
        if success:
            flash('!!!Post creato correttamente!!!', 'success')
        else:
            flash('!!!Errore nella creazione del post!!!', 'danger')
        return redirect(url_for('index'))
    else:
        return render_template('new-post.html')
    
@app.route('/amministratore')
def admin():
    # se viene premuto il bottone amministratore
    session['admin'] = True
    return redirect(url_for('index'))