import sqlite3

DATABASE_PATH = 'db/affitto.db'

#! GET ANNUNCI ORDINE PREZZO DECRESCENTE
def get_annunci():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT ANNUNCI.id, ANNUNCI.titolo, ANNUNCI.indirizzo, ANNUNCI.tipo, ANNUNCI.prezzo, ANNUNCI.arredato, ANNUNCI.locali, ANNUNCI.descrizione, ANNUNCI.disponibile, ANNUNCI.immagine_1, ANNUNCI.immagine_2, ANNUNCI.immagine_3, ANNUNCI.immagine_4, ANNUNCI.immagine_5, ANNUNCI.id_locatore, UTENTI.nickname FROM ANNUNCI, UTENTI WHERE ANNUNCI.id_locatore = UTENTI.id ORDER BY ANNUNCI.prezzo DESC'
    cursor.execute(sql)
    annunci = cursor.fetchall()

    cursor.close()
    conn.close()

    return annunci

#! GET ANNUNCI ORDINE LOCALI CRESCENTE
def get_annunci_locali():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT ANNUNCI.id, ANNUNCI.titolo, ANNUNCI.indirizzo, ANNUNCI.tipo, ANNUNCI.prezzo, ANNUNCI.arredato, ANNUNCI.locali, ANNUNCI.descrizione, ANNUNCI.disponibile, ANNUNCI.immagine_1, ANNUNCI.immagine_2, ANNUNCI.immagine_3, ANNUNCI.immagine_4, ANNUNCI.immagine_5, ANNUNCI.id_locatore, UTENTI.nickname FROM ANNUNCI, UTENTI WHERE ANNUNCI.id_locatore = UTENTI.id ORDER BY ANNUNCI.locali'
    cursor.execute(sql)
    annunci = cursor.fetchall()

    cursor.close()
    conn.close()

    return annunci

#! GET UTENTI
def get_users():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM UTENTI'
    cursor.execute(sql)
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return users

#! GET ANNUNCIO DA ID
def get_annuncio(id):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT ANNUNCI.id, ANNUNCI.titolo, ANNUNCI.indirizzo, ANNUNCI.tipo, ANNUNCI.prezzo, ANNUNCI.arredato, ANNUNCI.locali, ANNUNCI.descrizione, ANNUNCI.disponibile, ANNUNCI.immagine_1, ANNUNCI.immagine_2, ANNUNCI.immagine_3, ANNUNCI.immagine_4, ANNUNCI.immagine_5, ANNUNCI.id_locatore, UTENTI.nickname FROM ANNUNCI, UTENTI WHERE ANNUNCI.id_locatore = UTENTI.id AND ANNUNCI.id = ?'
    cursor.execute(sql, (id,))
    annuncio = cursor.fetchone()

    cursor.close()
    conn.close()

    return annuncio

#! AGGIUNGI ANNUNCIO
def add_annuncio(annuncio):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    
    sql = 'INSERT INTO ANNUNCI(titolo,indirizzo,tipo,prezzo,arredato,locali,descrizione,disponibile,immagine_1,immagine_2,immagine_3,immagine_4,immagine_5,id_locatore) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
    cursor.execute(sql, (annuncio['titolo'], annuncio['indirizzo'], annuncio['tipo'], annuncio['prezzo'], annuncio['arredato'], annuncio['locali'], annuncio['descrizione'], annuncio['disponibile'], annuncio['immagine_1'], annuncio['immagine_2'], annuncio['immagine_3'], annuncio['immagine_4'], annuncio['immagine_5'], annuncio['id_locatore']))

    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

#! PRENDO PRENOTAZIONI CON ID_ANNUNCIO
def get_bookings_by_id_annuncio(id):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT PRENOTAZIONI.id_annuncio, PRENOTAZIONI.id_utente, PRENOTAZIONI.stato, PRENOTAZIONI.data, PRENOTAZIONI.slot_ora, PRENOTAZIONI.tipo, PRENOTAZIONI.motivo, UTENTI.nickname, ANNUNCI.titolo, ANNUNCI.indirizzo FROM PRENOTAZIONI,ANNUNCI,UTENTI WHERE PRENOTAZIONI.id_annuncio = ? AND PRENOTAZIONI.id_annuncio = ANNUNCI.id AND ANNUNCI.id_locatore = UTENTI.id'
    cursor.execute(sql, (id,))
    bookings = cursor.fetchall()

    cursor.close()
    conn.close()

    return bookings

