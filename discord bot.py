import discord, random, os, asyncio, requests, bs4, re
from discord import File
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import Bot

# required for role removal after reaction removal (on_reaction_remove)
intents = discord.Intents.all()

# the bot
client = commands.Bot(command_prefix=".", intents = intents)

# function that creates a string object of "pingable" users with a line break between each
def makePingableStr(user_ids: list):
    ids_pingable = ""
    for user_id in user_ids:
        ids_pingable += f"<@{user_id}>\n"
    return ids_pingable


# function that creates a string object of "pingable" users with **NO** line break between each
def makePingableStrNoLb(user_ids: list):
    ids_pingable = ""
    for user_id in user_ids:
        ids_pingable += f"<@{user_id}> "
    return ids_pingable


reaction_title = ""
reactions = {
    "VC Notifications": "🔉",
    "Settlers": "1️⃣",
    "COD: Cold War": "2️⃣",  
}
reaction_message_id = ""

lfg_reaction_message_id = "" # the id of the message players react to to be added to the queue
interested_players = [] # for lfg command

# LFG global variables
lfg_embed_message_obj = ""
lfg_embed_author = ""
lfg_game_name = ""
lfg_number_of_players = ""

# lfg command
@client.command(name="lfg")
async def lfg(context, game, number_of_players: int):
    global interested_players, lfg_reaction_message_id, lfg_embed_author, lfg_game_name, lfg_number_of_players, lfg_embed_message_obj
    interested_players.clear()
    interested_players.append(context.author.id) # add pingable format later, remove this comment when you do
    
    lfg_embed = discord.Embed(title="Looking for Game (LFG)", description=f"<@{context.message.author.id}> wants to play `{game}`.\n\nReact to this message with :raised_hand: if you'd like to play and you'll be added to the queue.\nYou can remove your reaction if you change your mind.", color=0x24daff)
    lfg_embed.add_field(name=f"Players in queue\n", value=f"<@{context.author.id}>", inline=True) # make list a string at some point?
    lfg_embed.add_field(name="Player count", value=f"`{len(interested_players)}/{number_of_players}`", inline=True)
    lfg_embed.add_field(name="Author only:",value="\nReact with :white_check_mark: to end queue early and ping players currently in queue.\nReact with :x: to destroy queue.",inline=False)
    
    
    gen_ch = client.get_channel(688852636598141032) # TFL general

    message = await gen_ch.send(embed=lfg_embed)

    lfg_embed_message_obj = message # makes our original embed message a global variable for later editing

    lfg_reaction_message_id = str(message.id)
    lfg_embed_author = context.author.id
    lfg_game_name = game
    lfg_number_of_players = number_of_players

    await message.add_reaction("✋")
    await message.add_reaction("✅")
    await message.add_reaction("❌")





# sends the famous Del Griffith quote from Planes, Trains and Automobiles
@client.command(name="pta")
async def pta(context):
    await context.message.channel.send("""You wanna hurt me? Go right ahead if it makes you feel any better. I'm an easy target. Yeah, you're right. I talk too much. I also listen too much. I could be a cold-hearted cynic like you, but I don't like to hurt people's feelings. Well, you think what you want about me. I'm not changing. I like me. My wife likes me. My customers like me. 'Cause I'm the real article. What you see is what you get.""")


# generates Powerball numbers
@client.command(name="pball")
async def pball(context):
    def Powerball():
        result = []
        for i in range(5):
            number = random.randint(1,69)
            while number in result:
                number = random.randint(1,69)
            result.append(number)
        result.sort()
        result.append(random.randint(1,26))
        return result
    a = (Powerball())
    b = str(a[5])
    del a[5]
    a = str(a)
    await context.message.channel.send("Your numbers: " + a + " PB: " + b + ". Good luck!")



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    general_channel = client.get_channel(channel ID)

    statuses = ["for .info","for .role_assign",f"in {len(client.guilds)} servers","you","for your commands"]

    while not client.is_closed():
        status = random.choice(statuses)
        activity = discord.Activity(name=status, type=discord.ActivityType.watching)
        await client.change_presence(activity=activity)
        

        await asyncio.sleep(30)
    # await general_channel.send("The Eagle has landed.")
    # await client.change_presence(activity=discord.Game(name='The Sims'))
    # activity = discord.Activity(name="for .info", type=discord.ActivityType.watching)
    # await client.change_presence(activity=activity)


