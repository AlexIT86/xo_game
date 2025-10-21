"""
Views pentru aplicația de joc X și 0.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import GameRoom


def index(request):
    """
    Pagina principală - meniu cu opțiuni pentru a crea sau intra în cameră.
    """
    return render(request, 'game/index.html')


def create_room(request):
    """
    Creează o cameră nouă și redirecționează către aceasta.
    """
    if request.method == 'POST':
        # Generează cod unic
        code = GameRoom.generate_code()
        
        # Creează camera
        room = GameRoom.objects.create(
            code=code,
            status='waiting'
        )
        
        # Redirecționează către camera de joc
        return redirect('game_room', room_code=code)
    
    return redirect('index')


def join_room(request):
    """
    Verifică dacă codul camerei există și redirecționează.
    """
    if request.method == 'POST':
        code = request.POST.get('room_code', '').strip().upper()
        
        if not code:
            return render(request, 'game/index.html', {
                'error': 'Te rog introdu un cod valid.'
            })
        
        # Verifică dacă camera există
        try:
            room = GameRoom.objects.get(code=code)
            
            # Verifică dacă camera are loc
            if room.player_x and room.player_o:
                return render(request, 'game/index.html', {
                    'error': f'Camera {code} este plină. Maxim 2 jucători.'
                })
            
            return redirect('game_room', room_code=code)
            
        except GameRoom.DoesNotExist:
            return render(request, 'game/index.html', {
                'error': f'Camera cu codul {code} nu există.'
            })
    
    return redirect('index')


def game_room(request, room_code):
    """
    Pagina principală de joc pentru o cameră specifică.
    """
    room = get_object_or_404(GameRoom, code=room_code)
    
    context = {
        'room': room,
        'room_code': room_code,
    }
    
    return render(request, 'game/game_room.html', context)


def room_status(request, room_code):
    """
    API endpoint pentru a verifica statusul camerei.
    Util pentru polling sau debugging.
    """
    room = get_object_or_404(GameRoom, code=room_code)
    
    return JsonResponse(room.get_state())
