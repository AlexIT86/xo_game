# 🚀 Deployment pe Render.com

Ghid complet pentru deployment al jocului X și 0 pe Render.com cu suport WebSocket.

## 📋 Pregătire

### 1. Fișiere Create pentru Render

✅ **render.yaml** - Configurare automată Blueprint
✅ **build.sh** - Script de build pentru instalare și setup
✅ **settings_production.py** - Settings optimizate pentru producție
✅ **requirements.txt** - Actualizat cu dependențe producție

### 2. Ce Oferă Render.com (Plan Free)

- **Web Service** - Django + Daphne (HTTP + WebSocket)
- **PostgreSQL Database** - 256MB storage
- **Redis** - Pentru Channel Layers (WebSocket sync)
- **SSL/TLS** - HTTPS gratuit
- **Auto-deploy** - La fiecare push pe GitHub

## 🔧 Pași de Deployment

### Metoda 1: Blueprint Deploy (RECOMANDAT - Automatizat)

1. **Push pe GitHub** (deja făcut ✅)
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push
   ```

2. **Conectează la Render.com**
   - Mergi la: https://render.com
   - Click **"Get Started"** sau **"Sign Up"**
   - Autentifică-te cu **GitHub**

3. **Create New Blueprint**
   - Dashboard → **"New"** → **"Blueprint"**
   - **Connect Repository**: Selectează `AlexIT86/xo_game`
   - Render va detecta automat `render.yaml`
   - Click **"Apply"**

4. **Așteaptă Deploy** (~5-10 minute)
   - Redis se creează primul
   - PostgreSQL se creează
   - Web Service se build-uiește și pornește
   - Vei primi URL-ul: `https://xo-game.onrender.com`

### Metoda 2: Manual Setup (Mai multe controale)

#### A. Creează Redis
1. Dashboard → **"New"** → **"Redis"**
2. **Name**: `xo-game-redis`
3. **Region**: Frankfurt (sau cel mai aproape)
4. **Plan**: Free
5. Click **"Create Redis"**
6. **Copiază Internal Redis URL** (îl vei folosi mai târziu)

#### B. Creează PostgreSQL Database
1. Dashboard → **"New"** → **"PostgreSQL"**
2. **Name**: `xo-game-db`
3. **Database**: `xo_game`
4. **User**: `xo_game_user`
5. **Region**: Frankfurt (același ca Redis)
6. **Plan**: Free
7. Click **"Create Database"**
8. **Copiază Internal Database URL**

#### C. Creează Web Service
1. Dashboard → **"New"** → **"Web Service"**
2. **Connect Repository**: Selectează `AlexIT86/xo_game`
3. **Configurare**:
   - **Name**: `xo-game`
   - **Region**: Frankfurt
   - **Branch**: `main`
   - **Root Directory**: (lasă gol)
   - **Runtime**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `daphne -b 0.0.0.0 -p $PORT xo_game.asgi:application`
   - **Plan**: Free

4. **Environment Variables** (Advanced → Environment):
   ```
   PYTHON_VERSION=3.11.0
   DEBUG=False
   DJANGO_SETTINGS_MODULE=xo_game.settings_production
   SECRET_KEY=[Click "Generate" pentru o cheie sigură]
   DATABASE_URL=[Paste Internal Database URL de la PostgreSQL]
   REDIS_URL=[Paste Internal Redis URL]
   ALLOWED_HOSTS=xo-game.onrender.com
   ```

5. Click **"Create Web Service"**

## 🔐 Environment Variables Necesare

Asigură-te că ai setat toate acestea în Render Dashboard:

| Variabilă | Valoare | Descriere |
|-----------|---------|-----------|
| `PYTHON_VERSION` | `3.11.0` | Versiunea Python |
| `DEBUG` | `False` | Disable debug în producție |
| `SECRET_KEY` | `[Generate]` | Cheie secretă Django |
| `DATABASE_URL` | `[Auto from DB]` | Connection string PostgreSQL |
| `REDIS_URL` | `[Auto from Redis]` | Connection string Redis |
| `DJANGO_SETTINGS_MODULE` | `xo_game.settings_production` | Settings pentru producție |
| `ALLOWED_HOSTS` | `xo-game.onrender.com` | Hostname-ul aplicației |

## ✅ Verificare După Deploy

### 1. Check Health
```
https://your-app.onrender.com/
```
Ar trebui să vezi pagina principală

