"""
WebSocket Consumer pentru jocul X și 0.
Gestionează comunicarea în timp real între jucători.
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import GameRoom


class GameConsumer(AsyncWebsocketConsumer):
    """
    Consumer pentru gestionarea conexiunilor WebSocket ale jocului.
    """
    
    async def connect(self):
        """Gestionează conectarea unui jucător."""
        # Extrage codul camerei din URL
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = f'game_{self.room_code}'
        self.player_symbol = None
        
        # Verifică dacă camera există
        room_exists = await self.check_room_exists()
        if not room_exists:
            await self.close()
            return
        
        # Adaugă jucătorul la cameră
        self.player_symbol = await self.add_player_to_room()
        if not self.player_symbol:
            # Camera e plină
            await self.accept()
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Camera este plină. Maxim 2 jucători.',
            }))
            await self.close()
            return
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Trimite informații jucătorului
        await self.send(text_data=json.dumps({
            'type': 'player_assigned',
            'player': self.player_symbol,
        }))
        
        # Trimite starea jocului tuturor
        await self.broadcast_game_state()
    
    async def disconnect(self, close_code):
        """Gestionează deconectarea unui jucător."""
        # Elimină jucătorul din cameră
        if hasattr(self, 'room_code') and self.player_symbol:
            await self.remove_player_from_room()
            
            # Notifică ceilalți jucători
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'player_disconnected',
                    'player': self.player_symbol,
                }
            )
        
        # Leave room group
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
    
    async def receive(self, text_data):
        """Primește mesaje de la client."""
        try:
            data = json.loads(text_data)
            action = data.get('action')
            
            if action == 'move':
                # Jucătorul face o mutare
                position = data.get('position')
                result = await self.process_move(position)
                
                if result['success']:
                    # Broadcast starea actualizată
                    await self.broadcast_game_state()
                else:
                    # Trimite eroare înapoi jucătorului
                    await self.send(text_data=json.dumps({
                        'type': 'error',
                        'message': result['message'],
                    }))
            
            elif action == 'restart':
                # Restart jocul
                await self.restart_game()
                await self.broadcast_game_state()
            
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON',
            }))
    
    async def game_update(self, event):
        """Trimite actualizări de joc către client."""
        await self.send(text_data=json.dumps({
            'type': 'game_update',
            'game_state': event['game_state'],
        }))
    
    async def player_disconnected(self, event):
        """Notifică când un jucător se deconectează."""
        await self.send(text_data=json.dumps({
            'type': 'player_disconnected',
            'player': event['player'],
        }))
    
    # Database sync methods
    
    @database_sync_to_async
    def check_room_exists(self):
        """Verifică dacă camera există."""
        return GameRoom.objects.filter(code=self.room_code).exists()
    
    @database_sync_to_async
    def add_player_to_room(self):
        """Adaugă jucătorul curent în cameră."""
        try:
            room = GameRoom.objects.get(code=self.room_code)
            return room.add_player(self.channel_name)
        except GameRoom.DoesNotExist:
            return None
    
    @database_sync_to_async
    def remove_player_from_room(self):
        """Elimină jucătorul din cameră."""
        try:
            room = GameRoom.objects.get(code=self.room_code)
            room.remove_player(self.channel_name)
        except GameRoom.DoesNotExist:
            pass
    
    @database_sync_to_async
    def process_move(self, position):
        """Procesează o mutare."""
        try:
            room = GameRoom.objects.get(code=self.room_code)
            return room.make_move(position, self.player_symbol)
        except GameRoom.DoesNotExist:
            return {'success': False, 'message': 'Camera nu există'}
    
    @database_sync_to_async
    def get_game_state(self):
        """Obține starea curentă a jocului."""
        try:
            room = GameRoom.objects.get(code=self.room_code)
            return room.get_state()
        except GameRoom.DoesNotExist:
            return None
    
    @database_sync_to_async
    def restart_game(self):
        """Restart jocul."""
        try:
            room = GameRoom.objects.get(code=self.room_code)
            room.restart_game()
        except GameRoom.DoesNotExist:
            pass
    
    async def broadcast_game_state(self):
        """Trimite starea jocului tuturor jucătorilor din cameră."""
        game_state = await self.get_game_state()
        if game_state:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game_update',
                    'game_state': game_state,
                }
            )