@client.event
async def on_message(message):
    emojis = ["💯","😇","😁","😀","😃","😄", "😁", "😆", "😅", "😂","🐢","🤪","❤️"]

    if message.author == client.user:
       return
    if message.content == "regulators!".casefold():
        await message.channel.send("Mount up! <@581116327847264256> <@287323027979370507> <@547520456186658836>")
    # elif message.author != client.user:
    #     await message.add_reaction(emojis[0])

    # elif message.author.id == 350008068165337089:
    #     await message.add_reaction(emojis[10])
    #     await message.add_reaction(emojis[12])
    
    # bot auto reacts with emoji to all messages
    if message.channel.id == 795385854100373525:
        await message.add_reaction("😆")

    await client.process_commands(message)


# this is the embed message with all the commands and other info
@client.command(name="info")
async def info(context):
    myEmbed = discord.Embed(title="Justin's Discord Bot", description="""Hello! My name is Sir Walter Brimsdale, but you can call me Walt.
    I am a bot created by <@547520456186658836> and I answer to the following commands:""", color=0xfeee14)
    myEmbed.add_field(name="Fun", value="""
    `.age` / Returns your Discord age (how old your account is)
    `.m8ball "your_question_here"` / Ask the magic 8-ball a question and receive an answer
    `.pball` / Generates winning Powerball numbers. Seriously.
    `.poke @User` / Pokes the specified user via DM.
    `.rps *` / Play me in Rock, Paper, Scissors. Example: `.rps r`, `.rps p`, `.rps s`
    `.ud` / Returns a random word and its definition from UrbanDictionary.com""")
    myEmbed.add_field(name="Role Assignment", value="Enter `.role_assign` and follow the prompt.\nEnter `.vcn` to enable/disable voice channel notifications.", inline=False)
    myEmbed.add_field(name="Utilities", value="""
    `.clear *` / Deletes a specified number(*) of messages in the channel it is sent. Default is 5.
    `.coin` / Flips a coin
    `.dice` / Rolls two six-sided dice
    `.invite` / DMs you a temporary server invitation link you can share with others
    `.rng min max` / Randomly generates a number in a specified range. Example: `.rng 1 100`
    `.serverinfo` / Returns information about the server/guild
    `.stk ticker_symbol_here` / Returns info on price and performance of a stock (Ex: `.stk aapl` or `.stk tsla`)
    """, inline=False)
    await context.message.channel.send(embed=myEmbed)

# rolls two dice
@client.command(name="dice")
async def dice(context):
    def Roll():
        min_value = 1
        max_value = 6
        dye_1 = random.randint(min_value, max_value)
        dye_2 = random.randint(min_value, max_value)
        result = [dye_1, dye_2]
        return result

    the_roll = Roll()
    num1 = the_roll[0]
    num2 = the_roll[1]
    await context.message.channel.send(f"🎲 You roll a {num1} and a {num2} for a total of {num1 + num2}. 🎲")

# coin flip
@client.command(name="coin")
async def coin(context):
    outcomes = ['heads','tails']
    result = random.choice(outcomes)
    await context.message.channel.send(f"It's {result}.")


@client.command(name="rng")
async def rng(context, min_num: int, max_num: int):
    rgnumber = random.randint(min_num, max_num)
    if min_num != "" and max_num != "":
        await context.send(f"Random number: {rgnumber}")
    else:
        await context.send("Please provide a number range with your command. Example: for 1 to 100, type `.rng 1 100`")

# rock paper scissors game
@client.command(name="rps")
async def rps(context, user_move):
    rps_moves = ['r','p','s',]
    client_move = random.choice(rps_moves[0:2])
    player = context.message.author.display_name

    if user_move == client_move:
        await context.message.channel.send(f"I also chose {user_move}. It's a draw!")
    elif user_move == 'r' and client_move == 'p':
        await context.message.channel.send(f"I chose paper. Paper beats rock. I win!")
    elif user_move == 'r' and client_move == 's':
        await context.message.channel.send(f"I chose scissors. Rock beats scissors. You win!")
    elif user_move == 'p' and client_move == 'r':
        await context.message.channel.send(f"I chose rock. Paper beats rock. You win!")
    elif user_move == 'p' and client_move == 's':
        await context.message.channel.send(f"I chose scissors. Scissors beat paper. I win!")
    elif user_move == 's' and client_move == 'p':
        await context.message.channel.send(f"I chose paper. Scissors beat paper. You win!")
    elif user_move == 's' and client_move == 'r':
        await context.message.channel.send(f"I chose rock. Rock beats scissors. I win!")
    elif user_move not in rps_moves:
        await context.message.channel.send(f"Error: You must enter a value of either r, p, or s.\n\n Didn't you ever play this game in grade school, {player}?")

