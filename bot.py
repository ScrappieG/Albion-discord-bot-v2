
from typing import Optional
import discord
from discord import app_commands
import sqlite3
import crafting
from sql_queries import add_member, is_member,remove_member,update_guild_balance,find_guild_balance, find_all_balance

TOKEN = 'KEY'
REGEAR_CHANNEL = 123 #replace with the channel id you want the regears to be sent to
LOG_CHANNEL = 123 #replace with your log channel id


MY_GUILD = discord.Object(id=123)  # replace with your guild id


TAX_RATE = 10 #can be changed whenever needed to but hardcoded seems to be better for everyone


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        
        self.tree = app_commands.CommandTree(self)

    #synchronize apps to one guild instead of multiple 
    #By having one guild it makes the commands faster :) as we dont need to specify a guild in every command

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.all()
# give the bot intents (basically permissions)
client = MyClient(intents=intents)



@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

@client.event
async def on_member_join(member: discord.Member):
    """adds a player to the db when they join"""
    conn = sqlite3.connect('bot.db')
    if member.id == None:
        print(f'error adding member {member}')
    else:
        add_member(str(member.id), conn)
        await member.send('Welcome to goobers!')

    #This is a little harder on actually running the bot but makes it so an admin
    #doesnt have to register every member seperately (just a quality of life thing)

@client.event
async def on_member_remove(member: discord.Member):
    """removes member from db when they leave"""
    conn = sqlite3.connect('bot.db')
    if member.id == None:
        print(f'error removing member {member}')
    else:
        remove_member(str(member.id), conn)
    
    #just like the function above it is a quality of life thing that makes the bot a little harder to run
        

@client.tree.command()
async def banana(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f'banana., {interaction.user.mention}')

#just a way to test if the bot is functioning correctly in the server



@client.tree.command()
@app_commands.describe(member='The member you want to get the joined date from; defaults to the user who uses the command')
async def joined(interaction: discord.Interaction, member: Optional[discord.Member] = None):
    """Says when a member joined."""
    member = member or interaction.user

    await interaction.response.send_message(f'{member} joined {discord.utils.format_dt(member.joined_at)}')

    #allows people to know when another member joined


@client.tree.command()
@app_commands.rename(first_value = 'lootsplit_total',
                    third_value = 'tax',
                    balance = 'add_to_bal'
                     )
@app_commands.describe(first_value='Total Ammount Of The Loot Split')
@app_commands.describe(third_value='Default is set to 10%'+' (ex. 15% = 15)')
@app_commands.describe(balance='Use True if you want to add the loot split value to their balances')
async def lootsplit(interaction: discord.Interaction, first_value: int, third_value: Optional[int] = None, balance: Optional[bool] = False):
    """Creates easy loot splits"""


    if third_value == None:
        tax_rate = TAX_RATE/100
        print(tax_rate)
    else:
        tax_rate = third_value/100
    tax = round(first_value * tax_rate)
    loot_without_tax = first_value *(1-tax_rate)
    print(tax_rate)
    print(loot_without_tax)
 #calculation of the loot split
    channel_id = interaction.user.voice.channel.id
    channel = client.get_channel(channel_id)
    members = channel.members
    counter = 0
    response = discord.Embed(title = 'Loot split :D')
    for member in members:
        counter += 1
    players = counter
    Loot_value = round((loot_without_tax) / players)
    if balance == True:
        for member in members:
                    conn = sqlite3.connect('bot.db')
                    balance= find_guild_balance(str(member.id),conn)
                    ammount = Loot_value + balance
                    conn = sqlite3.connect('bot.db')
                    update_guild_balance(str(member.id),ammount,conn)
                    counter += 1
    #grabs number of members in the vc that the user is in and adds their split of the loot to their silver balance
    
    players = counter
    Loot_value = round((loot_without_tax) / players)

    response.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
    response.timestamp = interaction.created_at

    response.description = (f'Loot value per person: {Loot_value:,} Tax: {tax:,}')
    await interaction.response.send_message(embed=response,ephemeral=True, delete_after=60)
    log_channel = interaction.guild.get_channel(LOG_CHANNEL)
    await log_channel.send(embed=response)

    #makes the lootsplits a little easier


