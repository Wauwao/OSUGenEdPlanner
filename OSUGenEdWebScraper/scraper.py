from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
chrome_options = Options() 
chrome_options.add_experimental_option("detach", True)
#Creates a webdriver to manipulate the starting page
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://courses.erppub.osu.edu/psc/ps/EMPLOYEE/PUB/c/COMMUNITY_ACCESS.OSR_CAT_SRCH.GBL?PortalActualURL=https%3a%2f%2fcourses.erppub.osu.edu%2fpsc%2fps%2fEMPLOYEE%2fPUB%2fc%2fCOMMUNITY_ACCESS.OSR_CAT_SRCH.GBL&PortalRegistryName=EMPLOYEE&PortalServletURI=https%3a%2f%2fcourses.erppub.osu.edu%2fpsp%2fps%2f&PortalURI=https%3a%2f%2fcourses.erppub.osu.edu%2fpsc%2fps%2f&PortalHostNode=CAMP&NoCrumbs=yes&PortalKeyStruct=yes")
courseAttributes = []
for i in range(1, 8):
    courseAttributes.append("F" + str(i))
#Finds the input form for the course attribute and course attribute value and input necessary data
courseAttribute = driver.find_element(By.NAME, "OSR_CAT_SRCH_WK_CRSE_ATTR")
courseAttribute.send_keys("GE2")
for attribute in courseAttributes:
    courseAttributeValue = driver.find_element(By.NAME, "OSR_CAT_SRCH_WK_CRSE_ATTR_VALUE")
    courseAttributeValue.clear()
    courseAttributeValue.send_keys(attribute)
    #Clicks the search button to load the list of courses
    driver.find_element(By.NAME, "OSR_CAT_SRCH_WK_BUTTON1").click()
    wait = WebDriverWait(driver, 10)
    time.sleep(1)
    #Check if the courses loaded has more than 1 page
    isPresent = driver.find_elements(By.ID, "OSR_CAT_SRCH_WK_BUTTON_FORWARD")
    #Don't look for a forward buttton if there is only one page
    if len(isPresent) == 0:
        #Waits until a course loads
        wait.until(EC.presence_of_element_located((By.ID, "OSR_CAT_SRCH_OSR_CRSE_HEADER$0")))
        #Gets all the courses
        courseTitles = driver.find_elements(By.CLASS_NAME, "PSQRYTITLE")
        courseTitles.pop(0)
        courseDescriptions = driver.find_elements(By.CLASS_NAME, "PSLONGEDITBOX")
        for title in courseTitles:
            print(title.text)
        for description in courseDescriptions:
            print(description.text)
        numCoursesOnPage = int(courseDescriptions[-1].get_attribute("id")[-2:])
        for unitIndex in range(numCoursesOnPage):
            idToSearch = "OSR_CAT_SRCH_OSR_UNITS_DESCR$" + str(unitIndex)
            print(driver.find_element(By.ID, idToSearch).text)

    else:
        wait.until(EC.presence_of_element_located((By.ID, "OSR_CAT_SRCH_WK_BUTTON_FORWARD")))
        onceMore = iter([True, False])
        while driver.find_element(By.ID, "OSR_CAT_SRCH_WK_BUTTON_FORWARD").is_enabled() or next(onceMore):
            wait.until(EC.presence_of_element_located((By.ID, "OSR_CAT_SRCH_OSR_CRSE_HEADER$0")))
            courseTitles = driver.find_elements(By.CLASS_NAME, "PSQRYTITLE")
            courseTitles.pop(0)
            courseDescriptions = driver.find_elements(By.CLASS_NAME, "PSLONGEDITBOX")
            for title in courseTitles:
                print(title.text)
            for description in courseDescriptions:
                print(description.text)
            numCoursesOnPage = int(courseDescriptions[-1].get_attribute("id")[-2:])
            for unitIndex in range(numCoursesOnPage):
                idToSearch = "OSR_CAT_SRCH_OSR_UNITS_DESCR$" + str(unitIndex)
                print(driver.find_element(By.ID, idToSearch).text)
            #Finds and clicks the next page button
            driver.find_element(By.ID, "OSR_CAT_SRCH_WK_BUTTON_FORWARD").click()
            time.sleep(1)
            wait.until(EC.presence_of_element_located((By.ID, "OSR_CAT_SRCH_WK_BUTTON_FORWARD")))
    #Go back to the course attribute page
    time.sleep(1)
    wait.until(EC.presence_of_element_located((By.ID, "OSR_CAT_SRCH_WK_HYPERLINK")))
    driver.find_element(By.ID, "OSR_CAT_SRCH_WK_HYPERLINK").click()
    time.sleep(1)