# add error handling to rps command at some point

# magic 8 ball command
@client.command(name="m8ball")
async def m8ball(context, question):
    user_question = question
    responses = [
        'It is certain.', 
        'It is decidedly so.', 
        'Without a doubt.', 
        'Does a bear shit in the woods?',
        'Yes - definitely.',
        'You may rely on it.',
        'As I see it, yes.',
        'Most likely',
        'Outlook good.',
        'Yes.',
        'Signs point to yes.',
        'Reply hazy. Try again.',
        'Ask again later.',
        "It's for the best that I don't tell you.",
        "Don't count on it.",
        'Go pound sand.',
        "It's highly unlikely.",
        "It's comical that you would even consider that a possibility.",
        "It's an unequivocal yes from me.",
        "I am delighted to say: No.",
        "Incredibly unlikely. Like one in a billion. On a good day."]
    answer = random.choice(responses)
    await context.message.channel.send(f"((( You've summoned the Magic :8ball: ))) \n> Question: {question}\n> \n> Response: *{answer}*")

# returns a list of members who are currently in the CubbyStuffers vc
@client.command(name="vc")
async def vc(context):
    ch = client.get_channel(688852636598141035)
    mems = ch.voice_states.keys()
    mem_list = ""
    for usr_id in mems:
        mem_list += f"<@{usr_id}> "
    print(mem_list)
    await context.message.channel.send(f"The following users are in {ch}: {mem_list}")


# stock info fetcher
@client.command(name="stk")
async def stk(context, ticker):
    ticker_symbol = ticker
    stock_url = 'https://www.marketwatch.com/investing/stock/' + ticker_symbol
    get_stock_info = requests.get(stock_url)
    #get_company_name = requests.get(stock_url)
    
    get_stock_info.raise_for_status()
    #get_company_name.raise_for_status()
    
    # multiple assignments of html elements. Each shares the same source, so they're listed a = b = c = d = e = value
    soup_stock_price = soup_company_name = soup_stock_1yr = soup_stock_5d = soup_stock_1month = soup_stock_3month = soup_stock_YTD = bs4.BeautifulSoup(get_stock_info.text, 'html.parser')

    price_elem = soup_stock_price.select('body > div.container.container--body > div.region.region--intraday > div.column.column--aside > div > div.intraday__data > h3 > bg-quote')
    name_elem = soup_company_name.select('body > div.container.container--body > div.region.region--intraday > div:nth-child(2) > div > div:nth-child(2) > h1')
    five_day_elem = soup_stock_5d.select('body > div.container.container--body > div.region.region--primary > div:nth-child(2) > div.group.group--elements.right > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > ul > li.content__item.value.ignore-color')
    month1_elem = soup_stock_1month.select('body > div.container.container--body > div.region.region--primary > div:nth-child(2) > div.group.group--elements.right > div.element.element--table.performance > table > tbody > tr:nth-child(2) > td:nth-child(2) > ul > li.content__item.value.ignore-color')
    month3_elem = soup_stock_3month.select('body > div.container.container--body > div.region.region--primary > div:nth-child(2) > div.group.group--elements.right > div.element.element--table.performance > table > tbody > tr:nth-child(3) > td:nth-child(2) > ul > li.content__item.value.ignore-color')
    YTD_elem = soup_stock_YTD.select('body > div.container.container--body > div.region.region--primary > div:nth-child(2) > div.group.group--elements.right > div.element.element--table.performance > table > tbody > tr:nth-child(4) > td:nth-child(2) > ul > li.content__item.value.ignore-color')
    yr1_elem = soup_stock_1yr.select('body > div.container.container--body > div.region.region--primary > div:nth-child(2) > div.group.group--elements.right > div > table > tbody > tr:nth-child(5) > td:nth-child(2) > ul > li.content__item.value.ignore-color')

    company_name = name_elem[0].text
    trading_at_price = price_elem[0].text
    five_day_performance = five_day_elem[0].text
    month1_performance = month1_elem[0].text
    month3_performance = month3_elem[0].text
    YTD_performance = YTD_elem[0].text
    yr1_performance = yr1_elem[0].text

    stockEmbed = discord.Embed(title= company_name, description=f"Currently trading at: `${trading_at_price}`", color=0x3e9e3e)
    stockEmbed.add_field(name="Performance", value=f"""5 day: {five_day_performance}\n1 Month: {month1_performance}\n3 Months: {month3_performance}\nYTD: {YTD_performance}\n1 yr: {yr1_performance}""")

    await context.message.channel.send(embed=stockEmbed)
    # add volume info
    # add error message for indexerrors

