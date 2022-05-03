#導入 Discord.py
import discord
import os
#client 是我們與 Discord 連結的橋樑
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
from dotenv import load_dotenv
load_dotenv()
#調用 event 函式庫
@client.event
#當機器人完成啟動時
async def on_ready():
    print('目前登入身份：', client.user)

@client.event
#當有訊息時
async def on_message(message):
    #排除自己的訊息，避免陷入無限循環
    if message.author == client.user:
        return
    #如果包含 ping，機器人回傳 pong
    if message.content == 'ping':
        await message.channel.send('pong')

@client.event
async def on_member_join(member):
    print(F'{member} join')

@client.event
async def on_member_remove(member):
    print(F'{member} leave')

@client.event
async def on_voice_state_update(member,before, after):
    print(member)
    print(member.id)
    print(before)
    print(after)
    channelid = 662347467458871319
    memberid = member.id
    textChannel = client.get_channel(channelid)
    
    await textChannel.send('<@'+str(memberid)+'>' +' 進入公司上班,開始貢獻心力一同壯大麥歡樂企業!')

client.run(os.getenv('BOT_TOKEN')) #TOKEN 在剛剛 Discord Developer 那邊「BOT」頁面裡面