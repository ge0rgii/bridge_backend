# bridge_backend
backend for bridge app

requirements:
python
django

run server: 
cd backend
python3 manage.py runserver

admin:
http://localhost:8000/admin/

API:
http://localhost:8000/api/

Signup (send json with username and password, returns json with token):
http://localhost:8000/api/signup

Login (send json with username and password, returns json with token):
http://localhost:8000/api/login
