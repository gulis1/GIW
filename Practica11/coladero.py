# -*- coding: utf-8 -*-
"""
@title: El Coladero
@description: Aplicación web para detectar y corregir vulnerabilidades
@author: Enrique Martín Martín
@email: emartinm@ucm.es
"""

from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DBPATH = 'database.db'
SQLPATH = 'database.sql'


def reset_database():
    """ Elimina el fichero database.db (si existe) y lo crea con los valores por defecto"""
    try:
        os.remove(DBPATH)
    except FileNotFoundError:
        pass

    print('*** Recreando la base de datos ***')
    conn = sqlite3.connect(DBPATH)
    cur = conn.cursor()
    script_file = open(SQLPATH, 'r', encoding='utf8')
    script = script_file.read()
    script_file.close()
    cur.executescript(script)
    conn.commit()
    conn.close()


@app.route('/', methods=['GET'])
def root():
    return redirect(url_for('show_all_questions'))


@app.route('/show_all_questions', methods=['GET'])
def show_all_questions():
    conn = sqlite3.connect(DBPATH)
    cur = conn.cursor()
    query = """SELECT author,title,time,tags,id 
               FROM Questions 
               ORDER BY time DESC"""
    cur.execute(query)
    res = list(cur.fetchall())
    print(res)
    conn.close()
    return render_template('messages.html', questions=res)


@app.route('/insert_question', methods=['POST'])
def insert_question():
    author = request.form['author']
    title = request.form['title']
    tags = request.form['tags']
    body = request.form['body']

    conn = sqlite3.connect(DBPATH)
    cur = conn.cursor()
    qbody = """INSERT INTO Questions(author, title, tags, body, time) 
               VALUES ('{0}','{1}','{2}','{3}',CURRENT_TIMESTAMP)"""
    query = qbody.format(author, title, tags, body)
    cur.executescript(query)
    conn.commit()
    conn.close()
    return render_template("insert_ok.html", url=url_for("show_all_questions"))


@app.route('/show_question', methods=['GET'])
def show_question():
    ident = request.args.get('id')
    conn = sqlite3.connect(DBPATH)
    cur = conn.cursor()
    qbody1 = """SELECT author,title,time,tags,body 
                FROM Questions 
                WHERE id=:ident"""
    qbody2 = """SELECT author,time,body 
                FROM Replies 
                WHERE question_id=:ident"""
    params = {'ident': ident}
    cur.execute(qbody1, params)
    question = cur.fetchone()
    cur.execute(qbody2, params)
    replies = list(cur.fetchall())
    conn.close()
    return render_template("message_detail.html", q=question, replies=replies, ident=ident)


@app.route('/insert_reply', methods=['POST'])
def insert_reply():
    author = request.form['author']
    body = request.form['body']
    question_id = request.form['question_id']
    conn = sqlite3.connect(DBPATH)
    cur = conn.cursor()
    qbody = """INSERT INTO Replies(author,body,time,question_id) 
               VALUES (:author, :body, CURRENT_TIMESTAMP, :question_id)"""
    params = {'author': author, 'body': body, 'question_id': question_id}
    cur.execute(qbody, params)
    conn.commit()
    conn.close()
    return render_template("insert_ok.html", url=url_for("show_question", id=question_id))


@app.route('/search_question', methods=['GET'])
def search_question():
    tag = request.args['tag']
    conn = sqlite3.connect(DBPATH)
    cur = conn.cursor()
    qbody = """SELECT id,author,title,time,tags 
               FROM Questions 
               WHERE tags LIKE :pattern
               ORDER BY time DESC"""
    params = {'pattern': '%' + tag + '%'}
    cur.execute(qbody, params)
    res = list(cur.fetchall())
    conn.close()
    return render_template('messages_search.html', questions=res, tag=tag)


class FlaskConfig:
    """Configuración de Flask"""
    # Activa depurador y recarga automáticamente
    ENV = 'development'
    DEBUG = True
    TEST = True
    # Imprescindible para usar sesiones
    SECRET_KEY = "la_asignatura_giw&!_()"
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'


if __name__ == '__main__':
    app.config.from_object(FlaskConfig())
    app.run()
