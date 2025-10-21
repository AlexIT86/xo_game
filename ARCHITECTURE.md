# 🏗️ Arhitectura Aplicației - Joc X și 0

## 📋 Structura Proiectului

```
xo_game/
│
├── 📁 game/                          # Aplicația principală Django
│   ├── 📁 migrations/                # Migrări bază de date
│   │   └── __init__.py
│   │
│   ├── 📁 static/                    # Fișiere statice (CSS, JS)
│   │   ├── 📁 css/
│   │   │   └── style.css            # ~500 linii - Toate stilurile și animațiile
│   │   └── 📁 js/
│   │       └── game.js              # ~400 linii - WebSocket și logică UI
│   │
│   ├── 📁 templates/                 # Template-uri HTML
│   │   └── 📁 game/
│   │       ├── index.html           # Pagina principală (meniu)
│   │       └── game_room.html       # Pagina de joc (tabla)
│   │
│   ├── __init__.py
│   ├── admin.py                      # Configurare Django Admin
│   ├── apps.py                       # Configurare aplicație
│   ├── consumers.py                  # WebSocket Consumer (Channels)
│   ├── models.py                     # Model GameRoom + logică joc
│   ├── routing.py                    # WebSocket URL routing
│   ├── urls.py                       # URL patterns HTTP
│   └── views.py                      # Views Django (5 views)
│
├── 📁 xo_game/                       # Configurare proiect Django
│   ├── __init__.py
│   ├── asgi.py                       # ASGI config pentru WebSocket
│   ├── settings.py                   # Settings Django + Channels
│   ├── urls.py                       # Root URL configuration
│   └── wsgi.py                       # WSGI config pentru HTTP
│
├── 📁 venv/                          # Mediu virtual Python (ignorat în git)
│
├── .gitignore                        # Fișiere ignorate de Git
├── ARCHITECTURE.md                   # Acest fișier
├── COMMANDS.md                       # Comenzi rapide
├── FEATURES.md                       # Lista completă funcționalități
├── manage.py                         # CLI Django
├── QUICKSTART.md                     # Ghid start rapid
├── README.md                         # Documentație principală
├── requirements.txt                  # Dependențe Python
├── start.bat                         # Script start Windows
├── start.sh                          # Script start Linux/Mac
└── TEST_CHECKLIST.md                 # Checklist testare
```

## 🔄 Flow de Date

### 1. HTTP Request Flow (Pagini statice)

```
Browser
   │
   ├─→ GET / 
   │      └─→ views.index() 
   │            └─→ templates/game/index.html
   │
   ├─→ POST /create/
   │      └─→ views.create_room()
   │            ├─→ GameRoom.generate_code()
   │            ├─→ GameRoom.objects.create()
   │            └─→ redirect /room/{code}/
   │
   └─→ GET /room/{code}/
          └─→ views.game_room()
                └─→ templates/game/game_room.html
```

### 2. WebSocket Flow (Real-time)

```
Client (Browser)
   │
   └─→ WebSocket Connect: ws://host/ws/game/{code}/
          │
          └─→ GameConsumer.connect()
                 ├─→ Check room exists
                 ├─→ Add player (X or O)
                 ├─→ Join channel group
                 └─→ Broadcast game state
                        │
                        └─→ All clients in room receive update
                               └─→ UI updates automatically
```

### 3. Game Action Flow (Mutare)

```
Player 1 (X) clicks cell
   │
   ├─→ handleCellClick(position)
   │      └─→ Validations (client-side)
   │            ├─→ Is my turn?
   │            ├─→ Game active?
   │            └─→ Cell empty?
   │
   └─→ sendMove(position) via WebSocket
          │
          └─→ GameConsumer.receive()
                 │
                 └─→ GameRoom.make_move(position, player)
                        ├─→ Server validations
                        ├─→ Update board
                        ├─→ Check winner
                        ├─→ Update score if finished
                        └─→ Save to database
                               │
                               └─→ Broadcast to all players
                                      │
                                      ├─→ Player 1: "Așteaptă..."
                                      └─→ Player 2: "Tura ta!"
```

## 🗄️ Model de Date (Database Schema)

### GameRoom Model

```python
GameRoom
├── id (PK)                      # Auto-generated
├── code (UNIQUE, 6 chars)       # Ex: "ABC123"
├── player_x (Channel Name)      # WebSocket channel
├── player_o (Channel Name)      # WebSocket channel
├── board (JSON Array)           # ['', 'X', 'O', '', '', '', '', '', '']
├── current_turn ('X' or 'O')    # Tura curentă
├── status (waiting/playing/finished)
├── winner ('', 'X', 'O', 'draw')
├── score_x (Integer)            # Victorii X
├── score_o (Integer)            # Victorii O
├── score_draws (Integer)        # Remize
├── created_at (DateTime)
└── updated_at (DateTime)
```