@client.tree.command()
@app_commands.rename(
    first_value='first_name',
    second_value='last_name',
    item_tier='tier',
    material_1='material_1',
    material_2='material_2',
    )
@app_commands.describe(
    first_value='ex soldier,mage,light',
    second_value='ex armor,crossbow,sandals',
    item_tier='tier of the  item you are crafting',
    material_1='The ammount of your materials (ex: 999)',
    material_2='If there are not two materials needed put 0',
    )
async def t5_flat_craft(interaction: discord.Interaction, first_value: str, second_value: str, item_tier: int, material_1: int, material_2: int,return_rate:Optional[float] = None):
    crafted_list = crafting.main_crafter(first_name=first_value,Last_name=second_value,item_tier=item_tier,material_1=material_1,material_2=material_2,return_rate=return_rate)
    if crafted_list == 1:
        response = discord.Embed(title = 'Crafting recieved an error go scream at scwappie in his dms')

        response.description = (f'dork')
    else:
        response = discord.Embed(title = 'Crafting Wooooooo')

        response.description = (f"fees and taxes: {crafted_list['fees']} \n Material Cost {crafted_list['cost_of_material']} \n Black Market Price:{crafted_list['BM price']} \n Number of items {crafted_list['items']} \n Profit: {crafted_list['profit']} \n ROI: {crafted_list['roi']} \n Books fill: {crafted_list['books_filled']}")

    await interaction.response.send_message(embed=response,ephemeral=True, delete_after=60)

    #This is a work in progress, it just allows you to users to get an estimation for their profit on t5 flat crafting



@client.tree.command()
@app_commands.rename(
    first_value='tier',
    second_value='alt_ammount',
    )
@app_commands.describe(
    first_value='Player Name',
    second_value='Alternative ammount for the regear ammount',
    )
async def regear(interaction: discord.Interaction, member: discord.Member, first_value: int, second_value: Optional[int] = None):

    regear_ammounts = {6: 500000, 7 : 750000, 8: 1000000}
    member_id = member.id

    if first_value != 6 or first_value != 7 or first_value != 8:
        print('error with tier')
        response = discord.Embed(title = 'Regear Request Did not go Through D:')

        response.description = (f'Incorrect tier')

    if second_value != None:
        request_ammount = second_value
    else:
        request_ammount = regear_ammounts[(first_value)]

    conn = sqlite3.connect('bot.db')
    print(is_member(member_id=str(member_id), conn=conn))
    conn = sqlite3.connect('bot.db')
    
    if is_member(member_id=str(member_id), conn=conn) == True:
        conn = sqlite3.connect('bot.db')
        current_value = find_guild_balance(member_id=member_id, conn=conn)
        conn = sqlite3.connect('bot.db')
        ammount = current_value + request_ammount
        update_guild_balance(member_id=member_id, ammount=ammount, conn=conn)
        response = discord.Embed(title = 'Regear Request Submitted')

        response.description = (f'Ammount Requested: {request_ammount:,} \n Guild Balance {ammount:,}')
    else:
        print('error with member')
        response = discord.Embed(title = 'Regear Request Did not go Through D:')

        response.description = (f'The User is not a member please use /register <@member>')

    response.set_author(name=member.display_name, icon_url=member.display_avatar.url)
    response.timestamp = interaction.created_at

    await interaction.response.send_message(embed=response,ephemeral=True, delete_after=60)
    log_channel = interaction.guild.get_channel(REGEAR_CHANNEL)
    await log_channel.send(embed=response)

    #Command allows regears to be faster and saved automatically

@client.tree.command()
@app_commands.rename(
    first_value='ammount',
    )
@app_commands.describe(
    first_value='negative # if subtract positive if add',
    )
