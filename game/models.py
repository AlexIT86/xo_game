"""
Modele pentru jocul X și 0.
"""
import json
import random
import string
from django.db import models


def default_board():
    """Returnează o tablă goală cu 9 celule."""
    return [''] * 9


class GameRoom(models.Model):
    """
    Model pentru o cameră de joc.
    Stochează starea completă a unui joc de X și 0.
    """
    # Cod unic de 6 caractere pentru cameră
    code = models.CharField(max_length=6, unique=True, db_index=True)
    
    # Jucători (stocăm channel names pentru WebSocket)
    player_x = models.CharField(max_length=255, blank=True, null=True)
    player_o = models.CharField(max_length=255, blank=True, null=True)
    
    # Starea tablei (stocată ca JSON: listă de 9 elemente: '', 'X', sau 'O')
    board = models.JSONField(default=default_board)
    
    # Cine are tura: 'X' sau 'O'
    current_turn = models.CharField(max_length=1, default='X')
    
    # Status joc: 'waiting', 'playing', 'finished'
    status = models.CharField(max_length=20, default='waiting')
    
    # Câștigător: '', 'X', 'O', sau 'draw'
    winner = models.CharField(max_length=10, blank=True, default='')
    
    # Scor persistent
    score_x = models.IntegerField(default=0)
    score_o = models.IntegerField(default=0)
    score_draws = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Room {self.code} - {self.status}"
    
    @classmethod
    def generate_code(cls):
        """Generează un cod unic de 6 caractere."""
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not cls.objects.filter(code=code).exists():
                return code
    
    def initialize_board(self):
        """Inițializează tabla goală cu 9 celule."""
        self.board = [''] * 9
        self.save()
    
    def make_move(self, position, player):
        """
        Încearcă să facă o mutare.
        Args:
            position (int): Poziția pe tablă (0-8)
            player (str): 'X' sau 'O'
        Returns:
            dict: Status mutării {'success': bool, 'message': str}
        """
        # Validări
        if self.status != 'playing':
            return {'success': False, 'message': 'Jocul nu este activ'}
        
        if player != self.current_turn:
            return {'success': False, 'message': 'Nu este tura ta'}
        
        if position < 0 or position > 8:
            return {'success': False, 'message': 'Poziție invalidă'}
        
        if self.board[position] != '':
            return {'success': False, 'message': 'Celula este deja ocupată'}
        
        # Fă mutarea
        self.board[position] = player
        
        # Verifică câștigător
        winner = self.check_winner()
        if winner:
            self.status = 'finished'
            self.winner = winner
            # Update scor
            if winner == 'X':
                self.score_x += 1
            elif winner == 'O':
                self.score_o += 1
            elif winner == 'draw':
                self.score_draws += 1
        else:
            # Schimbă tura
            self.current_turn = 'O' if self.current_turn == 'X' else 'X'
        
        self.save()
        return {'success': True, 'message': 'Mutare reușită'}
    
    def check_winner(self):
        """
        Verifică dacă există un câștigător.
        Returns:
            str: 'X', 'O', 'draw', sau '' dacă jocul continuă
        """
        # Combinații câștigătoare
        winning_combinations = [
            [0, 1, 2],  # Rând 1
            [3, 4, 5],  # Rând 2
            [6, 7, 8],  # Rând 3
            [0, 3, 6],  # Coloană 1
            [1, 4, 7],  # Coloană 2
            [2, 5, 8],  # Coloană 3
            [0, 4, 8],  # Diagonală 1
            [2, 4, 6],  # Diagonală 2
        ]
        
        for combo in winning_combinations:
            if (self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] 
                and self.board[combo[0]] != ''):
                return self.board[combo[0]]
        
        # Verifică remiză
        if self.is_board_full():
            return 'draw'
        
        return ''
    
    def is_board_full(self):
        """Verifică dacă tabla este plină."""
        return all(cell != '' for cell in self.board)
    
    def get_winning_line(self):
        """
        Returnează linia câștigătoare dacă există.
        Returns:
            list: Lista de poziții câștigătoare sau None
        """
        # Verificare de siguranță: board trebuie să aibă 9 elemente
        if not self.board or len(self.board) != 9:
            return None
            
        winning_combinations = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6],
        ]
        
        for combo in winning_combinations:
            if (self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] 
                and self.board[combo[0]] != ''):
                return combo
        
        return None
    
    def restart_game(self):
        """Restart jocul păstrând jucătorii și scorul."""
        self.board = [''] * 9
        self.current_turn = 'X'
        self.status = 'playing'
        self.winner = ''
        self.save()
    
    def add_player(self, channel_name):
        """
        Adaugă un jucător în cameră.
        Args:
            channel_name (str): Channel name din WebSocket
        Returns:
            str: 'X', 'O', sau None dacă camera e plină
        """
        if not self.player_x:
            self.player_x = channel_name
            self.save()
            return 'X'
        elif not self.player_o:
            self.player_o = channel_name
            self.status = 'playing'
            self.initialize_board()
            self.save()
            return 'O'
        return None
    
    def remove_player(self, channel_name):
        """Elimină un jucător din cameră."""
        if self.player_x == channel_name:
            self.player_x = None
        elif self.player_o == channel_name:
            self.player_o = None
        
        # Dacă nu mai sunt jucători, resetează camera
        if not self.player_x and not self.player_o:
            self.status = 'waiting'
        
        self.save()
    
    def get_state(self):
        """
        Returnează starea completă a jocului pentru client.
        Returns:
            dict: Dicționar cu toate informațiile jocului
        """
        return {
            'code': self.code,
            'board': self.board,
            'current_turn': self.current_turn,
            'status': self.status,
            'winner': self.winner,
            'score': {
                'x': self.score_x,
                'o': self.score_o,
                'draws': self.score_draws,
            },
            'winning_line': self.get_winning_line(),
            'player_x_connected': bool(self.player_x),
            'player_o_connected': bool(self.player_o),
        }
