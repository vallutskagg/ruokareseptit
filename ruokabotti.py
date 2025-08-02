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

    # Käyttö: !resepti pancake
    if message.content.startswith("!resepti"):
        try:
            # 🔍 Poimitaan hakusana viestistä
            parts = message.content.split("!resepti ", 1)
            if len(parts) < 2 or parts[1].strip() == "":
                await message.channel.send("❗ Kirjoita komento näin: `!resepti pancake`")
                return
            
            hakusana = parts[1].strip()
            await message.channel.send(f"🔍 Haetaan reseptejä haulla: **{hakusana}**...")

            # 📡 1️⃣ Haetaan reseptilista Spoonacularista
            url = f"https://api.spoonacular.com/recipes/complexSearch"
            params = {
                "query": hakusana,
                "number": 2,  # ⬅ montako reseptiä näytetään
                "apiKey": SPOON_KEY
            }
            response = requests.get(url, params=params)
            data = response.json()

            if not data.get("results"):
                await message.channel.send("😔 En löytänyt reseptejä tuolla haulla, yritä uudestaan!")
                return

            # 📄 Rakennetaan vastausviesti
            for resepti in data["results"]:
                nimi = resepti["title"]
                kuva = resepti["image"]
                resepti_id = resepti["id"]

                # ✅ Luodaan linkki reseptiin
                slug = nimi.lower().replace(" ", "-")
                linkki = f"https://spoonacular.com/recipes/{slug}-{resepti_id}"

                # 📡 2️⃣ Haetaan reseptin tarkemmat tiedot (ohjeet)
                info_url = f"https://api.spoonacular.com/recipes/{resepti_id}/information"
                info_params = {"apiKey": SPOON_KEY}
                info_data = requests.get(info_url, params=info_params).json()

                ohjeet = info_data.get("instructions", None)
                if not ohjeet:
                    ohjeet = "😔 Valmistusohjeita ei löytynyt."

                # 📝 Lähetetään resepti Discordiin
                vastaus = f"🍽 **{nimi}**\n🔗 {linkki}\n🖼 {kuva}\n📜 **Ohjeet:** {ohjeet}"
                await message.channel.send(vastaus)

        except Exception as e:
            await message.channel.send(f"⚠️ Tapahtui virhe: {e}")

client.run(DISCORD_TOKEN)