#! PRENDO PRENOTAZIONI CON ID_CLIENTE
def get_bookings_by_id_cliente(id):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT PRENOTAZIONI.id_annuncio, PRENOTAZIONI.id_utente, PRENOTAZIONI.stato, PRENOTAZIONI.data, PRENOTAZIONI.slot_ora, PRENOTAZIONI.tipo, PRENOTAZIONI.motivo, UTENTI.nickname, ANNUNCI.titolo, ANNUNCI.indirizzo FROM PRENOTAZIONI,ANNUNCI,UTENTI WHERE PRENOTAZIONI.id_utente = ? AND PRENOTAZIONI.id_annuncio = ANNUNCI.id AND ANNUNCI.id_locatore = UTENTI.id'
    cursor.execute(sql, (id,))
    bookings = cursor.fetchall()

    cursor.close()
    conn.close()

    return bookings

#! AGGIUNGO PRENOTAZIONE
def add_booking(booking, data, id_annuncio, id_utente):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    success = False
    stato = '?'

    sql = 'INSERT INTO PRENOTAZIONI(id_annuncio,id_utente,stato,data,slot_ora,tipo,motivo) VALUES(?,?,?,?,?,?,?)'
    cursor.execute(sql, (id_annuncio, id_utente, stato, data, booking['slot_ora'], booking['tipo'], False))
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # se errore: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

#! GET USER BY NICKNAME
def get_user_by_nickname(nickname):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM UTENTI WHERE nickname = ?'
    cursor.execute(sql, (nickname,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user

#! GET USER BY ID
def get_user_by_id(id):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM UTENTI WHERE id = ?'
    cursor.execute(sql, (id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user

#! AGGIUNGI USER (RICORDA CHE ID AUTOINCREMENTALE)
def add_user(user):

    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    if user['locatore'] == 'loc':
        user['locatore'] = True
    else:
        user['locatore'] = False

    sql = 'INSERT INTO UTENTI(nickname,password,locatore) VALUES(?,?,?)'

    try:
        cursor.execute(sql, (user['nickname'], user['password'], user['locatore']))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

#! CAMBIA STATO
def change_state(id_utente, id_annuncio, nuovo):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'UPDATE PRENOTAZIONI SET stato = ? WHERE id_utente = ? AND id_annuncio = ?'

    try:
        cursor.execute(sql, (nuovo, id_utente, id_annuncio))
        conn.commit()
        success = True

    except Exception as e:
        print('ERROR', str(e))
        # se errore, rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

#! AGGIUNGI MOTIVO
def add_reason(id_utente, id_annuncio, motivo):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'UPDATE PRENOTAZIONI SET motivo = ? WHERE id_utente = ? AND id_annuncio = ?'

    try:
        cursor.execute(sql, (motivo, id_utente, id_annuncio))
        conn.commit()
        success = True

    except Exception as e:
        print('ERROR', str(e))
        # se errore, rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

#! MODIFICA ANNUNCIO
def update_annuncio(annuncio, id_annuncio):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    
    sql = 'UPDATE ANNUNCI SET titolo = ?, tipo = ?, locali = ?, descrizione = ?, prezzo = ?, arredato = ?, immagine_1 = ?, immagine_2 = ?, immagine_3 = ?, immagine_4 = ?, immagine_5 = ?, disponibile = ? WHERE id = ?'
    try:
        cursor.execute(sql, (annuncio['titolo'], annuncio['tipo'], annuncio['locali'], annuncio['descrizione'], annuncio['prezzo'], annuncio['arredato'], annuncio['immagine_1'], annuncio['immagine_2'], annuncio['immagine_3'], annuncio['immagine_4'], annuncio['immagine_5'], annuncio['disponibile'], id_annuncio))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # se errore, rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success