### Exemplu de Date

```json
{
  "id": 1,
  "code": "ABC123",
  "player_x": "specific.channel.name.xyz",
  "player_o": "specific.channel.name.abc",
  "board": ["X", "O", "X", "O", "X", "", "", "", "O"],
  "current_turn": "O",
  "status": "playing",
  "winner": "",
  "score_x": 2,
  "score_o": 1,
  "score_draws": 0,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:35:00Z"
}
```

## 🌐 WebSocket Messages (Protocol)

### Client → Server

#### 1. Move (Mutare)
```json
{
  "action": "move",
  "position": 4
}
```

#### 2. Restart (Joc Nou)
```json
{
  "action": "restart"
}
```

### Server → Client

#### 1. Player Assigned (La conectare)
```json
{
  "type": "player_assigned",
  "player": "X"
}
```

#### 2. Game Update (După fiecare acțiune)
```json
{
  "type": "game_update",
  "game_state": {
    "code": "ABC123",
    "board": ["X", "O", "X", "", "", "", "", "", ""],
    "current_turn": "O",
    "status": "playing",
    "winner": "",
    "score": {
      "x": 2,
      "o": 1,
      "draws": 0
    },
    "winning_line": null,
    "player_x_connected": true,
    "player_o_connected": true
  }
}
```

#### 3. Player Disconnected
```json
{
  "type": "player_disconnected",
  "player": "X"
}
```

#### 4. Error
```json
{
  "type": "error",
  "message": "Nu este tura ta!"
}
```

## 🎨 Frontend Architecture

### HTML Structure

```
index.html
├── Header (Logo + Titlu)
├── Main Card
│   ├── Error Message (dacă există)
│   ├── Buton "Creează Cameră"
│   ├── Divider
│   └── Form "Intră în Cameră"
├── Info Cards (3x)
└── Footer

game_room.html
├── Header
│   ├── Room Code + Copy Button
│   └── Home Button
├── Scoreboard (3 coloane)
├── Game Card
│   ├── Game Status
│   ├── Player Badge
│   ├── Game Board (3x3 grid)
│   ├── Winning Line SVG
│   └── Restart Button
├── Toast Container
└── Confetti Canvas
```

### CSS Architecture

```css
style.css
├── Variables CSS (:root)
│   ├── Colors
│   ├── Spacing
│   ├── Border Radius
│   ├── Shadows
│   └── Transitions
│
├── Reset & Base Styles
├── Background Gradient
├── Container & Layout
├── Logo & Header
├── Cards & Glassmorphism
├── Buttons (Primary, Secondary, Restart)
├── Form Elements (Input, Label)
├── Error Messages
├── Info Cards
├── Game Page
│   ├── Room Info
│   ├── Scoreboard
│   ├── Game Card
│   ├── Game Board
│   └── Winning Line
├── Toast Notifications
├── Spinner
├── Animații (@keyframes)
│   ├── fadeIn, fadeInUp
│   ├── pulse, shake
│   ├── symbolAppear
│   ├── drawLine
│   └── confetti
└── Responsive (@media)
```

### JavaScript Architecture

```javascript
game.js
├── Global Variables
│   ├── socket (WebSocket)
│   ├── myPlayer ('X' or 'O')
│   ├── gameState (object)
│   └── isMyTurn (boolean)
│
├── WebSocket Functions
│   ├── initWebSocket()
│   ├── handleWebSocketMessage()
│   └── sendMove()
│
├── UI Update Functions
│   ├── updateGameUI()
│   ├── updateBoard()
│   ├── updateScore()
│   ├── updateGameStatus()
│   └── updateButtons()
│
├── Game Logic
│   ├── handleCellClick()
│   ├── handleGameFinished()
│   └── restartGame()
│
├── Visual Effects
│   ├── showPlayerBadge()
│   ├── drawWinningLine()
│   ├── shakeBoardCell()
│   ├── showToast()
│   ├── triggerConfetti()
│   └── stopConfetti()
│
├── Utility Functions
│   └── copyRoomCode()
│
└── Event Listeners
    ├── DOMContentLoaded
    ├── Cell clicks
    └── Window resize
```

## 🔄 State Management

### Game States

