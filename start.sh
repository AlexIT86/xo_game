#!/bin/bash

echo "========================================"
echo "  Joc X si 0 - Start Rapid"
echo "========================================"
echo ""

# Verifică dacă există mediu virtual
if [ ! -d "venv" ]; then
    echo "[1/6] Creez mediul virtual..."
    python3 -m venv venv
else
    echo "[1/6] Mediul virtual există deja"
fi

echo "[2/6] Activez mediul virtual..."
source venv/bin/activate

echo "[3/6] Instalez dependențele..."
pip install -r requirements.txt

echo "[4/6] Creez migrările bazei de date..."
python manage.py makemigrations

echo "[5/6] Aplic migrările..."
python manage.py migrate

echo "[6/6] Pornesc serverul..."
echo ""
echo "========================================"
echo "  Server pornit!"
echo "  Deschide browser la: http://localhost:8000"
echo "  Apasă CTRL+C pentru a opri serverul"
echo "========================================"
echo ""
python manage.py runserver

