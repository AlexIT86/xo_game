// ========================================
// Variabile Globale
// ========================================
let socket = null;
let myPlayer = null;
let gameState = null;
let isMyTurn = false;

// ========================================
// Inițializare WebSocket
// ========================================
function initWebSocket() {
    // Construiește URL-ul WebSocket
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/game/${roomCode}/`;
    
    // Creează conexiunea WebSocket
    socket = new WebSocket(wsUrl);
    
    // Event: Conexiune deschisă
    socket.onopen = function(e) {
        console.log('WebSocket conectat');
        showToast('Conectat la cameră!', 'success');
    };
    
    // Event: Mesaj primit
    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        console.log('Mesaj primit:', data);
        
        handleWebSocketMessage(data);
    };
    
    // Event: Conexiune închisă
    socket.onclose = function(e) {
        console.log('WebSocket deconectat');
        showToast('Deconectat de la server', 'error');
        updateGameStatus('Deconectat', 'error');
    };
    
    // Event: Eroare
    socket.onerror = function(e) {
        console.error('WebSocket error:', e);
        showToast('Eroare de conexiune', 'error');
    };
}

// ========================================
// Gestionare Mesaje WebSocket
// ========================================
function handleWebSocketMessage(data) {
    const messageType = data.type;
    
    switch(messageType) {
        case 'player_assigned':
            // Am primit simbolul nostru (X sau O)
            myPlayer = data.player;
            showPlayerBadge(myPlayer);
            showToast(`Ești jucătorul ${myPlayer}!`, 'success');
            break;
            
        case 'game_update':
            // Update complet al stării jocului
            gameState = data.game_state;
            updateGameUI(gameState);
            break;
            
        case 'player_disconnected':
            // Un jucător s-a deconectat
            showToast(`Jucătorul ${data.player} s-a deconectat`, 'warning');
            break;
            
        case 'error':
            // Eroare de la server
            showToast(data.message, 'error');
            break;
            
        default:
            console.log('Tip mesaj necunoscut:', messageType);
    }
}

// ========================================
// Update UI Joc
// ========================================
function updateGameUI(state) {
    console.log('Update UI cu starea:', state);
    
    // Update tabla
    updateBoard(state.board);
    
    // Update scor
    updateScore(state.score);
    
    // Update status
    updateGameStatus(state);
    
    // Update butoane
    updateButtons(state);
    
    // Verifică dacă jocul s-a terminat
    if (state.status === 'finished') {
        handleGameFinished(state);
    }
}

// ========================================
// Update Tabla de Joc
// ========================================
function updateBoard(board) {
    const cells = document.querySelectorAll('.board-cell');
    
    cells.forEach((cell, index) => {
        const value = board[index];
        
        // Curăță celula
        cell.innerHTML = '';
        cell.classList.remove('filled', 'active', 'disabled');
        
        if (value) {
            // Celula are un simbol
            const symbolDiv = document.createElement('div');
            symbolDiv.className = `symbol ${value.toLowerCase()}`;
            symbolDiv.textContent = value;
            cell.appendChild(symbolDiv);
            cell.classList.add('filled');
        } else {
            // Celula este goală
            if (isMyTurn && gameState.status === 'playing') {
                cell.classList.add('active');
            } else {
                cell.classList.add('disabled');
            }
        }
    });
}

// ========================================
// Update Scor
// ========================================
function updateScore(score) {
    document.getElementById('scoreX').textContent = score.x;
    document.getElementById('scoreO').textContent = score.o;
    document.getElementById('scoreDraws').textContent = score.draws;
}

// ========================================
// Update Status Joc
// ========================================
function updateGameStatus(state) {
    const statusEl = document.getElementById('gameStatus');
    const statusIcon = statusEl.querySelector('.status-icon');
    const statusText = statusEl.querySelector('.status-text');
    
    // Șterge spinner-ul dacă există
    statusIcon.innerHTML = '';
    
    if (typeof state === 'string') {
        // Mesaj simplu de status
        statusText.textContent = state;
        return;
    }
    
    // Determină statusul bazat pe starea jocului
    if (state.status === 'waiting') {
        statusIcon.innerHTML = '<div class="spinner"></div>';
        statusText.textContent = 'Așteaptă al doilea jucător...';
        isMyTurn = false;
    } else if (state.status === 'playing') {
        isMyTurn = (state.current_turn === myPlayer);
        
        if (isMyTurn) {
            statusIcon.textContent = '🎮';
            statusText.textContent = 'Este tura ta!';
            statusText.style.color = 'var(--success-color)';
        } else {
            statusIcon.textContent = '⏳';
            statusText.textContent = 'Așteaptă adversarul...';
            statusText.style.color = 'var(--text-secondary)';
        }
    } else if (state.status === 'finished') {
        if (state.winner === 'draw') {
            statusIcon.textContent = '🤝';
            statusText.textContent = 'Remiză!';
            statusText.style.color = 'var(--warning-color)';
        } else if (state.winner === myPlayer) {
            statusIcon.textContent = '🎉';
            statusText.textContent = 'Ai câștigat!';
            statusText.style.color = 'var(--success-color)';
        } else {
            statusIcon.textContent = '😔';
            statusText.textContent = 'Ai pierdut!';
            statusText.style.color = 'var(--error-color)';
        }
    }
}

// ========================================
// Update Butoane
// ========================================
function updateButtons(state) {
    const restartBtn = document.getElementById('restartBtn');
    
    if (state.status === 'finished') {
        restartBtn.style.display = 'flex';
    } else {
        restartBtn.style.display = 'none';
    }
}

// ========================================
// Afișare Badge Jucător
// ========================================
function showPlayerBadge(player) {
    const badge = document.getElementById('playerBadge');
    const symbolEl = document.getElementById('playerSymbol');
    
    symbolEl.textContent = player;
    symbolEl.className = `badge-symbol ${player.toLowerCase()}-symbol`;
    badge.style.display = 'flex';
}

// ========================================
// Gestionare Click pe Celulă
// ========================================
function setupBoardClickHandlers() {
    const cells = document.querySelectorAll('.board-cell');
    
    cells.forEach((cell, index) => {
        cell.addEventListener('click', () => {
            handleCellClick(index);
        });
    });
}

function handleCellClick(position) {
    // Verificări
    if (!isMyTurn) {
        showToast('Nu este tura ta!', 'warning');
        return;
    }
    
    if (gameState.status !== 'playing') {
        showToast('Jocul nu este activ', 'warning');
        return;
    }
    
    if (gameState.board[position] !== '') {
        showToast('Celula este deja ocupată!', 'error');
        shakeBoardCell(position);
        return;
    }
    
    // Trimite mutarea la server
    sendMove(position);
}

// ========================================
// Trimite Mutare la Server
// ========================================
function sendMove(position) {
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
            action: 'move',
            position: position
        }));
    }
}

// ========================================
// Restart Joc
// ========================================
function restartGame() {
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
            action: 'restart'
        }));
        
        showToast('Joc nou început!', 'info');
        
        // Șterge linia câștigătoare cu resetare completă
        const winningLine = document.getElementById('winningLine');
        const line = winningLine.querySelector('line');
        
        // Resetează animația (reaplic stroke-dashoffset)
        line.style.animation = 'none';
        line.style.strokeDashoffset = '1000';
        winningLine.style.display = 'none';
        
        // Oprește confetti dacă e activ
        stopConfetti();
    }
}

// ========================================
// Gestionare Joc Terminat
// ========================================
function handleGameFinished(state) {
    // Afișează linia câștigătoare dacă există
    if (state.winning_line) {
        drawWinningLine(state.winning_line);
    }
    
    // Animație de victorie
    if (state.winner === myPlayer) {
        // Câștigător - confetti!
        triggerConfetti();
    } else if (state.winner === 'draw') {
        // Remiză - animație subtilă
        showToast('Joc terminat: Remiză!', 'info');
    } else {
        // Pierdere
        showToast('Joc terminat: Ai pierdut!', 'error');
    }
}

// ========================================
// Desenare Linie Câștigătoare
// ========================================
function drawWinningLine(positions) {
    const winningLine = document.getElementById('winningLine');
    const line = winningLine.querySelector('line');
    const board = document.getElementById('gameBoard');
    const cells = document.querySelectorAll('.board-cell');
    
    // Obține coordonatele celulelor
    const startCell = cells[positions[0]];
    const endCell = cells[positions[2]];
    
    const startRect = startCell.getBoundingClientRect();
    const endRect = endCell.getBoundingClientRect();
    const boardRect = board.getBoundingClientRect();
    
    // Calculează coordonatele relative
    const x1 = startRect.left - boardRect.left + startRect.width / 2;
    const y1 = startRect.top - boardRect.top + startRect.height / 2;
    const x2 = endRect.left - boardRect.left + endRect.width / 2;
    const y2 = endRect.top - boardRect.top + endRect.height / 2;
    
    // Setează coordonatele liniei
    line.setAttribute('x1', x1);
    line.setAttribute('y1', y1);
    line.setAttribute('x2', x2);
    line.setAttribute('y2', y2);
    
    // Afișează linia
    winningLine.style.display = 'block';
}

// ========================================
// Animație Shake pentru Celulă
// ========================================
function shakeBoardCell(index) {
    const cell = document.querySelectorAll('.board-cell')[index];
    cell.classList.add('shake');
    setTimeout(() => {
        cell.classList.remove('shake');
    }, 600);
}

// ========================================
// Toast Notifications
// ========================================
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icon = getToastIcon(type);
    toast.innerHTML = `
        <span style="font-size: 1.5rem;">${icon}</span>
        <span>${message}</span>
    `;
    
    container.appendChild(toast);
    
    // Auto-remove după 3 secunde
    setTimeout(() => {
        toast.style.animation = 'toastSlideIn 0.3s ease reverse';
        setTimeout(() => {
            container.removeChild(toast);
        }, 300);
    }, 3000);
}

function getToastIcon(type) {
    const icons = {
        success: '✅',
        error: '❌',
        warning: '⚠️',
        info: 'ℹ️'
    };
    return icons[type] || icons.info;
}

// ========================================
// Confetti Animation
// ========================================
function triggerConfetti() {
    const canvas = document.getElementById('confetti-canvas');
    const ctx = canvas.getContext('2d');
    
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    canvas.style.display = 'block';
    
    const particles = [];
    const particleCount = 150;
    const colors = ['#6366f1', '#8b5cf6', '#ec4899', '#10b981', '#f59e0b'];
    
    // Creează particule
    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height - canvas.height,
            r: Math.random() * 6 + 2,
            d: Math.random() * particleCount,
            color: colors[Math.floor(Math.random() * colors.length)],
            tilt: Math.floor(Math.random() * 10) - 10,
            tiltAngleIncremental: Math.random() * 0.07 + 0.05,
            tiltAngle: 0
        });
    }
    
    let animationFrame;
    
    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        particles.forEach((p, i) => {
            ctx.beginPath();
            ctx.lineWidth = p.r / 2;
            ctx.strokeStyle = p.color;
            ctx.moveTo(p.x + p.tilt + p.r / 4, p.y);
            ctx.lineTo(p.x + p.tilt, p.y + p.tilt + p.r / 4);
            ctx.stroke();
            
            // Update
            p.tiltAngle += p.tiltAngleIncremental;
            p.y += (Math.cos(p.d) + 3 + p.r / 2) / 2;
            p.x += Math.sin(p.d);
            p.tilt = Math.sin(p.tiltAngle - i / 3) * 15;
            
            // Reset când iese din ecran
            if (p.y > canvas.height) {
                particles[i] = {
                    x: Math.random() * canvas.width,
                    y: -20,
                    r: p.r,
                    d: p.d,
                    color: p.color,
                    tilt: p.tilt,
                    tiltAngle: p.tiltAngle,
                    tiltAngleIncremental: p.tiltAngleIncremental
                };
            }
        });
        
        animationFrame = requestAnimationFrame(draw);
    }
    
    draw();
    
    // Oprește după 5 secunde
    setTimeout(() => {
        cancelAnimationFrame(animationFrame);
        canvas.style.display = 'none';
    }, 5000);
}

function stopConfetti() {
    const canvas = document.getElementById('confetti-canvas');
    canvas.style.display = 'none';
}

// ========================================
// Copiere Cod Cameră
// ========================================
function copyRoomCode() {
    const code = document.getElementById('roomCode').textContent;
    
    // Încearcă să copieze în clipboard
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(code).then(() => {
            showToast('Cod copiat în clipboard!', 'success');
        }).catch(err => {
            console.error('Eroare la copiere:', err);
            showToast('Nu s-a putut copia codul', 'error');
        });
    } else {
        // Fallback pentru browsere mai vechi
        const textArea = document.createElement('textarea');
        textArea.value = code;
        textArea.style.position = 'fixed';
        textArea.style.opacity = '0';
        document.body.appendChild(textArea);
        textArea.select();
        
        try {
            document.execCommand('copy');
            showToast('Cod copiat în clipboard!', 'success');
        } catch (err) {
            console.error('Eroare la copiere:', err);
            showToast('Nu s-a putut copia codul', 'error');
        }
        
        document.body.removeChild(textArea);
    }
}

// ========================================
// Inițializare la Încărcare
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    console.log('Pagină încărcată, inițializez WebSocket...');
    
    // Inițializează WebSocket
    initWebSocket();
    
    // Setup event handlers pentru board
    setupBoardClickHandlers();
    
    // Handle window resize pentru winning line
    window.addEventListener('resize', function() {
        if (gameState && gameState.winning_line) {
            drawWinningLine(gameState.winning_line);
        }
    });
});

// ========================================
// Cleanup la Închidere
// ========================================
window.addEventListener('beforeunload', function() {
    if (socket) {
        socket.close();
    }
});
