import req_iab.request as rr
import json
def acreq(typ,showAbstract,idno):
    lx=typ
    if lx=='project':
        jsonstring=rr.getOrPost("{}","post","https://aerfaying.com/WebApi/Projects/"+str(idno)+"/Get/")
        if jsonstring=="<ERROR 3>无法在未安装requests库的情况下爬虫，请在cmd/Terminal中输入pip[版本] install requests安装，如pip3.8 install requests":
            print("错误:无法在未安装requests库的情况下爬虫，请在cmd/Terminal中输入pip[版本] install requests安装，如pip3.8 install requests")
            return
        if jsonstring=="<ERROR 4> 结果转码失败":
            print("错误:结果转码失败。")
            return
        if jsonstring=="<ERROR 1> 必须添加网址前缀https://":
            print("错误:必须添加网址前缀https://")
            return
        try:
            jsonDict=json.loads(jsonstring)
        except:
            print("错误:咨询作者并提供信息获取更新版本或解决方案。")
        try:
            print("获得了系统返回的消息:"+jsonDict['message']+"\n<Response 404>")
        except:
            pass
        try:
            print("系统发生错误:"+jsonDict['error']+"\n<Response 500>")
        except:
            try:
                print("作品ID:"+str(jsonDict['project']['id']))
            except:
                print("未找到变量project/id")
            try:
                print("作品标题:"+str(jsonDict['project']['title']))
            except:
                print("未找到变量project/title")
            try:
                print("作品封面图片:"+str(jsonDict['project']['thumbId']))
            except:
                print("未找到变量project/thumbID")
            try:
                print("作者ID:"+str(jsonDict['project']['creatorId']))
            except:
                print("未找到变量project/creatorId")
            try:
                print("版权方:"+str(jsonDict['project']['ownerType']))
            except:
                print("未找到变量project/ownerType")
            try:
                print("版权方ID:"+str(jsonDict['project']['ownerId']))
            except:
                print("未找到变量project/ownerId")
            try:
                print("最新版本:"+str(jsonDict['project']['version']))
            except:
                print("未找到变量project/version")
            try:
                print("点赞数量:"+str(jsonDict['project']['loverCount']))
            except:
                print("未找到变量project/loverCount")
            try:
                print("收藏数量:"+str(jsonDict['project']['favoriterCount']))
            except:
                print("未找到变量project/favoriterCount")
            try:
                print("再创作作品数量:"+str(jsonDict['project']['remixCount']))
            except:
                print("未找到变量project/remixCount")
            try:
                print("观看量:"+str(jsonDict['project']['viewCount']))
            except:
                print("未找到变量project/viewCount")
            try:
                print("已发布:"+str(jsonDict['project']['isPublished']))
            except:
                print("未找到变量project/PublishTime")
            try:
                print("对应任务ID:"+str(jsonDict['project']['missionId']))
            except:
                print("未找到变量project/missionId")
            try:
                print("评论开放等级:"+str(jsonDict['project']['commentOpenLevel']))
            except:
                print("未找到变量project/commentOpenLevel")
            if showAbstract=='y' or showAbstract=='Y':
                try:
                    print("作品简介:"+str(jsonDict['project']['descp']))
                except:
                    print("未找到变量project/descp")
            else:
                pass
            # print(json.dumps(obj=jsonDict,indent=4))
    elif lx=='mission':
        jsonstring=rr.getOrPost("{}","post","https://aerfaying.com/WebApi/Missions/"+str(idno)+"/Get/")
        if jsonstring[0:15]=="<!DOCTYPE html>":
            print("获得了系统返回的消息:资源不存在。"+"\n<Response 404>")
        else:
            jsonDict=json.loads(jsonstring)
            try:
                print("任务类型:"+str(jsonDict['mission']['type']))
            except:
                print("未找到变量mission/type")
            try:
                print("任务名称:"+str(jsonDict['mission']['name']))
            except:
                print("未找到变量mission/name")
            try:
                print("任务图片:"+str(jsonDict['mission']['thumbId']))
            except:
                print("未找到变量mission/thumbId")
            try:
                print("可以购买:"+str(jsonDict['mission']['isBuyable']))
            except:
                print("未找到变量mission/isBuyable")
            try:
                print("货币:"+str(jsonDict['mission']['currency']))
            except:
                print("未找到变量mission/currency")
            try:
                print("价格:"+str(jsonDict['mission']['price']))
            except:
                print("未找到变量mission/price")
            try:
                print("制作者ID:"+str(jsonDict['mission']['creator']['id']))
            except:
                print("未找到变量mission/creator/id")
            try:
                print("制作者管理等级:"+str(jsonDict['mission']['creator']['adminLevel']))
            except:
                print("未找到变量mission/creator/adminLevel")
            try:
                print("制作者用户名:"+str(jsonDict['mission']['creator']['username']))
            except:
                print("未找到变量mission/creator/username")
            try:
                print("制作者头像:"+str(jsonDict['mission']['creator']['thumbId']))
            except:
                print("未找到变量mission/creator/thumbId")
            try:
                print("制作者等级:"+str(jsonDict['mission']['creator']['level']))
            except:
                print("未找到变量mission/creator/level")
            try:
                print("制作者是否被ban:"+str(jsonDict['mission']['creator']['isBanned']))
            except:
                print("未找到变量mission/creator/isBanned")
            try:
                print("制作者前缀工作室ID:"+str(jsonDict['mission']['creator']['primaryStudio']['id']))
            except:
                print("未找到变量mission/creator/primaryStudio/id")
            try:
                print("制作者前缀名:"+str(jsonDict['mission']['creator']['primaryStudio']['shortName']))
            except:
                print("未找到变量mission/creator/primaryStudio/shortName")
            try:
                print("是否是官方任务:"+str(jsonDict['mission']['isOfficial']))
            except:
                print("未找到变量mission/isOfficial")
            try:
                print("含有教程:"+str(jsonDict['mission']['hasTutorial']))
            except:
                print("未找到变量mission/hasTutorial")
            try:
                print("接受任务人数:"+str(jsonDict['mission']['acceptCount']))
            except:
                print("未找到变量mission/acceptCount")
            try:
                print("完成任务人数:"+str(jsonDict['mission']['completeCount']))
            except:
                print("未找到变量mission/completeCount")
            try:
                print("标签:"+str(jsonDict['mission']['tags']))
            except:
                print("未找到变量mission/tags")
            try:
                print("基础奖励列表:"+str(jsonDict['mission']['basicPrizes']))
            except:
                print("未找到变量mission/basicPrizes")
            try:
                print("K12年级:"+str(jsonDict['mission']['k12Grade']))
            except:
                print("未找到变量mission/k12Grade")
            try:
                print("难度:"+str(jsonDict['mission']['difficultyLevel']))
            except:
                print("未找到变量mission/difficultyLevel")
            # print(json.dumps(obj=jsonDict,indent=4))
    elif lx=='studio':
        jsonstring=rr.getOrPost("{}","post","https://aerfaying.com/WebApi/Studios/"+str(idno)+"/Get/")
        jsonDict=json.loads(jsonstring)
        try:
            print("获得了系统返回的消息:"+jsonDict['message']+"\n<Response 404>")
        except:
            pass
        try:
            print("工作室名称:"+str(jsonDict['studio']['name']))
        except:
            print("未找到变量studio/name")
        try:
            print("工作室头像:"+str(jsonDict['studio']['thumbId']))
        except:
            print("未找到变量studio/thumbId")
        try:
            print("工作室地皮网址(没有地皮显示None,不加前缀aerfaying.com/):"+str(jsonDict['studio']['url']))
        except:
            print("未找到变量studio/url")
        try:
            print("工作室类型:"+str(jsonDict['studio']['type']))
        except:
            print("未找到变量studio/type")
        try:
            print("官方认证过期时间(如果不是None一般是4070880000000):"+str(jsonDict['studio']['verifiedExpireTime']))
        except:
            print("未找到变量studio/verifiedExpireTime")
        try:
            print("室长ID:"+str(jsonDict['studio']['creator']['id']))
        except:
            print("未找到变量studio/creator/id")
        try:
            print("室长用户名:"+str(jsonDict['studio']['creator']['username']))
        except:
            print("未找到变量studio/creator/username")
        try:
            print("室长头像:"+str(jsonDict['studio']['creator']['thumbId']))
        except:
            print("未找到变量studio/creator/thumbID")
        try:
            print("室长前缀工作室ID:"+str(jsonDict['studio']['creator']['primaryStudio']['id']))
        except:
            print("未找到变量studio/creator/primaryStudio/id")
        try:
            print("室长前缀名称:"+str(jsonDict['studio']['creator']['primaryStudio']['shortName']))
        except:
            print("未找到变量studio/creator/primaryStudio/shortName")
        try:
            print("室长等级:"+str(jsonDict['studio']['creator']['level']))
        except:
            print("未找到变量studio/creator/level")
        try:
            print("室长管理等级:"+str(jsonDict['studio']['creator']['adminLevel']))
        except:
            print("未找到变量studio/creator/adminLevel")
        try:
            print("室长是否被ban:"+str(jsonDict['studio']['creator']['isBanned']))
        except:
            print("未找到变量studio/creator/isBanned")
        try:
            print("工作室建立时间:"+str(jsonDict['studio']['createTime']))
        except:
            print("未找到变量studio/createTime")
        try:
            print("开通积分:"+str(jsonDict['studio']['enablePoints']))
        except:
            print("未找到变量studio/enablePoints")
        try:
            print("工作室对公账户金币数量:"+str(jsonDict['studio']['goldCoins']))
        except:
            print("未找到变量studio/goldCoins")
        try:
            print("工作室隔离等级:"+str(jsonDict['studio']['isolationLevel']))
        except:
            print("未找到变量studio/isolationLevel")
        try:
            print("工作室开放等级:"+str(jsonDict['studio']['openLevel']))
        except:
            print("未找到变量studio/openLevel")
        try:
            print("是否展示成员:"+str(jsonDict['studio']['showMembers']))
        except:
            print("未找到变量studio/showMembers")
        try:
            print("需要注册:"+str(jsonDict['studio']['requireRegister']))
        except:
            print("未找到变量studio/requireRegister")
        try:
            print("需要输入安全码:"+str(jsonDict['studio']['hasSecurityCode']))
        except:
            print("未找到变量studio/hasSecurityCode")
        try:
            print("评论开放等级:"+str(jsonDict['studio']['commentOpenLevel']))
        except:
            print("未找到变量studio/commentOpenLevel")
        if showAbstract=='y' or showAbstract=='Y':
            try:
                print("工作室简介:"+str(jsonDict['studio']['descp']))
            except:
                print("未找到变量studio/descp")
        else:
            pass
    elif lx=='user':
        jsonstring=rr.getOrPost("{}","post","https://aerfaying.com/WebApi/Users/"+str(idno)+"/Get/")
        jsonDict=json.loads(jsonstring)
        try:
            print("获得了系统返回的消息:"+jsonDict['message']+"\n<Response 404>")
        except:
            pass
        try:
            print("管理等级:"+str(jsonDict['user']['adminLevel']))
        except:
            print("未找到变量user/adminLevel")
        try:
            print("禁止登陆过期时间:"+str(jsonDict['user']['bannedLoginExpireTime']))
        except:
            print("未找到变量user/bannedLoginExpireTime")
        try:
            print("比特石数量:"+str(jsonDict['user']['bitStones']))
        except:
            print("未找到变量user/bitStones")
        try:
            print("评论开放等级:"+str(jsonDict['user']['commentOpenLevel']))
        except:
            print("未找到变量user/commentOpenLevel")
        try:
            print("注册时间:"+str(jsonDict['user']['createTime']))
        except:
            print("未找到变量user/createTime")
        try:
            print("总经验点数:"+str(jsonDict['user']['expPoints']))
        except:
            print("未找到变量user/expPoints")
        try:
            print("本级已获得经验点数:"+str(jsonDict['user']['expPointsCurLevel']))
        except:
            print("未找到变量user/expPointsCurLevel")
        try:
            print("升级需要经验点数:"+str(jsonDict['user']['expPointsNextLevel']))
        except:
            print("未找到变量user/expPointsNextLevel")
        try:
            print("金币数量:"+str(jsonDict['user']['goldCoins']))
        except:
            print("未找到变量user/goldCoins")
        try:
            print("是否被ban:"+str(jsonDict['user']['isBanned']))
        except:
            print("未找到变量user/isBanned")
        try:
            print("是否是VIP:"+str(jsonDict['user']['isVip']))
        except:
            print("未找到变量user/isVip")
        try:
            print("隔离级别:"+str(jsonDict['user']['isolationLevel']))
        except:
            print("未找到变量user/isolationLevel")
        try:
            print("用户等级:"+str(jsonDict['user']['level']))
        except:
            print("未找到变量user/level")
        try:
            print("前缀工作室ID:"+str(jsonDict['user']['primaryStudio']['id']))
        except:
            print("未找到变量user/primaryStudio/id")
        try:
            print("前缀名:"+str(jsonDict['user']['primaryStudio']['shortName']))
        except:
            print("未找到变量user/primaryStudio/shortName")
        try:
            print("头像地址:"+"https://cdn.mozhua.org/media?name="+str(jsonDict['user']['thumbId'])+"/")
        except:
            print("未找到变量user/thumbId")
        try:
            print("用户名:"+str(jsonDict['user']['username']))
        except:
            print("未找到变量user/username")
        try:
            print("VIP过期时间:"+str(jsonDict['user']['vipExpireTime']))
        except:
            print("未找到变量user/vipExpireTime")
        if showAbstract=='Y' or showAbstract=='y':
            try:
                print("个人介绍:\n\n"+str(jsonDict['user']['abstract'])+"\n")
            except:
                print("未找到变量user/abstract")
