from selenium import webdriver
from urllib.request import Request, urlopen
from time import sleep
from bs4 import BeautifulSoup
from os import makedirs
import csv


class treatment():
    def InitialiseBrowser(self):
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(executable_path=r"C:\Users\jayra\Downloads\chromedriver_win32\driver.exe", options=options)
        driver.implicitly_wait(30)
        return driver

    def CreateDirectory(self):
        makedirs("D:\\Disease Images", exist_ok=True)

    def DownloadImage(self, image_url, image_name):
        self.CreateDirectory()    # creating a directory to sdownload image icons
        q = Request(url=image_url, headers={'User-Agent': 'Mozilla/5.0'})    # sending an request to download image icon and using header agents to avoid 404 bad request exception
        image_data = urlopen(q).read()    # reading the binary data of the request response
        file_path = "D:\\Disease Images\\"+image_name.replace("/", " ")+".png"
        with open(file_path, "wb") as file:
            file.write(image_data)    # writing that binary data into .png file
        return file_path

    def WriteDataIntoCSV(self, data):
        with open('Disease.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)    # writing the data into csv file and csv file is stored in the current working directory (CWD)

    def scrapeInfo(self, browser):
        alphabet_disease_list = [["Disease Name", "Link", "Icon Path"]]
        browser.get("https://dermnetnz.org/image-library/")
        aplhabet_elements_list = browser.execute_script("return document.getElementsByClassName('imageList')")
        if aplhabet_elements_list:
            for aplhabet_element in aplhabet_elements_list:
                html_content = aplhabet_element.get_attribute('outerHTML')
                soup = BeautifulSoup(html_content, 'html.parser')
                imageList_group_content = soup.find(class_='imageList__group')
                if imageList_group_content:
                    flex_group_content = imageList_group_content.find(class_='flex')
                    if flex_group_content:
                        imageList__group__item = flex_group_content.find_all(class_='imageList__group__item')
                        if imageList__group__item:
                            for dieaese_element in imageList__group__item:
                                disease_list = []
                                disease_list.append(dieaese_element.text.strip())    # extracting name
                                #print("Disease name ---- "+ dieaese_element.text.strip())  # strip is used to remove leading and trailing spaces
                                scrapImage = dieaese_element.find(class_='imageList__group__item__image')
                                if scrapImage:
                                    img_tag = scrapImage.find('img')
                                    if img_tag is not None:
                                        #print('Disease URL ------ '+ img_tag['src'])
                                        file_path = self.DownloadImage(img_tag['src'], dieaese_element.text.strip())    # downloading image icons
                                        disease_list.append(img_tag['src'])    # extracting links
                                        disease_list.append(file_path)    # appending file name
                                        alphabet_disease_list.append(disease_list)
                                        sleep(2)
                                #print('`````````````````````````````````````````````&&&&&&&&&&&&&&&&&')
                        else:
                            print('imageList__group__item not found')
                    else:
                        print('flex class not found')
                else:
                    print('imageList_group_content not found')
            if alphabet_disease_list:
                self.WriteDataIntoCSV(alphabet_disease_list)    # writing the data into csv file
        else:
            print("No web elements found")
            
    def ExtractingData(self):
        browser = self.InitialiseBrowser()
        self.scrapeInfo(browser)


if __name__ == '__main__':
    Treatment = treatment() 
    try:
        Treatment.ExtractingData()
    except:
        print("not working")
 