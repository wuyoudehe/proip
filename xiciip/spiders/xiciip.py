# 2017.8.8 wuyoudehe win7 64 python:3.6 scrapy:1.4
import scrapy
from lxml import *
import queue
from threading import Thread
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import os


class xiciip(scrapy.Spider):
	name = 'xiciip'

	def __init__(self):
		self.start_urls = [
			"http://www.xicidaili.com/nn/1",
			"http://www.xicidaili.com/nn/2"]
		self.headers = {
			'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
		}
		self.pagetest = []
		self.prolist = []

	def start_requests(self):
		for url in self.start_urls:
			yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

# 进行网页数据处理
	def parse(self, response):
		tabledata = response.xpath('//table[@id="ip_list"]')[0]
		trdata = tabledata.xpath('//tr')[1:]
		iplist = trdata.xpath("td[2]/text()").extract()
		portlist = trdata.xpath("td[3]/text()").extract()
		proxylist = []
		for x, y in zip(iplist, portlist):
			porxy = 'http://' + x + ':' + y
			# print(porxy)
			proxylist.append(porxy)
		self.iplisttest(proxylist)

# 根据CPU数确定线程池数，进行多线程测试
	def iplisttest(self, proxylist):
		pool = ThreadPool(8)
		results = pool.map(self.ip_test, proxylist)
		pool.close()
		pool.join()
		print('开始进行文件写入')
		with open('{}//prolist.text'.format(os.getcwd()), 'wt') as f:
			for x in self.prolist:
				f.write(str(x) + '\r\n')

# 代理ip测试
	def ip_test(self, proxylist):
		print('开始进行ip代理测试')
		iptest = proxylist.split(' ')
		import requests
		import re
		for x in iptest:
			proxies = {
				'http': x
			}
			try:
				response = requests.get('http://www.baidu.com', headers=self.headers, timeout=4, proxies=proxies)
				print(response.status_code)
				splitlist = re.split('//:|', x)
				if response.status_code == 200:
					self.prolist.append(x)
			except IOError:
				print("connect failed!", iptest)
