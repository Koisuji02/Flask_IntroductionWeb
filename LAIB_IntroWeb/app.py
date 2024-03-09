from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import *
import dao
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import User

#! CREAZIONE DELL'APPLICAZIONE
app = Flask(__name__)
app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


#! HOMEPAGE (con 2 ordinamenti diversi)
@app.route('/', methods=['GET'])
def home():

    filtro = request.args.get('flag')
    if filtro:
        annunci = dao.get_annunci_locali()
    else:
        annunci = dao.get_annunci()
    return render_template('home.html', annunci=annunci)

#! SINGLE ANNUNCIO
@app.route('/annunci/<int:id>')
def single(id):
    annuncio = dao.get_annuncio(id)
    bookings = dao.get_bookings_by_id_annuncio(id)
    flag = True
    if current_user.is_authenticated:
        for booking in bookings:
            if booking['id_utente'] == current_user.id and booking['id_annuncio'] == id and booking['stato'] != 'F':
                flag = False
    return render_template('single.html', annuncio=annuncio, flag=flag)

#! NEW ANNUNCIO
@app.route('/annunci/new', methods=['GET', 'POST'])
@login_required
def new_annuncio():
    if request.method == 'POST':
        if current_user.is_authenticated:

            annuncio = request.form.to_dict()

            if annuncio['titolo'] == '':
                app.logger.error('Il titolo non può essere vuoto!')
                flash('Il titolo non può essere vuoto!', 'danger')
                return redirect(url_for('home'))

            if annuncio['indirizzo'] == '':
                app.logger.error('L\'indirizzo non può essere vuoto!')
                flash('L\'indirizzo non può essere vuoto!', 'danger')
                return redirect(url_for('home'))
            
            if annuncio['prezzo'] == '':
                app.logger.error('Il prezzo non può essere vuoto!')
                flash('Il prezzo non può essere vuoto!', 'danger')
                return redirect(url_for('home'))

            immagine1 = request.files['immagine_1']
            immagine2 = request.files['immagine_2']
            immagine3 = request.files['immagine_3']
            immagine4 = request.files['immagine_4']
            immagine5 = request.files['immagine_5']

            immagini=[immagine1, immagine2, immagine3, immagine4, immagine5]
            i=1

            for img in immagini:
                if img:
                    img.save('static/' + secure_filename(img.filename))
                    annuncio[f'immagine_{i}'] = '/static/' + secure_filename(img.filename)
                else:
                    annuncio[f'immagine_{i}'] = False #se non esiste l'immagine metto il campo a false
                i=i+1

            id_locatore = current_user.id
            annuncio['id_locatore'] = id_locatore

            success = dao.add_annuncio(annuncio)

            if success:
                flash('Annuncio creato correttamente', 'success')
            else:
                flash('Errore nella creazione dell\'annuncio: riprova!', 'danger')

    return redirect(url_for('home'))

