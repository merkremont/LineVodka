# -*- coding: utf-8 -*-
from LineAlpha import LineClient
from LineAlpha.LineApi import LineTracer
from LineAlpha.LineThrift.ttypes import Message
from LineAlpha.LineThrift.TalkService import Client
import time, datetime, random ,sys, re, string, os, json

reload(sys)
sys.setdefaultencoding('utf-8')

client = LineClient()
client._qrLogin("line://au/q/")

profile, setting, tracer = client.getProfile(), client.getSettings(), LineTracer(client)
offbot, messageReq, wordsArray, waitingAnswer = [], {}, {}, {}

print client._loginresult()

wait = {
    'readPoint':{},
    'readMember':{},
    'setTime':{},
    'ROM':{}
   }

setTime = {}
setTime = wait["setTime"]

def sendMessage(to, text, contentMetadata={}, contentType=0):
    mes = Message()
    mes.to, mes.from_ = to, profile.mid
    mes.text = text

    mes.contentType, mes.contentMetadata = contentType, contentMetadata
    if to not in messageReq:
        messageReq[to] = -1
    messageReq[to] += 1
    client._client.sendMessage(messageReq[to], mes)

def NOTIFIED_ADD_CONTACT(op):
    try:
        sendMessage(op.param1, client.getContact(op.param1).displayName + "謝謝加入~~ Thanks for add\n\n[戦神実験版" + datetime.datetime.today().strftime('%H:%M:%S') + "]")
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_ADD_CONTACT\n\n")
        return

tracer.addOpInterrupt(5,NOTIFIED_ADD_CONTACT)

def NOTIFIED_ACCEPT_GROUP_INVITATION(op):
    
    try:
        sendMessage(op.param1, client.getContact(op.param2).displayName + "歡迎來到 " + group.name)
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_ACCEPT_GROUP_INVITATION\n\n")
        return

tracer.addOpInterrupt(17,NOTIFIED_ACCEPT_GROUP_INVITATION)

def NOTIFIED_KICKOUT_FROM_GROUP(op):
    try:
        sendMessage(op.param1,"[戦神警告]:\n" + client.getContact(op.param3).displayName + "  已被踢出群組!\n" + "[" + datetime.datetime.today().strftime('%H:%M:%S') + "]")
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_KICKOUT_FROM_GROUP\n\n")
        return

tracer.addOpInterrupt(19,NOTIFIED_KICKOUT_FROM_GROUP)

def NOTIFIED_LEAVE_GROUP(op):
    try:
        sendMessage(op.param1,"" + client.getContact(op.param2).displayName + "  退出了...")
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_LEAVE_GROUP\n\n")
        return

tracer.addOpInterrupt(15,NOTIFIED_LEAVE_GROUP)

def NOTIFIED_READ_MESSAGE(op):
    #print op
    try:
        if op.param1 in wait['readPoint']:
            Name = client.getContact(op.param2).displayName
            if Name in wait['readMember'][op.param1]:
                pass
            else:
                wait['readMember'][op.param1] += "\n・" + Name
                wait['ROM'][op.param1][op.param2] = "・" + Name
        else:
            pass
    except:
        pass

tracer.addOpInterrupt(55, NOTIFIED_READ_MESSAGE)

def RECEIVE_MESSAGE(op):
    msg = op.message
    try:
        if msg.contentType == 0:
            try:
                if msg.to in wait['readPoint']:
                    if msg.from_ in wait["ROM"][msg.to]:
                        del wait["ROM"][msg.to][msg.from_]
                else:
                    pass
            except:
                pass
        else:
            pass
    except KeyboardInterrupt:
	       sys.exit(0)
    except Exception as error:
        print error
        print ("\n\nRECEIVE_MESSAGE\n\n")
        return

tracer.addOpInterrupt(26, RECEIVE_MESSAGE)

