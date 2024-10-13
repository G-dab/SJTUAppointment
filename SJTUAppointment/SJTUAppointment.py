from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from datetime import datetime, timedelta


from .utils.captcha_rec import captcha_rec
from .SJTUVenueTabLists import venueTabLists
from .config import JACCOUNT_USERNAME, JACCOUNT_PASSWORD

class SJTUAppointment:
    def __init__(self, task, headless=True):
        self.task = task
        self.tryTimes = 0
        self.ordered_flag = False
        self.venue = task['venue']
        self.venueItem = task['venueItem']
        self.date = task['date']
        self.time = task['time']

        self.user_name = JACCOUNT_USERNAME
        self.password = JACCOUNT_PASSWORD

        self.options = Options()
        if headless:
            self.options.add_argument("-headless") # 无头模式(不显示浏览器界面)
        self.driver = webdriver.Firefox(
            options=self.options)
        self.gen_date()

    # 生成真实日期
    def gen_date(self):
        deltaDays = self.date
        today = datetime.now()
        date = [today + timedelta(days=i) for i in deltaDays]
        self.date = [i.strftime('%Y-%m-%d') for i in date]


    # 打开体育预约网站
    def open_website(self):
        url = 'https://sports.sjtu.edu.cn'
        self.driver.get(url)
        if not self.driver.title == '上海交通大学体育场馆预约平台':
            raise Exception('Target site error.')
    
    # 登录
    def login(self):
        self.open_website()
        sleep(3)
        # 进入登录界面
        try:
            btn = self.driver.find_element('css selector', '#app #logoin button')
            btn.click()
        except:
            raise Exception('Failed to enter login page.')
        # Try 10 times in case that the captcha recognition process goes wrong
        times = 0
        while self.driver.title != '上海交通大学体育场馆预约平台' and times < 10:
            self.driver.refresh()
            sleep(1) # Wait for the captcha image to load
            times += 1

            userInput = self.driver.find_element('name', 'user')
            userInput.send_keys(self.user_name)
            passwdInput = self.driver.find_element('name', 'pass')
            passwdInput.send_keys(self.password)
            captcha = self.driver.find_element('id', 'captcha-img')
            captchaVal = captcha_rec(captcha) # captcha recognition
            userInput = self.driver.find_element('id', 'input-login-captcha')
            userInput.send_keys(captchaVal)
            btn = self.driver.find_element('id', 'submit-password-button')
            btn.click()

        assert times < 10, '[ERROR]: Tryed 10 times, but failed to login, please check the captcha recognition process.'
    
    # 选择场馆
    def searchVenue(self):
        sleep(1)
        # self.driver.get('https://sports.sjtu.edu.cn/pc/#/Venue/1')
        # btn = wait.until(EC.presence_of_element_located(('class name', 'el-button el-button--primary')))
        wait = WebDriverWait(self.driver, 10)
        # next steps are doubled to avoid the bug of the website
        venueInput = wait.until(EC.presence_of_element_located(('class name', 'el-input__inner')))
        venueInput.send_keys(self.venue)
        btn = wait.until(EC.presence_of_element_located(('class name', 'el-button--default')))
        btn.click()

        self.driver.refresh()
        sleep(1)
        venueInput = wait.until(EC.presence_of_element_located(('class name', 'el-input__inner')))
        venueInput.send_keys(self.venue)
        btn = wait.until(EC.presence_of_element_located(('class name', 'el-button--default')))
        btn.click()

        sleep(1)
        btn = wait.until(EC.presence_of_element_located(('class name', 'el-card__body')))
        # btn = self.driver.find_element('class name', 'el-card__body')
        btn.click()
        sleep(1)

    # 选择项目
    def searchVenueItem(self):
        wait = WebDriverWait(self.driver, 10)
        btn = wait.until(EC.presence_of_element_located(('id', venueTabLists[self.venue][self.venueItem])))
        # btn = self.driver.find_element('id', venueTabLists[self.venue][self.venueItem])
        btn.click()

    # 选择日期
    def searchTime(self):
        wait = WebDriverWait(self.driver, 10)
        for date in self.date:
            dateID = 'tab-' + date
            btn = wait.until(EC.presence_of_element_located(('id', dateID)))
            btn.click()
            for time in self.time:
                if self.ordered_flag == False:
                    try:
                        timeSlotId = time - 7
                        # wrapper = self.driver.find_element('class name', 'inner-seat-wrapper')
                        wrapper = wait.until(EC.presence_of_element_located(('class name', 'inner-seat-wrapper')))
                        timeSlot = wrapper.find_elements('class name', 'clearfix')[timeSlotId]
                        seats = timeSlot.find_elements('class name', 'unselected-seat')
                        if len(seats) > 0:
                            seats[0].click()
                            self.confirmOrder()
                            self.ordered_flag = True
                            sleep(1)
                    except Exception as e:
                        print(f'[Strange ERROR]: {e}')
                        sleep(1)

    # 确认预约
    def confirmOrder(self):
        btn = self.driver.find_element('css selector', '.drawerStyle>.butMoney>.is-round')
        btn.click()

        # process notice
        btn = self.driver.find_element('css selector', '.dialog-footer>.tk>.el-checkbox>.el-checkbox__input>.el-checkbox__inner')
        btn.click()
        btn = self.driver.find_element('css selector', '.dialog-footer>div>.el-button--primary')
        btn.click()
        sleep(1)

    def book(self):
        print("Start Booking")
        print(f"venue: {self.venue}\n venueItem: {self.venueItem}\n date: {self.date}\n time: {self.time}")
        try:
            self.searchVenue()
            self.searchVenueItem()
            while self.ordered_flag == False:
                self.searchTime()
                print(f"try {self.tryTimes} times")
                self.tryTimes += 1
                self.driver.refresh()
        except Exception as e:
            print(f"[Book ERROR]: {e}")
            sleep(1)

    def close(self):
        self.worker.close()