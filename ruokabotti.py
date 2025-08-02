import discord
import requests
import os

# 🔑 Aseta omat tunnukset tähän
DISCORD_TOKEN = "MTQwMTAwNDI5MzQ4MTQzNTIzNw.GWJ-vl.FsOIUf1OTaPe6dbF0oIrngWu-3ED72Ijt-LVvI"
SPOON_KEY = "e2aeb117ea1642758219bdd5da0a230c"

intents = discord.Intents.default()
intents.message_content = True  # 🔑 sallii viestien lukemisen
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ {client.user} on kirjautunut sisään ja on valmis resepteihin!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Käyttö: !resepti tomaatti, juusto
    if message.content.startswith("!resepti"):
        try:
            # Poimitaan ainekset viestistä
            parts = message.content.split("!resepti ", 1)
            if len(parts) < 2 or parts[1].strip() == "":
                await message.channel.send("❗ Kirjoita komento näin: `!resepti tomaatti, juusto`")
                return
            
            ainekset = parts[1].strip()
            await message.channel.send(f"🔍 Haetaan reseptejä aineksilla: **{ainekset}**...")

            # Kutsu Spoonacular API:in
            url = f"https://api.spoonacular.com/recipes/findByIngredients"
            params = {
                "ingredients": ainekset,
                "number": 3,
                "ranking": 1,
                "apiKey": SPOON_KEY
            }
            response = requests.get(url, params=params)
            data = response.json()

            if not data:
                await message.channel.send("😔 En löytänyt reseptejä noilla aineksilla.")
                return

            # Rakennetaan vastaus
            vastaus = "🍽 **Reseptiehdotuksia:**\n"
            for resepti in data:
                nimi = resepti["title"]
                kuva = resepti["image"]
                slug = nimi.lower().replace(" ", "-") 
                linkki = f"https://spoonacular.com/recipes/{slug}-{resepti['id']}"
                vastaus += f"👉 **{nimi}** \n🔗 {linkki} \n🖼 {kuva}\n\n"

            await message.channel.send(vastaus)

        except Exception as e:
            await message.channel.send(f"⚠️ Tapahtui virhe: {e}")

client.run(DISCORD_TOKEN)