```
WAITING
   │
   ├─→ Player 2 joins
   │
PLAYING
   │
   ├─→ Make moves (X → O → X → O...)
   │   │
   │   ├─→ Winner found?
   │   │      └─→ FINISHED
   │   │
   │   └─→ Board full?
   │          └─→ FINISHED (draw)
   │
FINISHED
   │
   └─→ Restart button
          └─→ PLAYING (board reset, score kept)
```

### Client State Sync

```
Server (Source of Truth)
   │
   ├─→ Database (SQLite)
   │      └─→ GameRoom model
   │
   └─→ Channel Layer (In-Memory)
          │
          └─→ Broadcast to all clients
                 │
                 ├─→ Client 1 (Player X)
                 │      └─→ Update local gameState
                 │            └─→ Render UI
                 │
                 └─→ Client 2 (Player O)
                        └─→ Update local gameState
                              └─→ Render UI
```

## 🔐 Security & Validation

### Server-Side Validations (models.py)

```python
make_move(position, player):
├── Game is active? (status == 'playing')
├── Correct turn? (player == current_turn)
├── Valid position? (0-8)
└── Cell empty? (board[position] == '')
```

### Client-Side Validations (game.js)

```javascript
handleCellClick(position):
├── Is my turn? (isMyTurn)
├── Game active? (status == 'playing')
└── Cell empty? (board[position] == '')
```

### Channel Security (asgi.py)

```python
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(  # ← Security
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    ),
})
```

## 📊 Performance Considerations

### Database Queries
- Indexing pe `code` field pentru lookup rapid
- Single query pentru game state
- Optimistic updates pe client

### WebSocket
- Channel groups pentru room isolation
- Broadcast doar la jucătorii din cameră
- Async/await pentru non-blocking operations

### Frontend
- CSS animations (GPU accelerated)
- RequestAnimationFrame pentru confetti
- Event delegation pentru board cells
- Debounced updates unde e necesar

## 🚀 Deployment Architecture

### Development
```
Django Dev Server (manage.py runserver)
├── HTTP: Port 8000
└── WebSocket: Same port (Daphne)
```

### Production (Recomandare)
```
Nginx (Reverse Proxy)
   │
   ├─→ Static Files (/static/, /media/)
   │
   └─→ Daphne (ASGI Server)
          ├── HTTP Requests
          └── WebSocket Connections
                 │
                 └─→ Redis (Channel Layer)
                        └─→ Cross-process communication
```

### Scalare
```
Load Balancer
   │
   ├─→ App Server 1 (Daphne)
   │      └─→ Redis
   │
   ├─→ App Server 2 (Daphne)
   │      └─→ Redis (Shared)
   │
   └─→ App Server N (Daphne)
          └─→ Redis
```

## 📦 Dependencies Explicații

```
requirements.txt:
├── Django==5.0
│      └─→ Framework web principal
│
├── channels==4.0.0
│      └─→ WebSocket support pentru Django
│
├── channels-redis==4.2.0
│      └─→ Redis backend pentru Channel Layers (production)
│
└── daphne==4.1.0
       └─→ ASGI server pentru HTTP + WebSocket
```

## 🎯 Design Patterns Folosite

### 1. MVC/MVT (Django)
- **Model**: GameRoom (models.py)
- **View**: views.py
- **Template**: HTML files

### 2. Observer Pattern
- WebSocket broadcast → All clients update

### 3. State Pattern
- Game states: waiting → playing → finished

### 4. Singleton Pattern
- WebSocket connection per client

### 5. Factory Pattern
- GameRoom.generate_code()

## 🔍 Debugging Flow

```
Issue Reported
   │
   ├─→ Frontend Issue?
   │      ├─→ Browser Console (F12)
   │      ├─→ Network Tab (WebSocket frames)
   │      └─→ game.js console.log()
   │
   ├─→ Backend Issue?
   │      ├─→ Server Console (manage.py runserver output)
   │      ├─→ Django Debug Toolbar
   │      └─→ Add print() in consumers.py/models.py
   │
   └─→ Database Issue?
          ├─→ Django Admin (/admin/)
          ├─→ Django Shell (manage.py shell)
          └─→ Direct SQLite inspection
```

---

## 📚 Pentru Mai Multe Detalii

- **Code**: Citește comentariile inline în fiecare fișier
- **Features**: Vezi FEATURES.md
- **Testing**: Vezi TEST_CHECKLIST.md
- **Commands**: Vezi COMMANDS.md
- **Quick Start**: Vezi QUICKSTART.md

---

**Această arhitectură este scalabilă, maintainabilă și production-ready! 🚀**


