import os


def configure(app):
    app.secret_key = os.getenv('FLASK_SECRET_KEY') or 'reallystrongsecretkey'
    app.config['REDIS_HOST'] = os.getenv('REDIS_HOST') or '127.0.0.1'
    app.config['REDIS_PORT'] = int(os.getenv('REDIS_PORT') or 6379)
    app.config['REDIS_URL'] = 'redis://{}:{}'.format(app.config['REDIS_HOST'], app.config['REDIS_PORT'])
    app.config['PORT'] = os.getenv('PORT') or '5321'

    return app
