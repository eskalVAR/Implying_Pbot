#INITIAL CHANNEL/SERVER SETUP
pbot_server = "YOUR_SERVER_ID" #Can be found in Server Settings -> Widget
main_unverified_role = "NAME_OF_YOUR_UNVERIFIED_ROLE" #Must match the name given in the server
main_admin_role = "THE_NAME_OF_YOUR_ADMIN_ROLE" #Must match the name given in the server
welcome_channel = "WELCOME_MESSAGE_CHANNEL_ID" #The ID of the channel you want welcome messages to be sent. The new member should preferably have read permissions on the channel.
goodbye_channel = "GOODBYE_MESSAGE_CHANNEL_ID" #Same as above but for goodbye messages. Can also be the same channel.


import json
import discord
import asyncio
import mysql.connector
from datetime import datetime
import time
from discord.ext.commands import Bot
from discord.ext import commands
from unidecode import unidecode
from urllib.request import urlopen
from json import load

def remove_non_ascii(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in str(text)])

conn = mysql.connector.connect(user='root', password='PASSWORD', host='127.0.0.1', database='pbot')
db = conn.cursor(buffered=True)

client = Bot(description="UwU", command_prefix=">>", pm_help = True, command_has_no_subcommand='Missing arguments!', command_not_found='Command not found. Do k!commands for a list of available commands')
@client.event
async def on_ready():
    print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
    await client.change_presence(game=discord.Game(name='your mom gay'))

@client.event
async def on_member_join(member):
 my_ip = load(urlopen('http://httpbin.org/ip'))['origin']
 print(str(member)+' just joined the server')
 member_non_ascii = remove_non_ascii(member)
 server = client.get_server(pbot_server)
 unverified = discord.utils.get(server.roles, name=main_unverified_role)
 await client.add_roles(member, unverified)
 timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
 db.execute("""INSERT into members_uwu (discord_name,discord_id,join_date,verified,in_server,real_name,email,reason_join,in_group,ip_addr) values(%s,%s,%s,0,1,0,0,0,0,0)""",(str(member_non_ascii), int(member.id), timestamp))
 conn.commit()
 await client.send_message(client.get_channel(welcome_channel), "Ahoy, <@!"+member.id+">! Welcome t' **>implying we can programming** jus' be sure that ye check out our rules 'n announcements... ye know, that shiney. 'ave a good time in here 'n farrg off. ***Please check yer' DMs.***")
 await client.send_message(member,"Welcome to the server please go to this link to complete your registration: http://"+my_ip+'/?id='+str(member.id))
 await asyncio.sleep(1800)
 member_id = member.id
 db.execute("SELECT verified from members_uwu WHERE discord_id="+member_id)
 value = db.fetchone()
 verified = value[0]
 print('The verified value is '+str(verified))
 if verified is 0:
     invite = await client.create_invite(client.get_channel('INVITE_CHANNEL'))
     await client.send_message(member,'Your failure to comply has resulted in a kick. Fear not you can join again using this invite '+invite.url)
     await asyncio.sleep(1)
     await client.kick(member)


@client.event
async def on_member_remove(member):
     await client.send_message(client.get_channel(goodbye_channel), "A'ight, farewell, **<@!"+member.id+">**...")
 db.execute("UPDATE members_uwu SET in_server=0 WHERE discord_id="+member.id)
 conn.commit()


@client.command(pass_context=True)
async def verify(ctx, member: discord.Member = None):
 member2 = ctx.message.author
 server = client.get_server(pbot_server)
 member2server = server.get_member(member2.id)
 unverified = discord.utils.get(server.roles, name=main_unverified_role)
 if unverified in member2server.roles:
  db.execute("SELECT verified from members_uwu WHERE discord_id="+member2.id)
  verified_status = db.fetchone()
  if verified_status[0] is 1:
        await client.remove_roles(member2server, unverified)
        await client.say(':white_check_mark: You have been verified. Enjoy your stay :champagne:')
  else:
        await client.say(':negative_squared_cross_mark: Please fill in the form first. Check your PMs')
 else:
  await client.say(':negative_squared_cross_mark: You are already verified')