#! FUNZIONE PER LA DATA DELLE NUOVE PRENOTAZIONI
@app.route('/prenotazioni/new/<int:id_annuncio>', methods=['POST'])
@login_required
# id = id dell'annuncio
def new_booking_data(id_annuncio):

    # vettore degli slot orari (che mi indica quali sono rimasti disponibili)
    vet=[True,True,True,True]
    # orari disponibili per quella data
    orari = ['0','0','0','0']
    # tutti i 4 slot orari
    tot = ['9-12','12-14','14-17','17-20']
    
    tmp = request.form.to_dict()

    if tmp['data'] == '':
        app.logger.error('La data non può essere vuota!')
        flash('Errore data!', 'danger')
        return redirect(url_for('single', id=id_annuncio))
    
    dataScelta = datetime.strptime(tmp['data'], '%Y-%m-%d')
    dataOggi = datetime.now() - timedelta(days=1)

    # dataMassima = 7 giorni dalla data di oggi
    dataMassima = dataOggi + timedelta(days=8)

    if dataScelta < dataOggi:
        flash('La data non deve essere precedente ad oggi!', 'danger')
        return redirect(url_for('single', id=id_annuncio))
    elif dataScelta > dataMassima:
        flash('La data deve essere entro 7 giorni da oggi!', 'danger')
        return redirect(url_for('single', id=id_annuncio))
    
    # prendo le prenotazioni: se c'è già una prenotazione per quell'annuncio in quello slot orario in quella data, errore; altrimenti aggiungi prenotazione

    # T = true, accettata; F = false, rifiutata; ? = pending
    bookings = dao.get_bookings_by_id_annuncio(id_annuncio)
    for e in bookings:
        if e['data'] == tmp['data'] and e['stato'] != 'F':

            if e['slot_ora'] == '9-12':
                vet[0]= False

            elif e['slot_ora'] == '12-14':
                vet[1]= False

            elif e['slot_ora'] == '14-17':
                vet[2]= False

            elif e['slot_ora'] == '17-20':
                vet[3]= False
    k = 0
    for i in vet:
        if i == True:
            orari[k] = tot[k]
        k+=1
    data = tmp['data']

    return render_template('orari.html', orari=orari, data=data, id_annuncio=id_annuncio)

#! FUNZIONE PER AGGIUNGERE PRENOTAZIONE
@app.route('/prenotazioni/new/orari/<int:id_annuncio>/<data_f>', methods=['POST'])
@login_required
# id = id dell'annuncio
def new_booking(id_annuncio, data_f):
    booking = request.form.to_dict()
    id_utente = current_user.id

    success = dao.add_booking(booking, data_f, id_annuncio, id_utente)
    if success:
        flash('Prenotazione richiesta correttamente!', 'success')
    else:
        flash('Errore nella richiesta della prenotazione!', 'danger')

    return redirect(url_for('single', id=id_annuncio))

#! LOAD USER
@login_manager.user_loader
def load_user(user_id):
    utente = dao.get_user_by_id(user_id)

    if utente is not None:
        user = User(id=utente['id'], nickname=utente['nickname'], password=utente['password'], locatore=utente['locatore'])
    else:
        user = None

    return user

#! LOGIN TEMPLATE
@app.route('/accedi')
def login():
    return render_template('login.html')

#! LOGIN METODO POST
@app.route('/accedi', methods=['POST'])
def login_post():
    nickname = request.form.get('nickname')
    password = request.form.get('password')

    user = dao.get_user_by_nickname(nickname)

    # se l'utente non è salvato o la password è sbagliata, errore
    if not user or not check_password_hash(user['password'], password):
        flash('Credenziali non valide, riprovare!', 'danger')

        return redirect(url_for('login'))
    # altrimenti
    else:
        new = User(id=user['id'], nickname=user['nickname'], password=user['password'],
                   locatore=user['locatore'])
        login_user(new, True)

        flash('Login con successo!', 'success')

        return redirect(url_for('home'))

#! SIGNUP TEMPLATE
@app.route('/iscriviti')
def signup():
    return render_template('signup.html')

#! SIGNUP METODO POST
@app.route('/iscriviti', methods=['POST'])
def signup_post():
    nickname = request.form.get('nickname')
    password = request.form.get('password')
    locatore = request.form.get('locatore')

    user_in_db = dao.get_user_by_nickname(nickname)

    if user_in_db:
        flash('C\'è già un utente registrato con questo nickname!', 'danger')
        return redirect(url_for('signup'))
    else:
        new_user = {
            "nickname": nickname,
            "password": generate_password_hash(password, method='pbkdf2:sha256'),
            "locatore": locatore
        }

        success = dao.add_user(new_user)

        if success:
            flash('Utente creato correttamente', 'success')
            return redirect(url_for('home'))
        else:
            flash('Errore nella creazione del utente: riprova!', 'danger')

    return redirect(url_for('signup'))

#! LOGOUT
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

