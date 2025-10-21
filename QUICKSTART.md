# 🚀 Start Rapid - Joc X și 0

## Metoda 1: Script Automat (Recomandat)

### Windows
Dublu-click pe `start.bat` sau rulează în cmd:
```bash
start.bat
```

### Linux/Mac
```bash
chmod +x start.sh
./start.sh
```

## Metoda 2: Manual

### Pasul 1: Creează mediu virtual
```bash
python -m venv venv
```

### Pasul 2: Activează mediul virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Pasul 3: Instalează dependențele
```bash
pip install -r requirements.txt
```

### Pasul 4: Creează baza de date
```bash
python manage.py makemigrations
python manage.py migrate
```

### Pasul 5: Rulează serverul
```bash
python manage.py runserver
```

### Pasul 6: Deschide browserul
```
http://localhost:8000
```

## 🎮 Testare Multiplayer

Pentru a testa funcționalitatea multiplayer:

1. Deschide aplicația în browser: `http://localhost:8000`
2. Click pe "Creează Cameră Nouă"
3. Copiază codul camerei (6 caractere)
4. Deschide o nouă fereastră/tab în modul incognito sau alt browser
5. Click pe "Intră în Cameră" și introdu codul
6. Acum poți juca între cele două ferestre!

## 🔧 Comenzi Utile

### Creează un admin user (opțional)
```bash
python manage.py createsuperuser
```

### Accesează admin panel
```
http://localhost:8000/admin
```

### Șterge baza de date și restart
```bash
# Windows
del db.sqlite3
python manage.py migrate

# Linux/Mac
rm db.sqlite3
python manage.py migrate
```

### Verifică versiunea Django
```bash
python manage.py --version
```

## ❓ Probleme Comune

### Eroare: "No module named django"
**Soluție:** Asigură-te că ai activat mediul virtual
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Eroare: "Port already in use"
**Soluție:** Rulează pe alt port
```bash
python manage.py runserver 8001
```

### WebSocket nu se conectează
**Soluție:** 
1. Verifică că serverul rulează
2. Deschide Console în browser (F12) și verifică erorile
3. Asigură-te că folosești un browser modern (Chrome, Firefox, Edge)

## 📱 Funcționalități de Testat

- ✅ Creare cameră cu cod unic
- ✅ Intrare în cameră cu cod
- ✅ Mutări în timp real între jucători
- ✅ Detectare câștigător / remiză
- ✅ Linie animată pe simbolurile câștigătoare
- ✅ Confetti la victorie
- ✅ Scor persistent per cameră
- ✅ Restart joc
- ✅ Notificări toast
- ✅ Copiere cod cameră
- ✅ Responsive design (testează pe mobile)

## 🎨 Features Vizuale

- Gradient animat pe fundal
- Glassmorphism pe carduri
- Animații smooth pe toate elementele
- Hover effects
- Pulse animation pe codul camerei
- Simboluri X și O animate când sunt plasate
- Shake effect la mutare invalidă
- Confetti explosion la victorie

## 📚 Next Steps

După ce testezi aplicația:

1. Explorează codul în `game/models.py` - logica jocului
2. Verifică `game/consumers.py` - WebSocket handling
3. Customizează stilurile în `game/static/css/style.css`
4. Modifică animațiile în `game/static/js/game.js`

## 🚀 Ready for Production?

Când ești gata să deployezi:

1. Instalează Redis
2. Configurează Redis în `settings.py`
3. Setează `DEBUG = False`
4. Generează `SECRET_KEY` nou
5. Configurează `ALLOWED_HOSTS`
6. Folosește PostgreSQL în loc de SQLite
7. Deploy pe Heroku/Railway/DigitalOcean

---

**Distractie placuta! 🎮**


