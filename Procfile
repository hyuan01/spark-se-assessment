web: gunicorn project.server.__init__:app
heroku ps:scale web=1
release: python manage.py db upgrade