# returns a random word from urban dictionary. User can also specify a word as an argument.
@client.command(name="ud")
async def ud(context, word=None):
    if word == None:
        ub_url = 'https://www.urbandictionary.com/random.php?page='
        random_num = random.randint(1,999)
        random_word = requests.get(ub_url + str(random_num))
        random_word.raise_for_status()

        soup_rword = bs4.BeautifulSoup(random_word.text, 'html.parser')
        word_elem = soup_rword.select('#content > div:nth-child(1) > div.def-header > a')
        definition_elem = soup_rword.select('#content > div:nth-child(1) > div.meaning')

        random_word = word_elem[0].text
        word_definition = definition_elem[0].text

        await context.message.channel.send(f"**{random_word}**: {word_definition}")
    
    if word != None:
        ub_url = 'https://www.urbandictionary.com/define.php?term='
        user_word = word
        user_word2 = requests.get(ub_url + user_word)
        user_word2.raise_for_status()

        soup_user_word = bs4.BeautifulSoup(user_word2.text, 'html.parser')
        word_elem = soup_user_word.select('#content > div:nth-child(1) > div.def-header > a')
        definition_elem = soup_user_word.select('#content > div:nth-child(1) > div.meaning')

        random_word = word_elem[0].text
        word_definition = definition_elem[0].text

        await context.message.channel.send(f"**{random_word}**: {word_definition}")

# # sends Allen Iverson quote
# @client.command(name="prac")
# async def prac(context):
#     await context.message.channel.send("If a coach say I missed practice, and y’all hear it, then that’s that. I might’ve missed one practice this year. But if somebody says, ‘He doesn’t come to practice — it can be one practice, out of all the practices this year — then that’s enough. … But it’s easy to talk about, it’s easy to sum it up when you just talk about practice. We sittin’ in here, I’m supposed to be the franchise player, and we in here talkin’ about practice. I mean listen, we talkin’ ’bout practice. Not a game, not a game, not a game. We talkin’ about practice. Not a game, not a, not a, not the game that I go out there and die for, and play every game like it’s my last. Not the game. We talkin’ bout practice, man. I mean how silly is that? We talkin’ bout practice. I know I’m supposed to be there, I know I’m supposed to lead by example. I know that, and I’m not shovin’ it aside, you know, like it don’t mean anything. I know it’s important, I do. I honestly do. But we talkin’ bout practice, man. What are we talkin’ about? Practice? We talkin’ about practice, man. [Reporters laughing] We talk — we talkin’ bout practice. We talkin’ bout practice! We ain’t talkin’ bout the game, we talkin’ bout practice, man. When you come into the arena, and you see me play, you see me play, don’t you? You see me give everything I got, right? But we talkin’ bout practice right now. [Reporter: ‘But it’s an issue that your coach raised.’] We talkin’ bout practice. Man look, I hear you, it’s funny to me too. I mean, it’s strange, it’s strange to me too. But we talkin’ bout practice, man. We not even talkin’ bout the game, the actual game, when it matters. We talkin’ bout practice.")

# Named jb for Jackbox. Sends a DM containing a room code to users active in the voice channel
@client.command(name="jb")
async def jb(context, code, *args):
    room_code = code
    ch = client.get_channel(688852636598141035)
    mems = ch.voice_states.keys()
    mem_list = ""
    for usr_id in mems:
        mem_list += f"{usr_id} "
    
    print(mem_list)
    users = mem_list.split()
    print(users)

    for user in users:
        person = client.get_user(int(user))
        await person.send(f"Room code: {room_code}")

    await discord.Message.delete(context.message)
    
# bulk deletes messages in a channel if user has permission
@client.command(name="clear")
async def clear(context, amount=5):
    auth_users = [547520456186658836,350008068165337089,287323027979370507]
    if context.message.author.id in auth_users:
        await context.channel.purge(limit= amount + 1)
    else:
        await context.message.channel.send("You do not have the permissions required to perform this command.")


