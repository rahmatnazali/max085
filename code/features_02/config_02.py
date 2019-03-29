
"""
Webdriver Options
"""

# WebDriverPath = 'path/to/your/webdriver.exe'
WebDriverPath = '/home/rahmat/PycharmProjects/Selenium Driver/chromedriver'
UseProxies              = True or False
ShowBrowserWindows      = True or False


"""
Credentials Option
"""
LoginPage = "https://example.com/login"
Credentials = ["user12:pass12", "user13:pass13"] # accepts emails too
XPathLoginSuccessProof = '//p' # any element that shows when login is success. if not found, code will throw "login failed"

XPathFormUserOrEmail    = '//*[@id="user"]'
XPathFormPassword       = '//*[@id="pass"]'
XPathRecaptcha          = '//*[@id="recaptcha-anchor"]/div[1]'
XPathLoginButton        = '//*[@id="login"]'






"""
Scrapping options
"""

XPathFiles              = (
    '/html/body/div[1]/div/div/a',
    '//*[@id="Download"]" , "//*[@id="button"]'
)

"""
This is an Xpath that links to any (single) element in the page after login.
We need to have this to ensure that the login process is succeed.


You need to define any element that you thing will be there after login process succeed.
The most common thing is to scrap a "Logout" text in the upper left of screen.

It can reallly be *any* element that are guaranteed to be there after login succeed, and not there if login failed
"""
LoggedInXPath = '//*[@class="logged_in"]'

"""
This is a custom intervals in seconds between each XPath download button click
"""
IntervalsBetweenFiles   = 10

"""
This is a custom intervals in seconds to move from each URL to the next
"""
IntervalsBetweenUrls    = 10

"""
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
(Not actually requesting. just use the samsung.com's html you gave as an html_page)
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
SequentialFiles = True