#! SPAZIO CLIENTE
@app.route("/cliente")
@login_required
def cliente():
    id=current_user.id
    bookings = dao.get_bookings_by_id_cliente(id)
    return render_template('cliente.html', bookings=bookings)

#! LOCATORE E GESTIONE LOCATORE
@app.route('/locatore')
@login_required
def locatore():
    # tmp = annunci totali, devo filtrarli per id_locatore
    tmp = dao.get_annunci()
    annunci = []
    # vettore di liste di prenotazioni per ogni annuncio
    vet_bookings = []
    for annuncio in tmp:
        if annuncio['id_locatore'] == current_user.id:
            annunci.append(annuncio)
            booking = dao.get_bookings_by_id_annuncio(annuncio['id'])
            vet_bookings.append(booking)
            
    # se c'è il flag lo prendo
    flag = request.args.get('flag')

    return render_template('locatore.html', flag=flag, annunci=annunci, bookings=vet_bookings)

#! LOCATORE ACCETTA
@app.route("/locatore_accetta/<int:id_utente>/<int:id_annuncio>", methods=['GET','POST'])
@login_required
def locatore_accetta(id_utente, id_annuncio):
    # nuovo stato (Accettato) da cambiare nel dao
    nuovo = 'T'
    success = dao.change_state(id_utente, id_annuncio, nuovo)
    if not success:
        flash('Richiesta di accettazione da rifare, riprova!', 'danger')
    # redirect alle prenotazioni
    return redirect(url_for('locatore'))

#! LOCATORE RIFIUTA
@app.route("/locatore_rifiuta/<int:id_utente>/<int:id_annuncio>", methods=['GET','POST'])
@login_required
def locatore_rifiuta(id_utente, id_annuncio):
    # nuovo stato (Rifiutato) da cambiare nel dao
    nuovo = 'F'
    success = dao.change_state(id_utente, id_annuncio, nuovo)
    if not success:
        flash('Richiesta di rifiuto da rifare, riprova!', 'danger')

    motivo = request.form.get('motivo')
    success = dao.add_reason(id_utente, id_annuncio, motivo)
    if not success:
        flash('Motivazione non aggiunta, riprova!', 'danger')  
    # redirect alle prenotazioni
    return redirect(url_for('locatore'))

#! LOCATORE MODIFICA ANNUNCIO
@app.route('/annunci/modify/<int:id_annuncio>', methods=['GET', 'POST'])
@login_required
def modifica_annuncio(id_annuncio):
    if request.method == 'POST':
        if current_user.is_authenticated:

            annuncio = request.form.to_dict()

            if annuncio['titolo'] == '':
                app.logger.error('Il titolo non può essere vuoto!')
                flash('Il titolo non può essere vuoto!', 'danger')
                return redirect(url_for('home'))
            
            if annuncio['prezzo'] == '':
                app.logger.error('Il prezzo non può essere vuoto!')
                flash('Il prezzo non può essere vuoto!', 'danger')
                return redirect(url_for('home'))

            immagine1 = request.files['immagine_1']
            immagine2 = request.files['immagine_2']
            immagine3 = request.files['immagine_3']
            immagine4 = request.files['immagine_4']
            immagine5 = request.files['immagine_5']

            immagini=[immagine1, immagine2, immagine3, immagine4, immagine5]
            i=1

            for img in immagini:
                if img:
                    img.save('static/' + secure_filename(img.filename))
                    annuncio[f'immagine_{i}'] = '/static/' + secure_filename(img.filename)
                else:
                    annuncio[f'immagine_{i}'] = False #se non esiste l'immagine metto il campo a false
                i=i+1

            id_locatore = current_user.id
            annuncio['id_locatore'] = id_locatore

            success = dao.update_annuncio(annuncio, id_annuncio)

            if success:
                flash('Annuncio creato correttamente', 'success')
            else:
                flash('Errore nella creazione dell\'annuncio: riprova!', 'danger')

    return redirect(url_for('single', id=id_annuncio))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
