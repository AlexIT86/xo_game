# 🎮 Joc X și 0 Multiplayer

O aplicație modernă Django pentru jocul clasic X și 0 (Tic-Tac-Toe) cu funcționalitate multiplayer în timp real folosind WebSockets.

## ✨ Funcționalități

- 🎯 **Multiplayer Real-Time**: Joacă cu prietenii folosind WebSockets
- 🔐 **Sistem de Camere**: Creează sau intră în camere folosind coduri unice de 6 caractere
- 🏆 **Scor Persistent**: Urmărește victoriile X, O și remizele
- 🎨 **UI Modern și Animat**: Design glassmorphism cu animații smooth
- 📱 **Responsive**: Funcționează perfect pe mobile și desktop
- 🎉 **Efecte Vizuale**: Confetti la victorie, animații pentru mutări, linii câștigătoare

## 🚀 Instalare și Rulare

### Cerințe

- Python 3.8+
- pip

### Pași de Instalare

1. **Clonează sau descarcă proiectul**

2. **Creează un mediu virtual**
```bash
python -m venv venv
```

3. **Activează mediul virtual**

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

4. **Instalează dependențele**
```bash
pip install -r requirements.txt
```

5. **Creează baza de date**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Creează un superuser (opțional)**
```bash
python manage.py createsuperuser
```

7. **Rulează serverul**
```bash
python manage.py runserver
```

8. **Deschide în browser**
```
http://localhost:8000
```

## 🎮 Cum se Joacă

1. **Creează o Cameră**
   - Click pe "Creează Cameră Nouă"
   - Primești un cod unic de 6 caractere
   - Trimite codul prietenului tău

2. **Intră în Cameră**
   - Click pe "Intră în Cameră"
   - Introdu codul primit de la prieten
   - Jocul începe automat când ambii jucători sunt conectați

3. **Joacă**
   - Primul jucător este X, al doilea este O
   - Click pe o celulă goală pentru a face o mutare
   - Alternarea este automată
   - Primul care face o linie de 3 câștigă!

4. **Joc Nou**
   - După ce jocul se termină, click pe "Joc Nou"
   - Scorul este păstrat pentru fiecare cameră

## 🏗️ Structura Proiectului

```
xo_game/
├── game/                      # Aplicația principală
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css     # Stiluri și animații
│   │   └── js/
│   │       └── game.js       # Logică WebSocket și UI
│   ├── templates/
│   │   └── game/
│   │       ├── index.html    # Pagina principală
│   │       └── game_room.html # Pagina de joc
│   ├── consumers.py          # WebSocket Consumer
│   ├── models.py             # Model GameRoom
│   ├── views.py              # Views
│   ├── urls.py               # URL patterns
│   └── routing.py            # WebSocket routing
├── xo_game/                  # Configurare proiect
│   ├── settings.py           # Settings Django + Channels
│   ├── asgi.py              # ASGI config
│   ├── urls.py              # URL root
│   └── wsgi.py              # WSGI config
├── manage.py
├── requirements.txt
└── README.md
```

## 🎨 Design și Tehnologii

### Frontend
- **HTML5 Semantic**
- **CSS3** cu animații avansate
  - Glassmorphism
  - Gradient animat
  - Transitions și transforms
  - Responsive design
- **Vanilla JavaScript**
  - WebSocket client
  - DOM manipulation
  - Canvas pentru confetti

### Backend
- **Django 5.0**
- **Django Channels 4.0** pentru WebSockets
- **Daphne** ASGI server
- **SQLite** pentru baza de date (development)

## 🔧 Configurare Producție

### Redis pentru Channels

Pentru producție, recomandăm folosirea Redis în loc de InMemoryChannelLayer:

1. Instalează Redis
2. Instalează channels-redis (deja în requirements.txt)
3. În `settings.py`, decomentează configurarea Redis:

```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
```

### Deployment

Aplicația poate fi deployată pe:
- **Heroku** (cu Redis addon)
- **Railway**
- **PythonAnywhere**
- **DigitalOcean**
- Orice platformă cu support pentru ASGI

### Setări Importante pentru Producție

În `settings.py`:
```python
DEBUG = False
SECRET_KEY = 'genereaza-o-cheia-securizata'
ALLOWED_HOSTS = ['domeniul-tau.com']
```

## 📋 Features Viitoare (Opțional)

- [ ] Sistem de autentificare
- [ ] Chat în cameră
- [ ] Istoric jocuri
- [ ] Leaderboard global
- [ ] Teme de culori personalizabile
- [ ] Sunet pentru mutări și victorii
- [ ] Spectatori în camere
- [ ] Tournament mode

## 🐛 Debugging

### WebSocket nu se conectează
- Verifică că serverul rulează cu `python manage.py runserver`
- Verifică console-ul browserului pentru erori
- Asigură-te că portul 8000 nu este blocat de firewall

### Erori la migration
```bash
python manage.py makemigrations game
python manage.py migrate
```

### Clear cache și restart
```bash
# Șterge fișierele cache
find . -type d -name __pycache__ -exec rm -r {} +

# Recreează baza de date (ATENȚIE: șterge datele)
del db.sqlite3  # Windows
rm db.sqlite3   # Linux/Mac

python manage.py migrate
```

## 👨‍💻 Dezvoltator

Creat cu ❤️ folosind Django & Channels

## 📄 Licență

Acest proiect este open source și disponibil sub licența MIT.

---

**Enjoy coding! 🚀**

