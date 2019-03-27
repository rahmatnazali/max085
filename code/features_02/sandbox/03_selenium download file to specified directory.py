from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : 'download'}
chrome_options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome('/home/rahmat/PycharmProjects/Selenium Driver/chromedriver', chrome_options=chrome_options)
driver.get('https://notepad-plus-plus.org/repository/7.x/7.6.4/npp.7.6.4.bin.minimalist.7z')



"""
possible alternative

prefs = {'download.prompt_for_download': False,
         'download.directory_upgrade': True,
         'safebrowsing.enabled': False,
         'safebrowsing.disable_download_protection': True}

options.add_argument('--headless')
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)
driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
driver.desired_capabilities['browserName'] = 'ur mum'
params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': r'C:\chickenbutt'}}
self.driver.execute("send_command", params)

"""