def SEND_MESSAGE(op):
    msg = op.message
    try:
        if msg.toType == 0:
            if msg.contentType == 0:
                if msg.text == "mid":
                    sendMessage(msg.to, msg.to)
                if msg.text == "me":
                    sendMessage(msg.to, text=None, contentMetadata={'mid': msg.from_}, contentType=13)
                if msg.text == "gift":
                    sendMessage(msg.to, text="gift sent", contentMetadata=None, contentType=9)
                else:
                    pass
            else:
                pass
        if msg.toType == 2:
            if msg.contentType == 0:
                if msg.text == "mid":
                    sendMessage(msg.to, msg.from_)
		if msg.text == "Mid":
                    sendMessage(msg.to, msg.from_)
                if msg.text == "gid":
                    sendMessage(msg.to, msg.to)
		if msg.text == "Gid":
                    sendMessage(msg.to, msg.to)
		if msg.text == "kicker":
                    sendMessage(msg.to,"Error")
		if msg.text == "Kicker":
                    sendMessage(msg.to,"Error")
		if msg.text == "作者":
                    sendMessage(msg.to,"[半垢作者]:\n 戦神:http://line.me/ti/p/4-ZKcjagH0\n\n[戦神実験版" + datetime.datetime.today().strftime('%H:%M:%S') + "]")
		if msg.text == "Author":
                    sendMessage(msg.to,"[半垢作者]:\n 戦神:http://line.me/ti/p/4-ZKcjagH0\n\n[戦神実験版" + datetime.datetime.today().strftime('%H:%M:%S') + "]")
		if msg.text == "作成者":
                    sendMessage(msg.to,"[半垢作者]:\n 戦神:http://line.me/ti/p/4-ZKcjagH0\n\n[戦神実験版" + datetime.datetime.today().strftime('%H:%M:%S') + "]")
		if msg.text == "author":
                    sendMessage(msg.to,"[半垢作者]:\n 戦神:http://line.me/ti/p/4-ZKcjagH0\n\n[戦神実験版" + datetime.datetime.today().strftime('%H:%M:%S') + "]")
		if msg.text == "Ps":
                    sendMessage(msg.to,"戦神実験版-注意事項\n\n1. 禁止在副本or私訊發出指令\n2.打完指令若沒反應,請耐心等待,禁止不斷輸入指令\n3.10人以下群組會造成機器不穩定\n4.當伺服器不穩,機器也會不穩,請見諒\n\n仍有疑問請詢問作者\n戦神:http://line.me/ti/p/4-ZKcjagH0\n\n[戦神実験版" + datetime.datetime.today().strftime('%H:%M:%S') + "]")
		if msg.text == "ps":
                    sendMessage(msg.to,"戦神実験版-注意事項\n\n1. 禁止在副本or私訊發出指令\n2.打完指令若沒反應,請耐心等待,禁止不斷輸入指令\n3.10人以下群組會造成機器不穩定\n4.當伺服器不穩,機器也會不穩,請見諒\n\n仍有疑問請詢問作者\n戦神:http://line.me/ti/p/4-ZKcjagH0\n\n[戦神実験版" + datetime.datetime.today().strftime('%H:%M:%S') + "]")
		if msg.text == "Ver":
                    sendMessage(msg.to,"戦神実験版\n\n[版本version]\n実験版ver.3.7.1\n\n[版本詳情]\n実験版\n 3.1.0\n   基本指令\n 3.2.0\n   增加邀請系統\n 3.3.0\n   修改細部回覆內容\n 3.4.0\n   增加Nk功效\n   增加bot指令\n 3.5.0\n   增加kicker指令\n   增加help指令\n   增加指令下達時間顯示\n   指令支援大小寫\n   增加隱藏指令\n 3.6.0\n   增加ps指令\n 3.7.0\n   更改退群回覆\n   更改Nk後回覆\n\n[戦神実験版" + datetime.datetime.today().strftime('%H:%M:%S') + "]")
		if msg.text == "ver":
                    sendMessage(msg.to,"戦神実験版\n\n[版本version]\n実験版ver.3.7.1\n\n[版本詳情]\n実験版\n 3.1.0\n   基本指令\n 3.2.0\n   增加邀請系統\n 3.3.0\n   修改細部回覆內容\n 3.4.0\n   增加Nk功效\n   增加bot指令\n 3.5.0\n   增加kicker指令\n   增加help指令\n   增加指令下達時間顯示\n   指令支援大小寫\n   增加隱藏指令\n 3.6.0\n   增加ps指令\n 3.7.0\n   更改退群回覆\n   更改Nk後回覆\n\n[戦神実験版" + datetime.datetime.today().strftime('%H:%M:%S') + "]")
                if msg.text == "ginfo":
                    group = client.getGroup(msg.to)
                    md = "戦神実験版-群組詳情\n\n" + "[群組名稱]\n" + group.name + "\n\n[gid]\n" + group.id + "\n\n[群組照片]\nhttp://dl.profile.line-cdn.net/" + group.pictureStatus
                    if group.preventJoinByTicket is False: md += "\n\n群組URL: 開啟中\n"
                    else: md += "\n\n群組URL: 關閉中\n"
                    if group.invitee is None: md += "\n成員人數: " + str(len(group.members)) + "人\n\n招待中: 0人"
                    else: md += "\n成員人數: " + str(len(group.members)) + "人\n招待中: " + str(len(group.invitee)) + "人\n\n" + datetime.datetime.today().strftime('%H:%M:%S') + "]"
                    sendMessage(msg.to,md)
		if msg.text == "Ginfo":
                    group = client.getGroup(msg.to)
                    md = "戦神実験版-群組詳情\n\n" + "[群組名稱]\n" + group.name + "\n\n[gid]\n" + group.id + "\n\n[群組照片]\nhttp://dl.profile.line-cdn.net/" + group.pictureStatus
                    if group.preventJoinByTicket is False: md += "\n\n群組URL: 開啟中\n"
                    else: md += "\n\n群組URL: 關閉中\n"
                    if group.invitee is None: md += "\n成員人數: " + str(len(group.members)) + "人\n\n招待中: 0人"
                    else: md += "\n成員人數: " + str(len(group.members)) + "人\n招待中: " + str(len(group.invitee)) + "人\n\n" + datetime.datetime.today().strftime('%H:%M:%S') + "]"
                    sendMessage(msg.to,md)
		if msg.text == "help":
                    sendMessage(msg.to,"戦神実験版Ver.3.7.1-help\n\n[help] 查看指令\n[ver] 查看版本\n[ps] 重要注意事項!\n[author] 此半垢作者連結\n[mid] 查看自己mid\n" + "[gid] 查看群組gid\n" + "[me︎] 送出自己的友資\n[ginfo] 查看群組詳細資料\n" + "[url] 取得群組網址\n[urlon] 開啟群組網址\n[urloff] 關閉群組網址\n[invite:] 利用mid邀請\n[kick:] 利用mid踢人\n" + 
				"[Nk:] 利用名字踢人(完整用戶名稱)\n" + "[cancel] 取消全部邀請\n[bot] 追加保護\n[kicker] 查看追加保護狀態\n[show:] 顯示mid友資\n[set] 設定已讀點\n[read] 顯示已讀用戶\n[time] 顯示現在時間\n[gift] 發送禮物\n\n\n[戦神実験版" + datetime.datetime.today().strftime('%H:%M:%S') + "]")
                if msg.text == "Help":
                    sendMessage(msg.to,"戦神実験版Ver.3.7.1-help\n\n[help] 查看指令\n[ver] 查看版本\n[ps] 重要注意事項!\n[author] 此半垢作者連結\n[mid] 查看自己mid\n" + "[gid] 查看群組gid\n" + "[me︎] 送出自己的友資\n[ginfo] 查看群組詳細資料\n" + "[url] 取得群組網址\n[urlon] 開啟群組網址\n[urloff] 關閉群組網址\n[invite:] 利用mid邀請\n[kick:] 利用mid踢人\n" + 
				"[Nk:] 利用名字踢人(完整用戶名稱)\n" + "[cancel] 取消全部邀請\n[bot] 追加保護\n[kicker] 查看追加保護狀態\n[show:] 顯示mid友資\n[set] 設定已讀點\n[read] 顯示已讀用戶\n[time] 顯示現在時間\n[gift] 發送禮物\n\n\n[戦神実験版" + datetime.datetime.today().strftime('%H:%M:%S') + "]")
		if "gname:" in msg.text:
                    key = msg.text[22:]
                    group = client.getGroup(msg.to)
                    group.name = key
                    client.updateGroup(group)
                    sendMessage(msg.to,"Group Name"+key+"Canged to")
                if msg.text == "url":
                    sendMessage(msg.to,"此群網址URL")
                    sendMessage(msg.to,"line://ti/g/" + client._client.reissueGroupTicket(msg.to) + "\n\n[戦神実験版" + datetime.datetime.today().strftime('%H:%M:%S') + "]")
		if msg.text == "Url":
                    sendMessage(msg.to,"此群網址URL")
                    sendMessage(msg.to,"line://ti/g/" + client._client.reissueGroupTicket(msg.to) + "\n\n[戦神実験版" + datetime.datetime.today().strftime('%H:%M:%S') + "]")
                if msg.text == "urlon":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == False:
                        sendMessage(msg.to, "URL 已開啟")
                    else:
                        group.preventJoinByTicket = False
                        client.updateGroup(group)
                        sendMessage(msg.to, "URL 已開啟")
		if msg.text == "Urlon":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == False:
                        sendMessage(msg.to, "URL 已開啟")
                    else:
                        group.preventJoinByTicket = False
                        client.updateGroup(group)
                        sendMessage(msg.to, "URL 已開啟")
                if msg.text == "urloff":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == True:
                        sendMessage(msg.to, "URL 已關閉")
                    else:
                        group.preventJoinByTicket = True
                        client.updateGroup(group)
                        sendMessage(msg.to, "URL 已關閉")
		if msg.text == "Urloff":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == True:
                        sendMessage(msg.to, "URL 已關閉")
                    else:
                        group.preventJoinByTicket = True
                        client.updateGroup(group)
                        sendMessage(msg.to, "URL 已關閉")
                if "kick:" in msg.text:
                    key = msg.text[5:]
                    client.kickoutFromGroup(msg.to, [key])
                    contact = client.getContact(key)
                    sendMessage(msg.to, ""+contact.displayName+"掰掰囉(づ￣ ³￣)づ\n" + "[戦神実験版" + datetime.datetime.today().strftime('%H:%M:%S') + "]")
                if "Nk:" in msg.text:
                    key = msg.text[3:]
                    group = client.getGroup(msg.to)
                    Names = [contact.displayName for contact in group.members]
                    Mids = [contact.mid for contact in group.members]
                    if key in Names:
                        kazu = Names.index(key)
			contact = client.getContact(Mids[kazu])
                        sendMessage(msg.to,contact.displayName + "掰掰拉^^\n" + "[戦神実験版" + datetime.datetime.today().strftime('%H:%M:%S') + "]")
                        client.kickoutFromGroup(msg.to, [""+Mids[kazu]+""])
                        contact = client.getContact(Mids[kazu])
                        sendMessage(msg.to, ""+contact.displayName+" 被我踢出了 嘿嘿")
                    else:
                        sendMessage(msg.to, "戦神找不到這位成員><\n" + "[戦神実験版" + datetime.datetime.today().strftime('%H:%M:%S') + "]")
		if "nk:" in msg.text:
                    key = msg.text[3:]
                    group = client.getGroup(msg.to)
                    Names = [contact.displayName for contact in group.members]
                    Mids = [contact.mid for contact in group.members]
                    if key in Names:
                        kazu = Names.index(key)
			contact = client.getContact(Mids[kazu])
                        sendMessage(msg.to,contact.displayName + "掰掰拉^^\n" + "[戦神実験版" + datetime.datetime.today().strftime('%H:%M:%S') + "]")
                        client.kickoutFromGroup(msg.to, [""+Mids[kazu]+""])
                        contact = client.getContact(Mids[kazu])
                        sendMessage(msg.to, ""+contact.displayName+" 被我踢出了 嘿嘿")
                    else:
                        sendMessage(msg.to, "戦神找不到這位成員><\n" + "[戦神実験版" + datetime.datetime.today().strftime('%H:%M:%S') + "]")
                if msg.text == "cancel":
                    group = client.getGroup(msg.to)
                    if group.invitee is None:
                        sendMessage(op.message.to, "戦神發現...招待中沒人><\n" + "[戦神実験版" + datetime.datetime.today().strftime('%H:%M:%S') + "]")
                    else:
                        gInviMids = [contact.mid for contact in group.invitee]
                        client.cancelGroupInvitation(msg.to, gInviMids)
                        sendMessage(msg.to, str(len(group.invitee)) + "人 已被戦神取消(´∀｀)♡\n" + "[戦神実験版" + datetime.datetime.today().strftime('%H:%M:%S') + "]")
		if msg.text == "c":
                    group = client.getGroup(msg.to)
                    if group.invitee is None:
                        sendMessage(op.message.to, "戦神發現...招待中沒人><\n" + "[戦神実験版" + datetime.datetime.today().strftime('%H:%M:%S') + "]")
                    else:
                        gInviMids = [contact.mid for contact in group.invitee]
                        client.cancelGroupInvitation(msg.to, gInviMids)
                        sendMessage(msg.to, str(len(group.invitee)) + "人 已被戦神取消(´∀｀)♡\n" + "[戦神実験版" + datetime.datetime.today().strftime('%H:%M:%S') + "]")
		if msg.text == "Cancel":
                    group = client.getGroup(msg.to)
                    if group.invitee is None:
                        sendMessage(op.message.to, "戦神發現...招待中沒人><\n" + "[戦神実験版" + datetime.datetime.today().strftime('%H:%M:%S') + "]")
                    else:
                        gInviMids = [contact.mid for contact in group.invitee]
                        client.cancelGroupInvitation(msg.to, gInviMids)
                        sendMessage(msg.to, str(len(group.invitee)) + "人 已被戦神取消(´∀｀)♡\n" + "[戦神実験版" + datetime.datetime.today().strftime('%H:%M:%S') + "]")
		if msg.text == "C":
                    group = client.getGroup(msg.to)
                    if group.invitee is None:
                        sendMessage(op.message.to, "戦神發現...招待中沒人><\n" + "[戦神実験版" + datetime.datetime.today().strftime('%H:%M:%S') + "]")
                    else:
                        gInviMids = [contact.mid for contact in group.invitee]
                        client.cancelGroupInvitation(msg.to, gInviMids)
                        sendMessage(msg.to, str(len(group.invitee)) + "人 已被戦神取消(´∀｀)♡\n" + "[戦神実験版" + datetime.datetime.today().strftime('%H:%M:%S') + "]")
                if "invite:" in msg.text:
                    key = msg.text[-33:]
                    client.findAndAddContactsByMid(key)
                    client.inviteIntoGroup(msg.to, [key])
                    contact = client.getContact(key)
                    sendMessage(msg.to, ""+contact.displayName+" 已被招待\n" + "[戦神実験版" + datetime.datetime.today().strftime('%H:%M:%S') + "]")
                if msg.text == "me":
                    M = Message()
                    M.to = msg.to
                    M.contentType = 13
                    M.contentMetadata = {'mid': msg.from_}
                    contact = client.getContact(key)
		    client.sendMessage(M)
		    sendMessage(msg.to, "[名字]\n" + contact.displayName + "")
                if "show:" in msg.text:
                    key = msg.text[-33:]
                    sendMessage(msg.to, text=None, contentMetadata={'mid': key}, contentType=13)
                    contact = client.getContact(key)
                    sendMessage(msg.to, "這是 "+contact.displayName+" 的友資")
                if msg.text == "time":
                    sendMessage(msg.to, "戦神実験版[" + datetime.datetime.today().strftime('%Y年%m月%d日 %H:%M:%S') + "]")
                if msg.text == "gift":
                    sendMessage(msg.to, text="gift sent", contentMetadata=None, contentType=9)
		if msg.text == "Gift":
                    sendMessage(msg.to, text="gift sent", contentMetadata=None, contentType=9)
                if msg.text == "set":
                    sendMessage(msg.to, "已抓已讀點♪\n\n" + "[戦神" + datetime.datetime.today().strftime('%Y年%m月%d日 %H:%M:%S') + "]")
                    try:
                        del wait['readPoint'][msg.to]
                        del wait['readMember'][msg.to]
                    except:
                        pass
                    wait['readPoint'][msg.to] = msg.id
                    wait['readMember'][msg.to] = ""
                    wait['setTime'][msg.to] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                    wait['ROM'][msg.to] = {}
                    print wait
		if msg.text == "Set":
                    sendMessage(msg.to, "已抓已讀點♪\n\n" + "[戦神" + datetime.datetime.today().strftime('%Y年%m月%d日 %H:%M:%S') + "]")
                    try:
                        del wait['readPoint'][msg.to]
                        del wait['readMember'][msg.to]
                    except:
                        pass
                    wait['readPoint'][msg.to] = msg.id
                    wait['readMember'][msg.to] = ""
                    wait['setTime'][msg.to] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                    wait['ROM'][msg.to] = {}
                    print wait
                if msg.text == "read":
                    if msg.to in wait['readPoint']:
                        if wait["ROM"][msg.to].items() == []:
                            chiya = ""
                        else:
                            chiya = ""
                            for rom in wait["ROM"][msg.to].items():
                                print rom
                                chiya += rom[1] + "\n"

                        sendMessage(msg.to, "戦神実験版-已讀詳情\n" + "已讀的人: %s\n\n已讀不回的人:\n%s >< ♪\n\n抓已讀點的時間:\n[%s]"  % (wait['readMember'][msg.to],chiya,setTime[msg.to]))
                    else:
                        sendMessage(msg.to, "還沒抓已讀點喔♪")
		if msg.text == "Read":
                    if msg.to in wait['readPoint']:
                        if wait["ROM"][msg.to].items() == []:
                            chiya = ""
                        else:
                            chiya = ""
                            for rom in wait["ROM"][msg.to].items():
                                print rom
                                chiya += rom[1] + "\n"

                        sendMessage(msg.to, "戦神実験版-已讀詳情\n" + "已讀的人: %s\n\n已讀不回的人:\n%s >< ♪\n\n抓已讀點的時間:\n[%s]"  % (wait['readMember'][msg.to],chiya,setTime[msg.to]))
                    else:
                        sendMessage(msg.to, "還沒抓已讀點喔♪")
                else:
                    pass
        else:
            pass

    except Exception as e:
        print e
        print ("\n\nSEND_MESSAGE\n\n")
        return

tracer.addOpInterrupt(25,SEND_MESSAGE)

while True:
    tracer.execute()
