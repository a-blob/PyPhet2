#import stuff
import os
import random

import discord
from discord import app_commands
from discord.ext import tasks

from keep_alive import keep_alive

#define stuff
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

pyphet_answers = [
    "Yes.", "Definitely.", "My answer is yes.", "Ofcourse.", "It's certain.",
    "No.", "The answer is no.", "I would say no.", "Not likely.",
    "Certainly not."
]

activity_choices = ["yes/no questions", "no/yes questions"]

pyphet_dice = [" 1⚀ ", " 2⚁ ", " 3⚂ ", " 4⚃ ", " 5⚄ ", " 6⚅ "]

pyphet_coin = [":coin: Heads", ":arrows_counterclockwise: Tails"]


#basic events
@client.event
async def on_ready():
  change_status.start()
  print('We have logged in as {0.user}'.format(client))
  await tree.sync()


@tasks.loop(seconds=10)
async def change_status():
  await client.change_presence(
      activity=discord.Activity(type=discord.ActivityType.listening,
                                name=random.choice(activity_choices)))


#define events
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if (message.content.startswith('!pyphet') or client.user
      in message.mentions) and ('dictator' in message.content
                                or 'dictate' in message.content
                                or 'domination' in message.content):
    pyphet_answer = "I'd rather not say."
    await message.channel.send(pyphet_answer)
  elif message.content.startswith(
      '!pyphet') or client.user in message.mentions:
    pyphet_answer = random.choice(pyphet_answers)
    await message.channel.send(pyphet_answer)


@tree.command(name="help", description="Having trouble with PyPhet?")
async def help_command(ctx):
  embed_help = discord.Embed(
      title=":grey_question:PyPhet Help",
      description=
      "Pyphet is a simple Discord bot that helps you make life decisions easier.",
      color=discord.Color.purple())
  embed_help.add_field(
      name=":crystal_ball: Yes or no?",
      value=
      "You can ask PyPhet yes/no questions; it works like a magic 8 ball. To ask, type `!pyphet` in chat followed by your question.",
      inline=False)
  embed_help.add_field(
      name=":game_die: Dice rolling",
      value=
      "To roll some dice, run the command `/rolladice` followed by the amount of dice. You can also run the command `/dicepro`, which allows you to specify the amount of sides your dice have.",
      inline=False)
  embed_help.add_field(
      name=":rock: Rock paper scissors",
      value=
      "To play rock paper scissors with PyPhet, run the command `/rps` followed by your choice of either rock, paper, or scissors.",
      inline=False)
  embed_help.add_field(name=":coin: Flip a coin",
                       value="To flip a coin, run the command `/flipacoin`.",
                       inline=False)
  await ctx.response.send_message(embed=embed_help)


@tree.command(name="rolladice", description="Roll a dice.")
async def rolladice(ctx, amount: app_commands.Range[int, 1, 1000]):
  dice_result = ""
  dice_count = 0
  while dice_count < amount:
    dice_count += 1
    dice_result = dice_result + random.choice(pyphet_dice)
  embed_rolladie = discord.Embed(title="",
                                 description="# " + dice_result,
                                 color=discord.Color.purple())
  await ctx.response.send_message(embed=embed_rolladie)


@tree.command(
    name="dicepro",
    description=
    "Dice Roller Pro Plus Premium Max 2nd Generation Ultra Mini Light Zoom 12th Edition"
)
async def dicepro(ctx, sides: app_commands.Range[int, 1, 100],
                  amount: app_commands.Range[int, 1, 1000]):
  dice_result = ""
  dice_total = 0
  dice_count = 0
  while dice_count < amount:
    dice_count += 1
    dice_random = random.randint(1, sides)
    if dice_count == amount:
      dice_result = dice_result + str(dice_random)
    elif dice_count == amount - 1:
      dice_result = dice_result + str(dice_random) + ", and "
    else:
      dice_result = dice_result + str(dice_random) + ", "
    dice_total = dice_total + dice_random
  embed_rolladie = discord.Embed(
      title=":game_die: PyPhet Dice Roller Pro",
      description="You rolled " + str(amount) + " dice that have " +
      str(sides) + " sides.\n" + "You rolled: " + dice_result + "\n\nTotal: " +
      str(dice_total),
      color=discord.Color.purple())
  await ctx.response.send_message(embed=embed_rolladie)


@tree.command(name="flipacoin", description="Flip a coin.")
async def flipacoin(ctx):
  coin_result = random.choice(pyphet_coin)
  embed_flipacoin = discord.Embed(title="",
                                  description="# " + coin_result,
                                  color=discord.Color.purple())
  await ctx.response.send_message(embed=embed_flipacoin)


pyphet_rps = ["paper", "rock", "scissors"]
wc = ["rockscissors", "paperrock", "scissorspaper"]


@tree.command(name="rps", description="Play rock paper scissors")
async def rps(ctx, user_choice: str):
  if user_choice not in pyphet_rps:
    await ctx.response.send_message(
        "Please choose between rock, paper, and scissors!")
    return
  rps_a = random.choice(pyphet_rps)
  if user_choice == rps_a:
    await ctx.response.send_message(rps_a + "\nIt's a tie!")
  elif user_choice + rps_a in wc:
    await ctx.response.send_message(rps_a + "\nYou win!")
  else:
    await ctx.response.send_message(rps_a + "\nYou loose!")


#run bot
keep_alive()

try:
  token = os.getenv("TOKEN") or ""
  if token == "":
    raise Exception("Please add your token to the Secrets pane.")
  client.run(token)
except discord.HTTPException as e:
  if e.status == 429:
    print(
        "The Discord servers denied the connection for making too many requests"
    )
    print(
        "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
    )
  else:
    raise e