# spams a mentioned user with pings
# @client.command(name="spam")
# async def spam(context, person):
#     for i in range(15):
#         await context.message.channel.send(f"{person} LMAO GET SPAMMED!!!")

# creates the post which allows users to react to self-assign roles
@client.command(name="role_assign")
async def role_assign(context):

    embed = discord.Embed(title="Self-assign Your User Role(s)", color=0xf63707)
    embed.set_author(name="Justin's Discord Bot (AKA Walt)")
    embed.add_field(name="Set Your Role(s)", value="""To assign yourself a role, react to this message in the following ways. To remove a role, remove your reaction.\n
    :sound: - VC Notifications (If enabled, you'll receive a DM notification whenever somebody joins a voice channel. You can opt in/out at any time.)\n\n:one: - Settlers of Catan\n:two: - Call of Duty: Black Ops Cold War""")
    embed.add_field(name="Having trouble?", value="If you experience any issues, have a question or a suggestion, ping or message <@547520456186658836> for assistance.", inline=False)

    message = await context.send(embed=embed)

    global reaction_message_id
    reaction_message_id = str(message.id)

    for role in reactions:
        await message.add_reaction(reactions[role])
    
    await context.message.delete()

# when user adds reaction, assign them their chosen role
@client.event
async def on_reaction_add(reaction, user):
    global interested_players, gen_ch, lfg_embed_author, lfg_game_name, lfg_number_of_players

    if not user.bot:
        message = reaction.message

        if str(message.id) == reaction_message_id:
            # add roles to users

            role_to_give = ""

            for role in reactions:
                if reactions[role] == reaction.emoji:
                    role_to_give = role
            
            role_for_reaction = discord.utils.get(user.guild.roles, name=role_to_give)
            await user.add_roles(role_for_reaction)
            await user.send("Role updated! You have added the `" + str(role_for_reaction) + "` role in `" + str(user.guild) + "`.", delete_after=120)

        elif str(message.id) == lfg_reaction_message_id:
            if reaction.emoji == "✋":
                if user.id not in interested_players: # NOT IN adds reacting user to interested player list if they aren't already in it
                    interested_players.append(user.id)

                    ids_pingable = makePingableStr(interested_players)
                    # interested_players_pingable = "" 
                    # for user_id in interested_players:
                    #     interested_players_pingable += f"<@{user_id}>\n"

                    if len(interested_players) == int(lfg_number_of_players): # queue is now full
                        await lfg_embed_message_obj.channel.send(f"Queue is now full! Let's play {lfg_game_name}!\n{ids_pingable}")

                    # edits embed to add player's name/id
                    new_lfg_embed = discord.Embed(title="Looking for Game (LFG)", description=f"<@{lfg_embed_author}> wants to play `{lfg_game_name}`.\nReact to this message with :raised_hand: if you'd like to play and you'll be added to the queue.\nYou can remove your reaction if you change your mind.\nPlayers in queue will be pinged when queue is full.", color=0x24daff)
                    new_lfg_embed.add_field(name=f"Players in queue\n", value=ids_pingable, inline=True)
                    new_lfg_embed.add_field(name="Player count", value=f"`{len(interested_players)}/{lfg_number_of_players}`", inline=True)
                    new_lfg_embed.add_field(name="Author only:",value="\nReact with :white_check_mark: to end queue early and ping players currently in queue.\nReact with :x: to destroy queue.",inline=False)

                    await lfg_embed_message_obj.edit(embed=new_lfg_embed) # original embed is overwritten by new_lfg_embed
            
            elif reaction.emoji == "✅" and user.id == int(lfg_embed_author): # queue is ended early by author and while under max capacity
                interested_players_early = makePingableStr(interested_players)
                # for user_id in interested_players:
                #     interested_players_early += f"<@{user_id}>\n"
                await lfg_embed_message_obj.channel.send(f":white_check_mark: Queue ended by <@{lfg_embed_author}>. Let's play {lfg_game_name}!\n{interested_players_early}")
            
            elif reaction.emoji == "❌" and user.id == int(lfg_embed_author): # queue is aborted by the author
                await lfg_embed_message_obj.delete()
                await lfg_embed_message_obj.channel.send(":x: Queue destroyed.")

            else:
                return
        
        # add timeout functionality where LFG post is destroyed if inactive for too long



