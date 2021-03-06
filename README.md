# InstaKiloGram
InstaKiloGram is a simple Instagram clone web app built with Django and Bootstrap

## Authors
  - Ryszard Orlikowski
  - Rafał Brauner
  - Dawid Piela
  - Sebastian Słomka
  - Kacper Czarnik

## Features
  - User registration, login
  - User profile with avatar
  - Search users
  - Follow users
  - Add, edit, delete post
  - Like, unlike post
  - Add, delete comment
  - Supported tags


## Demo
 [instakilogram.pythonanywhere.com](https://instakilogram.pythonanywhere.com)
      Username: admin
      Password: admin

## Documentation

### Structure
  - app - consists of app sources
  - app/migrations - consists of migrations generated by `python manage.py makemigrations`
  - app/templatetags - consists of methods that can be used in templates
  - app/admin.py - consists of admin models
  - app/app.py - has class with main app config
  - app/models.py - consists of app models
  - app/tests.py - consists of tests
  - app/urls.py - consists of routings with defined views for each of them
  - app/views.py - consists of view classes to handle requests and prepare response
  - instakilogram - consists of configuration files
  - instakilogram/settings.py - define most configs/settings of app
  - instakilogram/urls.py - define app configs (it can include app/urls.py)
  - instakilogram/wsgi.py - wsgi configs
  - media - consists of assets, files etc. used by whole website or like default values
  - templates - consists of view html templates
  - templates/account - consists of templates used to manage account, login and logout
  - templates/app - consists of templates used by app such as homepage, posts, comments, user details etc.
  - templates/base.html - common html for all templates
  - .gitignore - specify which files and folders should be omited in git
  - LICENSE - license file
  - manage.py - file used by Django to managing app using cli
  - README.md - help file
  - requirements.txt - all depenedencies used by app

### Installation
  1. `pip install -r requirements.txt`

### Making migration (creating class in `app/migrations` which consists of models snapshoot)
  1. `python manage.py makemigrations`

### Migrate (update db schemat using migrations)
  1. `python manage.py migrate`

### Run application
  1. `python manage.py runserver`
