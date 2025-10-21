# ✅ Checklist de Testare - Joc X și 0

## Pre-Test Setup

### 1. Instalare
```bash
# Activează mediul virtual
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalează dependențele
pip install -r requirements.txt

# Creează baza de date
python manage.py makemigrations
python manage.py migrate

# Rulează serverul
python manage.py runserver
```

### 2. Verificări Inițiale
- [ ] Serverul pornește fără erori
- [ ] Console-ul nu arată warnings importante
- [ ] Browser se deschide la http://localhost:8000
- [ ] Pagina principală se încarcă

## 🎨 Test UI/UX - Pagina Principală

### Visual Design
- [ ] Background gradient animat se vede
- [ ] Logo X și 0 cu animație pulse
- [ ] Titlu cu gradient text
- [ ] Carduri cu efect glassmorphism
- [ ] Butoane cu hover effect (scale + glow)

### Funcționalitate
- [ ] Buton "Creează Cameră Nouă" funcționează
- [ ] Redirecționează către pagina de joc
- [ ] Input pentru cod cameră acceptă text
- [ ] Input transformă automat în uppercase
- [ ] Validare: cod gol arată eroare
- [ ] Validare: cod inexistent arată eroare
- [ ] Mesaj de eroare are animație shake

### Responsive
- [ ] Layout OK pe desktop (> 768px)
- [ ] Layout OK pe tablet (768px)
- [ ] Layout OK pe mobile (< 480px)
- [ ] Butoanele sunt touch-friendly

## 🎮 Test Gameplay - Camera de Joc

### Setup Test Multiplayer
```
1. Browser 1: http://localhost:8000
2. Click "Creează Cameră Nouă"
3. Copiază codul (ex: ABC123)
4. Browser 2 (Incognito/Alt Browser): http://localhost:8000
5. Click "Intră în Cameră"
6. Introdu codul ABC123
```

### Conexiune și Setup
- [ ] Jucătorul 1 primește X
- [ ] Jucătorul 2 primește O
- [ ] Ambii văd mesaj "Conectat la cameră!"
- [ ] Player badge apare cu simbolul corect
- [ ] Status: "Este tura ta!" pentru X
- [ ] Status: "Așteaptă adversarul..." pentru O

### Gameplay Flow
- [ ] X poate face prima mutare
- [ ] O nu poate face mutare înainte de X
- [ ] Simbolul X apare cu animație (scale + rotate)
- [ ] Tura se schimbă automat la O
- [ ] Simbolul O apare cu animație
- [ ] Ambii jucători văd mutările în timp real
- [ ] Click pe celulă ocupată: shake + toast error
- [ ] Click când nu e tura: toast "Nu este tura ta!"

### Câștigător - Linie Orizontală
```
Test: X câștigă pe rândul 1
X | X | X
---------
O | O |  
---------
  |   |  
```
- [ ] Linie animată apare peste simbolurile câștigătoare
- [ ] Confetti explosion pentru X
- [ ] Status: "Ai câștigat!" pentru X
- [ ] Status: "Ai pierdut!" pentru O
- [ ] Scor X incrementat cu 1
- [ ] Buton "Joc Nou" apare

### Câștigător - Linie Verticală
```
Test: O câștigă pe coloana 2
X | O | X
---------
  | O |  
---------
X | O |  
```
- [ ] Linie verticală desenată corect
- [ ] Confetti pentru O
- [ ] Scor O incrementat

### Câștigător - Diagonală
```
Test: X câștigă diagonal
X | O | O
---------
  | X |  
---------
O |   | X
```
- [ ] Linie diagonală desenată corect
- [ ] Animație victorie

### Remiză
```
Test: Remiză (tablă plină, fără câștigător)
X | O | X
---------
O | O | X
---------
X | X | O
```
- [ ] Status: "Remiză!"
- [ ] Icon 🤝
- [ ] Scor remize incrementat
- [ ] Fără confetti
- [ ] Buton "Joc Nou" apare

### Restart Joc
- [ ] Click "Joc Nou" resetează tabla
- [ ] Scorul rămâne (nu se resetează)
- [ ] Tura revine la X
- [ ] Status: "Este tura ta!" pentru X
- [ ] Linia câștigătoare dispare
- [ ] Confetti se oprește

## 🎯 Test Validări

### Mutări Invalide
- [ ] Nu poți plasa simbol pe celulă ocupată
- [ ] Nu poți face mutare când nu e tura ta
- [ ] Nu poți face mutare după ce jocul s-a terminat
- [ ] Toate validările arată toast notification

### Camere
- [ ] Cod inexistent: eroare "Camera nu există"
- [ ] Cameră plină (2 jucători): eroare "Camera e plină"
- [ ] Al 3-lea jucător nu poate intra

## 🔔 Test Notificări Toast

### Tipuri de Toast
- [ ] Success (verde): "Conectat la cameră!"
- [ ] Error (roșu): "Celula este deja ocupată!"
- [ ] Warning (portocaliu): "Nu este tura ta!"
- [ ] Info (albastru): "Joc nou început!"

### Comportament Toast
- [ ] Apare din dreapta (slide-in)
- [ ] Auto-dismiss după 3 secunde
- [ ] Multiple toasts stack vertical
- [ ] Icon emoji corespunzător