# when user removes reaction, remove their chosen role
@client.event
async def on_reaction_remove(reaction, user):
    global interested_players, gen_ch, lfg_embed_author, lfg_game_name, lfg_number_of_players

    if not user.bot:
        message = reaction.message

        if str(message.id) == reaction_message_id:
            # remove roles from users

            role_to_remove = ""

            for role in reactions:
                if reactions[role] == reaction.emoji:
                    role_to_remove = role
            
            role_for_removal = discord.utils.get(user.guild.roles, name=role_to_remove)
            await user.remove_roles(role_for_removal)
            await user.send("Role updated! You have removed the `" + str(role_for_removal) + "` role in `" + str(user.guild) + "`.", delete_after=120)

        elif user.id != int(lfg_embed_author):
            # if not user.bot:
            # message = reaction.message

            if str(message.id) == lfg_reaction_message_id:
                if user.id in interested_players:
                    interested_players.remove(user.id)

                    interested_players_pingable = makePingableStr(interested_players)
                    # for user_id in interested_players:
                    #     interested_players_pingable += f"<@{user_id}>\n"
                    


                    # edit embed to remove players name/id
                    new_lfg_embed = discord.Embed(title="Looking for Game (LFG)", description=f"<@{lfg_embed_author}> wants to play `{lfg_game_name}`.\nReact to this message with :raised_hand: if you'd like to play and you'll be added to the queue.\nYou can remove your reaction if you change your mind.", color=0x24daff)
                    new_lfg_embed.add_field(name=f"Players in queue\n", value=interested_players_pingable, inline=True)
                    new_lfg_embed.add_field(name="Player count", value=f"`{len(interested_players)}/{lfg_number_of_players}`", inline=True)
                    new_lfg_embed.add_field(name="Author only:",value="\nReact with :white_check_mark: to end queue early and ping players currently in queue.\nReact with :x: to destroy queue.",inline=False)

                    await lfg_embed_message_obj.edit(embed=new_lfg_embed)

                else:
                    return
    else:
        return
            


# sends a pic of Bruce Willis
@client.command(name="bruce")
async def bruce(context):
    os.chdir('/home/pi/My_bot/bruce.jpeg')
    os.path('/home/pi/My_bot/bruce.jpeg')
    with open('bruce.jpeg', 'rb') as fp:
        await context.channel.send(file=discord.File(fp, 'new_filename.png'))

# allows user to anonymously DM anyone through the bot
@client.command(name="dm")
async def dm(context, user_id, message):
    msg_contents = message # + "\n\nNote: Replies in this DM channel are only visible to you. The sender cannot see them."
    recipient = client.get_user(int(user_id))
    me = client.get_user(int(547520456186658836))

    dm = await recipient.send(msg_contents,delete_after=180)
    await me.send(f"\nRecipient: <@{recipient.id}> // Sender: <@{context.author.id}>\nMessage: `{msg_contents}`")
    await context.message.delete()

# let me google that for you. needs to be fixed to accomodate search queries of varying lengths
@client.command(name="lmgtfy")
async def lmgtfy(context, search_query):
    search_terms = str(search_query).split()
    search_url = "https://lmgtfy.app/?q=" + search_terms[0] + "+" + search_terms[1] + "+" + search_terms[2] + "+" + search_terms[3]
    await context.send(search_url)
    

@client.command(name="poke")
async def poke(context, user: discord.User):
    person_poked = client.get_user(user.id)
    await person_poked.send(f"<@{context.author.id}> poked you.")
    await context.message.delete()


@client.command(name="age")
async def age(context):
    member = context.author.id
    time_created = discord.utils.snowflake_time(member)
    msg_time = context.message.created_at
    await context.send(f"{context.author.name}, your Discord age is: `{msg_time - time_created}` old.\nYour account was created: `{time_created.strftime('%B %-d, %Y %I:%M:%S %p %z')}`")


