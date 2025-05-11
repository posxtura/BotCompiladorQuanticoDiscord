import hikari
import openai
import random
import os

# Hikari bot
bot = hikari.GatewayBot(token=os.getenv("DISCORD_TOKEN"))

# OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

@bot.listen()
async def on_message(event: hikari.GuildMessageCreateEvent):
    print(f"Mensagem recebida: {event.message.content}")  # Log para depuração

    if event.is_bot:
        return

    # Verificar se o bot foi mencionado
    if bot.get_me().id in event.message.user_mentions_ids:
        question = event.message.content.replace(f"<@{bot.get_me().id}>", "").strip()
        if question:
            try:
                response = await openai.ChatCompletion.acreate(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": question}]
                )
                answer = response.choices[0].message.content
                await event.message.respond(f"{answer}")
            except Exception as e:
                print(f"Erro ao chamar a API do OpenAI: {e}")
                await event.message.respond("Desculpe, ocorreu um erro ao processar sua solicitação.")

    # Verificar comandos de rolagem de dados
    content = event.message.content.lower()
    if content.startswith("!rolar"):
        try:
            dice_type = content.split(" ")[1]
            if dice_type in ["d100", "d20", "d10", "d8", "d6", "d4"]:
                max_value = int(dice_type[1:])
                roll_result = random.randint(1, max_value)
                await event.message.respond(f"🎲 Você rolou um {dice_type}: {roll_result}")
            else:
                await event.message.respond("Po cara, tu rolou um dado inválido! Use um dos seguintes: d100, d20, d10, d8, d6, d4.")
        except IndexError:
            await event.message.respond("Po mano, especifica o tipo do dado! Exemplo: !roll d20")

# Run Bot
bot.run()
