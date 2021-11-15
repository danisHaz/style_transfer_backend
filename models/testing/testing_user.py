from init import my_db

class User(my_db.Model):
    id = my_db.Column(my_db.Integer, primary_key=True)
    username = my_db.Column(my_db.String(80), unique=True, nullable=False)
    email = my_db.Column(my_db.String(120), unique=True, nullable=False)