@client.event
async def on_voice_state_update(member, before, after):
    if member.bot is False: # checking if member is a bot account. If bot joins vc, no notification is sent.
        if before.channel is None and after.channel is not None: # filters out other voice status updates from triggering a notification (mute, unmute, deafen, undeafen, streaming, not streaming, etc.)
            if member.voice != None: # error handling, as member.voice.channel is None when a user leaves (or is not in) a vc
                ch = member.voice.channel
            else:
                return # we don't want to be notified when a person leaves or is not in a vc
            

            ##############################
            # FIGURING OUT WHO TO NOTIFY #
            ##############################

            guild_members = member.guild.members # returns a list of all server members in the server where the voice channel was joined
            
            guild_member_ids = [] # a list of all server member ID numbers
            for guild_member in guild_members: # makes a list of all server member ID numbers so that we can role check each
                guild_member_ids.append(guild_member.id)

            vc_notification_users = [] # a list of user ID numbers of the server members who have the "VC Notifications" role assigned

            for guild_member in guild_member_ids: # checking to see what members currently have the "VC Notifications" role assigned to them
                person = member.guild.get_member(guild_member)
                
                for role in person.roles: # returns a list of all roles assigned to each server member, then checks if "VC Notifications" is one of them
                    if role.name == "VC Notifications":
                        vc_notification_users.append(guild_member)


            ######################################################
            # GETTING THE CURRENT OCCUPANTS OF THE VOICE CHANNEL #
            ######################################################

            # occupants = ch.members # a list of current occupants of the voice channel and their attributes
            occupants = []
            for user in ch.members:
                if user.bot is False: # filtering out bot accounts from the list of occupants
                    occupants.append(user)


            occupant_ids = [] # a list of the user IDs for the voice channel occupants. Later used to check if a person to be notified is already a VC occupant (thus no DM sent)
            for occupant in occupants:
                if occupant.bot is False:
                    occupant_ids.append(occupant.id)
            
            ids_pingable = makePingableStrNoLb(occupant_ids)

            ##############################################################
            # NOTIFYING USERS WHO HAVE THE VC NOTIFICATIONS ROLE ENABLED #
            ##############################################################

            for user in vc_notification_users:
                notification_recipient = member.guild.get_member(user) # initializing our Member object
                
                if notification_recipient.id not in occupant_ids: # if person to be notified is already in voice channel, do not send them a notification
            
                    # if there is one user in the voice channel, send this via DM:
                    if len(occupants) > 0 and len(occupants) < 2:
                        await notification_recipient.send(f"{len(occupants)} user ({ids_pingable}) is now in the `{ch}` voice channel in `{occupant.guild.name}`.\n\nNote: You received this notification because you're assigned the `VC Notifications` role in `{occupant.guild.name}`. If you'd like to stop these notifications, opt in or out at any time by entering the `.vcn` command message in the server.", delete_after=300)
                    
                    # if there are 2 or more users in the voice channel, send this via DM:
                    elif len(occupants) >= 2:
                        await notification_recipient.send(f"\n{len(occupants)} users ({ids_pingable}) are now in the `{ch}` voice channel in `{occupant.guild.name}`.\n\nNote: You received this notification because you're assigned the `VC Notifications` role in `{occupant.guild.name}`. If you'd like to stop these notifications, opt in or out at any time by entering the `.vcn` command message in the server.", delete_after=300)
                
                else:
                    return
        else:
            return
    else:
        return


# command to enable/disable voice channel notifications
@client.command(name="vcn")
async def vcn(context):
    vcn_role_id = 796766816449200189
    vcn_role = context.author.guild.get_role(vcn_role_id)
    message = context.message

    if vcn_role not in context.author.roles:
        # add role AKA enable vcn
        role_to_add = discord.utils.get(context.author.guild.roles, name="VC Notifications")
        await context.author.add_roles(role_to_add)
        await message.add_reaction("✅")
        await context.channel.send(f"**Change confirmed:** You have successfully **added** the <@&{vcn_role_id}> role.\nYou will now receive voice channel notifications via DM when someone joins a voice channel.\nYou can disable these at any time by issuing the `.vcn` command.")
        

    elif vcn_role in context.author.roles:
        # remove role AKA disable vcn
        role_for_removal = discord.utils.get(context.author.guild.roles, name="VC Notifications")
        await context.author.remove_roles(role_for_removal)
        await message.add_reaction("✅")
        await context.channel.send(f"**Change confirmed:** You have successfully **removed** the <@&{vcn_role_id}> role.\nYou will no longer receive voice channel notifications when someone joins a voice channel.\nYou can re-enable at any time by issuing the `.vcn` command.")
    


