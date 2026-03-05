@echo off
title Serveur d'Interception
echo =========================================
echo Lancement du serveur Python Flask...
echo =========================================
echo.

:: Lancement du script
python app.py

:: Si le script s'arrête ou plante, cette commande garde la fenêtre ouverte
echo.
echo Le serveur s'est arrete.
pause