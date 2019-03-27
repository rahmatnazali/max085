
"""
Webdriver Options
"""

WebDriverPath = 'path/to/your/webdriver.exe'
UseProxies              = True or False
ShowBrowserWindows      = True or False


"""
Credentials Option
"""
LoginPage = "https://example.com/login"
Credential = "user12:pass12" # accepts emails too
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


IntervalsBetweenFiles   = 10 # this is a custom intervals in seconds between each XPath download button click
IntervalsBetweenUrls    = 10 # this is a custom intervals in seconds to move from each URL to the next
URLCountToSwitch        = 20 # every # of URLS completed, clear cookies (logout), set next custom proxy, login(different account), continue




"""
Save/Directory options
"""

SaveDirectory           = 'C:\Script\Zipfiles'
DefaultSaveDirectory    = 'result'




"""
Anti Captcha options

1 -> Show captcha in browser window and prompt the user to solve it
2 -> anti-captcha.com service
"""
ReCaptchaOption         = 1
AntiCaptchaAPIKey       = "dce6bcbb1a728ea8d563de6d169a2057"
