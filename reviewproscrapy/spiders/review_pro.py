import scrapy
from reviewproscrapy.items import PageItem

class ReviewProSpider(scrapy.Spider):
    name = "review_pro"
    allowed_domains = ["www.shijigroup.com"]
    start_urls = ["https://www.shijigroup.com/reviewpro-reputation"]

    def parse(self, response):
        products = []
        for product in response.css("div.nav-side-pannel__el"):
            product_sections = []
            product_title = product.css("p.nav-side-pannel__title::text").get(default="").strip()
            href = product.xpath("./a/@href").get()
            product_url = response.urljoin(href) if href else None
            for section in product.xpath(".//ul[@role='list']/li"):
                section_title = section.xpath("./a/text()").get(default="").strip()
                href = section.xpath("./a/@href").get()
                section_url = response.urljoin(href) if href else None
                product_sections.append({"title": section_title, "url": section_url})
            products.append({"title": product_title, "url": product_url, "sections": product_sections})

        solutions = []
        for solution in response.xpath("//div[contains(@class,'is--solution')]/following-sibling::div//div[@data-w-tab='All']//a[contains(@class,'solutions__card')]"):
            solution_title = solution.xpath("./div/p/text()").get(default="").strip()
            href = solution.xpath("./@href").get()
            solution_url = response.urljoin(href) if href else None
            solutions.append({"title": solution_title, "url": solution_url})

        if not solutions and not products:
            self.logger.warning("No data extracted from %s", response.url)

        yield PageItem(
            source_url=response.url,
            solutions=solutions,
            products=products,
        )