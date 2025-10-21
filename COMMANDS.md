# 🚀 Comenzi Rapide - Joc X și 0

## Setup Inițial

### Creează și activează mediul virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Instalează dependențele
```bash
pip install -r requirements.txt
```

### Setup baza de date
```bash
python manage.py makemigrations
python manage.py migrate
```

## Comenzi de Dezvoltare

### Rulează serverul
```bash
python manage.py runserver
```

### Rulează pe alt port
```bash
python manage.py runserver 8001
```

### Rulează pe toate interfețele (accesibil în rețea)
```bash
python manage.py runserver 0.0.0.0:8000
```

## Comenzi Database

### Creează migrări
```bash
python manage.py makemigrations
```

### Aplică migrări
```bash
python manage.py migrate
```

### Verifică starea migrărilor
```bash
python manage.py showmigrations
```

### Reset database (ATENȚIE: șterge toate datele!)
```bash
# Windows
del db.sqlite3
python manage.py migrate

# Linux/Mac
rm db.sqlite3
python manage.py migrate
```

## Admin Panel

### Creează superuser
```bash
python manage.py createsuperuser
```
Urmează instrucțiunile și alege:
- Username: admin
- Email: (opțional)
- Password: (parolă sigură)

### Accesează admin
```
http://localhost:8000/admin
```

## Django Shell

### Deschide shell
```bash
python manage.py shell
```

### Exemple de comenzi în shell

#### Vezi toate camerele
```python
from game.models import GameRoom

# Toate camerele
rooms = GameRoom.objects.all()
for room in rooms:
    print(f"Cod: {room.code}, Status: {room.status}, Scor: X={room.score_x} O={room.score_o}")
```

#### Creează o cameră manual
```python
from game.models import GameRoom

room = GameRoom.objects.create(
    code="TEST01",
    status="waiting"
)
room.initialize_board()
print(f"Cameră creată: {room.code}")
```

#### Șterge toate camerele
```python
from game.models import GameRoom
GameRoom.objects.all().delete()
print("Toate camerele au fost șterse")
```

#### Verifică o cameră specifică
```python
from game.models import GameRoom
room = GameRoom.objects.get(code="ABC123")
print(f"Board: {room.board}")
print(f"Status: {room.status}")
print(f"Tura: {room.current_turn}")
```

## Comenzi Static Files

### Colectează static files (pentru producție)
```bash
python manage.py collectstatic
```

### Verifică unde sunt static files
```bash
python manage.py findstatic style.css
```

## Testing și Debugging

### Verifică configurarea
```bash
python manage.py check
```

### Vezi toate comenzile disponibile
```bash
python manage.py help
```

### Verifică versiunea Django
```bash
python manage.py version
```

### Test ASGI/Channels
```bash
python manage.py runserver
# Verifică în console că Daphne rulează
# Trebuie să vezi: "Starting ASGI/Daphne"
```

## Comenzi Utile de Dezvoltare

### Instalează o dependență nouă
```bash
pip install nume_pachet
pip freeze > requirements.txt
```

### Upgrade dependențe
```bash
pip install --upgrade django
pip install --upgrade channels
```

### Verifică dependențele instalate
```bash
pip list
```

### Dezactivează mediul virtual
```bash
deactivate
```

## Git (după ce adaugi în repo)

### Status
```bash
git status
```

### Add și commit
```bash
git add .
git commit -m "Mesaj commit"
```

### Push
```bash
git push origin main
```

### .gitignore este deja configurat!
- `__pycache__/`
- `db.sqlite3`
- `venv/`
- `*.pyc`

## Troubleshooting

### Eroare: "No module named X"
```bash
# Asigură-te că ai activat venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Reinstalează dependențele
pip install -r requirements.txt
```

### Eroare: "Port already in use"
```bash
# Găsește procesul care folosește portul (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9

# SAU rulează pe alt port
python manage.py runserver 8001
```

### Eroare: "No such table"
```bash
# Recreează baza de date
python manage.py migrate
```

### WebSocket nu funcționează
```bash
# Verifică că Daphne este instalat
pip show daphne

# Verifică settings.py
# ASGI_APPLICATION trebuie să fie 'xo_game.asgi.application'

# Verifică că Channels este în INSTALLED_APPS
python manage.py shell
>>> from django.conf import settings
>>> 'channels' in settings.INSTALLED_APPS
True
```

## Performance Monitoring

### Vezi query-urile SQL (debug)
```python
# În settings.py, setează:
DEBUG = True

# În shell sau view:
from django.db import connection
print(connection.queries)
```

### Profiling
```bash
pip install django-debug-toolbar
# Adaugă în INSTALLED_APPS și middleware
```

## Production

### Generează SECRET_KEY nouă
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### Setări pentru producție
```python
# În settings.py:
DEBUG = False
SECRET_KEY = 'noua-ta-cheie-secreta'
ALLOWED_HOSTS = ['domeniul-tau.com', 'www.domeniul-tau.com']

# Channel Layers cu Redis
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
```

## Quick Commands (cel mai des folosite)

```bash
# Start rapid
venv\Scripts\activate && python manage.py runserver

# Reset complet
del db.sqlite3 && python manage.py migrate

# Update după schimbări în model
python manage.py makemigrations && python manage.py migrate

# Creează admin user
python manage.py createsuperuser

# Colectează static și runserver
python manage.py collectstatic --noinput && python manage.py runserver
```

## Começi pentru Testare

### Test toate camerele
```bash
python manage.py shell
>>> from game.models import GameRoom
>>> GameRoom.objects.all().count()
```

### Creează camere de test
```bash
python manage.py shell
>>> from game.models import GameRoom
>>> for i in range(5):
...     code = GameRoom.generate_code()
...     room = GameRoom.objects.create(code=code, status='waiting')
...     room.initialize_board()
...     print(f"Cameră creată: {code}")
```

## Backup și Restore

### Backup database
```bash
# Windows
copy db.sqlite3 db.sqlite3.backup

# Linux/Mac
cp db.sqlite3 db.sqlite3.backup
```

### Restore database
```bash
# Windows
copy db.sqlite3.backup db.sqlite3

# Linux/Mac
cp db.sqlite3.backup db.sqlite3
```

### Export data (JSON)
```bash
python manage.py dumpdata game > backup.json
```

### Import data
```bash
python manage.py loaddata backup.json
```

---

## 📚 Documentație Oficială

- Django: https://docs.djangoproject.com/
- Channels: https://channels.readthedocs.io/
- Daphne: https://github.com/django/daphne

---

**Pro Tip:** Salvează acest fișier și folosește-l ca referință rapidă! 🚀

