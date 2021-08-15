from selenium import webdriver
from bs4 import BeautifulSoup
import time
from tabulate import tabulate

options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--incognito")
options.add_argument("--headless")
driver = webdriver.Chrome("./chromedriver.exe", options=options)

website = "http://portals.au.edu.pk/auresult/"
sleep_time = 0.2
skip_roll_number = 2


class ResultAutomation:
    def __init__(self):
        pass

    def Automation(self, roll_number):
        driver.get(website)
        search_bar = driver.find_element_by_class_name("form-control")
        search_bar.clear()
        search_bar.send_keys(roll_number)
        driver.find_element_by_id("AUContent_btnShow").click()
        time.sleep(sleep_time)
        page_source = driver.page_source

        soup = BeautifulSoup(page_source, "lxml")

        try:
            # Get Information Code
            data_table = soup.find("table", id="AUContent_DataList1")
            information = data_table.find("td").text
            information = (
                information.replace("  ", "").replace("\n\n", "\n").split("\n")
            )
            data = []
            for each in information:
                data.append([each])
            print(tabulate(data, headers=["Personal Information"], tablefmt="rst"))

            # Get Result Code
            result_table = soup.find("table", id="AUContent_GridView1")
            result_table_trs = result_table.find_all("tr")

            result_table_tds = []
            for tr in result_table_trs:
                tds = tr.find_all("td")
                temp = []
                for td in tds:
                    temp.append(td.text)
                result_table_tds.append(temp)

            print(
                tabulate(
                    result_table_tds,
                    headers=["Subject", "Credit Hour", "Grade"],
                    tablefmt="rst",
                )
            )

            result_gpa = soup.find("span", id="AUContent_lbl_gpa").text
            print("GPA: " + result_gpa)
            print("=" * 70)
            print("\n")
        except:
            pass

    def Process(self, start, end):
        for roll_number in range(start, end + skip_roll_number, skip_roll_number):
            self.Automation(roll_number)


if __name__ == "__main__":

    print("1) List of Roll Number\n2) Single Roll Number\n")
    choice = int(input("Enter your choice:"))

    AOBJ = ResultAutomation()

    if choice == 1:
        start_roll_number = int(input("Enter Starting Roll Number:"))
        end_roll_number = int(input("Enter End Roll Nunber:"))
        AOBJ.Process(start_roll_number, end_roll_number)
    elif choice == 2:
        roll_number = int(input("Enter single Roll Number:"))
        AOBJ.Automation(roll_number)
    else:
        print("Invalid Input")
