# -*- coding: utf-8 -*-
from models.Biliapi import BiliWebApi
from models.PushMessage import PushMessage
import json, time
import logging

def bili_exp(cookieData, pm):
   "B站直播签到，投币分享获取经验，模拟观看一个视频"
   try:
       biliapi = BiliWebApi(cookieData)
   except Exception as e: 
       logging.info(f'登录验证id为{cookieData["DedeUserID"]}的账户失败，原因为({str(e)})，跳过此账户后续所有操作')
       pm.addMsg(f'id为：{cookieData["DedeUserID"]} 的账户登录失败')
       return

   pm.addMsg(f'目前账户为：({biliapi.getUserName()})')
   logging.info(f'登录账户 ({biliapi.getUserName()}) 成功')

   rdata = {
       "直播签到": False,
       "投币数量": 0,
       "视频观看": False,
       "视频分享": False,
       "脚本执行前经验": 0,
       "脚本执行前硬币": 0,
       }

   try:
       if biliapi.vipPrivilegeReceive(1)["code"] == 0:
           rdata["领取大会员B币"] = True
       if biliapi.vipPrivilegeReceive(2)["code"] == 0:
           rdata["领取会员购优惠券"] = True
   except:
       pass

   try:
       xliveInfo = biliapi.xliveSign()
       logging.info(f'bilibili直播签到信息：{str(xliveInfo)}')
       rdata["直播签到"] = (xliveInfo["code"] == 0)
   except Exception as e:
       logging.warning(f'直播签到异常，原因为{str(e)}')

   try:
        room_id = biliapi.xliveGetRecommendList()["data"]["list"][6]["roomid"]
        uid = biliapi.xliveGetRoomInfo(room_id)["data"]["room_info"]["uid"]
        now_time = int(time.time())
        bagList = biliapi.xliveGiftBagList()["data"]["list"]
        for x in bagList:
            if x["expire_at"] - now_time < 172800: #礼物到期时间小于2天
                ret = biliapi.xliveBagSend(room_id, uid, x["bag_id"], x["gift_id"], x["gift_num"])
                if ret["code"] == 0:
                    logging.info(f'{ret["data"]["send_tips"]} {ret["data"]["gift_name"]} 数量{ret["data"]["gift_num"]}')
   except Exception as e:
       logging.warning(f'直播送出即将过期礼物异常，原因为{str(e)}')

   try:
       reward = biliapi.getReward()
       logging.info(f'经验脚本开始前经验信息 ：{str(reward)}')
   except Exception as e: 
       logging.warning(f'获取账户经验信息异常，原因为{str(e)}，跳过此账户后续所有操作')
       pm.addMsg(str(rdata))
       return

   rdata["脚本执行前经验"] = reward["level_info"]["current_exp"]

   try:
       coin_num = biliapi.getCoin()
   except Exception as e: 
       logging.warning(f'获取账户剩余硬币数异常，原因为{str(e)}')
       coin_num = 0

   rdata["脚本执行前硬币"] = coin_num

   coin_exp_num = (50 - reward["coins_av"]) // 10
   toubi_num = coin_exp_num if coin_num > coin_exp_num else coin_num

   try:
       datas = biliapi.getRegions()
   except Exception as e: 
       logging.warning(f'获取B站分区视频信息异常，原因为{str(e)}，跳过此账户后续所有操作')
       pm.addMsg(str(rdata))
       return

   if(toubi_num > 0):
       for i in range(toubi_num):
           try:
               info = biliapi.coin(datas[i]["aid"], 1, 1)
               logging.info(f'投币信息 ：{str(info)}')
               if(info["code"] == 0):
                   rdata["投币数量"] += 1
           except Exception as e: 
               logging.warning(f'投币异常，原因为{str(e)}')

   try:
       info = biliapi.report(datas[5]["aid"], datas[5]["cid"], 300)
       logging.info(f'模拟视频观看进度上报：{str(info)}')
       rdata["视频观看"] = (info["code"] == 0)
   except Exception as e: 
       logging.warning(f'模拟视频观看异常，原因为{str(e)}')

   try:
       info = biliapi.share(datas[5]["aid"])
       logging.info(f'分享视频结果：{str(info)}')
       rdata["视频分享"] = (info["code"] == 0)
   except Exception as e: 
       logging.warning(f'分享视频异常，原因为{str(e)}')

   pm.addMsg(str(rdata))
   logging.info('本账户操作全部完成')

def main(*args):
    try:
        logging.basicConfig(filename="exp.log", filemode='a', level=logging.INFO, format="%(asctime)s: %(levelname)s, %(message)s", datefmt="%Y/%d/%m %H:%M:%S")
    except:
        pass

    with open('config.json','r',encoding='utf-8') as fp:
        configData = json.load(fp)

    pm = PushMessage(title="B站经验脚本消息推送", email=configData["email"])

    for x in configData["cookieDatas"]:
        bili_exp(x, pm)

    try:
        pm.pushMessage()
    except Exception as e: 
        logging.warning(f'消息推送异常，原因为{str(e)}')

if __name__=="__main__":
    main()
