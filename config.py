class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:danchik112345@localhost:3306/aviasales'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CSRF_ENABLED = True
    # Connected with @Pomah3: https://github.com/pomah3
    SECRET_KEY = 'you-will-never-guess'