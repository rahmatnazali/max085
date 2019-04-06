# max085
Python flexible web scrapper

**this documentation is still work in progress**


##### Feature

This code has two features.

- Feature 1

  Scrapping data from a page that did not require JS/script to load and did not need to login.
  
  The code will accept flexible enough variety of any URL, with the trade-off that the configuration must be done thoroughly, because user will need to exactly specify the XPath of the desired data.

  - Requirement 1: [F1.txt](requirements/F1.txt)
  - Requiremetn 2: [F1-Xpath](requirements/F1-XPath.txt)
  - Testing feedback
    - Feedback 1: [Testing 01](requirements/F1-Testing_01-Notes.txt)
    - Feedback 2: [Testing 02](requirements/F1-Testing_02-Notes.txt)
    - Feedback 3: [Testing 03](requirements/F1-Testing_03-Notes.txt)

- Feature 2

  Same as Feature 1, but this is for a case where JS/scipt must be load and/or a login is needed to access the page. This feature will also able to switch proxy, given a list of valid proxies.

  - Requirement 2: [F2.txt](requirements/F2.txt)





## Before Starting
- Make sure to have Python 3.x (Development is in v3.6.7)
- Go to project directory by opening your console (cmd/powershell) and type
  ```
  cd /path/to/your/code/max085
  ```
  
  You can also SHIFT + LEFT CLICK from exploler pointed at your directory, and choose "Open Powershell here".




### Important Notes
What I know is that we differ in system. You use windows and I use Linux.
The logical will still the same, but you might encounter different syntax.

Example: 
- I used `python3 python_file.py` to run python file. You might be need to use `python python_file.py` instead
- I used `pip3 install module_name` to install a module. You might be need to use `pip install module_name` instead


