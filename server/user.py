import sqlite3
from flask_restx import Namespace, Resource, reqparse, inputs
api = Namespace('users', description='User resources')
from flask import request

#---------------------------------------------------------------------------
@api.route('/users/<int:user_id>')
@api.param('user_id', description='User ID')
class User(Resource):
    def get(self, user_id):
        db = sqlite3.connect('db.sqlite')
        c = db.cursor()
        c.execute("select name from appuser where id = ?", (user_id,))
        for name, in c:
            return {'id': user_id, 'name': name}  #Выводим пользователя в виде json.


@api.route('/users/')
class Users(Resource):
    def get(self):
        db = sqlite3.connect('db.sqlite')
        c = db.cursor()
        c.execute("SELECT id, name FROM appuser")
        return {'users': {str(name[0]): name[1] for name in c}} #Выводим всех пользователей в виде json.


@api.route('/users/insert/')
class Insert(Resource):
    def post(self):
        if request.values:
            user = dict(request.values)
            if 'name' in user:
                db = sqlite3.connect('db.sqlite')
                c = db.cursor()
                c.execute("INSERT INTO appuser (name) VALUES (?)", (user['name'],)) # Добавлено автоинкр. поле для id.
                db.commit()
                return 'Пользователь добавлен'
        else:
            return 'Повторите попытку' #В ТЗ отсутствует указание о необходимости выведения HTTP ошибок.
