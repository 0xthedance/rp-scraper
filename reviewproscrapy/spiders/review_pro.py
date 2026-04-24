import scrapy
from reviewproscrapy.items import PageItem

class ReviewProSpider(scrapy.Spider):
    name = "review_pro"
    allowed_domains = ["www.shijigroup.com"]
    start_urls = ["https://www.shijigroup.com/reviewpro-reputation"]

    def parse(self, response):
        products = self._parse_products(response)
        solutions = self._parse_solutions(response)

        if not solutions and not products:
            self.logger.warning("No data extracted from %s", response.url)

        yield PageItem(
            source_url=response.url,
            solutions=solutions,
            products=products,
        )

    def _parse_products(self, response):
        products = []
        for product in response.css("div.nav-side-pannel__el"):
            product_title = product.css("p.nav-side-pannel__title::text").get(default="").strip()
            sections = [
                {"title": section.xpath("./text()").get(default="").strip(), "url": self._extract_url(response, section)}
                for section in product.xpath(".//ul[@role='list']/li/a")
            ]
            products.append({"title": product_title, "url": self._extract_url(response, product.xpath("./a")), "sections": sections})
        return products

    def _parse_solutions(self, response):
        solutions = [
            {"title": s.xpath("./div/p/text()").get(default="").strip(), "url": self._extract_url(response, s)}
            for s in response.xpath("//div[contains(@class,'is--solution')]/following-sibling::div//div[@data-w-tab='All']//a[contains(@class,'solutions__card')]")
        ]
        if not solutions:
            self.logger.warning("Solutions not found in nav, falling back to footer")
            solutions = self._parse_footer_solutions(response)
        return solutions

    def _parse_footer_solutions(self, response):
        footer = response.css("div.footer__top")
        items = footer.xpath(".//p[normalize-space(text())='Solutions']/../following-sibling::div//li/a")
        solutions = [
            {"title": item.xpath("./p/text()").get(default="").strip(), "url": self._extract_url(response, item)}
            for item in items
        ]
        return solutions

    def _extract_url(self, response, node):
        href = node.xpath("./@href").get()
        return response.urljoin(href) if href else None