### Setting virtual environtment
[What is Virtual Env?](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/) or  [Why should I use virtual env?](https://stackoverflow.com/questions/41972261/what-is-a-virtualenv-and-why-should-i-use-one)

This is optional. But I strongly recommend that you use virtual env so you did not messed up your global dependency, knowing that you also code in python already.

- Installing virtualenv (if you did not have one) 
  ```
  py -m pip install --user virtualenv
  ```
- Creating virtualenv    

  ```
  py -m virtualenv env
  ```
  You will note that a new folder called "env" will be present on you directory
  
  ![](assets/env_directory.png)

- activate your virtualenv
  ```
  .\env\Scripts\activate
  ```

  if your cmd/powershell change like this, then it succeed (note the leading **(env)**)
  
  ![](assets/virtual_env_enter.png)
  
  Note:
    - as long as there are leading **(env)** in your cmd, you are in virtual environtment scope
    - to exit from that, type `deactivate`
  
- install dependency

  Assuming that you are inside virtual env, run:
  ```
  pip3 install -r requirements.txt
  ```
- Check if dependency is installed by running

  ```
    pip3 freeze
  ```
  
  A list of installed dependency will shown as below.
  
  ![](assets/pip_freeze.png)
  
  Note:
   I code with Linux Mint, so your list of dependency might a bit different because our system differ. 
   It is completely fine. Just make sure that these major module are printed at your console:
     - lxml
     - pandas
     - python-dateutil
     - requests
     
     
You are ready to go.  

## Feature 1

### Configuring

- Open [code/features_01/config.py](code/features_01/config_01.py)
- Change according to your need
  - `Xpath`: describe the attribute you want to obtain from HTML, and its XPath. 
    Because we agreed to divide each element with each XPath, there will not be OR or AND on the deepest (right-most) 
    elements. But occurrence in the middle element is possible.
    
    Example:
      - `"Source Image": "/div/img/@src"` 
        
        valid. we seek `<img src="">` inside `<div>`
      - `"Source Image" : "/div[@class and @id]/img/@src"` 
      
        valid. because we seek `<img src="">` inside `<div>` that have `class` AND `id`
      - `"Source Image: "/div/img/[@src | @class]"` 
      
        **invalid**. the code can't decide if the "Source Image" comes from `src` or `class`. You should reformat it to 
        two XPath that likely will like this:
        - `"Source Image: "/div/img/@src"` 
        - `"Source Image's Class: "/div/img/@class"`

    Don't forget the trailing comma after each XPath declared.
  
  - `Regex`: place your regex here and what the replace string will be
  
    **Disable Feature:** If you want to disable this features, simply declare Xpath as empty tuple `Regex = ()`

  - `Columns`: place one or multiple Column's name that you want to be considered so that no multi occurrence appears
    
    Example:
      - `'Link'`: means the Link attribute should always be unique
      - `'Link', 'Model Name'`: means the Link and Model Name attribute should always be unique
    
    **Disable Feature:** If you want to disable this features, simply declare Columns as empty tuple `Columns = ()`

  - Test Mode and Debug Mode
    - `TestMode`: to test if you can run the code. If `True`, the code will not request an HTML via internet. 
      This will only scrap [code/features_01/example_2.html](code/features_01/example_2.html) 
      (the one you gave in Xpath.txt, leading to samsung.com).
      
      Turn this to `False` for production/actual internet scrapping.
    - `DebugMode`: to tell the verbosity. Good to find if attribute is correctly regexed or not, or if 
      multiple occurrence is evalueted correclty or not. 
      
      Turn this to `True` to enable verbose mode, but the CLI will get a bit dirty. Turn this to `False` to minimize 
      the verbosity.
    
    - `GenerateNewFiles`
      - `True`: the software as it is, no change.
      - `False`: instead of creating new output-time.csv files on every run, append all results to the **end** or begening of output.csv

### Running

- Assuming that you already inside virtualenv, go to `Feature 01` directory and run [main_01.py](code/features_01/main_01.py)
  ```
  cd code/features_01/
  python3 main_01.py
  ```
  
  The output will be like this:
  
  ![](assets/running_the_scripts.png)
  
  The Output.csv will also be generated:

  ![](assets/result_directory.png)
  
  And if we open Output.csv, it will look like this :
  
  ![](assets/result_csv.png)
  
  
  Note that Output.csv only contains 10 elements. This is because I picked 1 element and put it into Done.csv.
  The code will know that duplucate link exist, and it will not be logged into Output.csv
  
## Feature 2

**Note**: Make sure to do all the step in "Before Starting" before configuring the code.

Additionally, you might want to run this code again to renew the dependency, assuming you are inside the virutal environtment.
```
pip3 install -r requirements.txt
```


### Configuring

(work in progress)

#### Webdriver Options

- WebDriverPath
  
  Path to your chromedriver. You can get chromedriver at: http://chromedriver.chromium.org/

  For now, the default will be using Chrome webdriver, but you can change it to firefox (gecko driver) if you want. I will describe how to do it in the code, when webdriver is initialized on lib_common/init_webdriver.


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

  Download file mode. Sequential (i.e. using requests module) or not (i.e. using selenium click).

  True: The download will be done with requests module in the background. This will check for file completion and wait for interval.

  False: The download will be done with selenium click with interval waiting, so this will *not* check for file completion.


- RequestHeatder (dictionary)

  This is the default request header for requests module. This will make the request looks like it came from a Chrome browser

  For some case like amazon.com, the site will reject if no appropriate agent (browser) is preset on the request's header


- SaveDirectory and DefaultSaveDirectory

  Save/Directory options. Make SaveDirectory to empty string '' and code will look at DefaultSaveDirectory.





#### Credentials Option

- LoginPage

  The link to the login page of a site. This link must directly cotains login form to scrap.


- Credentials (list of string)

  This list is for storing credentials with format: `USERNAME:PASSWORD`. This also accepts emails as the username.

  example:
  
  ```
  Credentials = [
    "user01:my_secret_password", 
    "user02:my_other_secret_password",
    "max@gmail.com:my_password"
  ]

  ```

- XPathFormUserOrEmail, XPathFormPassword, XPathLoginButton

  The 3 variables above are each for storing xpath input form regarding Username, password, and the login button. Code will fill the username and password, and then click the login button.



- LoginTimeout (integer)
  
  This is the amount of seconds to be waited (sleep) until we are sure that login is completed. This will vary according to your internet connection and/or proxy speed.

  The code will wait explicitly for the XPathLoginSuccessProof (explained below) with a maximum timeout of this variable.

  If xpath is found, the code will directly resume without waiting until full sleep.

  If xpath is not found until the sleep is end,then the code will declare a warning to show that "it is unsure that the login process is succeed"


##### === CAPTCHA SECTION ===

**Important Note**: 
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




- `ReCaptchaOption` (integer)
For now we have 2 options:
1. Wait for certain seconds to solve recaptcha
2. CLI will ask for input (it will wait forever). So user can take time to solve captcha, 
   and after that user will need to go to CLI and press any key (say, enter)
3. ~~Requesting anti-captcha service~~ (for now it is not available because we need the 
documentation of the API service. Feel free to inform me about this)


- XPathRecaptcha

  This xpath is for finding the recaptcha.

  If captcha element is found, then there are 2 options (declared in variable ReCaptchaOption):
    - calling anti-captcha service, with the given api (I can not tested it yet until now. Let me know the case if you have)
    - code will wait (forever) until you click/press any key at CLI. So at this time you can solve the captcha at your 
      browser and press any key at CLI to continue


- AntiCaptchaAPIKey

  For now, this seems unused. For we are to request a anti-captcha service, we must first know the documentation of the service.




##### === END OF: CAPTCHA SECTION ===


      
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







#### Scrapping options


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



### Running
- Assuming that you already inside virtualenv, go to `Feature 01` directory and run [main_02.py](code/features_02/main_02.py)
  ```
  cd code/features_02/
  python3 main_02.py
  ```


### Example Case

#### Case 1: APKPure

##### Purpose

We want to download all the APK from the homepage of [apkpure.com](https://apkpure.com).

This case is done without Login and Proxy feature

##### Analyze

- Opening apkpure.com
- We then know that for every link that lead to the download page of an APK will have an XPath like this
  `//dl/dd[@class = "down"]/a[@href]`
  
  in other word: `<a href>` inside of `<dd class = "down">` inside of `<dl>`
  
- We then write the xpath into `config_02/XPathFiles`
- Set `RequiredLogin` and `UseProxy` to **`False`**

##### Run the code

- Assuming that you already inside virtualenv, go to `Feature 01` directory and run [main_02.py](code/features_02/main_02.py)
  ```
  cd code/features_02/
  python3 main_02.py
  ```

This is the example video capture of the run: [Captured video](/assets/f2/Kazam_screencast_00002.mp4)

It shows that the code are capable of downloading each APK with separate interval around 5-10 seconds.

#### Case 2, and so on 
(feel free to ask with any link, and I will insert the step-by-step here)
 
