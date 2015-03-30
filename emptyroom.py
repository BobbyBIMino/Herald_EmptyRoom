#!/usr/bin/env python
#coding:utf-8

import tornado.ioloop
import tornado.web
import tornado.auth
import tornado.simple_httpclient
import tornado.httpclient
import tornado.httpserver
import tornado.options
import os.path
import json
import urllib.request       #python3
# import urllib2 			#python2
import tornado.gen
import sys
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from tornado.options import define, options
define("port", default=8029, help="run on the given port", type=int)
url='http://herald.seu.edu.cn/api/emptyroom'
uuid='0000000000000000000000000000000000000000'

class GetHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("emptyroom.html",emptyroom="",place="jlh",classBegin="1",classEnd="1",
        	week="1",day="1",index1="3",index2="2",select1="cur",select2="")
class SimpleHander(tornado.web.RequestHandler):
	@tornado.gen.engine
	@tornado.web.asynchronous
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
		'arg4':arg4
		}
		data = urllib.parse.urlencode(postdata)
		http_client = tornado.httpclient.AsyncHTTPClient()
		response = yield tornado.gen.Task(http_client.fetch,url,method='POST',headers=None,body=data )
		dataDict = json.loads(response.body.decode())
		dataD=""
		counter=0
		for item in dataDict:
			counter=counter+1
			dataD+=item
			dataD+="  "
			if counter%3==0 :
				dataD+='\n'


		self.render("emptyroom.html",emptyroom = dataD,place=arg1,classBegin=arg3,classEnd=arg4,
			week="1",day="1",index1="3",index2="2",select1="cur",select2="")

class ComplexHander(tornado.web.RequestHandler):
	@tornado.gen.engine
	@tornado.web.asynchronous
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
		'arg5':arg5
		}
		data = urllib.parse.urlencode(postdata)
		requestR =HTTPRequest(
			url,
			method='POST',
			headers=None,
			body=data
			)
		http_client=tornado.httpclient.AsyncHTTPClient()
		response = yield tornado.gen.Task(http_client.fetch,requestR)
		dataDict = json.loads(response.body.decode('utf-8'))
		dataD=""
		counter=0
		for item in dataDict:
			counter=counter+1
			dataD+=item
			dataD+="  "
			if counter%3==0 :
				dataD+='\n'

		self.render("emptyroom.html",emptyroom = dataD,place=arg1,classBegin=arg4,classEnd=arg5,
			week= arg2 ,day = arg3,index1="2",index2="3",select1="",select2="cur")


handlers = [
    (r"/",GetHandler),
    (r"/simple",SimpleHander),
    (r"/complex",ComplexHander)
]

path=sys.path[0]


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers, path)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()