import discord
import os
import google.generativeai as genai

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

system_instruction = """
You are 'Boss AI' - the ultimate, 100% reliable personal Chief of Staff and Master Agent for your boss, Sadak Hossain.
Your mission is to execute tasks with absolute precision and zero errors.
Crucial Rule: Before executing any complex task, planning, or coding, ALWAYS ask: "Boss, ami ki thik ei jinista korbo?" and wait for approval.
Adapt your expertise based on the Discord channel name (e.g., act as a Video/Content Expert in #youtube, a Tech/Dev Expert in #coding, a Marketing/Business Expert in #lead-research).
Always reply in friendly Bengali (Bangla font).
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} - Boss AI is ready for Einstein Server!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    channel_name = message.channel.name
    user_input = message.content

    prompt = f"[Channel context: #{channel_name}]\nBoss's command: {user_input}"
    
    try:
        async with message.channel.typing():
            response = model.generate_content(prompt)
            
        text = response.text
        if len(text) > 2000:
            for chunk in [text[i:i+2000] for i in range(0, len(text), 2000)]:
                await message.channel.send(chunk)
        else:
            await message.channel.send(text)
            
    except Exception as e:
        await message.channel.send(f"Sorry Boss, ekta technical error hoyeche: {str(e)}")

client.run(DISCORD_TOKEN)
