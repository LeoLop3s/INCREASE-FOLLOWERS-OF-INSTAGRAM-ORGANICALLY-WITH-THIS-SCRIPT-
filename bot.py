#welcome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from random import randint
import pandas as pd

#use chromedriver according to your chromeversion

webdriver = webdriver.Chrome(executable_path="C:\\Users\\rahul negi\\Downloads\\chromedriver.exe") # Change this to your own chromedriver path!
sleep(2)
webdriver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
#request = requests.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
sleep(10)

username = webdriver.find_element_by_name('username')
username.send_keys('username') #type your username here
password = webdriver.find_element_by_name('password')
password.send_keys('password') #type your password here

button_login = webdriver.find_element_by_css_selector('#loginForm > div > div:nth-child(3) > button > div')
button_login.click()
sleep(10)

not_now = webdriver.find_element_by_css_selector('#react-root > section > main > div > div > div > div > button')
not_now.click()

notnow = webdriver.find_element_by_css_selector('body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.HoLwm')
notnow.click() #comment these last 2 lines out, if you don't get a pop up asking about notifications

hashtag_list = ['lmao','indianmeme', 'laughdaily', 'sarcasmdaily', 'wholesomememe', 'sarcasmmeme', 'memesdaily'] #use your hashtags here

prev_user_list = [] #- if it's the first time you run it, use this line and comment the two below
prev_user_list = pd.read_csv('20200315-223730_users_followed_list.csv', delimiter=',').iloc[:,1:2]  # useful to build a user log
prev_user_list = list(prev_user_list['0'])

new_followed = []
tag = -1
followed = 0
likes = 0
comments = 0

for hashtag in hashtag_list:
    tag += 1
    webdriver.get('https://www.instagram.com/explore/tags/' + hashtag_list[tag] + '/')
    sleep(20)
    first_thumbnail = webdriver.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')

    first_thumbnail.click()
    sleep(randint(1, 2))
    try:
         for x in range(1, 1000):
            username = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[1]/span/a').text
 # If we already follow, do not unfollow
            if username not in prev_user_list:
                 
                if webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').text == 'Follow':
                    #print('path is same')

                    webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').click()

                    new_followed.append(username)
                    followed += 1
                    sleep(5)
                    # Liking the picture
                    
                    # button_like = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button/svg/path')
                    button_like = webdriver.find_element_by_css_selector('body > div._2dDPU.CkGkG > div.zZYga > div > article > div.eo2As > section.ltpMr.Slqrh > span.fr66n > button')
                    
                    button_like.click()
                    likes += 1
                    sleep(randint(18, 25))

                    # Comments and tracker
                    comm_prob = randint(2, 10)
                    print('{}_{}: {}'.format(hashtag, x, comm_prob))
                    if comm_prob > 7:
                        comments += 1
                        webdriver.find_element_by_xpath('body > div._2dDPU.CkGkG > div.zZYga > div > article > div.eo2As > section.ltpMr.Slqrh > span.fr66n > button').click()
                       # webdriver.find_element_by_css_selector('body > div._2dDPU.CkGkG > div.zZYga > div > article > div.eo2As > section.ltpMr.Slqrh > span._15y0l > button > svg#').click()
                        comment_box = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[3]/section[3]/div/form/textarea')
                        #comment_box = webdriver.find_element_by_css_selector('body > div._2dDPU.CkGkG > div.zZYga > div > article > div.eo2As > section.sH9wk._JgwE > div > form > textarea')

                        if (comm_prob < 7):
                            comment_box.send_keys('DO NOT CHECK MY BIO')
                            sleep(1)
                        elif (comm_prob > 6) and (comm_prob < 9):
                            comment_box.send_keys('check my memes you will fall in love with my page :)')
                            sleep(1)
                        elif comm_prob == 9:
                            comment_box.send_keys('Birds are flying white as dove, i wanna reach 1k followers before dying, show some love :(')
                            sleep(1)
                        elif comm_prob == 10:
                            comment_box.send_keys(' You stole my meme ')
                            sleep(1)
                        # Enter to post comment
                        comment_box.send_keys(Keys.ENTER)
                        sleep(randint(22, 28))

                # Next picture
                webdriver.find_element_by_link_text('Next').click()
                sleep(randint(25, 29))
            else:
                webdriver.find_element_by_link_text('Next').click()
                sleep(randint(20, 26))
    # some hashtag stops refreshing photos (it may happen sometimes), it continues to the next
    except:
       continue

for n in range(0, len(new_followed)):
    prev_user_list.append(new_followed[n])

updated_user_df = pd.DataFrame(prev_user_list)
updated_user_df.to_csv('{}_users_followed_list.csv'.format(strftime("%Y%m%d-%H%M%S")))
print('Liked {} photos.'.format(likes))
print('Commented {} photos.'.format(comments))
print('Followed {} new people.'.format(followed))
