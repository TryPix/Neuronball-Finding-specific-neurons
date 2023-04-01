"""
Finding neurons with the prefix 'Cobra' in the multiplayer game neuronball.com,
using the scrapy framweork in Python.

31/03/2023-01/04/2023
"""

import scrapy
from scrapy.crawler import CrawlerProcess

class CobraFinder(scrapy.Spider):

    name = "hunter"
    cobraTeamsFile = "cobraTeams.txt" 
    s = 1300000
    e = 1348148
    URL = 'https://www.neuronball.com/en/player/{}/' # format with player number

    def start_requests(self):
        urls = []
        for i in range (self.s, self.e): # fetch range
            urls.append(self.URL.format(str(i)))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        containsCobra = False
        htmlAsString = response.text

        if ('<div class="neuron-name">Cobra' in htmlAsString) and ('Standard' not in htmlAsString):
            containsCobra = True

        if (containsCobra):
            with open(self.cobraTeamsFile, "a") as f:
                f.write("\n" + response.url + "\n")

                
if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(CobraFinder)
    process.start()