### 2. Check WebSocket
- Creează o cameră
- Intră din 2 browsere diferite
- Testează că mutările se sincronizează în timp real

### 3. Check Admin
```
https://your-app.onrender.com/admin/
```

## 🐛 Troubleshooting

### Eroare: "Application failed to respond"
**Cauză**: Daphne nu pornește corect
**Soluție**:
1. Check Logs în Render Dashboard
2. Verifică că `DJANGO_SETTINGS_MODULE=xo_game.settings_production`
3. Verifică că toate env vars sunt setate

### Eroare: "DisallowedHost at /"
**Cauză**: ALLOWED_HOSTS nu include hostname-ul Render
**Soluție**:
1. Dashboard → Service → Environment
2. Adaugă/Modifică: `ALLOWED_HOSTS=your-app.onrender.com`
3. Salvează → Auto-redeploy

### WebSocket nu se conectează
**Cauză**: Redis nu este configurat sau URL greșit
**Soluție**:
1. Verifică că Redis service rulează (Dashboard)
2. Verifică `REDIS_URL` în Environment Variables
3. Ar trebui să fie ceva de genul: `redis://red-xxxxx:6379`

### Static files nu se încarcă
**Cauză**: WhiteNoise nu este configurat corect
**Soluție**:
1. Verifică în Logs: `python manage.py collectstatic`
2. Check `settings_production.py` are WhiteNoise în MIDDLEWARE

### Database migrations nu rulează
**Soluție**:
```bash
# În Render Shell (Dashboard → Shell)
python manage.py migrate
python manage.py createsuperuser
```

## 🔄 Update Aplicația

### Automatic Deploy
Render auto-deploy-uiește la fiecare push pe `main`:
```bash
git add .
git commit -m "Update features"
git push
```

### Manual Deploy
1. Render Dashboard → Service
2. **"Manual Deploy"** → **"Deploy latest commit"**

## 📊 Monitoring

### Logs
- Dashboard → Service → **Logs**
- Vezi logs în timp real
- Filtrează după nivel (Info, Warning, Error)

### Metrics
- Dashboard → Service → **Metrics**
- CPU usage
- Memory usage
- Request count

## 💰 Costuri

### Plan Free (Demo și Testing)
✅ Web Service: 750 ore/lună gratuit
✅ PostgreSQL: 256MB storage gratuit
✅ Redis: 25MB gratuit
⚠️ Sleep după 15 min inactivitate
⚠️ 512MB RAM

**Perfect pentru:**
- Portfolio projects
- Demonstrații
- Testing
- Învățare

### Plan Starter ($7/lună) - Recomandat pentru Producție
✅ Nu face sleep
✅ 512MB+ RAM
✅ Suport tehnic
✅ Custom domains

## 🌐 Custom Domain (Opțional)

1. Dashboard → Service → **Settings**
2. **Custom Domain** → **Add Domain**
3. Introdu domeniul tău (ex: `xogame.ro`)
4. Configurează DNS:
   ```
   Type: CNAME
   Name: www (sau @)
   Value: your-app.onrender.com
   ```
5. SSL se configurează automat în ~5 minute

## 🎯 Performance Tips

### 1. Redis Connection Pooling
✅ Deja configurat în `settings_production.py`

### 2. Database Connection Pooling
✅ `conn_max_age=600` activat

### 3. Static Files Compression
✅ WhiteNoise cu `CompressedManifestStaticFilesStorage`

### 4. Gunicorn Workers (dacă folosești Gunicorn)
```
workers = (2 * cpu_count) + 1
```

## 🔒 Security Checklist

- ✅ DEBUG=False
- ✅ SECRET_KEY securizată (generate)
- ✅ HTTPS redirect activat
- ✅ HSTS activat
- ✅ Secure cookies
- ✅ CSRF protection
- ✅ XSS protection
- ✅ Content-Type nosniff

## 📞 Support

### Render Documentation
- https://render.com/docs
- https://render.com/docs/deploy-django

### Django Channels on Render
- https://render.com/docs/deploy-django-channels

### Forum
- https://community.render.com

## 🎉 Success!

După deployment, aplicația ta va fi live la:
```
https://your-app.onrender.com
```

Distribuie link-ul și joacă X și 0 cu prietenii! 🎮

---

**Pro Tip:** Plan Free face sleep după 15 min. Prima cerere va dura ~30s pentru wake-up. Pentru producție reală, upgrade la Starter plan.

**Enjoy your deployed app! 🚀**

