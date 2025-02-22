import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"
def run():
    app.run(host='0.0.0.0', port=25565)
def start_flask():
    t = Thread(target=run)
    t.start()
if __name__ == "__main__":
    start_flask()

TOKEN = "MTM0MjMyNzY3Njk5NTg5OTQ4Mw.G7gTJC.asmdXKHVSYVrSRlLq7jCA0q_ZXVdVNJZiWBJNA"
MESSAGE_ID_RULES = 1342344847583084565
MESSAGE_ID_COLOR = 1342369910961078402
MESSAGE_ID_FLAGS = 1342372377719210024
RULE_ROLES = {
    "✅": 1342291211729375292,
}
FLAG_ROLES = {
    "🇫🇷": 1342299101911580692,
    "🇬🇧": 1342299222078128181,
    "🇪🇸": 1342299306723381268,
    "🇵🇹": 1342299840977309696,
    "🇷🇺": 1342299876419178496,
    "🇸🇦": 1342299906605449266,
}
AUTHORIZED_USER_ID = [1192627953989857421]

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix="sudo ", intents=intents)

@bot.event
async def on_ready():
    print(f"Connected as{bot.user}")
    
@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    if not member:
        return
    if payload.message_id == MESSAGE_ID_RULES and payload.emoji.name in RULE_ROLES:
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
    if payload.message_id == MESSAGE_ID_RULES and payload.emoji.name in RULE_ROLES:
        role = guild.get_role(RULE_ROLES[payload.emoji.name])
        if role:
            await member.remove_roles(role)
            print(f"Removing {role.name} from {member.name}")
    elif payload.message_id == MESSAGE_ID_FLAGS and payload.emoji.name in FLAG_ROLES:
        role = guild.get_role(FLAG_ROLES[payload.emoji.name])
        if role:
            await member.remove_roles(role)
            print(f"Removing {role.name} from {member.name}")

@bot.command()
async def react(ctx, message_id: int, emoji: str):
if ctx.author.id not in AUTHORIZED_USER_ID:
        await ctx.send(f"```ini\n[ Reaction Add ]\n\nYou are not allowed to use this command```")
        return
    try:
        message = await ctx.channel.fetch_message(message_id)
        await message.add_reaction(emoji)
        await ctx.send(f"```ini\n[ Reaction Add ]\n\nReaction {emoji} added to message {message_id} successfuly```")
    except discord.NotFound:
        await ctx.send(f"```ini\n[ Reaction Add ]\n\nUnfound Message```")
    except discord.HTTPException as e:
        await ctx.send(f"```ini\n[ Reaction Add ]\n\nError {e}```")

@bot.command()
async def sendmsg(ctx, *, message: str):
if ctx.author.id not in AUTHORIZED_USER_ID:
        await ctx.send("```ini\n[ Send Message ]\n\nYou are not allowed to use this command```")
        return
    await ctx.send(message)

@bot.command()
async def replymsg(ctx, *, message: str):
if ctx.author.id not in AUTHORIZED_USER_ID:
        await ctx.send("```ini\n[ Reply Message ]\n\nYou are not allowed to use this command```")
        return
    await ctx.reply(message)

bot.run(TOKEN)
