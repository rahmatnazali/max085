"""
Configuration files for Feature 2
"""


"""
Webdriver Options

For now, the default will be using Chrome webdriver.

UseProxies
True: will obtain proxy from Proxies.txt
False: browser will run without proxy enabled.

ShowBrowserWindows
True: browser will be shown
False: browser will be run in headless mode

"""

WebDriverPath = '/home/rahmat/PycharmProjects/Selenium Driver/chromedriver'
ShowBrowserWindows      = True or False

# todo: separate login and proxy instance
UseProxies              = False
RequireLogin=True or False

# request header for requests module
RequestHeader = {
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

"""
Credentials Option
"""
LoginPage = "https://example.com/login"
Credentials = ["user12:pass12", "user13:pass13"] # accepts emails too. example: max@gmail.com:password123
XPathLoginSuccessProof = '//p' # any element that shows when login is success. if not found, code will throw "login failed"

XPathFormUserOrEmail    = '//*[@id="user"]'
XPathFormPassword       = '//*[@id="pass"]'
XPathRecaptcha          = '//*[@id="recaptcha-anchor"]/div[1]'
XPathLoginButton        = '//*[@id="login"]'

LoginTimeout            = 30 # will wait 30 second until login seems to completed




"""
Scrapping options
"""

# XPathFiles              = (
#     '/html/body/div[1]/div/div/a',
#     '//*[@id="Download"]" , "//*[@id="button"]'
# )

# add test from apkpure.com
XPathFiles = (
    '//dl/dd[@class = "down"]/a[@href]',
    # '//dl/dd/a[@href]',
    # '/html/body/div[3]/div[4]/div/ul/li[3]/dl/dd[4]/a',
    # '/html/body/div[3]/div[4]/div/ul/li[3]/dl/dd[4]/a',
)



"""
This is an Xpath that links to any (single) element in the page after login.
We need to have this to ensure that the login process is succeed.


You need to define any element that you thing will be there after login process succeed.
The most common thing is to scrap a "Logout" text in the upper right of screen.

It can reallly be *any* element that are guaranteed to be there after login succeed, and wont be there if login failed
"""
LoggedInXPath = '//*[@class="logged_in"]'



"""
This is a custom intervals in seconds between each XPath download button click (or) when downloading with request

Give it an integer -> it will wait for a fixed time
Give it a tuple -> it will wait for a range of time

example
20 -> fixed wait for 20 seconds
(20, 30) -> randomly wait between 20 to 30 seconds
"""

# IntervalsBetweenFiles   = 10
IntervalsBetweenFiles   = (1, 5)



"""
This is a custom intervals in seconds to move from each URL to the next

Give it an integer -> it will wait for a fixed time
Give it a tuple -> it will wait for a range of time

example
20 -> fixed wait for 20 seconds
(20, 30) -> randomly wait between 20 to 30 seconds
"""
# IntervalsBetweenUrls    = 10
IntervalsBetweenUrls    = (20, 30)




"""
Limit of used proxy and credentials.

Every # of URLS completed, clear cookies (logout), set next custom proxy, login(different account), continue
"""
URLCountToSwitch        = 20




"""
Save/Directory options

Make SaveDirectory to empty string '' and code will look at DefaultSaveDirectory.
"""

SaveDirectory           = 'C:\Script\Zipfiles'
DefaultSaveDirectory    = 'download'




"""
Anti Captcha options

1 -> Show captcha in browser window and prompt the user to solve it
2 -> anti-captcha.com service
"""
ReCaptchaOption         = 1
AntiCaptchaAPIKey       = "dce6bcbb1a728ea8d563de6d169a2057"






"""
To Test 
(Not actually requesting)
value: True | False
"""

TestMode = True




"""
To Debug
Will print every data verbosely
value: True | False
"""

DebugMode = False





"""
Download file mode: sequential or not.

True -> will check for file completion and wait for interval. Download is made by requests module
False -> will NOT check for file completion. Just wait for interval. Download is made by selenium
"""
SequentialFiles = False

