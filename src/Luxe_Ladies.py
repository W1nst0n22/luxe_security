import discord
from discord.ext import commands
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the bot token, guild ID, and client ID from the environment variables
bot_token = os.getenv('LL_TOKEN')
guild_id = int(os.getenv('GUILD_ID'))
client_id = int(os.getenv('CLIENT_ID'))

# Create an instance of Intents
intents = discord.Intents.all()
intents.members = True  # This is necessary to receive member events like on_member_join

# Create an instance of the bot with intents
bot = commands.Bot(command_prefix='/', intents=intents)

# Function to award balance and write to a text file
def award_balance(user_id, amount):
    # Retrieve current balance from the file
    try:
        with open("balances.txt", "r") as file:
            balances = eval(file.read())
    except FileNotFoundError:
        balances = {}

    # Update or create the balance for the user
    balances[user_id] = balances.get(user_id, 0) + amount

    # Write the updated balances back to the file
    with open("balances.txt", "w") as file:
        file.write(str(balances))
# Function to read balances from the file
def read_balances():
    try:
        with open("balances.txt", "r") as file:
            balances = eval(file.read())
        return balances
    except FileNotFoundError:
        return {}

@bot.event
async def on_ready():
    log_message = f'{bot.user.name} is ready to serve.'
    print(log_message)
    logging.info(log_message)
    print('------')

@bot.event
async def on_member_join(member):
    # Send a private message to the new member
    welcome_message = ("Welcome to Luxe Lounge! Please take your seat at the table and enjoy a $5,000 credit for new members.\n\n"
                      "https://www.pokernow.club/games/pglvi_R_XzI4q34W0zVDNtUdU")
    try:
        await member.send(welcome_message)
    except discord.Forbidden:
        # Handle cases where the bot is not allowed to send DMs
        print(f"Could not send a welcome message to {member.display_name}. DMs are disabled.")


@bot.command(name="promote", description="Promote someone to a different role")
async def promote_patron(ctx, member: discord.Member):  # Add a parameter for the member to be promoted
    # Get the server (guild) and the target role
    guild = ctx.guild
    target_role_id = 1190756016745365574  # Replace with the actual role ID
    target_role = guild.get_role(target_role_id)

    if target_role is not None:
        # Filter out the @everyone role
        roles_to_remove = [role for role in member.roles if role.name != "@everyone"]

        # Print debug information
        print(f"Roles to remove: {[r.name for r in roles_to_remove]}")
        print(f"Target role: {target_role.name}")

        # Remove all existing roles from the member
        try:
            await member.remove_roles(*roles_to_remove)
        except discord.NotFound as e:
            print(f"Error removing roles: {e}")

        # Add the target role to the member
        await member.add_roles(target_role)

        # Create the log message
        log_message = f'{member.display_name} has been granted {target_role.name} status at the Luxe Lounge. Please enjoy your stay.'

        # Send the log message to the same channel where the command is invoked
        await ctx.send(log_message)

        # Print the log message to the console
        print(log_message)
        logging.info(log_message)
    else:
        print(f"Error: Target role with ID {target_role_id} not found.")
        logging.error(f"Target role with ID {target_role_id} not found.")




@bot.command(name="demote", description="Demote someone to a specified role")
async def demote_member(ctx, member: discord.Member):  # Add a parameter for the member to be demoted
    # Get the server (guild) and the target role
    guild = ctx.guild
    target_role_id = 1189082673193435186  # Replace with the actual role ID for the demotion
    target_role = guild.get_role(target_role_id)

    if target_role is not None:
        # Filter out the @everyone role
        roles_to_remove = [role for role in member.roles if role.name != "@everyone"]

        # Print debug information
        print(f"Roles to remove: {[r.name for r in roles_to_remove]}")
        print(f"Target role: {target_role.name}")

        # Remove all existing roles from the member
        try:
            await member.remove_roles(*roles_to_remove)
        except discord.NotFound as e:
            print(f"Error removing roles: {e}")

        # Add the target role to the member
        await member.add_roles(target_role)

        # Create the log message
        log_message = f'{member.display_name} has been demoted to {target_role.name}.'

        # Send the log message to the same channel where the command is invoked
        await ctx.send(log_message)

        # Print the log message to the console
        print(log_message)
        logging.info(log_message)
    else:
        print(f"Error: Target role with ID {target_role_id} not found.")
        logging.error(f"Target role with ID {target_role_id} not found.")


# Slash command to award balance
@bot.command(name='award', help='Award balance to a player')
async def award_balance_command(ctx, user: discord.User, amount: int):
    # Award balance to the specified user
    award_balance(user.id, amount)

    # Send a confirmation message
    await ctx.send(f"Balance of {amount} awarded to {user.mention}")

# Slash command to display balances
@bot.command(name='balances', help='Display user balances')
async def display_balances(ctx):
    # Read balances from the file
    balances = read_balances()

    # Send a message with the balances
    if balances:
        message = "User Balances:\n"
        for user_id, balance in balances.items():
            user = bot.get_user(int(user_id))
            if user:
                message += f"{user.display_name}: {balance}\n"
        await ctx.send(message)
    else:
        await ctx.send("No balances found.")

# Run the bot with your token
bot.run(bot_token)