@client.command(name="serverinfo")
async def serverinfo(context):
    guild_member_ids = []
    bot_ids = []
    mobile_users = []
    online_members = []
    idle_members = []
    dnd_members = []
    offline_members = []
    
    for user in context.guild.members:
        guild_member_ids.append(user.id)
        if user.bot == True:
            bot_ids.append(user.id)
        if user.is_on_mobile() == True:
            mobile_users.append(user.id)

    
    for user_id in guild_member_ids:
        user = context.guild.get_member(user_id)
        if user.status == discord.Status.online:
            online_members.append(user_id)
        elif user.status == discord.Status.idle:
            idle_members.append(user_id)
        elif user.status == discord.Status.dnd:
            dnd_members.append(user_id)
        elif user.status == discord.Status.offline:
            offline_members.append(user_id)
    
    percent_online = float(len(online_members) / context.guild.member_count)
    percent_idle = float(len(idle_members) / context.guild.member_count)
    percent_dnd = float(len(dnd_members) / context.guild.member_count)
    percent_offline = float(len(offline_members) / context.guild.member_count)
    percent_bots = float(len(bot_ids) / context.guild.member_count)


    server_info_embed = discord.Embed(title=f"Server info for {context.guild.name}", description=f"\nServer owner: <@{context.guild.owner.id}>\nCreation date: `{context.guild.created_at.strftime('%B %d, %Y  %I:%M %p %z')}`\n")
    server_info_embed.add_field(name="Members", value=f"`{context.guild.member_count}` total members\n\n`{len(online_members)}` Online  ({'{:.0%}'.format(percent_online)} of server members)\n`{len(idle_members)}` Idle  ({'{:.0%}'.format(percent_idle)} of server members)\n`{len(dnd_members)}` Do Not Disturb  ({'{:.0%}'.format(percent_dnd)} of server members)\n`{len(offline_members)}` Offline  ({'{:.0%}'.format(percent_offline)} of server members)\n\n`{len(mobile_users)}` user(s) on mobile""")
    server_info_embed.add_field(name="\n\nBots", value=f"`{len(bot_ids)}` bots in server  ({'{:.0%}'.format(percent_bots)} of server members)", inline=False)
    await context.channel.send(embed=server_info_embed)


@client.command(name="joke")
async def joke(context):
    
    with open('/home/pi/Documents/Walt Discord bot jokes.txt', 'r') as f:
        quotes = f.readlines()
        quote = quotes[random.randint(1, len(quotes))]
 
    await context.send(quote)



@client.command(name="invite")
async def invite(context):
    invitation = await context.channel.create_invite(max_age=1800, max_uses=3, temporary=True, reason=f"Created by {context.author.name} to grant someone temporary server membership. Invitee is kicked automatically after disconnecting.")
    await context.author.send(f"Here's your invitation link!\nInvitation type: Temporary / Expires after: 30 minutes / Uses: 3\n{invitation}", delete_after=1800)


# used for fetching activity data while coding new commands/events
# @client.command(name="act")
# async def act(context, user):
#     person = context.guild.get_member(int(user))
#     print(person.name)
#     print(person.status)
#     print("\n")
#     print(person.activities)
#     for activity in person.activities:
#         if activity.type == discord.ActivityType.playing:
#             print("Hallelujah")
#         elif activity.type == discord.ActivityType.listening:
#             print("this user be listening my guy")

#     await context.message.delete()


# Streaming status LIVE notification event THIS IS THE WORKING ONE
@client.event
async def on_member_update(before, after): # removed self
    # Get the guild ID.
    guild_id = after.guild.id
    # Get the discord name of the author from their ID.
    author = client.get_user(after.id)
    # Get the channel you want your message to send in.
    channel = client.get_channel(688852636598141032)
    # This makes sure the message only sends once. The update is processed once for each guild the bot is in.
    if guild_id == 688852635981447352:
        after_activity_type = None
        stream_url = None
        # Get the URL of the stream and the activity (hopefully streaming) that they're doing.
        try:
            after_activity_type = after.activity.type
            stream_url = after.activity.url
        except:
            pass
        # Make sure they're streaming.
        if after_activity_type is discord.ActivityType.streaming:
            # Get the website they're streaming on and the name of the user.
            stream_url_split = stream_url.split(".")
            streaming_service = stream_url_split[1]
            streaming_service = streaming_service.capitalize()
            author_string = str(author)
            author_full_id = author_string.split("#")
            author_name = author_full_id[0]
            myEmbed = discord.Embed(title= f":red_circle: **LIVE**\n{author_name} is now streaming!", description=f"<@{after.id}> is LIVE on {streaming_service}\n\n [Click or tap here to tune in!]({stream_url})", color=0x6441a5)
            await channel.send(embed=myEmbed)

client.run('TOKEN HERE')



