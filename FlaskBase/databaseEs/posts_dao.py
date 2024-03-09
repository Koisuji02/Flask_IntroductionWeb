# dao sta per data access object
import sqlite3

def get_posts():
    conn = sqlite3.connect('db/blog.db')
    # uso Row che è una sorta di dizionario (per non usare le tuple)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # li ordino secondo aggiunta più recente
    sql = 'SELECT * FROM posts ORDER BY date DESC'
    cursor.execute(sql)
    posts = cursor.fetchall()
    cursor.close()
    conn.close()
    return posts

def get_post(id):
    conn = sqlite3.connect('db/blog.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    sql = 'SELECT * FROM posts WHERE id = ?'
    cursor.execute(sql, (id,))
    post = cursor.fetchone()
    cursor.close()
    conn.close()
    return post

def add(post):
    conn = sqlite3.connect('db/blog.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    success = False
    sql = 'INSERT INTO posts(title, date, tag, content, user_id) VALUES(?, ?, ?, ?, ?)'
    # prova a creare il post, se riesce commit, altrimenti rollback (come a basi di dati)
    try:
        cursor.execute(sql, (post['title'], post['date'], post['tag'], post['content'], 1))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()
    cursor.close()
    conn.close()
    return success

def get_comments(id):
    conn = sqlite3.connect('db/blog.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    sql = 'SELECT content FROM comments WHERE post_id = ?'
    cursor.execute(sql, (id,))
    comments = cursor.fetchall()
    cursor.close()
    conn.close()
    return comments