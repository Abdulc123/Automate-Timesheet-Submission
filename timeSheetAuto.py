from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from drexelHelper import password, username 
from datetime import datetime
authentication_code = "584965"

url = "https://connect.drexel.edu/idp/profile/cas/login?"

# Hours for time in and time out in the format "HH:MM" in the lists below
mondayTimes =    ["9:00", "11:00", "12:00", "12:30", "4:00", "5:00"]
tuesdayTimes  =  ["12:00", "3:30"]
wednesdayTimes = ["9:00", "11:00", "12:00", "12:30"]
thursdayTimes =  ["9:00", "12:00", "1:00", "2:00", "3:00", "3:30" ]
fridayTimes =    ["12:00", "2:00", "3:00", "5:00"]

week_dic = {}
week_dic["Monday Times"] = mondayTimes 
week_dic["Tuesday Times"] = tuesdayTimes
week_dic["Wednesday Times"] = wednesdayTimes
week_dic["Thursday Times"] = thursdayTimes
week_dic["Friday Times"] = fridayTimes

CompleteFully = False

driver =  webdriver.Chrome()
driver.get(url)
wait = WebDriverWait(driver, 10)

def checkValidTimes(dayHours, nameOfList):
    # If len is not even it will raise an valueError
    if len(dayHours) % 2 != 0:
        raise ValueError (f"{nameOfList} does not have an even number of time inputs")
    elif len(dayHours) > 10:
        raise ValueError (f"{nameOfList} should only have a maximum of 10 entries inside. Currently It has {len(dayHours)} entries")
    for time_str in dayHours:
        try: 
            # Attempt to parse the time string using the datetime module
            datetime.strptime(time_str, '%H:%M')
        except ValueError:
            error_message = (f"'{time_str}' is not in the correct format for time (HH:MM) " f"in the list [{nameOfList}]")
            raise ValueError(error_message)

def GotoTimeSheetPage():
    time.sleep(.4)

    # Find the username and password input fields and submit button
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "j_username")))
    password_field = wait.until(EC.presence_of_element_located((By.NAME, "j_password")))
    submit_button = wait.until(EC.presence_of_element_located((By.NAME, "_eventId_proceed"))) # You need to inspect the HTML to find the correct name or ID for the submit button

    # Enter your credentials
    username_field.send_keys(username)
    password_field.send_keys(password)

    # Submit the login form
    submit_button.click()
    print("Clicked the Connect button.")

    authentication_code_input = wait.until(EC.presence_of_element_located((By.ID, "j_mfaToken")))

    # Input the authentication code and click "CONNECT" again
    authentication_code_input.send_keys(authentication_code)

    # Find the "CONNECT" button in the two-step authentication form and click it
    authenetication_button = driver.find_element(By.CSS_SELECTOR, ".btn-success")
    authenetication_button.click()
    print("Connect Button Clicked")

    # Wait for the Time Reporting link 
    banner_web_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@class='btn btn-primary' and contains(@href, 'bmenu.P_MainMnu')]"))
    )
    # Click the "BannerWeb" link
    banner_web_link.click()
    print("Banner Web Button Clicked")

    employee_services_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/span/map/table/tbody/tr[1]/td/table/tbody/tr/td[3]/a"))
    )
    # Click the "Employee Services" link
    employee_services_link.click()
    print("Employee service button Clicked")

    # Wait for the "Time Reporting" link to be clickable
    time_reporting_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/table[1]/tbody/tr[5]/td[2]/a"))
    )
    # Click the "Time Reporting" link
    time_reporting_link.click()
    print("Time Reporting Link Clicked")

    # Wait for the "Time Sheet" link to be clickable
    time_sheet_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/table[1]/tbody/tr[1]/td[2]/a"))
    )
    # Click the "Time Sheet" link
    time_sheet_link.click()
    print("Time Sheet Link Clicked")

    # Wait for the "Time Sheet" submit button to be clickable
    go_to_time_sheet = wait.until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/form/table[2]/tbody/tr/td/input"))
    )
    # Click the "Time Sheet" submit button
    go_to_time_sheet.click()
    print("Succesfully Reached Time Sheet Page")

