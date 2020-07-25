# bot.py
import asyncio
import os  # for importing env vars for the bot to use
import random
from twitchio.ext import commands
from twitchio.abcs import Messageable

nick_bot = ''
inicia_canal = ''


bot = commands.Bot(
    # set up the bot
    irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL']]
)


# parou


@bot.event
async def event_ready():
    'Chama quando o bot está online.'
    print(f"@{nick_bot} está online!")
    ws = bot._ws  # só é chamado no evento inicial

    await ws.send_privmsg(inicia_canal, 'o bot está online')

    msg_aleatoria = list(open('files/texto_engajamento.txt', encoding='utf-8'))

    if len(msg_aleatoria) > 0:
        while True:
            msg_selecionada = random.choice(msg_aleatoria)

            await ws.send_privmsg(inicia_canal, msg_selecionada)
            await asyncio.sleep(180.0)


@bot.command(name='points')
async def fn_points(ctx):
    return


@bot.command(name='addengajar')
async def fn_add_mensagem_engajamento(ctx):
    if len(ctx.content) > 30:
        # gravar a mensagem de ban comprada pelo usuário
        arquivo_texto_engajamento = open(
            'files/texto_engajamento.txt', 'a+', encoding='utf-8')

        arquivo_texto_engajamento.write(f"{ctx.content.lower()[12:]} \n")
        # TODO: CRIAR MÉTODO PARA ADICIONAR EM VOTAÇÃO NO CHAT
        arquivo_texto_engajamento.close()

        print(f"texto de engajamento adicionado por @{ctx.author.name}")
        await ctx.send('Mensagem de engajamento adicionada. aguardando aprovação.')


@bot.command(name='ban')
async def fn_ban(ctx):
    if len(ctx.content.split(' ')[1]) < 4:
        await ctx.send("para banir alguém, é preciso incluir o nome o usuário")

    if len(ctx.content.split(' ')[1]) > 3:
        lista_ban = open('files/texto_bans.txt', encoding='utf-8')

        banido = ctx.content.lower().split(' ')[1]
        tipo_ban = random.choice(list(lista_ban))

        print(
            f"comando de banir executado por @{ctx.author.name} para o @{banido}")

        await ctx.send(f"{banido} {tipo_ban}")
        # await Messageable.timeout(banido, 15, tipo_ban)
        # await ctx.send(f"/timeout {banido} 20")
        # await ctx.send(f".timeout {banido} 20")


@bot.command(name='addban')
async def fn_addban(ctx):
    if len(ctx.content) > 30:
        # gravar a mensagem de ban comprada pelo usuário

        arquivo_texto_bans = open(
            'files/texto_moderacao_bans.txt', 'a+', encoding='utf-8')

        arquivo_texto_bans.write(f"{ctx.content.lower()[8:]} \n")
        # TODO: CRIAR MÉTODO PARA ADICIONAR EM VOTAÇÃO NO CHAT
        arquivo_texto_bans.close()

        print(f"texto de ban adicionado por @{ctx.author.name}")
        await ctx.send('Mensagem de ban adicionada. aguardando aprovação.')


@bot.event
async def event_message(ctx):
    'Roda toda vez que uma mensagem no chat é enviada.'

    # make sure the bot ignores itself and the streamer
    if ctx.author.name.lower() == nick_bot.lower():
        return

    await bot.handle_commands(ctx)

    # await ctx.channel.send(ctx.content)

    if 'bom dia' in ctx.content.lower():
        await ctx.channel.send(f"Bom dia, @{ctx.author.name}! Como você está?")

    if 'boa tarde' in ctx.content.lower():
        await ctx.channel.send(f"Boa tarde, @{ctx.author.name}! Como você está?")

    if 'boa noite' in ctx.content.lower():
        await ctx.channel.send(f"Boa noite, @{ctx.author.name}! Como você está?")

    if 'salve' in ctx.content.lower():
        await ctx.channel.send(f"Ta salvado, @{ctx.author.name}! Como você está?")


@bot.command(name='test')
async def test(ctx):
    await ctx.send('teste passou.')


if __name__ == "__main__":
    bot.run()
