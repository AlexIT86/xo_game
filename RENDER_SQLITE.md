# 🚀 Deploy pe Render.com cu SQLite

## ⚡ Setup Manual (Simplu)

### 1️⃣ Creează Redis (pentru WebSocket)

1. Dashboard → **New** → **Redis**
2. **Name**: `xo-game-redis`
3. **Region**: Frankfurt
4. **Plan**: Free
5. Click **Create Redis**
6. **Copiază Internal Redis URL** (ex: `redis://red-xxxxx:6379`)

### 2️⃣ Creează Web Service

1. Dashboard → **New** → **Web Service**
2. **Connect Repository**: `AlexIT86/xo_game`
3. **Configurare**:

#### Basic Settings:
```
Name: xo-game
Region: Frankfurt
Branch: main
Root Directory: (lasă gol)
Runtime: Python 3
```

#### Build & Deploy:
```
Build Command:
pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate

Start Command:
daphne -b 0.0.0.0 -p $PORT xo_game.asgi:application
```

#### Advanced → Disk (IMPORTANT pentru SQLite):
```
Name: sqlite-data
Mount Path: /opt/render/project/src
Size: 1 GB
```
⚠️ **Fără disk, baza de date se șterge la fiecare restart!**

#### Environment Variables:
```
PYTHON_VERSION = 3.11.0
DEBUG = False
SECRET_KEY = [Click "Generate"]
ALLOWED_HOSTS = xo-game.onrender.com
REDIS_URL = [Paste din Redis - ex: redis://red-xxxxx:6379]
```

4. Click **Create Web Service**

### 3️⃣ Așteaptă Deploy (~3-5 min)

- Redis pornește primul
- Web Service se build-uiește
- Vei primi URL: `https://xo-game.onrender.com`

---

## ✅ Verificare

1. Deschide URL-ul
2. Creează o cameră
3. Testează WebSocket din 2 browsere
4. Joacă! 🎮

---

## 📋 Summary - Copy/Paste Ready

### Build Command:
```bash
pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate
```

### Start Command:
```bash
daphne -b 0.0.0.0 -p $PORT xo_game.asgi:application
```

### Environment Variables:
| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11.0` |
| `DEBUG` | `False` |
| `SECRET_KEY` | `[Generate]` |
| `ALLOWED_HOSTS` | `xo-game.onrender.com` |
| `REDIS_URL` | `redis://red-xxxxx:6379` |

### Disk (Persistent Storage):
| Field | Value |
|-------|-------|
| Name | `sqlite-data` |
| Mount Path | `/opt/render/project/src` |
| Size | `1 GB` |

---

## ⚠️ Limitări SQLite pe Render

### Plan Free:
- ✅ Funcționează perfect pentru demo/portfolio
- ⚠️ **Sleep după 15 min inactivitate**
- ⚠️ **Disk persistent LIMITAT** (1GB max pe free)
- ⚠️ **Datele persistă doar cu disk mount**

### Recommended pentru Producție:
- PostgreSQL (scalabilitate mai bună)
- Sau upgrade la plan Starter cu mai mult disk

---

## 🔄 Update App

```bash
git add .
git commit -m "Update"
git push
```

Render auto-deploy! 🚀

---

## 🐛 Troubleshooting

### Database se resetează la restart
**Problem**: Nu ai configurat disk mount
**Solution**: Adaugă Disk în Settings cu mount path `/opt/render/project/src`

### WebSocket nu funcționează
**Problem**: REDIS_URL lipsește sau greșit
**Solution**: Copiază exact Internal Redis URL din Redis service

### Static files nu se încarcă
**Problem**: ALLOWED_HOSTS greșit
**Solution**: Setează exact hostname-ul: `your-app.onrender.com`

---

**Gata! App-ul tău cu SQLite este LIVE! 🎉**

