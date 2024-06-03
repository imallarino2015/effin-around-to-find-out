import json

import requests
from lxml import html

from WebAutomation import RequestHelper


def search(keyword: str, store_name: str | None = None) -> list[dict]:
    params = {
        "_nkw": keyword,
        "_ssn": store_name
    }
    response = requests.get(f"https://www.ebay.com/sch/i.html", params=params)
    print(response)

    if not response.ok:
        raise RequestHelper.NetworkError(response)

    soup = html.fromstring(response.content, "lxml")

    return [
        {
            "link": result.xpath(".//a")[0].get("href").split("?")[0].strip(),
            "name": "".join(result.xpath(".//span[@role='heading']")[0].itertext()).strip(),
            "condition": "".join(result.xpath(".//span[@class='SECONDARY_INFO']")[0].itertext()).strip(),
            "price": "".join(result.xpath(".//span[@class='s-item__price']")[0].itertext()).strip(),
            "seller": "".join(result.xpath(".//span[@class='s-item__seller-info-text']")[0].itertext()).strip().split(" ")[0],
            "rating": {
                "star_rating": "".join(result.xpath(".//div[@class='x-star-rating']/span[@class='clipped']")[0].itertext()).strip(),
                "review_count": "".join(result.xpath(".//span[@class='s-item__reviews-count']/span")[0].itertext()).strip()
            } if len(result.xpath(".//div[@class='s-item__reviews']")) > 0 else None
        }
        for result
        in soup.xpath("//div[@id='srp-river-results']/ul/li[contains(normalize-space(@class), 's-item')]")
    ]


def get_product_info(url) -> dict:
    response = requests.get(url)
    print(response)

    if not response.ok:
        raise RequestHelper.NetworkError(response)

    soup = html.fromstring(response.content, "lxml")

    options = {
        "".join(selection.xpath(".//span[@class='x-msku__label-text']")[0].itertext()).strip(): [
            "".join(option.itertext()).strip()
            for option
            in selection.xpath(".//select/option")
        ]
        for selection
        in soup.xpath("//div[@class='x-msku__box-cont']")
    }

    if len(soup.xpath("//div[@class='vim x-rating-details']")) > 0:
        ratings_element = soup.xpath("//div[@class='vim x-rating-details']")[0]
        ratings = {
            "overall": "".join(ratings_element.xpath(".//span[@data-testid='review--start--rating']")[0].itertext()).strip(),
            "review_count": "".join(ratings_element.xpath(".//span[@class='ux-summary__count']")[0].itertext()).strip(),
            "review_hist": {
                "".join(rating.xpath(".//p[@class='ux-histogram__item--bar--stars']")[0].itertext()).strip():
                    "".join(rating.xpath(".//div[@class='ux-histogram__item--bar--c']")[0].itertext()).strip()
                for rating
                in ratings_element.xpath(".//div[@class='ux-histogram__item--bar']")
            },
            "review_aspects": {
                "".join(aspect.itertext()).strip():
                    aspect.xpath(".//div[@data-testid='reviews--aspect']")[0].get("data-percent")
                for aspect
                in ratings_element.xpath(".//div[@data-testid='ux-aspect']")
            }
        }
    else:
        ratings = None

    return {
        "id": url.split("/")[-1],
        "name": "".join(soup.xpath("//div[@data-testid='x-item-title']")[0].itertext()).strip(),
        "price": "".join(soup.xpath("//div[@data-testid='x-price-primary']")[0].itertext()).strip(),
        "seller": soup.xpath("//div[@data-testid='x-sellercard-atf']/div/div")[0].get("title").strip(),
        "condition": "".join(soup.xpath("//span[@data-testid='ux-textual-display']")[0].itertext()).strip(),
        "options": options,
        "product_rating": ratings
    }


def get_seller_info(name) -> dict:
    params = {
        "_tab": "feedback"
    }
    response = requests.get(f"https://www.ebay.com/str/{name}", params=params)
    print(response)

    if not response.ok:
        raise RequestHelper.NetworkError(response)

    soup = html.fromstring(response.content, "lxml")

    return {
        "store_id": name,
        "store_name": "".join(soup.xpath("//div[@class='str-seller-card__store-name']")[0].itertext()).strip(),
        "stats": {
            list(shop_stat.itertext())[1].strip():
                "".join(shop_stat.xpath(".//span")[0].itertext()).strip()
            for shop_stat
            in soup.xpath("//div[@class='str-seller-card__stats-content']/div")
        },
        "feedback": {
            "".join(shop_stat.xpath(".//span")[0].itertext()).strip():
                "".join(shop_stat.xpath(".//a/span[@class='INLINE_LINK']")[0].itertext()).strip()
            for shop_stat
            in soup.xpath("//div[@class='fdbk-overall-rating__details']/div")
        },
        "seller_ratings": {
            "".join(shop_stat.xpath(".//div[@class='fdbk-detail-seller-rating__label']")[0].itertext()).strip():
                "".join(shop_stat.xpath(".//span[@class='fdbk-detail-seller-rating__value']")[0].itertext()).strip()
            for shop_stat
            in soup.xpath("//div[@class='fdbk-seller-rating__detailed-list']/div")
        }
    }


def main():
    config = json.load(open("config.json", "r"))

    # log_in(config["username"], config["password"])

    with open("urls") as f:
        file_lines = [
            line.strip()
            for line
            in f.readlines()
        ]

    # print(search("test"))

    # for line in file_lines:
    #     print(line)
    #     try:
    #         if line.startswith("https://www.ebay.com/itm/"):
    #             print(get_product_info(line))
    #         else:
    #             print(get_seller_info(line))
    #     except Exception as e:
    #         print(e)
    #     break


if __name__ == "__main__":
    main()