def getTotalTime(weekData):
    for timeLists in weekData.values():
        for times in timeLists:
            hours, minutes = map(int, times.split(':'))



def checkIfPM(time_str):
   # Split the time string into hours and minutes
    hours, minutes = map(int, time_str.split(':'))

    # Check if the time is between 9:00 AM and 11:59 AM
    if 9 <= hours <= 11:
        return False
    # Check if the time is between 12:00 PM and 5:59 PM
    elif 12 <= hours <= 17:
        return True
    # Otherwise, the time is in the evening (PM)
    else:
        return True
        
def swapToPM(zpath):
    clickPM = wait.until(
        EC.element_to_be_clickable((By.XPATH, zpath))
    )
    clickPM.click()

def writeInTextBox(zpath, time_txt):
    # Select the textbox 0 time in
    textBox = driver.find_element(By.XPATH, zpath) #'/html/body/div[3]/form/table[2]/tbody/tr[2]/td[2]/input'
    # Clear the "textbox" 0 time in
    textBox.clear()
    textBox.send_keys(time_txt)

def clearTextBox(zpath):
    # Select the textbox 0 time in
    textBox = driver.find_element(By.XPATH, zpath) #'/html/body/div[3]/form/table[2]/tbody/tr[2]/td[2]/input'
    # Clear the "textbox" 0 time in
    textBox.clear()

def fillInTimes(weekData):
    for listName , timeLists in weekData.items():
        row = 2 # Initalize for start of time entries
        column = 2
        for i in range(len(timeLists)):

            writeInTextBox(f'/html/body/div[3]/form/table[2]/tbody/tr[{row}]/td[{column}]/input', timeLists[i])
            #print(f" List = {listName} i = {i} time = {timeLists[i]} ||| PM Status = {checkIfPM(timeLists[i])}")
            column += 1
            #time.sleep(1)

            if checkIfPM(timeLists[i]):
                swapToPM(f'/html/body/div[3]/form/table[2]/tbody/tr[{row}]/td[{column}]/select/option[2]')
            column += 1
            #time.sleep(1)

            if timeLists[i]  == timeLists[-1]:
                break
            elif column > 5:
                column = 2
                row += 1
            #time.sleep(1)

        if listName != "Friday Times":
            nextDayLink = driver.find_element(By.XPATH, '/html/body/div[3]/form/table[3]/tbody/tr[1]/td/input[3]')
            nextDayLink.click()

# maybe create a restart function to avoid errors and call it after reaching timesheetpage
def restartTimeSheet():
    restartButton = wait.until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/table[1]/tbody/tr[5]/td/form/table[2]/tbody/tr/td[5]/input'))
    )
    restartButton.click()

    confirmRestartButton = wait.until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/form/table[1]/tbody/tr/td[3]/input'))
    )
    confirmRestartButton.click()

def MondayFillSheetHomeLoop():
    # Wait for the Monday link to be clickable
    MondayLink = wait.until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/table[1]/tbody/tr[5]/td/form/table[1]/tbody/tr[2]/td[8]/div/a"))
    )
    # Click the "Monday" link
    MondayLink.click()
    # fill in time slots for monday through friday
    fillInTimes(week_dic)

    # Go back to Home Time Sheet page by pressing "Time Sheet" when on friday
    HomeSheet = wait.until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/form/table[3]/tbody/tr[1]/td/input[1]'))
    )
    HomeSheet.click()
    

try:
    for listName, dayHours in week_dic.items():
        checkValidTimes(dayHours, listName)
    
    # Continue with other code here if checkValidTimes succeeds
    GotoTimeSheetPage() 

    restartTimeSheet()

    MondayFillSheetHomeLoop()

    NextWeekLink = wait.until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/table[1]/tbody/tr[5]/td/form/table[2]/tbody/tr/td[6]/input')))
    NextWeekLink.click()

    MondayFillSheetHomeLoop()

    if CompleteFully:
        SubmitForApprovalPage = wait.until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/table[1]/tbody/tr[5]/td/form/table[2]/tbody/tr/td[4]/input')))
        SubmitForApprovalPage.click()

    time.sleep(120)
    print("Successfully Completed Time Sheet for blank hours")

except ValueError as e:
    # Halts code when error occurs
    print(f"Error: {e}")
