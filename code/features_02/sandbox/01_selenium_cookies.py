# todo:
# get cookies
# set cookies
# delete cookies from webdriver

# Clear cookies (logout)



all_cookies = driver.get_cookies()
# return list of dict, for each dict is a cookie in each site

for cookie in all_cookies:
    driver.add_cookie(cookie)
    # driver.add_cookie({'name': 'tour.index', 'value': 'complete', 'domain': self.store['base'] + url})

driver.delete_all_cookies()
