class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:danchik112345@localhost:3306'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CSRF_ENABLED = True
    # Connected with @Pomah3: https://github.com/pomah3
    SECRET_KEY = 'you-will-never-guess'

    # MYSQL_HOST = 'localhost'
    # MYSQL_USER = 'admin'
    # MYSQL_PASSWORD = 'danchik112345'
    MYSQL_DB = 'aviasales'