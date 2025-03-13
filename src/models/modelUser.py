from models.entities.user import User
from werkzeug.security import check_password_hash


class ModelUSer():

    @classmethod
    def login(cls, db, user):
        try:
            cur = db.connection.cursor()  
            sql = 'SELECT * FROM usuarios WHERE email = %s'
            cur.execute(sql, (user.email,))
            row = cur.fetchone()
            if row:
                 if check_password_hash(row[3], user.password):
                    return User(row[0],row[1],row[2],row[3])
            return None
        except Exception as e:
            raise Exception(e)
        
    @classmethod
    def get_by_id(cls, db, id):
        try:
            cur = db.connection.cursor()  
            sql = 'SELECT * FROM usuarios WHERE id = %s'
            cur.execute(sql, (id,))
            row = cur.fetchone()
            if row:
                return User(row[0],row[1],row[2],row[3])
            return None
        except Exception as e:
            raise Exception(e)

    @classmethod
    def getContactos(cls, db, user_id):

        try:
            cur = db.connection.cursor()
            sql = 'SELECT * FROM contactos WHERE user_id = %s'
            cur.execute(sql, (user_id, ))
            data = cur.fetchall()
            if data:
                return data
            return None
        except Exception as e:
            raise Exception(e)
        
    @classmethod
    def addContactos(cls, db, nombre, telefono, descripcion, user_id):

        try:
            cur = db.connection.cursor()
            cur.execute('INSERT INTO contactos VALUES(%s,%s,%s,%s,%s)', (None,user_id, nombre, telefono, descripcion))
            db.connection.commit()

        except Exception as e:
            raise Exception(e)