async def update_balance(interaction: discord.Interaction, member: discord.Member,  first_value: int):
    """Allow moderator to change a users guild balance directly"""

    conn = sqlite3.connect('bot.db')
    
    if is_member(member_id=str(member.id), conn=conn) == True:
        conn = sqlite3.connect('bot.db')
        current_value = find_guild_balance(member_id=member.id, conn=conn)
        conn = sqlite3.connect('bot.db')
        ammount = current_value + (first_value)
        update_guild_balance(member_id=member.id, ammount=ammount, conn=conn)
        response = discord.Embed(title = 'Balance is updated')

        response.description = (f'New balance: {ammount:,}')
    else:
        response = discord.Embed(title = 'Balance could not be Updated D:')

        response.description = (f'User is not a member please use /register <@user>')

    response.set_author(name=member.display_name, icon_url=member.display_avatar.url)
    response.timestamp = interaction.created_at

    await interaction.response.send_message(embed=response,ephemeral=True, delete_after=60)
    log_channel = interaction.guild.get_channel(LOG_CHANNEL)
    await log_channel.send(embed=response)

    #allows moderators to update a members silver balance

@client.tree.command()
async def all_balances(interaction:discord.Interaction):

    conn = sqlite3.connect('bot.db')

    balance_list = find_all_balance(conn=conn)
    print(balance_list)

    message = ''
    

    for i in range(len(balance_list)):
        temp = balance_list[i]
        guild_balance = temp[0]

        user = await client.fetch_user(int(temp[1]))
        name = user.display_name
        message = (f'{message} \n {name}: ${guild_balance}')
        
    response = discord.Embed(title = 'Balances :D')

    response.description = (f'{message}')

    await interaction.response.send_message(embed=response, ephemeral=True,delete_after=120)

#allows moderators to pull all members silver balances




@client.tree.command()
async def register(interaction: discord.Interaction, member:Optional[discord.Member] = None):
    """register a member into the db"""
    member = member or interaction.user
    conn = sqlite3.connect('bot.db')

    if member.id == None:
        await interaction.response.send_message(f'This does not appear to be a member',delete_after=60, ephemeral=True)
    else:
        members = []

        members = client.get_all_members()

        print(member.id)

        conn = sqlite3.connect('bot.db')
        match = is_member(str(member.id), conn)

        print('match')
        print(match)

        if match == True:
            print('match == True')
            await interaction.response.send_message('This user has already been registered',delete_after=60, ephemeral=True)

        if member in members and match == False:
            conn = sqlite3.connect('bot.db')
            add_member(str(member.id), conn)
            print(str(member.id))
            await interaction.response.send_message(f'{member.display_name} has been registered',delete_after=60, ephemeral=True)

    #registers a member to the database




@client.tree.context_menu(name='Show Join Date')
async def show_join_date(interaction: discord.Interaction, member: discord.Member):
    """shows join date of a member"""
    await interaction.response.send_message(f'{member} joined at {discord.utils.format_dt(member.joined_at)}',delete_after=60, ephemeral=True)

#allows moderators to view the date at which a member joined


@client.tree.context_menu(name='Report to Moderators')
async def report_message(interaction: discord.Interaction, message: discord.Message):
    """report a message"""
    await interaction.response.send_message(
        f'Thanks for reporting this message by {message.author.mention} to our moderators.', ephemeral=True
    )

    log_channel = interaction.guild.get_channel(LOG_CHANNEL)

    embed = discord.Embed(title='Reported Message')
    if message.content:
        embed.description = message.content

    embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
    embed.timestamp = message.created_at

    url_view = discord.ui.View()
    url_view.add_item(discord.ui.Button(label='Go to Message', style=discord.ButtonStyle.url, url=message.jump_url))

    await log_channel.send(embed=embed, view=url_view)

    #allows a member to report a message 



@client.tree.context_menu(name='view guild balance')
async def view_guild_balance(interaction: discord.Interaction, member: discord.Member):
    """view a members guild balance"""

    conn = sqlite3.connect('bot.db')

    member_id = member.id

    balance = find_guild_balance(str(member_id), conn)
    print(balance)
  # replace with your regear Channel

    embed = discord.Embed(title='Guild Silver Balance')
            
    embed.description = (f'Total: {balance}')
    embed.set_author(name=member.display_name, icon_url=member.display_avatar.url)
    embed.timestamp = interaction.created_at

    await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=120)

    #allows members to view their own and others guild balances







    


client.run(TOKEN)