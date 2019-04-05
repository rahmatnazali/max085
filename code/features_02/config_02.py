"""
Configuration files for Feature 2
"""


"""
Webdriver Options


- WebDriverPath
Path to your chromedriver.
You can get chromedriver at: http://chromedriver.chromium.org/

For now, the default will be using Chrome webdriver, but you can change it to firefox (gecko driver) if you want.
I will describe how to do it in the code, when webdriver is initialized on lib_common/init_webdriver.


- ShowBrowserWindows
True: browser will be shown
False: browser will be run in headless mode


- UseProxies
True: will obtain proxy from Proxies.txt
False: browser will run without proxy enabled.


- RequireLogin
True: will open a login page, trying to login, and check that curretly logged
False: will skip the login phase


- SequentialFiles
Download file mode: sequential (i.e. using requests module) or not (i.e. using selenium click).
True: The download will be done with requests module in the background. This will check for file completion and wait for interval.
False: The download will be done with selenium click with interval waiting, so this will *not* check for file completion.


- RequestHeatder (dictionary)
This is the default request header for requests module.
This will make the request looks like it came from a Chrome browser
For some case like amazon.com, the site will reject if no appropriate agent (browser) is preset on the request's header


- SaveDirectory
- DefaultSaveDirectory
Save/Directory options.
Make SaveDirectory to empty string '' and code will look at DefaultSaveDirectory.


"""

WebDriverPath = '/home/rahmat/PycharmProjects/Selenium Driver/chromedriver'
ShowBrowserWindows      = True or False

UseProxies              = False
RequireLogin            = True

SequentialFiles         = False

RequestHeader           = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


SaveDirectory           = 'C:\Script\Zipfiles'
DefaultSaveDirectory    = 'download'



"""
Credentials Option

- LoginPage
The link to the login page of a site. This link must directly cotains login form to scrap.


- Credentials (list of string)
This list is for storing credentials with format: USERNAME:PASSWORD
This also accepts emails as the username.

example:

Credentials = [
    "user01:my_secret_password", 
    "user02:my_other_secret_password",
    "max@gmail.com:my_password"
]


- XPathFormUserOrEmail
- XPathFormPassword
- XPathLoginButton

The 3 variables above are each for storing xpath input form regarding Username, password, and the login button.
Code will fill the username and password, and then click the login button.



- LoginTimeout (integer)
This is the amount of seconds to be waited (sleep) until we are sure that login is completed. 
This will vary according to your internet connection and/or proxy speed.

The code will wait explicitly for the XPathLoginSuccessProof (explained below) with a maximum timeout of this variable.
If xpath is found, the code will directly resume without waiting until full sleep.
If xpath is not found until the sleep is end,then the code will declare a warning to show 
that "it is unsure that the login process is succeed"


=== CAPTCHA SECTION ===

Important Note: 
Captcha is famous for a reason. It will effectively kill any bot/scrapper. 
I researched some of anti-captcha API services, and not all of them is reliable. 
Most of them need around 30-60 secs of request just to solve the simplest captcha (reading number/text from picture).
As for this day, I still can not find a service to solve google's captcha.


Should you find a big problem here, it is either to solve manually, or I would suggest this approach as the currently best options:
- First, we will login manually by normal browser, solve captcha, etc
- Then extract all the cookies from your browser (can be sniffed by builtin Chrome's developer tools)
- paste all the cookies (string) to the config.py.
- then webdriver will init the browser with the cookies attached
- webdriver can then access a protected link as if it were accessed from your normal browser

The step-by-step above is litterally doing the login by human, and continue to automate with code with given cookies.
It seems no different with login aoutomatically with bot, but with this way you can be very sure that the login is succeeed,
and the code will not suspect to session error.

Let me know if you want this approach, because currently I did not made it until there.



- ReCaptchaOption (integer)
Option taken when Captcha is found
1: Show captcha in browser window and prompt the user to solve it
2: anti-captcha.com service


- XPathRecaptcha
This xpath is for finding the recaptcha.
If captcha element is found, then there are 2 options (declared in variable ReCaptchaOption):
    - calling anti-captcha service, with the given api (I can not tested it yet until now. Let me know the case if you have)
    - code will wait (forever) until you click/press any key at CLI. So at this time you can solve the captcha at your 
      browser and press any key at CLI to continue


- AntiCaptchaAPIKey
For now, this seems unused.
For we are to request a anti-captcha service, 

Anti Captcha options



=== END OF: CAPTCHA SECTION ===


      
- XPathLoginSuccessProof
This is a mechanism to detect if login has been done successfully.
The idea is to check wheter a certain element is *exist* after we click login button, 
with a timeout for several seconds.

If the elemen *do* appears, then we can be sure that the login is succeed.
If not, then the code may continue, but it will be suspectible of an error because the code can 
not guarantee that the session is obtained.

You can pick any element for this. 
For example the common case is when you are just logged into freelancer.com, you will see 
your account's name on the top right of the page. We are sure that if the name shows in the page then the login
process was succeed. Hence, we should put that element to the xpath.

If not found, code will throw a warning such as "login failed", but the code will still continue.

"""
LoginPage = 'https://example.com/login'
Credentials = ["user12:pass12", "user13:pass13"] # accepts emails too. example: max@gmail.com:password123

XPathFormUserOrEmail    = '//*[@id="user"]'
XPathFormPassword       = '//*[@id="pass"]'
XPathLoginButton        = '//*[@id="login"]'

ReCaptchaOption         = 1
XPathRecaptcha          = '//*[@id="recaptcha-anchor"]/div[1]'
AntiCaptchaAPIKey       = "dce6bcbb1a728ea8d563de6d169a2057"

LoginTimeout            = 30 # will wait 30 second until login seems to completed

XPathLoginSuccessProof = '//*[@class="login-success"]'






"""
Scrapping options


- XPathFiles
XPath to be searched for downloads


- IntervalsBetweenFiles

This is a custom intervals in seconds between each XPath download button click (or) when downloading with request

Give it an integer -> it will wait for a fixed time
Give it a tuple -> it will wait for a range of time

example
20 : fixed wait for 20 seconds
(20, 30) : randomly wait between 20 to 30 seconds



- IntervalsBetweenUrls

This is a custom intervals in seconds to move from each URL to the next

Give it an integer -> it will wait for a fixed time
Give it a tuple -> it will wait for a range of time

example
20 : fixed wait for 20 seconds
(20, 30) : randomly wait between 20 to 30 seconds




- URLCountToSwitch
Limit of used proxy and credentials.

Every # of URLS completed, clear cookies (logout), set next custom proxy, login(different account), continue
"""

XPathFiles = (
    # add test from apkpure.com
    '//dl/dd[@class = "down"]/a[@href]',
)

# IntervalsBetweenFiles   = 10
IntervalsBetweenFiles   = (1, 5)

# IntervalsBetweenUrls    = 10
IntervalsBetweenUrls    = (20, 30)

URLCountToSwitch        = 20






"""
To Test 
Will not requesting from URLs.txt.
This mode will only try to test downloading notepad++ installer and then exit.
value: True | False
"""

TestMode = True




"""
To Debug
Will verbosely print every data the code can print
value: True | False
"""

DebugMode = False

