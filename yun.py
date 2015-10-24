#-*- coding:utf-8 -*-
#百度云网盘模块只提供与备份相关的接口
#参考文章及内容：
#https://github.com/Yangff/node_pcsapi/blob/master/baidulogin.md
#python库baidupcsapi-0.3.5
import json
import cookielib
import urllib
import urllib2
import time

#根据文件完整路径获取文件名
def get_filename(path):
	return path.split('/')[-1].split('\\')[-1]

#短时间内多次登陆百度账号会导致需要输入验证码，以致无法登陆
class BaiduDisk:
	def __init__(self, username, password):
		cookie = cookielib.LWPCookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
		self.username = username
		self.password = password

	def post(self, url, **kvargv):
		req = urllib2.Request(url=url, **kvargv)
		#res = urllib2.urlopen(req).read()
		res = self.opener.open(req).read()
		return res

	def login(self):
		#获取cookie
		url = 'http://www.baidu.com'
		self.post(url)

		#获取token
		url = 'https://passport.baidu.com/v2/api/?getapi&tpl=mn&apiver=v3&class=login&tt=%s&logintype=dialogLogin&callback=%s' % (int(time.time()), 0)
		self.token = json.loads(self.post(url).replace("'", '"'))['data']['token']

		url = 'https://passport.baidu.com/v2/api/?logincheck&token=%stpl=mn&apiver=v3&tt=%s&username=%s&isphone=false&callback=%s' % (self.token, int(time.time()), '', 0)
		self.post(url)

		url = 'https://passport.baidu.com/v2/api/?login'
		data = {
			'staticpage': 'http://www.baidu.com/cache/user/html/v3Jump.html',
			'charset': 'UTF-8',
			'token': self.token,
			'tpl': 'mn',
			'apiver': 'v3',
			'tt': int(time.time()),
			'codestring': '',
			'isPhone': 'false',
			'safeflg': '0',
			'u': 'http://www.baidu.com/',
			'quick_user': '0',
			'usernamelogin': '1',
			'splogin': 'rate',
			'username': self.username,
			'password': self.password,
			'verifycode': '',
			'mem_pass': 'on',
			'ppui_logintime': '5000',
			'callback': 'parent.bd__pcbs__oa36qm'
		}
		ret = self.post(url, data=urllib.urlencode(data))
		return ret.split('err_no=')[1].split('&')[0]

	def post_pan(self, method, params):
		url = 'http://pan.baidu.com/api/%s' % method
		return self.post(url, data=urllib.urlencode(params))

	def post_pcs(self, method, params, data):
		url = 'http://c.pcs.baidu.com/rest/2.0/pcs/%s?%s' % (method, urllib.urlencode(params))

	#获得配额信息
	def quota(self):
		return self.post_pan('quota', {'method': 'info'})

	#查看目录下的文件
	def show(self, path='/'):
		return self.post_pan('list', {'dir': path})

	#比较文件
	def compare(self):
		pass

	#创建目录
	def mkdir(self, path):
		return self.post_pan('create', {'path': path, 'isdir': 1})

	#删除文件
	def delete(self, file_list):
		return self.post_pan('filemanager?opera=delete', {'filelist': json.dumps(file_list)})

	#上传文件
	def upload(self, file_name):
		data = {'method': 'upload', 'dir': 'a.txt', 'ondup': 'newcopy', 'filename': 'a.txt'}

	#获取文件或目录的元信息
	def get_metas(self, file_list):
		return self.post_pan('filemetas', {'dlink': 1, 'target': json.dumps(file_list)})
	
	#获取下载链接
	def get_link(self, file_list):
		metas = json.loads(self.get_metas(file_list))
		return [(get_filename(path), info['dlink']) for info, path in zip(metas['info'], file_list) if info.has_key('dlink')]

	#下载文件
	def download(self, file_list, path):
		dlink_list = self.get_link(file_list)
		for file_name, dlink in dlink_list:
			data = self.post(dlink)
			print data


if __name__ == '__main__':
	disk = BaiduDisk('baidu_yun_test@sina.com', 'test123456')
	disk.login()
	disk.quota()
	disk.show('/')