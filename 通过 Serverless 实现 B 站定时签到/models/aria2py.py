import json, time
import subprocess
import os

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 6800
DEFAULT_SECRET = ''

class Aria2Py(object):
    '''Aria2下载器'''
    def __init__(self,
                 host=DEFAULT_HOST,
                 port=DEFAULT_PORT,
                 secret=DEFAULT_SECRET,
                 session=None,
                 remote=False
                 ):
        self.server_uri = f'http://{host}:{port}/jsonrpc'
        self.secret = secret
        import requests
        self.session = requests.session()

        if not remote:
            if self.isAria2Running():
                return
            if not Aria2Py.isAria2Installed():
                raise Exception('未找到aria2')

            cmd = f'aria2c' \
                  ' --enable-rpc' \
                 f' --rpc-listen-port {port}' \
                  ' --continue' \
                  ' --max-concurrent-downloads=20' \
                  ' --max-connection-per-server=10' \
                  ' --rpc-max-request-size=1024M'

            if not session is None:
                cmd += f' --input-file={session}' \
                       ' --save-session-interval=60' \
                      f' --save-session={session}'

            subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

        try:
            data = self.getGlobalStat()
            if 'error' in data:
                raise Exception(f'连接aria2失败({data["error"]["Unauthorized"]})')
        except:
            raise Exception('连接aria2失败')

    def sendJsonRPC(self, data):
        '''发送RPC请求'''
        return self.session.post(self.server_uri, data=data).json()

    def getRPCBody(self, method, params=[]):
        '''创建RPC请求'''
        uid = '14515821564dsfdvzxvdf'
        if self.secret:
            params.insert(0, f'token:{self.secret}')
        j = json.dumps({
            'jsonrpc': '2.0',
            'id': uid,
            'method': method,
            'params': params
        })
        return j

    def addUri(self, uris, options=None, position=None):
        '''
        添加一个HTTP(S)/FTP/BitTorrent Magnet下载任务.
        uris: list, 链接数组
        options: dict, 附加参数
        position: int, 队列里的位置
        '''
        params = [[uris]]
        if options:
            params.append(options)
        if position:
            params.append(position)
        return self.sendJsonRPC(data=self.getRPCBody('aria2.addUri', params))

    def remove(self, gid):
        '''
        移除下载任务.
        gid: string, 任务GID.
        '''
        params = [gid]
        return self.sendJsonRPC(data=self.getRPCBody('aria2.remove', params))

    def forceRemove(self, gid):
        '''
        强制移除下载任务.
        gid: string, 任务GID.
        '''
        params = [gid]
        return self.sendJsonRPC(data=self.getRPCBody('aria2.forceRemove', params))

    def pause(self, gid):
        '''
        暂停任务.
        gid: string, GID.
        return: GID.
        '''
        params = [gid]
        return self.sendJsonRPC(data=self.getRPCBody('aria2.pause', params))

    def pauseAll(self):
        '''
        暂停全部任务.
        return: 成功返回OK.
        '''
        return self.sendJsonRPC(data=self.getRPCBody('aria2.pauseAll'))

    def forcePause(self, gid):
        '''
        强制暂停任务.
        gid: string, GID.
        '''
        params = [gid]
        return self.sendJsonRPC(data=self.getRPCBody('aria2.forcePause', params))

    def forcePauseAll(self):
        '''
        强制暂停全部任务.
        return: 成功返回OK.
        '''
        return self.sendJsonRPC(data=self.getRPCBody('aria2.forcePauseAll'))

    def unpause(self, gid):
        '''
        解除任务暂停状态.
        gid: string, GID.
        '''
        params = [gid]
        return self.sendJsonRPC(data=self.getRPCBody('aria2.unpause', params))

    def unpauseAll(self):
        '''
        解除所有任务暂停状态.
        return: 成功返回OK.
        '''
        return self.sendJsonRPC(data=self.getRPCBody('aria2.unpauseAll'))

    def tellStatus(self, gid, keys=None):
        '''
        返回下载进度.
        gid: string, GID.
        keys: list, 需要返回的参数列表.
        '''
        params = [gid]
        if keys:
            params.append(keys)
        return self.sendJsonRPC(data=self.getRPCBody('aria2.tellStatus', params))

    def tellActive(self, keys=None):
        '''
        返回活跃的任务.
        keys: list, 需要返回的参数列表.
        '''
        params = []
        if keys:
            params.append(keys)
        return self.sendJsonRPC(data=self.getRPCBody('aria2.tellActive', params))

    def getGlobalStat(self):
        '''
        获得全局参数比如上传或下载速度.
        return: The method response is of type struct and contains following keys.
        '''
        return self.sendJsonRPC(data=self.getRPCBody('aria2.getGlobalStat'))

    @staticmethod
    def isAria2Installed():
        '''Aria2是否已经安装'''
        if os.path.exists('aria2c'):
            return True
        if os.path.exists('aria2c.exe'):
            return True
        for cmdpath in os.environ['PATH'].split(':'):
            if os.path.isdir(cmdpath) and 'aria2c' in os.listdir(cmdpath):
                return True
        return False

    def isAria2Running(self):
        '''Aria2是否已经启动并能成功连接'''
        ret = True
        try:
            data = self.getGlobalStat()
            if 'error' in data:
                ret = False
        except:
            ret = False
        return ret