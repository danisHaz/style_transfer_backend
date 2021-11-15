class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:////home/juvenal/github_projects/style_transfer_backend/dbs/test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CSRF_ENABLED = True
    # Remember you @Pomah3: https://github.com/pomah3
    SECRET_KEY = 'you-will-never-guess'