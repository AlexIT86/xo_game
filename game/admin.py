"""
Admin configuration pentru modelele de joc.
"""
from django.contrib import admin
from .models import GameRoom


@admin.register(GameRoom)
class GameRoomAdmin(admin.ModelAdmin):
    """Admin interface pentru GameRoom."""
    list_display = ['code', 'status', 'current_turn', 'winner', 
                    'score_x', 'score_o', 'score_draws', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['code']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informații Cameră', {
            'fields': ('code', 'status')
        }),
        ('Jucători', {
            'fields': ('player_x', 'player_o')
        }),
        ('Stare Joc', {
            'fields': ('board', 'current_turn', 'winner')
        }),
        ('Scor', {
            'fields': ('score_x', 'score_o', 'score_draws')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
