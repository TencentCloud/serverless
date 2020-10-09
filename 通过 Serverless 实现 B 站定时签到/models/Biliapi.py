# -*- coding: utf-8 -*-
import requests
import json
class BiliWebApi(object):
    "B站web的api接口"
    def __init__(self, cookieData=None):
        #创建session
        self.__session = requests.session()
        #设置header
        self.__session.headers.update({"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/63.0.3239.108","Referer": "https://www.bilibili.com/",'Connection': 'keep-alive'})
        if cookieData == None:
            return

        #添加cookie
        requests.utils.add_dict_to_cookiejar(self.__session.cookies, cookieData)
        if 'bili_jct' in cookieData:
            self.__bili_jct = cookieData["bili_jct"]
        else:
            self.__bili_jct = ''
        #self.__uid = cookieData["DedeUserID"]

        data = self.__session.get("https://api.bilibili.com/x/web-interface/nav").json()
        if data["code"] != 0:
            raise Exception("参数验证失败，登录状态失效")
        self.__name = data["data"]["uname"]
        self.__uid = data["data"]["mid"]
        #print(self.__session.cookies)

    def getUserName(self):
        "获取登录的账户用户名"
        return self.__name

    def getReward(self):
        "取B站经验信息"
        url = "https://account.bilibili.com/home/reward"
        return self.__session.get(url).json()["data"]

    def getWebNav(self):
        "取导航信息"
        url = "https://api.bilibili.com/x/web-interface/nav"
        return self.__session.get(url).json()["data"]

    @staticmethod
    def getId(url):
        "取B站指定视频链接的aid和cid号"
        import re
        content = requests.get(url, headers=Biliapi.__headers)
        match = re.search( 'https:\/\/www.bilibili.com\/video\/av(.*?)\/\">', content.text, 0)
        aid = match.group(1)
        match = re.search( '\"cid\":(.*?),', content.text, 0)
        cid = match.group(1)
        return {"aid": aid, "cid": cid}

    def getCoin(self):
        "获取剩余硬币数"
        url = "https://api.bilibili.com/x/web-interface/nav?build=0&mobi_app=web"
        return int(self.__session.get(url).json()["data"]["money"])

    def coin(self, aid, num, select_like):
        "给指定av号视频投币"
        url = "https://api.bilibili.com/x/web-interface/coin/add"
        post_data = {
            "aid": aid,
            "multiply": num,
            "select_like": select_like,
            "cross_domain": "true",
            "csrf": self.__bili_jct
            }
        return self.__session.post(url, post_data).json()

    def share(self, aid):
        "分享指定av号视频"
        url = "https://api.bilibili.com/x/web-interface/share/add"
        post_data = {
            "aid": aid,
            "csrf": self.__bili_jct
            }
        return self.__session.post(url, post_data).json()

    def report(self, aid, cid, progres):
        "B站上报观看进度"
        url = "http://api.bilibili.com/x/v2/history/report"
        post_data = {
            "aid": aid,
            "cid": cid,
            "progres": progres,
            "csrf": self.__bili_jct
            }
        return self.__session.post(url, post_data).json()

    def getHomePageUrls(self):
        "取B站首页推荐视频地址列表"
        import re
        url = "https://www.bilibili.com"
        content = self.__session.get(url)
        match = re.findall( '<div class=\"info-box\"><a href=\"(.*?)\" target=\"_blank\">', content.text, 0)
        match = ["https:" + x for x in match]
        return match

    @staticmethod
    def getRegions(rid=1, num=6):
        "获取B站分区视频信息"
        url = "https://api.bilibili.com/x/web-interface/dynamic/region?ps=" + str(num) + "&rid=" + str(rid)
        datas = requests.get(url).json()["data"]["archives"]
        ids = []
        for x in datas:
            ids.append({"title": x["title"], "aid": x["aid"], "bvid": x["bvid"], "cid": x["cid"]})
        return ids

    @staticmethod
    def getRankings(rid=1, day=3):
        "获取B站分区排行榜视频信息"
        url = "https://api.bilibili.com/x/web-interface/ranking?rid=" + str(rid) + "&day=" + str(day)
        datas = requests.get(url).json()["data"]["list"]
        ids = []
        for x in datas:
            ids.append({"title": x["title"], "aid": x["aid"], "bvid": x["bvid"], "cid": x["cid"], "coins": x["coins"], "play": x["play"]})
        return ids

    def repost(self, dynamic_id, content="", extension='{"emoji_type":1}'):
        "转发B站动态"
        url = "https://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/repost"
        post_data = {
            "uid": self.__uid,
            "dynamic_id": dynamic_id,
            "content": content,
            "extension": extension,
            #"at_uids": "",
            #"ctrl": "[]",
            "csrf_token": self.__bili_jct
            }
        return self.__session.post(url, post_data).json()

    def dynamicRepostReply(self, rid, content="", type=1, repost_code=3000, From="create.comment", extension='{"emoji_type":1}'):
        "评论动态并转发"
        url = "https://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/reply"
        post_data = {
            "uid": self.__uid,
            "rid": rid,
            "type": type,
            "content": content,
            "extension": extension,
            "repost_code": repost_code,
            "from": From,
            "csrf_token": self.__bili_jct
            }
        return self.__session.post(url, post_data).json()

    def followed(self, followid: 'up的uid', isfollow=True):
        "关注或取关up主"
        url = "https://api.vc.bilibili.com/feed/v1/feed/SetUserFollow"
        post_data = {
            "type": 1 if isfollow else 0,
            "follow": followid,
            "csrf_token": self.__bili_jct
            }
        return self.__session.post(url, post_data).json()

    def followedModify(self, followid: 'up的uid', act=1, re_src=11):
        "改变关注状态(增加、删除关注的up)"
        url = "https://api.bilibili.com/x/relation/modify"
        post_data = {
            "fid": followid,
            "act": act,
            "re_src": re_src,
            "csrf": self.__bili_jct
            }
        return self.__session.post(url, post_data).json()

    def groupAddFollowed(self, followid: 'up的uid', tagids=0):
        "移动关注的up主的分组"
        url = "https://api.bilibili.com/x/relation/tags/addUsers?cross_domain=true"
        post_data = {
            "fids": followid,
            "tagids": tagids, #默认是0，特别关注是-10
            "csrf": self.__bili_jct
            }
        return self.__session.post(url, post_data).json()

    def getFollowing(self, uid=0, pn=1, ps=50, order='desc'):
        "获取指定账户的关注者(默认取本账户)"
        if uid == 0:
            uid = self.__uid
        url = f"https://api.bilibili.com/x/relation/followings?vmid={uid}&pn={pn}&ps={ps}&order={order}"
        return self.__session.get(url).json()

    def getTopicInfo(self, tag_name):
        "取B站话题信息"
        url = f'https://api.bilibili.com/x/tag/info?tag_name={tag_name}'
        return self.__session.get(url).json()

    def getTopicList(self, tag_name):
        "取B站话题列表，返回一个可迭代对象"
        topic_id = self.getTopicInfo(tag_name)["data"]["tag_id"]
        url = f'https://api.vc.bilibili.com/topic_svr/v1/topic_svr/topic_new?topic_id={topic_id}'
        jsobj = self.__session.get(url).json()
        cards = jsobj["data"]["cards"]
        for x in cards:
            yield x
        has_more = (jsobj["data"]["has_more"] == 1)
        while has_more:
            offset = jsobj["data"]["offset"]
            jsobj = self.__session.get(f'https://api.vc.bilibili.com/topic_svr/v1/topic_svr/topic_history?topic_name={tag_name}&offset_dynamic_id={offset}').json()
            if not 'cards' in jsobj["data"]:
                break
            cards = jsobj["data"]["cards"]
            for x in cards:
                yield x
            has_more = (jsobj["data"]["has_more"] == 1)

    def getDynamicNew(self, type_list='268435455'):
        "取B站用户最新动态数据"
        url = f'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/dynamic_new?uid={self.__uid}&type_list={type_list}'
        content = self.__session.get(url)
        content.encoding = 'utf-8' #需要指定编码
        return json.loads(content.text)

    def getDynamic(self, uid=0, type_list='268435455'):
        "取B站用户动态数据，生成器"
        if not uid:
            uid = self.__uid
        url = f'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/dynamic_new?uid={uid}&type_list={type_list}'
        content = self.__session.get(url)
        content.encoding = 'utf-8' #需要指定编码
        jsobj = json.loads(content.text)
        cards = jsobj["data"]["cards"]
        for x in cards:
            yield x
        hasnext = True
        offset = cards[len(cards) - 1]["desc"]["dynamic_id"]
        while hasnext:
            content = self.__session.get(f'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/dynamic_history?uid={uid}&offset_dynamic_id={offset}&type={type_list}')
            content.encoding = 'utf-8'
            jsobj = json.loads(content.text)
            hasnext = (jsobj["data"]["has_more"] == 1)
            #offset = jsobj["data"]["next_offset"]
            cards = jsobj["data"]["cards"]
            for x in cards:
                yield x
            offset = cards[len(cards) - 1]["desc"]["dynamic_id"]

    def getMyDynamic(self, uid=0):
        "取B站用户自己的动态列表，生成器"
        import time
        def retry_get(url):
            times = 3
            while times:
                try:
                    jsobj = self.__session.get(url).json()
                    assert jsobj["code"] == 0
                    return jsobj
                except:
                    times -= 1
                    time.sleep(3)
            raise Exception(str(jsobj))

        if uid == 0:
            uid = self.__uid
        url = f'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid={uid}&need_top=1&offset_dynamic_id='
        hasnext = True
        offset = ''
        while hasnext:
            jsobj = retry_get(f'{url}{offset}')
            hasnext = (jsobj["data"]["has_more"] == 1)
            if not 'cards' in jsobj["data"]:
                continue
            cards = jsobj["data"]["cards"]
            for x in cards:
                yield x
            offset = x["desc"]["dynamic_id_str"]

    def removeDynamic(self, dynamic_id: int):
        "删除自己的动态"
        url = f'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/rm_dynamic'
        post_data = {
            "dynamic_id": dynamic_id,
            "csrf_token": self.__bili_jct
            }
        return self.__session.post(url, post_data).json()

    def getLotteryNotice(self, dynamic_id: int):
        "取指定抽奖信息"
        url = f'https://api.vc.bilibili.com/lottery_svr/v1/lottery_svr/lottery_notice?dynamic_id={dynamic_id}'
        content = self.__session.get(url)
        content.encoding = 'utf-8'#不指定会出错
        return json.loads(content.text)

    def xliveSign(self):
        "B站直播签到"
        url = "https://api.live.bilibili.com/xlive/web-ucenter/v1/sign/DoSign"
        return self.__session.get(url).json()

    def xliveGetStatus(self):
        "B站直播获取金银瓜子状态"
        url = "https://api.live.bilibili.com/pay/v1/Exchange/getStatus"
        return self.__session.get(url).json()

    def silver2coin(self):
        "银瓜子兑换硬币"
        url = "https://api.live.bilibili.com/pay/v1/Exchange/silver2coin"
        post_data = {
            "csrf_token": self.__bili_jct
            }
        return self.__session.post(url, post_data).json()

    def createArticle(self, tilte="", content="", aid=0, category=0, list_id=0, tid=4, original=1, image_urls="", origin_image_urls="", submit=False):
        "发表专栏"
        post_data = {
            "title": tilte,
            "content": content,
            "category": category,#专栏分类,0为默认
            "list_id": list_id,#文集编号，默认0不添加到文集
            "tid": 4, #4为专栏封面单图,3为专栏封面三图
            "reprint": 0,
            "media_id": 0,
            "spoiler": 0,
            "original": original,
            "csrf": self.__bili_jct
            }
        url = 'https://api.bilibili.com/x/article/creative/draft/addupdate'#编辑地址,发表前可以通过这个来编辑草稿,没打草稿不允许发表
        if aid:
            post_data["aid"] = aid
            if submit:
                url = 'https://api.bilibili.com/x/article/creative/article/submit'#正式发表地址
        if origin_image_urls and image_urls:
            post_data["origin_image_urls"] = origin_image_urls
            post_data["image_urls"] = image_urls
        return self.__session.post(url, post_data).json()

    def deleteArticle(self, aid: int):
        "删除专栏"
        url = 'https://member.bilibili.com/x/web/draft/delete'
        post_data = {
            "aid": aid,
            "csrf": self.__bili_jct
            }
        return self.__session.post(url, post_data).json()

    def getArticle(self, aid: int):
        "获取专栏内容"
        url = f'https://api.bilibili.com/x/article/creative/draft/view?aid={aid}'
        return self.__session.get(url).json()

    def articleUpcover(self, file):
        "上传本地图片,返回链接"
        url = 'https://api.bilibili.com/x/article/creative/article/upcover'
        files = {
            'binary':(file)
            }
        post_data = {
            "csrf": self.__bili_jct
            }
        return self.__session.post(url, post_data, files=files, timeout=(5, 60)).json()

    def articleCardsBvid(self, bvid: 'str 加上BV前缀'):
        "根据bv号获取视频信息，在专栏引用视频时使用"
        url = f'https://api.bilibili.com/x/article/cards?ids={bvid}&cross_domain=true'
        return self.__session.get(url).json()

    def articleCardsCvid(self, cvid: 'str 加上cv前缀'):
        "根据cv号获取专栏，在专栏引用其他专栏时使用"
        url = f'https://api.bilibili.com/x/article/cards?id={cvid}&cross_domain=true'
        return self.__session.get(url).json()

    def articleCardsId(self, epid: 'str 加上ep前缀'):
        "根据ep号获取番剧信息，在专栏引用站内番剧时使用"
        return self.articleCardsCvid(epid)

    def articleCardsAu(self, auid: 'str 加上au前缀'):
        "根据au号获取音乐信息，在专栏引用站内音乐时使用"
        return self.articleCardsCvid(auid)

    def articleCardsPw(self, pwid: 'str 加上pw前缀'):
        "根据au号获取会员购信息，在专栏引用会员购时使用"
        return self.articleCardsCvid(pwid)

    def articleMangas(self, mcid: 'int 不加mc前缀'):
        "根据mc号获取漫画信息，在专栏引用站内漫画时使用"
        url = f'https://api.bilibili.com/x/article/mangas?id={mcid}&cross_domain=true'
        return self.__session.get(url).json()

    def articleCardsLv(self, lvid: 'str 加上lv前缀'):
        "根据lv号获取直播信息，在专栏引用站内直播时使用"
        return self.articleCardsCvid(lvid)

    def articleCreateVote(self, vote):
        "创建一个投票"
        '''
        vote = {
            "title": "投票标题",
            "desc": "投票说明",
            "type": 0, #0为文字投票，1为图片投票
            "duration": 604800,#投票时长秒,604800为一个星期
            "options":[
                {
                    "desc": "选项1",
                    "cnt": 0,#不知道什么意思
                    "idx": 1, #选项序号，第一个选项为1
                    #"img_url": "http://i0.hdslb.com/bfs/album/d74e83cf96a9028eb3e280d5f877dce53760a7e2.jpg",#仅图片投票需要
                },
                {
                    "desc": "选项2",
                    "cnt": 0,
                    "idx": 2, #选项序号，第二个选项为2
                    #"img_url": ""
                }
                ]
            }
        '''
        post_data = {
            "info": vote,
            "csrf": self.__bili_jct
            }
        return self.__session.post(url, post_data).json()

    def videoPreupload(self, filename, filesize):
        "申请上传，返回上传信息"
        from urllib.parse import quote
        name = quote(filename)
        url = f'https://member.bilibili.com/preupload?name={name}&size={filesize}&r=upos&profile=ugcupos%2Fbup&ssl=0&version=2.8.9&build=2080900&upcdn=bda2&probe_version=20200628'
        return self.__session.get(url).json()

    def videoUploadId(self, url, auth):
        "向上传地址申请上传，得到上传id等信息"
        return self.__session.post(f'{url}?uploads&output=json', headers={"X-Upos-Auth": auth}).json()

    def videoUpload(self, url, auth, upload_id, data, chunk, chunks, start, total):
        "上传视频分块"
        size = len(data)
        end = start + size
        content = self.__session.put(f'{url}?partNumber={chunk+1}&uploadId={upload_id}&chunk={chunk}&chunks={chunks}&size={size}&start={start}&end={end}&total={total}', data=data, headers={"X-Upos-Auth": auth})
        return True if content.text == "MULTIPART_PUT_SUCCESS" else False

    def videoUploadInfo(self, url, auth, parts, filename, upload_id, biz_id):
        "查询上传视频信息"
        from urllib.parse import quote
        name = quote(filename)
        return self.__session.post(f'{url}?output=json&name={name}&profile=ugcupos%2Fbup&uploadId={upload_id}&biz_id={biz_id}', json={"parts":parts}, headers={"X-Upos-Auth": auth}).json()

    def videoRecovers(self, fns: '视频编号'):
        "查询以前上传的视频信息"
        url = f'https://member.bilibili.com/x/web/archive/recovers?fns={fns}'
        return self.__session.get(url=url).json()

    def videoTags(self, title: '视频标题', filename: "上传后的视频名称", typeid="", desc="", cover="", groupid=1, vfea=""):
        "上传视频后获得推荐标签"
        from urllib.parse import quote
        url = f'https://member.bilibili.com/x/web/archive/tags?typeid={typeid}&title={quote(title)}&filename=filename&desc={desc}&cover={cover}&groupid={groupid}&vfea={vfea}'
        return self.__session.get(url=url).json()

    def videoAdd(self, videoData:"dict 视频参数"):
        "发布视频"
        url = f'https://member.bilibili.com/x/vu/web/add?csrf={self.__bili_jct}'
        return self.__session.post(url, json=videoData).json()

    def videoPre(self):
        "视频预操作"
        url = 'https://member.bilibili.com/x/geetest/pre'
        return self.__session.get(url=url).json()

    def videoDelete(self, aid, geetest_challenge, geetest_validate, geetest_seccode):
        "删除视频"
        url = 'https://member.bilibili.com/x/web/archive/delete'
        post_data = {
            "aid": aid,
            "geetest_challenge": geetest_challenge,
            "geetest_validate": geetest_validate,
            "geetest_seccode": geetest_seccode,
            "success": 1,
            "csrf": self.__bili_jct
            }
        return self.__session.post(url, post_data).json()

    @staticmethod
    def activityList(plat='2', mold=0, http=3, start_page=1, end_page=10):
        "获取B站活动列表，生成器"
        session = requests.session()
        url = f'https://www.bilibili.com/activity/page/list?plat={plat}&mold={mold}&http={http}&page={start_page}'
        list = session.get(url).json()["data"]["list"]
        while len(list):
            for x in list:
                yield x
            if start_page == end_page:
                break
            start_page += 1
            url = f'https://www.bilibili.com/activity/page/list?plat={plat}&mold={mold}&http={http}&page={start_page}'
            list = session.get(url).json()["data"]["list"]
        session.close()

    @staticmethod
    def activityAll():
        "获取B站活动列表"
        url = 'https://member.bilibili.com/x/app/h5/activity/videoall'
        return requests.get(url).json()

    def activityAddTimes(self, sid: 'str 活动sid', action_type: 'int 操作类型'):
        "增加B站活动的参与次数"
        url = 'https://api.bilibili.com/x/activity/lottery/addtimes'
        post_data = {
            "sid": sid,
            "action_type": action_type,
            "csrf": self.__bili_jct
            }
        #响应例子{"code":75405,"message":"获得的抽奖次数已达到上限","ttl":1}
        return self.__session.post(url, post_data).json()

    def activityDo(self, sid: 'str 活动sid', type: 'int 操作类型'):
        "参与B站活动"
        #B站有时候举行抽奖之类的活动，活动页面能查出活动的sid
        post_data = {
            "sid": sid,
            "type": type,
            "csrf": self.__bili_jct
            }
        #响应例子{"code":75415,"message":"抽奖次数不足","ttl":1,"data":null}
        return self.__session.post('https://api.bilibili.com/x/activity/lottery/do', post_data).json()

    def activityMyTimes(self, sid: 'str 活动sid'):
        "获取B站活动次数"
        url = f'https://api.bilibili.com/x/activity/lottery/mytimes?sid={sid}'
        #响应例子{"code":0,"message":"0","ttl":1,"data":{"times":0}}
        return self.__session.get(url=url).json()

    def xliveGetAward(self, platform="android"):
        "B站直播模拟客户端打开宝箱领取银瓜子"
        url = f'https://api.live.bilibili.com/lottery/v1/SilverBox/getAward?platform={platform}'
        return self.__session.get(url).json()

    def xliveGetCurrentTask(self, platform="android"):
        "B站直播模拟客户端获取时间宝箱"
        url = f'https://api.live.bilibili.com/lottery/v1/SilverBox/getCurrentTask?platform={platform}'
        return self.__session.get(url).json()

    def xliveGiftBagList(self):
        "B站直播获取背包礼物"
        url = 'https://api.live.bilibili.com/xlive/web-room/v1/gift/bag_list'
        return self.__session.get(url=url).json()

    def xliveGetRecommendList(self):
        "B站直播获取首页前10条直播"
        url = f'https://api.live.bilibili.com/relation/v1/AppWeb/getRecommendList'
        return self.__session.get(url=url).json()

    def xliveBagSend(self, biz_id, ruid, bag_id, gift_id, gift_num, storm_beat_id=0, price=0, platform="pc"):
        "B站直播送出背包礼物"
        url = 'https://api.live.bilibili.com/gift/v2/live/bag_send'
        post_data = {
            "uid": self.__uid,
            "gift_id": gift_id, #背包里的礼物id
            "ruid": ruid, #up主的uid
            "send_ruid": 0,
            "gift_num": gift_num, #送礼物的数量
            "bag_id": bag_id, #背包id
            "platform": platform, #平台
            "biz_code": "live",
            "biz_id": biz_id, #房间号
            #"rnd": rnd, #直播开始时间
            "storm_beat_id": storm_beat_id,
            "price": price, #礼物价格
            "csrf": self.__bili_jct
            }
        return self.__session.post(url,post_data).json()

    def xliveGetRoomInfo(self, room_id: 'int 房间id'):
        "B站直播获取房间信息"
        url = f'https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByRoom?room_id={room_id}'
        return self.__session.get(url=url).json()

    def xliveWebHeartBeat(self, biz_id, last=11, platform="web"):
        "B站直播 直播间心跳"
        import base64
        hb = base64.b64encode(f'{last}|{biz_id}|1|0'.encode('utf-8')).decode()
        url = f'https://live-trace.bilibili.com/xlive/rdata-interface/v1/heartbeat/webHeartBeat?hb={hb}&pf={platform}'
        return self.__session.get(url).json()

    def xliveHeartBeat(self):
        "B站直播 心跳(大约2分半一次)"
        url = f'https://api.live.bilibili.com/relation/v1/Feed/heartBeat'
        return self.__session.get(url).json()

    def xliveUserOnlineHeart(self):
        "B站直播 用户在线心跳(很少见)"
        url = f'https://api.live.bilibili.com/User/userOnlineHeart'
        post_data = {
            "csrf": self.__bili_jct
            }
        content = self.__session.post(url, post_data)
        return self.__session.post(url, post_data).json()

    def mangaClockIn(self, platform="android"):
        "模拟B站漫画客户端签到"
        url = "https://manga.bilibili.com/twirp/activity.v1.Activity/ClockIn"
        post_data = {
            "platform": platform
            }
        return self.__session.post(url, post_data).json()

    def mangaGetWallet(self, platform="web"):
        "获取钱包信息"
        url = f'https://manga.bilibili.com/twirp/user.v1.User/GetWallet?platform={platform}'
        #{"code":0,"msg":"","data":{"remain_coupon":0,"remain_gold":0,"first_reward":false,"point":"1270","first_bonus_percent":0,"bonus_percent":0,"unusable_gold":0,"remain_item":0,"remain_tickets":0,"remain_discount":0,"account_level":0}}
        #                               劵的数量        金币数量         是否第一次充值          积分
        return self.__session.post(url, json={}).json()

    def mangaComrade(self, platform="web"):
        "站友日漫画卷兑换"
        url = f'https://manga.bilibili.com/twirp/activity.v1.Activity/Comrade?platform={platform}'
        #{"code":0,"msg":"","data":{"now":"2020-09-20T21:10:38+08:00","received":0,"active":0,"lottery":0,"svip":1}}
        return self.__session.post(url, json={}).json()

    def mangaGetEpisodeBuyInfo(self, ep_id: int, platform="web"):
        "获取漫画购买信息"
        url = f'https://manga.bilibili.com/twirp/comic.v1.Comic/GetEpisodeBuyInfo?platform={platform}'
        post_data = {
            "ep_id": ep_id
            }
        return self.__session.post(url, json=post_data).json()

    def mangaBuyEpisode(self, ep_id: int, buy_method=1, coupon_id=0, auto_pay_gold_status=0, platform="web"):
        "购买漫画"
        url = f'https://manga.bilibili.com/twirp/comic.v1.Comic/BuyEpisode?&platform={platform}'
        post_data = {
            "buy_method": buy_method,
            "ep_id": ep_id
            }
        #{"buy_method":2,"ep_id":283578,"coupon_id":2064528,"auto_pay_gold_status":2}
        if coupon_id:
            post_data["coupon_id"] = coupon_id
        if auto_pay_gold_status:
            post_data["auto_pay_gold_status"] = auto_pay_gold_status

        #{"code":1,"msg":"没有足够的卡券使用次数，请刷新重试。","data":{"auto_use_item":""}}
        return self.__session.post(url, json=post_data).json()

    def mangaGetTopic(self, page_num=1, platform='phone'):
        "B站漫画app活动中心列表"
        url = 'https://manga.bilibili.com/twirp/comic.v1.Comic/Topic'
        post_data = {
            "page_num": page_num,
            "platform": platform
            }
        return self.__session.post(url, post_data).json()

    def mangaListFavorite(self, page_num=1, page_size=50, order=1, wait_free=0, platform='web'):
        "B站漫画追漫列表"
        url = 'https://manga.bilibili.com/twirp/bookshelf.v1.Bookshelf/ListFavorite?platform={platform}'
        post_data = {
            "page_num": page_num,
            "page_size": page_size,
            "order": order,
            "wait_free": wait_free
            }
        return self.__session.post(url, json=post_data).json()

    def mangaPayBCoin(self, pay_amount: int, product_id=1, platform='web'):
        "B币购买漫画"
        url = f'https://manga.bilibili.com/twirp/pay.v1.Pay/PayBCoin?platform={platform}'
        post_data = {
            "pay_amount": pay_amount,
            "product_id": product_id
            }
        #{"code":0,"msg":"","data":{"id":"1600656017507211119"}}
        return self.__session.post(url, json=post_data).json()

    def mangaGetBCoin(self, platform='web'):
        "获取B币与漫读劵的信息"
        url = f'https://manga.bilibili.com/twirp/pay.v1.Pay/GetBCoin?platform={platform}'
        #{"code":0,"msg":"","data":{"amount":0,"exchange_rate":100,"first_max_coin":18800,"first_bonus_percent":0,"bonus_percent":0,"coupon_rate":2,"coupon_exp":30,"point_rate":200,"coin_amount":0,"coupon_amount":0,"is_old_version":true}}
        return self.__session.post(url, json={}).json()

    def mangaGetCoupons(self, not_expired=True, page_num=1, page_size=50, tab_type=1, platform='web'):
        "获取账户中的漫读劵信息"
        url = f'https://manga.bilibili.com/twirp/user.v1.User/GetCoupons?platform={platform}'
        post_data = {
            "not_expired": not_expired,
            "page_num": page_num,
            "page_size": page_size,
            "tab_type": tab_type
            }
        #{"code":0,"msg":"","data":{"total_remain_amount":4,"user_coupons":[{"ID":2093696,"remain_amount":2,"expire_time":"2020-10-21 10:40:17","reason":"B币兑换","type":"福利券","ctime":"2020-09-21 10:40:17","total_amount":2,"limits":[],"type_num":7,"will_expire":0,"discount":0,"discount_limit":0,"is_from_card":0},{"ID":2093703,"remain_amount":2,"expire_time":"2020-10-21 10:47:43","reason":"B币兑换","type":"福利券","ctime":"2020-09-21 10:47:43","total_amount":2,"limits":[],"type_num":7,"will_expire":0,"discount":0,"discount_limit":0,"is_from_card":0}],"coupon_info":{"new_coupon_num":0,"coupon_will_expire":0,"rent_will_expire":0,"new_rent_num":0,"discount_will_expire":0,"new_discount_num":0,"month_ticket_will_expire":0,"new_month_ticket_num":0,"silver_will_expire":0,"new_silver_num":0,"remain_item":0,"remain_discount":0,"remain_coupon":4,"remain_silver":0}}}
        return self.__session.post(url, json=post_data).json()

    def mangaDetail(self, comic_id: int, device='pc', platform='web'):
        "获取漫画信息"
        url = f'https://manga.bilibili.com/twirp/comic.v1.Comic/ComicDetail?device={device}&platform={platform}'
        post_data = {
            "comic_id": comic_id
            }
        return self.__session.post(url, json=post_data).json()

    def mangaGetPoint(self):
        "获取漫画积分"
        url = f'https://manga.bilibili.com/twirp/pointshop.v1.Pointshop/GetUserPoint'
        return self.__session.post(url, json={}).json()

    def mangaShopList(self):
        "漫画积分商城列表"
        url = f'https://manga.bilibili.com/twirp/pointshop.v1.Pointshop/ListProduct'
        return self.__session.post(url, json={}).json()

    def mangaShopExchange(self, product_id: int, point: int, product_num=1):
        "漫画积分商城兑换"
        url = f'https://manga.bilibili.com/twirp/pointshop.v1.Pointshop/Exchange'
        post_data = {
            "product_id": product_id,
            "point": point,
            "product_num": product_num
            }
        return self.__session.post(url, json=post_data).json()

    def mangaImageToken(self, urls=[], device='pc', platform='web'):
        "获取漫画图片token"
        url = f'https://manga.bilibili.com/twirp/comic.v1.Comic/ImageToken?device={device}&platform={platform}'
        post_data = {
            "urls": json.dumps(urls)
            }
        return self.__session.post(url, json=post_data).json()

    def mangaImageIndex(self, ep_id: int, device='pc', platform='web'):
        "获取漫画图片列表"
        url = f'https://manga.bilibili.com/twirp/comic.v1.Comic/GetImageIndex?device={device}&platform={platform}'
        post_data = {
            "ep_id": ep_id
            }
        return self.__session.post(url, json=post_data).json()

    def mangaGetImageBytes(self, url: str):
        "获取漫画图片"
        return self.__session.get(url).content

    def vipPrivilegeMy(self):
        "B站大会员权益列表"
        url = 'https://api.bilibili.com/x/vip/privilege/my'
        #{"code":0,"message":"0","ttl":1,"data":{"list":[{"type":1,"state":1,"expire_time":1601481599},{"type":2,"state":0,"expire_time":1601481599}]}}
        return self.__session.get(url).json()

    def vipPrivilegeReceive(self, type=1):
        "领取B站大会员权益"
        url = 'https://api.bilibili.com/x/vip/privilege/receive'
        post_data = {
            "type": type,
            "csrf": self.__bili_jct
            }
        #{"code":69801,"message":"你已领取过该权益","ttl":1}
        return self.__session.post(url, data=post_data).json()

    @staticmethod
    def webView(bvid: str):
        "通过bv号获取视频信息"
        url = f'https://api.bilibili.com/x/web-interface/view?bvid={bvid}'
        return requests.get(url,headers={"User-Agent": "Mozilla/5.0","Referer": "https://www.bilibili.com/"}).json()

    @staticmethod
    def webStat(aid: int):
        "通过av号获取视频信息"
        url = f'https://api.bilibili.com/x/web-interface/archive/stat?aid={aid}'
        return requests.get(url,headers={"User-Agent": "Mozilla/5.0","Referer": "https://www.bilibili.com/"}).json()

    @staticmethod
    def playList(bvid='', aid=0):
        "获取播放列表"
        if bvid:
            url = f'https://api.bilibili.com/x/player/pagelist?bvid={bvid}'
        elif aid:
            url = f'https://api.bilibili.com/x/player/pagelist?bvid={aid}'
        return requests.get(url).json()

    @staticmethod
    def epPlayList(ep_or_ss: str):
        "获取番剧播放列表"
        import re
        url = f'https://www.bilibili.com/bangumi/play/{ep_or_ss}'
        text = requests.get(url, headers={'User-Agent':'Mozilla/5.0'}).text
        find = re.findall(r'window.__INITIAL_STATE__=({.*});\(function\(\)', text, re.S)
        return json.loads(find[0])

    def webPlayUrl(self, cid=0, aid=0, bvid='', epid=0, qn=16):
        "获取番剧播放地址(普通视频请用playerUrl方法)"
        url = 'https://api.bilibili.com/pgc/player/web/playurl'
        data = {"qn":qn}
        if cid:
            data["cid"] = cid
        if aid:
            data["avid"] = aid
        if bvid:
            data["bvid"] = bvid
        if epid:
            data["ep_id"] = epid
        #{'code': -10403, 'message': '抱歉您所在地区不可观看！'}
        #{'code': -10403, 'message': '大会员专享限制'}
        return self.__session.get(url, params=data).json()

    def playerUrl(self, cid: int, aid=0, bvid='', qn=16, reverse_proxy=''):
        "获取视频播放地址"
        if reverse_proxy:
            url = reverse_proxy
        else:
            url = 'https://api.bilibili.com/x/player/playurl'
        #data = {"qn":qn,"cid":cid,'fnval':80}
        data = {"qn":qn,"cid":cid}
        if aid:
            data["avid"] = aid
        if bvid:
            data["bvid"] = bvid
        return self.__session.get(url, params=data).json()

    @staticmethod
    def videoGetPart(url: str, start, end):
        "下载视频分段"
        headers = {"Range":f'bytes={start}-{end}',"Referer": "https://www.bilibili.com/"}
        return requests.get(url, headers=headers).content

    @staticmethod
    def dmList(oid: int):
        "获得弹幕xml"
        url = f'https://api.bilibili.com/x/v1/dm/list.so?oid={oid}'
        content = requests.get(url)
        content.encoding = 'utf-8'
        return content.text

    @staticmethod
    def dmHistory(oid: int, data: str):
        "获得历史弹幕xml"
        url = f'https://api.bilibili.com/x/v2/dm/history?type=1&oid={oid}&date={data}'
        content = requests.get(url)
        content.encoding = 'utf-8'
        return content.text
