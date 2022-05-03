#導入 Discord.py
import imp
import discord
import os
from discord.ext import commands
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()
from discord.ext import tasks
from database import DataBase
users_infodic={}
loop_time = 0
store_database_time = 2 #循環幾次儲存資料進資料庫
#client 是我們與 Discord 連結的橋樑
intents = discord.Intents.default()
intents.members = True
#client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='#')
database = DataBase()
#調用 event 函式庫
@client.event
#當機器人完成啟動時
async def on_ready():
    myLoop.start()
    print('目前登入身份：', client.user)
    

@client.command()
async def check(ctx):
    global users_infodic
    print("user id:")
    print(ctx.message.author.id)
    print(users_infodic)
    _userid = str(ctx.message.author.id)
    if _userid in users_infodic.keys():
        await ctx.send('<@'+str(_userid)+'>' +' 目前正在公司,累積貢獻度中')
    else:
        await ctx.send('<@'+str(_userid)+'>' +' 不在公司,請進入任一語音頻道開始累積,如果已經在頻道中請重新進入.')

@client.command()
async def info(ctx):
    _userid = str(ctx.message.author.id)
    if database.checkUser(_userid) is True:
        user_info = database.getUser(_userid)
        user_money = user_info['user_score']
        await ctx.send('<@'+str(_userid)+'>' +' 累積貢獻度:'+str(user_money))
    else:
        await ctx.send('<@'+str(_userid)+'>' +' 歡迎加入麥歡樂企業')
        database.createUser(_userid)

@client.command()
async def rank(ctx):
    top5 = database.getTop5Ranking()
    result =""
    for user in top5:
        print(user)
        id = user['id']
        score = user['score']
        result+='<@'+str(id)+'>' +' 分數:'+str(score)+"\n"
    await ctx.send(result)


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
    memberid = str(member.id)
    textChannel = client.get_channel(channelid)
    if after.channel == None:
        print("離開")
        print('<@'+str(memberid)+'>' +' 離開公司,停止計算貢獻值!')
        if memberid in users_infodic.keys():
            print("此員工已在資料表內 移除此員工站存資料")
            del users_infodic[memberid]
        else:
            print("好像有錯誤... 某人離開了 但他沒加入資料過")
        await textChannel.send('<@'+str(memberid)+'>' +' 離開公司,停止計算貢獻值!')
    elif after.channel is not None:
        print('<@'+str(memberid)+'>' +' 進入公司上班,開始貢獻心力一同壯大麥歡樂企業!')
        await textChannel.send('<@'+str(memberid)+'>' +' 進入公司上班,開始貢獻心力一同壯大麥歡樂企業!')
        if memberid in users_infodic.keys():
            print("此員工已在資料表內 不在更動")
        else:
            #使用者 - 分數
            print("此員工不在資料表內 將他加入工作中列表")
            users_infodic[memberid] = 0

    
@tasks.loop(seconds = 10) # repeat after every 10 seconds
async def myLoop():
    print('每10秒成長貢獻值 : 1')
    print("目前列表")
    global users_infodic
    global loop_time
    global store_database_time
    print(users_infodic)
    for user in users_infodic:
        users_infodic[user] += 1
    loop_time+=1
    if loop_time>=store_database_time:
        await dataBase()
        loop_time = 0

async def dataBase():
    print('每20秒資料庫儲存')
    print("目前列表")
    global users_infodic
    print(users_infodic)
    for user in users_infodic:
        if database.checkUser(user) == False:
            print("此玩家不在資料庫 創建")
            database.createUser(user,users_infodic[user])
        else:
            user_info = database.getUser(user)
            user_score = user_info["user_score"] 
            user_score = int(user_score) + users_infodic[user]
            database.SetUserScoreById(user,user_score)
    for user in users_infodic:
        users_infodic[user] = 0
    
if __name__ == "__main__":
    client.run(os.getenv('BOT_TOKEN')) #TOKEN 在剛剛 Discord Developer 那邊「BOT」頁面裡面
    