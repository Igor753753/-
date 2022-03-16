import scrapy

import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SuperjobruSpider(scrapy.Spider):
    name = 'superjobru'
    allowed_domains = ['superjob.ru']
    vacancy = 'python'
    start_urls = [f'https://www.superjob.ru/vacancy/search/?keywords={vacancy}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@rel="next"]/@href').extract_first()


        vacancy = response.xpath('//div[@class="_3zucV _1fMKr undefined _1NAsu"]/*/*/*/*/*/*/a/@href').extract()

        for link in vacancy:
            yield response.follow(link, callback=self.vacancy_parse)
        #yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(selfself, response: HtmlResponse):
        name = response.xpath('//h1/text()').extract_first()
        salary = response.xpath('//span[@class="_1OuF_ ZON4b"]//text()').extract()
        url = response.url
        company = response.xpath('//span[@class="_3mfro _1hP6a _2JVkc _2VHxz"]/text() ').extract_first()

        location = response.xpath('//div[@class="f-test-address _3AQrx"]//text()').extract()

        yield JobparserItem(name=name, salary=salary, location=location, url=url, company=company)

