import hikari
import random
import os
import deepseek

# Hikari bot
bot = hikari.GatewayBot(token=os.getenv("DISCORD_TOKEN"))

# Configurar o cliente DeepSeek
client = deepseek.Client()

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
                answer = client.ask(question)
                await event.message.respond(f"🤖 {answer}")
            except Exception as e:
                print(f"Erro ao chamar o DeepSeek: {e}")
                await event.message.respond("Desculpe, ocorreu um erro ao processar sua solicitação.")

    # Verificar comandos de rolagem de dados
    content = event.message.content.lower()
    if content.startswith("!rolar"):
        try:
            dice_type = content.split(" ")[1]
            if dice_type.startswith("d") and dice_type[1:].isdigit():
                max_value = int(dice_type[1:])
                if max_value > 0:
                    roll_result = random.randint(1, max_value)
                    await event.message.respond(f"🎲 Você rolou um {dice_type}: {roll_result}")
                else:
                    await event.message.respond("O número de lados do dado deve ser maior que 0.")
            else:
                await event.message.respond("Formato inválido! Use o formato dX, onde X é o número de lados do dado.")
        except IndexError:
            await event.message.respond("Por favor, especifique um tipo de dado! Exemplo: !rolar d20")

# Run the bot
bot.run()
