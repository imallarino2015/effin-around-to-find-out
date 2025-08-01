import json

import requests
import bs4


"""
TODO:
    Steam user/
    Extract following list
"""


class SteamGame(object):
    store_page = None
    application_config = None

    id = None
    link = None

    name = None
    description = None
    publish_date = None

    base_price = None
    discount = None
    final_price = None

    bundles = None

    is_early_access = None
    has_demo = None

    platforms = None
    sd_compatibility = None

    review_total = None
    review_recent = None

    features = None
    controllers = None
    accessibility_features = None
    drm_notices = None

    def __init__(self, game_name=None, game_id=None):
        assert game_name is not None or game_id is not None
        self.name = game_name
        self.id = game_id

        if self.get_game_link():
            # print("Link found")
            self.fetch_store_page()
            # print(self.store_page)

            if self.name is None:
                self.fetch_name()
            self.fetch_description()
            self.fetch_bundle_info()
            self.fetch_publish_date()
            self.fetch_early_access_status()
            self.fetch_features()
            self.fetch_review()
            self.fetch_price_info()
            self.fetch_platforms()
            self.fetch_steam_deck_status()
            pass
        else:
            print("No link found")

        return

    def get_game_link(self):
        page = 1
        if self.id is not None:
            self.link = f"https://store.steampowered.com/app/{self.id}/"
            return self.link
        while True:
            url = "https://store.steampowered.com/search/?term=" + \
                  self.name.replace(" ", "+") + "&page=" + \
                  str(page)
            print(url)

            response = requests.get(url)
            soup = bs4.BeautifulSoup(response.content, features="lxml")
            results = soup.find_all("a", attrs={"class": "search_result_row"})

            if len(results) > 0:
                for result in results:
                    item_title = result.find("span", attrs={"class": "title"}).text.strip()
                    item_id = result["data-ds-itemkey"].split("_")[1]
                    if item_title == self.name or item_id == self.id:
                        self.name = item_title
                        self.id = item_id
                        self.link = result["href"]
                        self.link = self.link.replace(self.link.split("/")[-1], "")
                        return result["href"]
                page += 1
            else:
                break
        return None

    def fetch_store_page(self):
        response = requests.get(self.link, cookies={"birthtime": "470725201"})
        self.store_page = bs4.BeautifulSoup(response.content, features="lxml")

        return None

    def update_store_page(self):
        if self.store_page is None:
            self.get_game_link()
            self.fetch_store_page()

        return None

    def fetch_application_config(self):
        self.update_store_page()

        app_config_element = self.store_page.find("div", attrs={"id": "application_config"})
        self.application_config = {
            key: json.loads(app_config_element[key])
            for key
            in app_config_element.attrs
            if key.startswith("data-")
        }

        return None

    def fetch_steam_deck_status(self):
        if self.application_config is None:
            self.fetch_application_config()

        if "data-deckcompatibility" not in self.application_config:
            self.sd_compatibility = "Unknown"
        elif "resolved_category" not in self.application_config["data-deckcompatibility"]:
            self.sd_compatibility = "Unknown"
        else:
            match self.application_config["data-deckcompatibility"]["resolved_category"]:
                case 1:
                    self.sd_compatibility = "Unsupported"
                case 2:
                    self.sd_compatibility = "Playable"
                case 3:
                    self.sd_compatibility = "Verified"
                case _:
                    self.sd_compatibility = "Unknown"

        return None

    def fetch_name(self):
        self.update_store_page()

        self.name = self.store_page.find("div", attrs={"id": "appHubAppName"}).text.strip()

        return None

    def fetch_description(self):
        self.update_store_page()

        self.description = self.store_page.find("div", attrs={"class": "game_description_snippet"}).text.strip()

        return None

    def fetch_price_info(self):
        # self.base_price, self.discount, self.final_price = ("", "0", "")
        self.update_store_page()

        game_area_purchase = self.store_page.find("div", attrs={"id": "game_area_purchase"})

        self.has_demo = game_area_purchase.find("div", attrs={"class": "demo_above_purchase"}) is not None

        free_game_button = game_area_purchase.find("div", attrs={"id": "freeGameBtn"})
        if free_game_button is not None:
            self.final_price = " ".join([item for item in game_area_purchase.find("div", attrs={"class": "game_purchase_price price"}).text.split() if item != ""])
            return None

        coming_soon_area = game_area_purchase.find("div", attrs={"class": "game_area_comingsoon"})
        if coming_soon_area is not None:
            self.final_price = " ".join([item for item in coming_soon_area.find("h1").text.split() if item != ""])
            return None

        game_area_wrappers = game_area_purchase.find_all("div", attrs={"class": "game_area_purchase_game_wrapper"})
        game_purchase_elements = [
            game_area_wrapper
            for game_area_wrapper
            in game_area_wrappers
            if "dynamic_bundle_description" not in game_area_wrapper["class"]
        ]

        if len(game_purchase_elements) < 1:
            return None
        else:
            game_purchase_element = game_purchase_elements[0].find("div", attrs={"class", "game_purchase_action_bg"})

        price_element = game_purchase_element.find("div", {"class": "game_purchase_price"})
        if price_element is not None:
            self.base_price = price_element.text.strip()
            self.final_price = price_element.text.strip()
        else:
            price_element = game_purchase_element.find("div", {"class": "game_purchase_discount"})
            if price_element is not None:
                self.base_price = price_element.find("div", attrs={"class", "discount_original_price"}).text.strip()
                self.discount = price_element.find("div", attrs={"class", "discount_pct"}).text.strip()
                self.final_price = price_element.find("div", attrs={"class", "discount_final_price"}).text.strip()
            else:
                self.base_price = game_purchase_elements[1].find("div", attrs={"class", "discount_original_price"}).text.strip()
                self.discount = game_purchase_elements[1].find("div", attrs={"class", "discount_pct"}).text.strip()
                self.final_price = game_purchase_elements[1].find("div", attrs={"class", "discount_final_price"}).text.strip()

        self.base_price = float(self.base_price.replace("$", "").strip())
        self.discount = float(self.discount.replace("%", "").strip())
        self.final_price = float(self.final_price.replace("$", "").strip())
        # TODO: get currency type
        return None

    def fetch_early_access_status(self):
        self.update_store_page()

        self.is_early_access = len(self.store_page.find_all("div", attrs={"class": "early_access_header"})) > 0

        return None

    def fetch_features(self):
        self.update_store_page()

        feature_element_container = self.store_page.find("div", attrs={"class": "game_area_features_list_ctn"})
        feature_elements = feature_element_container.find_all("div", attrs={"class": "label"})
        if len([feature_elements]) > 0:
            self.features = [
                feature_element.text.strip()
                for feature_element
                in feature_elements
            ]

        controller_element = self.store_page.find("div", attrs={"data-featuretarget": "store-sidebar-controller-support-info"})
        if controller_element is not None:
            self.controllers = json.loads(controller_element.get("data-props"))

        accessibility_feature_element = self.store_page.find("div", attrs={"data-featuretarget": "store-sidebar-accessibility-info"})
        if accessibility_feature_element is not None:
            self.accessibility_features = json.loads(accessibility_feature_element.get("data-props"))

        drm_notice_elements = self.store_page.find_all("div", attrs={"class": "DRM_notice"})
        if len(drm_notice_elements) > 0:
            self.drm_notices = [
                drm_notice_element.text.strip().replace(b"\xa0".decode(encoding="windows-1252"), " ")
                for drm_notice_element
                in drm_notice_elements
            ]

        return None

    def fetch_platforms(self):
        self.update_store_page()

        platform_container = self.store_page.find("div", attrs={"class": "game_area_purchase_platform"})
        if platform_container is not None:
            self.platforms = [
                platform["class"][1]
                for platform
                in platform_container.find_all("span", attrs={"class": "platform_img"})
            ]
        else:
            self.platforms = None

        return None

    def fetch_bundle_info(self):
        self.update_store_page()

        self.bundles = [
            {
                "bundle_name": bundle.find("h2").text.replace("BUNDLE", "").replace("(?)", "").strip(),
                **json.loads(bundle["data-ds-bundle-data"])
            }
            for bundle
            in self.store_page.find_all("div", attrs={"class": "dynamic_bundle_description"})
        ]

        return None

    def fetch_publish_date(self):
        self.update_store_page()

        date_element = self.store_page.find("div", attrs={"class": "release_date"}).find("div", attrs={"class": "date"})
        self.publish_date = date_element.text if date_element is not None else None

        return None

    def fetch_review(self):
        self.update_store_page()

        review_elem = self.store_page.find("div", attrs={"id": "userReviews"})
        match review_elem.find_all("a", attrs={"class": "user_reviews_summary_row"}):
            case [x]:
                if "data-tooltip-html" in x:
                    self.review_total = (
                        x["data-tooltip-html"].strip().split()[0],
                        x["data-tooltip-html"].strip().split()[3]
                    )
                else:
                    self.review_total = (
                        x.find("span", attrs={"class": "not_enough_reviews"}).text.strip()
                        if x.find("span", attrs={"class": "not_enough_reviews"}) is not None
                        else None,
                        x.find("span", attrs={"class": "responsive_reviewdesc"}).text.strip()
                        if x.find("span", attrs={"class": "responsive_reviewdesc"}) is not None
                        else None
                    )
                self.review_recent = (None, None)
            case [x, y, *_]:
                self.review_recent = (
                    x["data-tooltip-html"].strip().split()[0],
                    x["data-tooltip-html"].strip().split()[3]
                )
                self.review_total = (
                    y["data-tooltip-html"].strip().split()[0],
                    y["data-tooltip-html"].strip().split()[3]
                )
            case _:
                pass

        return None

    def __iter__(self):
            yield "ID",                       self.id
            yield "Link",                     self.link

            yield "Name",                     self.name
            yield "Description",              self.description
            yield "Publish Date",             self.publish_date

            yield "Base Price",               self.base_price
            yield "Discount %",               self.discount
            yield "Final Price",              self.final_price

            yield "Bundles",                  self.bundles

            yield "Early Access",             self.is_early_access
            yield "Has Demo",                 self.has_demo

            yield "Platforms",                self.platforms
            yield "Steam Deck Compatibility", self.sd_compatibility

            yield "Overall Review",           self.review_total
            yield "Recent Review",            self.review_recent

            yield "Features",                 self.features
            yield "Controllers",              self.controllers
            yield "Accessibility Features",   self.accessibility_features
            yield "DRM Notices",              self.drm_notices

    def __str__(self):
        game_details = dict(self)
        return "\n".join([
            str(key) + ": " + str(game_details[key])
            for key
            in game_details.keys()
            if game_details[key] is not None
        ])


def test():
    return 0


if __name__ == "__main__":
    test()
