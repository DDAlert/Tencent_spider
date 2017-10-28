# -*- coding: utf-8 -*-
import scrapy
from Tencent.items import TencentItem

class TencentSpider(scrapy.Spider):
    #爬虫名
    name = 'tencent'
    #爬虫爬取数据的域范围
    allowed_domains = ['tencent.com']
    baseURL = "http://hr.tencent.com/position.php?atart=0&start="
    offset = 0 #偏移量,每次+10
    start_urls = [baseURL + str(offset)]

    def parse(self, response):
        #提取每个response的数据
        node_list = response.xpath("//tr[@class='even'] | //tr[@class='odd']")

        for node in node_list:
            #构建一个item对象
            item = TencentItem()
            #提取每个职位的信息，并且将提取出来的Unicode字符串编码为utf-8编码
            item['positionName']= node.xpath("./td[1]/a/text()").extract()[0]#.encode("utf-8")
            item['positionLink'] = node.xpath("./td[1]/a/@href").extract()[0]#.encode("utf-8")
            #提取的值有的为空的，需要判断一下
            if len(node.xpath("./td[2]/text()")):
                item['positionType'] = node.xpath("./td[2]/text()").extract()[0]#.encode("utf-8")
            else:
                item['positionType'] = ""

            item['peopleNumber'] = node.xpath("./td[3]/text()").extract()[0]#.encode("utf-8")
            item['workLocation'] = node.xpath("./td[4]/text()").extract()[0]#.encode("utf-8")
            item['publishTime'] = node.xpath("./td[5]/text()").extract()[0]#.encode("utf-8")
            #yield的重要性，返回数据之后还能回来接着只小南国代码
            yield item
        #     #方式一，拼接url
        #  # 适用于页面没有点击的请求连接，必须通过拼接url才能获取响应
        # #实现翻页并继续提取数据
        # #使用偏移量，就是拼接的方法（找url的规律得到）
        # #该方法的弊端：如果页面改变了数量就会改变下面2210这个判断的值
        # #解决的办法：一页提取完之后自动获取下一页的url
        # if self.offset < 2210:
        #     self.offset += 10
        #     url = self.baseURL + str(self.offset)
        #     yield scrapy.Request(url,callback=self.parse)
        #
        #     #方式二
        #     #直接从response获取需要爬去的连接，并发送请求处理，直到连接全部提取完
        #     找到每一页的"下一页"按钮的url
        if len(response.xpath("//a[@class='noactive' and @id='next']")) == 0:
            url = response.xpath("//a[@id='next']/@href").extract()[0]
            yield scrapy.Request("http://hr.tencent.com/" + url,callback=self.parse)





