## 📱 Test Responsive

### Desktop (1920x1080)
- [ ] Layout simetric
- [ ] Spacing generos
- [ ] Hover effects funcționează
- [ ] Toate elementele vizibile

### Tablet (768x1024)
- [ ] Grid adaptat
- [ ] Butoane mai mari
- [ ] Touch friendly

### Mobile (375x667)
- [ ] Layout single column
- [ ] Tabla joc ocupă width optim
- [ ] Cod cameră se vede complet
- [ ] Buton "Joc Nou" accesibil

### Test DevTools
```
1. F12 > Device Toolbar
2. Test: iPhone SE, iPad, Desktop
3. Rotație: Portrait și Landscape
```
- [ ] Layout se adaptează
- [ ] Fără overflow horizontal
- [ ] Toate butoanele funcționează

## 🎨 Test Animații

### La Încărcare
- [ ] Fade-in pentru logo
- [ ] Fade-in-up pentru carduri
- [ ] Smooth transitions

### Interacțiuni
- [ ] Hover pe butoane: scale + glow
- [ ] Hover pe celule: border + scale
- [ ] Input focus: border glow + scale
- [ ] Buton loading state la submit

### Gameplay
- [ ] Pulse pe codul camerei
- [ ] Simboluri apar cu rotate + scale
- [ ] Shake la mutare invalidă
- [ ] Cell pulse pentru celula activă
- [ ] Winning line draw animation
- [ ] Confetti physics

## 🔧 Test Tehnic

### WebSocket
```
F12 > Console > Network > WS
```
- [ ] WebSocket connection established
- [ ] Mesaj "player_assigned" primit
- [ ] Mesaj "game_update" la fiecare mutare
- [ ] Mesaj "player_disconnected" la disconnect
- [ ] Fără erori în console

### Database
```bash
python manage.py shell
```
```python
from game.models import GameRoom
rooms = GameRoom.objects.all()
print(f"Camere create: {rooms.count()}")
for room in rooms:
    print(f"{room.code}: {room.status}, X={room.score_x}, O={room.score_o}")
```
- [ ] Camerele se salvează în DB
- [ ] Scorul se actualizează
- [ ] Status-ul se schimbă corect

### Admin Panel
```
1. python manage.py createsuperuser
2. http://localhost:8000/admin
3. Login cu credentials
```
- [ ] GameRoom apare în admin
- [ ] List display arată toate câmpurile
- [ ] Poți edita o cameră
- [ ] Poți șterge o cameră

## 🌐 Test Cross-Browser

### Chrome/Edge (Chromium)
- [ ] Toate funcționalitățile OK
- [ ] WebSocket funcționează
- [ ] Animații smooth

### Firefox
- [ ] WebSocket OK
- [ ] CSS Grid OK
- [ ] Animații OK

### Safari (Mac/iOS)
- [ ] Layout OK
- [ ] WebSocket OK
- [ ] Touch events OK

## 🔍 Test Edge Cases

### Deconectare Jucător
```
1. Joacă cu 2 jucători
2. Închide tab-ul unuia dintre jucători
```
- [ ] Celălalt jucător vede "Jucător deconectat"
- [ ] Toast notification apare
- [ ] Board se dezactivează

### Refresh Pagină
```
1. În mijlocul jocului, refresh (F5)
```
- [ ] Reconectare automată
- [ ] Starea jocului se păstrează
- [ ] Simbolul jucătorului se păstrează

### Multiple Camere
```
1. Creează Camera A
2. Creează Camera B
3. Joacă în ambele simultan (4 tab-uri)
```
- [ ] Fiecare cameră independentă
- [ ] Nu se amestecă mutările
- [ ] Scor separat per cameră

## ⚡ Test Performance

### Load Time
- [ ] Pagina principală < 1s
- [ ] Pagina joc < 1s
- [ ] Fonts se încarcă rapid
- [ ] Fără FOUC (Flash of Unstyled Content)

### Runtime
- [ ] Animații smooth (60fps)
- [ ] Fără lag la mutări
- [ ] WebSocket latency < 100ms
- [ ] Memory usage constant

### Network
```
F12 > Network
```
- [ ] CSS: 1 request
- [ ] JS: 1 request
- [ ] Fonts: 1 request
- [ ] Total < 200KB

## 📋 Rezultat Final

### Bugs Găsite
```
# Listează aici orice bug găsit:
1. 
2. 
3. 
```

### Îmbunătățiri Sugerate
```
# Idei pentru viitor:
1. 
2. 
3. 
```

### Status Test
- [ ] Toate testele trecute ✅
- [ ] Gata pentru demonstrație
- [ ] Gata pentru deployment

---

## 🎉 Dacă Toate Testele Trec

**FELICITĂRI! Ai o aplicație full-stack profesională! 🚀**

Următorii pași:
1. Deploy pe Heroku/Railway
2. Adaugă în portfolio
3. Share cu prietenii
4. Continuă dezvoltarea cu features noi

---

**Data testării:** _______________  
**Testat de:** _______________  
**Status:** ⬜ PASSED / ⬜ FAILED  


