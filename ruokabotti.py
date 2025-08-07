import discord
import requests
import re  # HTML-tägien poistoon
import os

# 🔑 Aseta omat tunnukset tähän
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
SPOON_KEY = os.environ['SPOON_KEY']

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ {client.user} on kirjautunut sisään ja on valmis resepteihin!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!resepti"):
        try:
            parts = message.content.split("!resepti ", 1)
            if len(parts) < 2 or parts[1].strip() == "":
                await message.channel.send("❗ Kirjoita komento näin: `!resepti tomaatti, juusto`")
                return

            ainekset = parts[1].strip()
            await message.channel.send(f"🔍 Haetaan reseptejä aineksilla: **{ainekset}**...")

            # Haetaan reseptit aineksilla
            url = "https://api.spoonacular.com/recipes/findByIngredients"
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

            for resepti in data:
                nimi = resepti["title"]
                kuva = resepti["image"]
                resepti_id = resepti["id"]

                # Haetaan ohjeet erikseen
                info_url = f"https://api.spoonacular.com/recipes/{resepti_id}/information"
                info_params = {"apiKey": SPOON_KEY}
                info_response = requests.get(info_url, params=info_params)
                info_data = info_response.json()

                ohjeet_raw = info_data.get("instructions", "")
                ohjeet = re.sub("<.*?>", "", ohjeet_raw)

                if len(ohjeet) > 2000:
                    ohjeet = ohjeet[:2000] + "... (lyhennetty)"

                if not ohjeet.strip():
                    ohjeet = "😔 Valmistusohjeita ei löytynyt."

                linkki = f"https://spoonacular.com/recipes/{nimi.lower().replace(' ', '-')}-{resepti_id}"

                vastaus = (
                    f"🍽 **{nimi}**\n"
                    f"🔗 {linkki}\n"
                    f"🖼 {kuva}\n"
                    f"📜 **Ohjeet:** {ohjeet}"
                )
                await message.channel.send(vastaus)

        except Exception as e:
            await message.channel.send(f"⚠️ Tapahtui virhe: {e}")

client.run(DISCORD_TOKEN)