@client.command(pass_context=True)
async def check(ctx, arg):
 server = client.get_server(pbot_server)
 member2 = ctx.message.author
 user2check = ctx.message.raw_mentions
 user_id = ''.join(user2check)
 db.execute("SELECT discord_name from members_uwu WHERE discord_id="+user_id)
 discord_name = db.fetchone()
 join_date = server.get_member(user_id).joined_at
 embed = discord.Embed(title=':mag: >PBot User Lookup', color=0xc242f4)
 embed.add_field(name='Discord Name', value=arg, inline=False)
 embed.add_field(name='Discord ID', value=user_id)
 embed.add_field(name='Name in DB', value=discord_name[ 0 ], inline=False)
 embed.add_field(name='Join Date', value=join_date)
 await client.say(embed=embed)


@client.event
async def on_member_update(before, after):
 user_id = before.id
 old_name = before.name
 new_name = after.name+'#'+after.discriminator
 new_name2 = remove_non_ascii(new_name)
 new_name_store = new_name2.replace(" ", "_")
 if old_name != after.name:
  await client.send_message(client.get_channel(namechange_channel), ':white_check_mark: <@!'+user_id+'> changed their name from **'+old_name+'** to **'+after.name+'**')
  db.execute("UPDATE members_uwu SET discord_name="+new_name_store+" WHERE discord_id="+user_id)
  conn.commit()


@client.command(pass_context=True)
async def logmembers(ctx):
 server = client.get_server(pbot_server)
 member2 = ctx.message.author
 admin = discord.utils.get(server.roles, name=main_admin_role)
 if admin in member2.roles:
  for member in client.get_all_members():
     member_non_ascii = remove_non_ascii(member)
     member_id = member.id
     timestamp = member.joined_at
     db.execute("""INSERT into members_uwu (discord_name,discord_id,join_date,verified) values(%s,%s,%s,1)""",(str(member_non_ascii), int(member_id), timestamp))
     conn.commit()
     print('Added to db '+str(member_non_ascii)+' '+str(member_id)+' '+str(timestamp))
     await client.say(':white_check_mark: '+member+' logged successfully')
 else:
    await client.say(':negative_squared_cross_mark: Only admins can use this!')


#DOESN'T WORK SO COMMENTED OUT
#@client.command(pass_context=True)
async def massdelete(ctx,msgfrom,msgto):
 del_msg_count = 0
 server = client.get_server(pbot_server)
 channel = ctx.message.channel
 print(channel.name)
 await client.send_message(channel,'I work')
 message_after = client.get_message(channel,msgfrom)
 message_before = client.get_message(channel,msgto)
 member2 = ctx.message.author
 admin = discord.utils.get(server.roles, name=main_admin_role)
 if admin in member2.roles:
     del_list = client.purge_from(channel,100,message_before,message_after)
     print(str(del_list))
     await client.say(':white_check_mark: Successfully deleted '+str(del_list)+' messages !')
 else:
    await client.say(':negative_squared_cross_mark: Only admins can use this!')

@client.command()
async def registerbump():
 await client.say('Got it! Will notify you 6 hours later...')
 await asyncio.sleep(21600)
 await client.say('@here Please bump again on discord.me')


@client.command(pass_context=True)
async def verifyuser(ctx,arg):
 server = client.get_server(pbot_server)
 member2 = ctx.message.author
 admin = discord.utils.get(server.roles, name=main_admin_role)
 if admin in member2.roles:
     unverified = discord.utils.get(server.roles, name=main_unverified_role)
     user2check = ctx.message.raw_mentions
     user_id = ''.join(user2check)
     db.execute("UPDATE members_uwu SET verified=1 WHERE discord_id="+user_id)
     conn.commit()
     await client.remove_roles(server.get_member(user_id), unverified)
     await client.say(':white_check_mark: Manually verified <@!'+str(user_id)+'> !')
 else:
     await client.say(':negative_squared_cross_mark: Only admins can use this!')





client.run('YOUR_BOT_TOKEN')
