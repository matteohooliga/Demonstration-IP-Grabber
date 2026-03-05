# 🎯 Démonstartion IP Grabber (Cybersécurité)

Ce projet est un outil éducatif en Python (Flask). Il permet d'illustrer comment un lien en apparence inoffensif peut intercepter des données de connexion (IP, Localisation, FAI, User-Agent) de manière invisible, les envoyer sur un serveur Discord, puis rediriger instantanément la cible vers un site web légitime.

> ⚠️ **Avertissement :** Ce script est fourni à des fins strictement éducatives (sensibilisation à l'OSINT et au Phishing). À n'utiliser qu'avec le consentement explicite des personnes testées.

---

## 🛠️ Prérequis et Installation

1. **Python 3.x** : [Télécharger Python](https://www.python.org/downloads/) (Cochez _"Add Python to PATH"_ lors de l'installation).
2. **Modules Python** : Ouvrez un terminal (`cmd`) dans le dossier du projet et tapez :
   ```cmd
   pip install flask requests
   ```

````

3. **Configuration du script** : Ouvrez `app.py` et modifiez :
* `WEBHOOK_URL` : Votre lien de Webhook Discord.
* `TARGET_URL` : Le site vers lequel rediriger la cible.



---

## 🚀 Étape 1 : Démarrer le serveur local

Avant d'exposer le lien sur Internet, il faut lancer l'application sur votre PC :

1. Double-cliquez sur le fichier `start.bat`.
2. Une console noire s'ouvre : le script écoute désormais sur le port `5000`. **Ne fermez pas cette fenêtre.**

---

## 🌍 Étape 2 : Exposer le serveur sur Internet (2 Méthodes)

Pour que votre lien fonctionne en dehors de votre réseau Wi-Fi, vous devez créer un tunnel. Choisissez l'une des deux méthodes ci-dessous.

### Méthode A : Avec Ngrok (Le plus rapide)

Idéal pour des tests rapides, mais la version gratuite affiche parfois une page d'avertissement avant la redirection.

1. Téléchargez et installez [Ngrok](https://ngrok.com/download).
2. Ouvrez une nouvelle invite de commande (`cmd`) et tapez la commande suivante :
```cmd
ngrok http 5000 --request-header-add ngrok-skip-browser-warning:true

````

3. Dans la console Ngrok, repérez la ligne `Forwarding` et copiez le lien en `https://...`. C'est votre lien de démonstration.

### Méthode B : Avec Cloudflare Tunnels (Le plus pro & invisible)

Idéal pour une redirection 100% transparente et pour utiliser votre propre nom de domaine. Ne nécessite pas d'ouvrir les ports de votre box Internet.

1. **Préparation :**

- Créez un compte gratuit sur [Cloudflare](https://dash.cloudflare.com/).
- Ajoutez votre nom de domaine et remplacez vos serveurs DNS chez votre hébergeur par ceux fournis par Cloudflare.

2. **Création du Tunnel :**

- Dans Cloudflare, allez dans **Zero Trust** (menu de gauche) > **Networks** > **Tunnels**.
- Cliquez sur **Create a tunnel**, choisissez **Cloudflared**, et nommez-le.
- Choisissez votre système d'exploitation (Windows) et copiez la commande fournie pour installer le connecteur dans un terminal lancé en administrateur.

3. **Configuration du routage :**

- Cliquez sur **Next**.
- Dans l'onglet _Public Hostname_, sélectionnez votre domaine.
- Dans _Service_, choisissez `HTTP` et entrez `localhost:5000`.
- Enregistrez. Dès que le tunnel est "Healthy" (En bonne santé), votre nom de domaine pointera de manière invisible vers votre script Python local !

> **💡 Astuce Cloudflare (Optionnel) :** Pour forcer la récupération d'adresses IPv4 au lieu d'IPv6, allez dans le tableau de bord Cloudflare classique de votre domaine > **Network** > Activez **Pseudo IPv4** sur _Overwrite Headers_.

---

## 📁 Structure des fichiers

- `app.py` : Le cœur de l'intercepteur.
- `start.bat` : L'exécutable pour démarrer l'application facilement.
- `logs.txt` : Fichier généré automatiquement pour l'historique local.
- `README.md` : Ce fichier de documentation.
