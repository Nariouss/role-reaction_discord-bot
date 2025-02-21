import discord
from discord.ext import commands
from flask import Flask
import threading

# Variables de votre bot Discord
TOKEN = "MTM0MjMyNzY3Njk5NTg5OTQ4Mw.G7gTJC.asmdXKHVSYVrSRlLq7jCA0q_ZXVdVNJZiWBJNA"
MESSAGE_ID = 123456789012345678
MESSAGE_ID_FLAGS = 1342331752319811616
RULE_ROLES = {
    "✅": 123456789012345678,
}
FLAG_ROLES = {
    "🇫🇷": 1342299101911580692,
    "🇬🇧": 1342299222078128181,
    "🇪🇸": 1342299306723381268,
    "🇵🇹": 1342299840977309696,
    "🇷🇺": 1342299876419178496,
    "🇸🇦": 1342299906605449266,
}

# Initialisation des intents pour le bot Discord
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Création de l'application Flask pour le health check
app = Flask(__name__)

# Route pour le health check
@app.route("/")
def health_check():
    return "OK", 200

# Fonction pour démarrer le serveur Flask dans un thread séparé
def run_flask():
    app.run(host="0.0.0.0", port=8000)

# Événements pour le bot Discord
@bot.event
async def on_ready():
    print(f"Connected as {bot.user}")

@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    if not member:
        return
    if payload.message_id == MESSAGE_ID and payload.emoji.name in RULE_ROLES:
        role = guild.get_role(RULE_ROLES[payload.emoji.name])
        if role:
            await member.add_roles(role)
            print(f"Adding {role.name} to {member.name}")
    elif payload.message_id == MESSAGE_ID_FLAGS and payload.emoji.name in FLAG_ROLES:
        role = guild.get_role(FLAG_ROLES[payload.emoji.name])
        if role:
            await member.add_roles(role)
            print(f"Adding {role.name} to {member.name}")

@bot.event
async def on_raw_reaction_remove(payload):
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    if not member:
        return
    if payload.message_id == MESSAGE_ID and payload.emoji.name in RULE_ROLES:
        role = guild.get_role(RULE_ROLES[payload.emoji.name])
        if role:
            await member.remove_roles(role)
            print(f"Removing {role.name} from {member.name}")
    elif payload.message_id == MESSAGE_ID_FLAGS and payload.emoji.name in FLAG_ROLES:
        role = guild.get_role(FLAG_ROLES[payload.emoji.name])
        if role:
            await member.remove_roles(role)
            print(f"Removing {role.name} from {member.name}")

# Démarrer le serveur Flask dans un thread séparé
threading.Thread(target=run_flask).start()

# Lancer le bot Discord
bot.run(TOKEN)
