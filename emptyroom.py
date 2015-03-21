#!/usr/bin/env python
#coding:utf-8

import tornado.ioloop
import tornado.web
import tornado.auth
import tornado.simple_httpclient
import tornado.httpserver
import tornado.options
import os.path
import json
import urllib.request       #python3
# import urllib2 			#python2
import tornado.gen

from tornado.options import define, options
define("port", default=8094, help="run on the given port", type=int)

url='http://herald.seu.edu.cn/api/nic/emptyroom'
uuid=''

class GetHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("emptyroom.html",emptyroom="",classBegin="输入数字",place="jlh",
        	classEnd="输入数字",week="输入数字",day="输入数字",index1="3",index2="2",select1="cur",select2="")

class SimpleHander(tornado.web.RequestHandler):
	def post(self):
		arg1=self.get_argument("arg1")
		arg2=self.get_argument("arg2")
		if arg2 == "查询今天":
			arg2 ="today"
		else :
			arg2="tomorrow"
		arg3=self.get_argument("arg3")
		arg4=self.get_argument("arg4")
		postdata={
		'uuid':uuid,
		'arg1':arg1,
		'arg2':arg2,
		'arg3':arg3,
		'arg4':arg4,
		}
		data = urllib.parse.urlencode(postdata)
		http = tornado.httpclient.AsyncHTTPClient()
		response = yield tornado.gen.Task(http.fetch, url, method='POST', headers=None, body=data) 
		self.render("emptyroom.html",emptyroom=response,classBegin=arg3,place=arg1,
			classEnd=arg4,week="输入数字",day="输入数字",index1="3",index2="2",select1="cur",select2="")


class ComplexHander(tornado.web.RequestHandler):
	def post(self):
		arg1=self.get_argument("arg1")
		arg2=self.get_argument("arg2")
		arg3=self.get_argument("arg3")
		arg4=self.get_argument("arg4")
		arg5=self.get_argument("arg5")
		postdata ={
		'uuid':uuid,
		'arg1':arg1,
		'arg2':arg2,
		'arg3':arg3,
		'arg4':arg4,
		'arg5':arg5,
		}
		req = urllib.request.Request(url, data)
		http = tornado.httpclient.AsyncHTTPClient()
		response = yield tornado.gen.Task(http.fetch, url, method='POST', headers=None, body=data) 

		self.render("emptyroom.html",emptyroom=response,classBegin=arg4,place=arg1,
			classEnd=arg5,week=arg2,day=arg3,index1="2",index2="3",select1="",select2="cur")


handlers = [
    (r"/",GetHandler),
    (r"/simple",SimpleHander),
    (r"/complex",ComplexHander)

]
path = "E:\Herald\MyOwn\Web\EmptyRoom"

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers, path)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()