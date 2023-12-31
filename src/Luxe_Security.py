import discord
from discord.ext import commands
import os
import logging
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Get the bot token, guild ID, and client ID from the environment variables
bot_token = os.getenv('LS_TOKEN')
guild_id = int(os.getenv('GUILD_ID'))
client_id = int(os.getenv('CLIENT_ID'))

# Create an instance of Intents
intents = discord.Intents.all()
intents.members = True  # This is necessary to receive member events like on_member_join

# Create an instance of the bot with intents
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    log_message = f'{bot.user.name} is ready for duty.'
    print(log_message)
    logging.info(log_message)
    print('------')

@bot.event
async def on_member_join(member):
    # Get the server (guild) and the target role
    guild = member.guild
    target_role_id = 1189082673193435186  # Replace with the actual role ID
    target_role = guild.get_role(target_role_id)

    # Assign the target role to the new member
    await member.add_roles(target_role)

    # Get the channel where you want to send the log message
    log_channel_id = 1189081098056122411  # Replace with the actual channel ID
    log_channel = guild.get_channel(log_channel_id)

    # Send the log message to the specified channel
    log_message = f'{member.display_name} has been granted {target_role.name} status at the Luxe Lounge. Please enjoy your stay.'
    await log_channel.send(log_message)

    # Print the log message to the console
    print(log_message)
    logging.info(log_message)

@bot.command(name="clear", description="Clear all messages in a specified channel")
async def clear_channel(ctx, channel: discord.TextChannel = None):
    # If the channel is not provided, use the current channel
    if channel is None:
        channel = ctx.channel

    # Check if the bot has the necessary permissions to manage messages
    if ctx.author.guild_permissions.manage_messages:
        # Purge (delete) all messages in the specified channel
        await channel.purge()

        # Send a confirmation message
        confirmation_message = f"All messages in {channel.mention} have been cleared."
        await ctx.send(confirmation_message)

        # Print the confirmation message to the console
        print(confirmation_message)
        logging.info(confirmation_message)
    else:
        # Send a message if the user doesn't have the necessary permissions
        error_message = "You don't have the necessary permissions to manage messages."
        await ctx.send(error_message)

        # Print the error message to the console
        print(error_message)
        logging.error(error_message)


# Run the bot with your token
bot.run(bot_token)
