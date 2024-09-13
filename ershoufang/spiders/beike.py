import scrapy
from scrapy import Request, Selector
from scrapy.http import HtmlResponse
from ershoufang.items import ErshoufangItem

class BeikeSpider(scrapy.Spider):
    name = 'beike'
    allowed_domains = ['xa.ke.com']
    # cookie={
    #     'Cookie': '''
    #     SECKEY_ABVK=UslraKIHY5wI9XPGuL4vx7JnaDcYUAutH0dxcbPfroBw4+jZZzYrmoKaMxcTKCs2; BMAP_SECKEY=UslraKIHY5wI9XPGuL4vxwaGYotzZpac39F0-FuXW7NtphUM986mXv_BANVSj4m19MQji0EO1Q24cdykk_FXMtiEoi4_MXpZu8B1_cK3_Y-63-KD5c-dECdLIl8ClZoKvRgXT96E0PdgEsJcUznSgnj1zT80qimi60WN9gdc03RLaaluqxKZX5Jegy8ZCBTzQDbfsQqjw5qOmG1AsLtcCA; lianjia_uuid=fc0bcb2a-6d19-49ac-b0f8-1b4c145ed8b2; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22191cad7639410c7-08df711768bbef-26001151-2090547-191cad76395a5e%22%2C%22%24device_id%22%3A%22191cad7639410c7-08df711768bbef-26001151-2090547-191cad76395a5e%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; Hm_lvt_b160d5571570fd63c347b9d4ab5ca610=1725684999,1725761985; HMACCOUNT=62CC119626349217; lianjia_ssid=a23f3363-7b8a-4698-be29-ce8150f3d4af; digv_extends=%7B%22utmTrackId%22%3A%22%22%7D; hip=fQN11v_Yk6rcHg3jtbBNcSQ7XLKl_3UL7vTViHzbyha6mWLNjNBdj8M1i3z8ieFBMxO1U8OC0EJ_zebChYJdX9MGzLAiF-80YW6GnShS5v2M6TvLpMc9sR34B3u3A3LmIBz_iAITYJ38OYvaZ92Rwab1_wSIgm_jbxfdsCrTd3RZeZ1Rhf0%3D; login_ucid=2000000443293965; lianjia_token=2.001307970f43e8dbee02aabe3e8c29d4b7; lianjia_token_secure=2.001307970f43e8dbee02aabe3e8c29d4b7; security_ticket=oWYPe3AGDVIM+V6aueEeLNmCVHbmoP9k89PUUIxtNM101KuZN479kTwMI6bzu9udJlHNjTFbIgXPK9UpRj2nth9B6bgxi7/OeP/JVVdiTJzTsrAK8qgWWzqyJfmeVUpEV4zMEmpCXb0H7Nbjix2qtanv1tVlK5Tu1eDgZqka19k=; ftkrc_=185f6ef6-b366-4644-a51a-c829269b613f; lfrc_=b50815ad-93ca-4611-964c-9f32840b71ac; Hm_lpvt_b160d5571570fd63c347b9d4ab5ca610=1725764806; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiNWU5NTI3NWNiMzQ1OGYyY2RkOTg4YzQyMzdhNDJhZmNhNTc5ZmU4YTYxOWNjMzljNTEyZDRhNjhiNTdhZjNlOWI2NDA2MGE5MWE4YTY0NTVlODJjODllMDU0YzUyNDYyNjg2MDg5NTQ5MzY5YjBjMjdhODZiYmUxMTZmZWJiY2Y1OWU1NWQ0MmE5Yjc1MzNmMGZmZGY5NTY4MDI0OWNjMGUyYWEwODRjY2Q5NDRkYjczZjFkN2VmMmYzYjMwMTZlN2QxYWNlYTMzMGNhMTQ2ZmFmM2M0NmIyMWY0NmRlOGFlMDJlZjcyNDZlNjM5NmMyN2ZhMWEwN2ZlY2RkYWNkZWE2ZmM2Y2Q5ZDFjODMzNmRmYTIwZTdiMzAwYjkwNjBhXCIsXCJrZXlfaWRcIjpcIjFcIixcInNpZ25cIjpcImU5NzhmODUwXCJ9IiwiciI6Imh0dHBzOi8veGEua2UuY29tL2Vyc2hvdWZhbmcvMTAxMTI2NDMwNTY3Lmh0bWw/ZmJfZXhwb19pZD04ODUxMTU2NDc5OTc1MzQyMTAiLCJvcyI6IndlYiIsInYiOiIwLjEifQ==; select_city=110000
    #     '''
    #     }
    # start_urls = ['https://xa.ke.com/ershoufang/pg'+i for i in range(1,5)]
    def start_requests(self):
        for page in range(1, 3):
            url = "https://xa.ke.com/ershoufang/pg{}".format(page)
            yield Request(url)

    def parse(self, response):

        list_item=response.xpath('//li[@class="clear"]/div[@class="info clear"]')
        for item in list_item:
            ershoufangItem=ErshoufangItem()
            title=item.xpath('./div[1]/a/text()').extract_first()
            location=item.xpath('./div[2]/div[1]/div/a/text()').extract_first()
            price=item.xpath('.//div[contains(@class,"totalPrice")]/span/text()').extract_first()+item.xpath('.//div[contains(@class,"totalPrice")]/i[2]/text()').extract_first()
            ershoufangItem['title']=title
            ershoufangItem['location']=location
            ershoufangItem['price']=price
            detail_url=item.xpath('./div[1]/a/@href').extract_first()
        
            yield Request(detail_url, callback=self.parse_detail, cb_kwargs={'item':ershoufangItem})
           
            
            
    def parse_detail(self, response: HtmlResponse, **kwargs):
        ershoufangItem = kwargs['item']  
        
        house_type=response.xpath('//div[@class="room"]/div[@class="mainInfo"]/text()').extract_first()
        beike_id=response.xpath('//div[@class="houseRecord"]/span[@class="info"]/text()').extract_first()
        ershoufangItem['house_type']=house_type
        ershoufangItem['beike_id']=beike_id
        yield ershoufangItem
        
		# 返回数据给管道
        # yield movie_item
