import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

sleep_time = 0.2


def Automation(url, filename):
    page_source = requests.get(url).text

    soup = BeautifulSoup(page_source, "lxml")

    # Names and Address of the Targets
    names = soup.find_all(
        "div", class_="src-domain-geoentity-GeoentityListItem__name--2ThYA"
    )

    start_name = soup.find(
        "h1", class_="src-domain-geoentity-GeoentityCardHeader__title--3TmoS"
    )

    addresses = soup.find_all(
        "div", class_="src-domain-geoentity-GeoentityListItem__text--2gkVp"
    )

    start_address = soup.find(
        "h2", class_="src-domain-geoentity-GeoentityCardHeader__type--1IEFd"
    )

    names = list(names)
    names.insert(0, start_name)

    addresses = list(addresses)
    addresses.insert(0, start_address)

    # Link of the targets(hrefs)
    List_of_a_tags = list()
    for a in soup.find_all(
        "a", class_="src-domain-geoentity-GeoentityListItem__link--3zK_-", href=True
    ):
        List_of_a_tags.append(a["href"])

    Numbers = list()
    Sites = list()

    number, site = numbers(url)
    Numbers.append(number)
    Sites.append(site)

    for link in List_of_a_tags:
        full_url = "https://fr.mappy.com" + link
        number, site = numbers(full_url)
        Numbers.append(number)
        Sites.append(site)

    try:
        file = open(filename + ".txt", "a")
        for i in range(len(Numbers)):
            file.write("Name: " + names[i].text + "\n")
            file.write("Address: " + addresses[i].text + "\n")
            file.write("Phone No.: " + Numbers[i] + "\n")
            file.write("Site Url: " + Sites[i] + "\n")
            file.write("\n\n")
        file.close()
    except:
        pass


def numbers(full_url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome("./chromedriver.exe", options=options)

    driver.get(full_url)
    driver.find_element_by_id("didomi-notice-agree-button").click()
    check = driver.page_source
    soup = BeautifulSoup(check, "lxml")
    find_check_divs = soup.find_all(
        "span",
        class_="src-domain-genericComponents-CircledButtonWithLabel__container--2_mGj",
    )
    find_check_divs = list(find_check_divs)

    site_url = ""
    try:
        if find_check_divs[0].text == "Site web":
            driver.find_element_by_class_name(
                "src-domain-genericComponents-CircledButtonWithLabel__container--2_mGj"
            ).click()
            driver.switch_to.window(driver.window_handles[1])
            site_url = driver.current_url
            driver.switch_to.window(driver.window_handles[0])
        else:
            site_url = "None"
    except:
        site_url = "None"

    phone_number = ""
    try:
        if find_check_divs[0].text == "Téléphone":
            driver.find_element_by_class_name(
                "src-domain-genericComponents-CircledButtonWithLabel__container--2_mGj"
            ).click()
        elif find_check_divs[1].text == "Téléphone":
            driver.find_element_by_xpath(
                '//*[@id="app"]/div/div[3]/div/div[1]/div[1]/div/div[2]/div/span/span'
            ).click()
        elif find_check_divs[2].text == "Téléphone":
            driver.find_element_by_xpath(
                '//*[@id="app"]/div/div[3]/div/div[1]/div[1]/div/div[3]/div/span/span'
            ).click()

        time.sleep(0.7)
        phone_number = driver.find_element_by_class_name(
            "src-domain-genericComponents-SimplePhoneCartridge__SimplePhoneCartridge--1E-p-"
        ).text
    except:
        phone_number = "None"

    driver.quit()
    return phone_number, site_url


if __name__ == "__main__":

    url = input("Enter your url:")
    filename = input("Enter filename:")
    Automation(url, filename)
