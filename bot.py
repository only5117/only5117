import discord
import os
import requests # Isse aap APIs se data fetch kar sakte hain
import json # Data ko parse karne ke liye

# Yahan aapko aapka bot token dalna hoga
# **WARNING:** Aapne jo token diya hai, woh publically visible hai.
# Usko immediately revoke (delete) karke naya token bana lijiye.
# Tokens ko code mein hardcode karna secure practice nahi hai.
# Isko environment variables mein store karna behtar hai.
DISCORD_BOT_TOKEN = 'YOUR_ACTUAL_BOT_TOKEN_HERE' # Yahan naya token daalen

# Ye wahi API key hai jo aapke HTML mein thi
GEMINI_API_KEY = "AIzaSyDlL_MnKrTsEjJ2ck48P4nUXdy6J9EToZw"

# Discord Bot ke liye intents define karte hain
intents = discord.Intents.default()
intents.message_content = True # Bot ko messages padhne ki permission deni padegi

# Client object banate hain
client = discord.Client(intents=intents)

# API se fact fetch karne ka function
def get_fact(topic=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

    if topic and topic.strip():
        prompt = f"Generate a short, interesting 'Did You Know?' fact about {topic}. Write it in Hinglish, no more than 2 sentences."
    else:
        prompt = "Science ya history ke baare mein ek chhota, interesting 'Did You Know?' fact banaayein. Ise Hinglish mein likhein, 2 sentences se zyada nahi."

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
        response.raise_for_status() # HTTP errors ke liye exception raise karta hai
        data = response.json()

        # API response ko parse karte hain
        fact_text = data.get('candidates')[0].get('content').get('parts')[0].get('text')
        return fact_text

    except requests.exceptions.RequestException as e:
        print(f"API se fact fetch karne mein error: {e}")
        return "Maaf kijiye, abhi fact nahi de paaya. Kripya baad mein try karein."
    except (KeyError, IndexError, TypeError) as e:
        print(f"API response ko parse karne mein error: {e}")
        return "API response ka format galat hai."


# Bot ke ready hone par
@client.event
async def on_ready():
    print(f'Hum log Discord mein log-in kar chuke hain, bhai. Bot ka naam hai: {client.user}')

# Jab koi message bheja jaye
@client.event
async def on_message(message):
    # Bot ke messages ko ignore karen
    if message.author == client.user:
        return

    # !fact command ko handle karen
    if message.content.startswith('!fact'):
        # Command ke baad ka topic nikaalte hain
        # Example: !fact Mars
        command_parts = message.content.split(' ', 1)
        topic = command_parts[1] if len(command_parts) > 1 else None

        fact = get_fact(topic)
        await message.channel.send(fact) # Fact ko channel mein send karte hain

# Bot ko run karte hain
client.run(DISCORD_BOT_TOKEN)
