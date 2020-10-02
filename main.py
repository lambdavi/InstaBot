#
# Author: Davide Buoso
#
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from random import randint
from datetime import datetime


def get_date():
    now = datetime.now()  # current date and time
    now.strftime("%Y")
    now.strftime("%m")
    now.strftime("%d")
    date_time = now.strftime("%d/%m/%Y")
    return date_time


try:
    with open('followed.txt', 'r+') as f:
        prev_user_list = f.read().splitlines()
    print(prev_user_list)
except IOError:
    with open('followed.txt', 'w+') as f:
        prev_user_list = []
    print("New list created")

USERNAME = ''
PSWD = ''
webdriver = webdriver.Edge('msedgedriver.exe')
sleep(2)
webdriver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
sleep(3)
username = webdriver.find_element_by_name('username')
username.send_keys(USERNAME)
password = webdriver.find_element_by_name('password')
password.send_keys(PSWD)
submit = webdriver.find_element_by_tag_name('form')
submit.submit()
sleep(5)

not_now = webdriver.find_element_by_xpath('//button[text()="Non ora"]')
not_now.click()
sleep(3)

hashtag_list = ['nature', 'photooftheday', 'girls', 'food']

tag = -1
followed = 0
likes = 0
comments = 0
n = 10
counter = 0
for hashtag in hashtag_list:
    counter = 0
    tag += 1
    webdriver.get('https://www.instagram.com/explore/tags/' + hashtag_list[tag] + '/')
    sleep(5)
    first_thumbnail = webdriver.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a')
    first_thumbnail.click()
    sleep(randint(1, 2))
    try:
        for x in range(1, n):
            username = webdriver.find_element_by_xpath(
                '/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[1]/span/a').text
            print(username)
            if username not in prev_user_list:
                counter += 1

                if webdriver.find_element_by_xpath(
                        '/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').text == 'Segui':
                    webdriver.find_element_by_xpath(
                        '/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').click()

                prev_user_list.append(username)
                followed += 1

                # Liking the picture
                button_like = webdriver.find_element_by_xpath(
                    '/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[1]/button/div/span')

                button_like.click()
                likes += 1
                sleep(randint(18, 25))

                # Comments and tracker
                comm_prob = randint(1, 10)
                print('{}_{}: {}'.format(hashtag, x, comm_prob))
                webdriver.find_element_by_xpath(
                    '/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[2]').click()
                comment_box = webdriver.find_element_by_xpath(
                    '/html/body/div[4]/div[2]/div/article/div[3]/section[3]/div/form/textarea')
                if comm_prob < 6:
                    sleep(1)
                elif (comm_prob >= 6) and (comm_prob < 9):
                    comment_box.send_keys('Did you use a pro camera? This photo is great.'
                                          'Anyway if u wanna pass by my profile and leave a like, it would be great.')
                    comments += 1
                    comment_box.send_keys(Keys.ENTER)
                    sleep(randint(22, 28))
                    sleep(1)
                elif comm_prob == 9:
                    comment_box.send_keys('This photo is pretty good. Did you use your phone to shoot it? '
                                          'Anyway if u wanna, passh by my profile and leave a like it would be great!.'
                                          ' Thanks')
                    comments += 1
                    comment_box.send_keys(Keys.ENTER)
                    sleep(randint(22, 28))
                    sleep(1)
                elif comm_prob == 10:
                    comment_box.send_keys('Nice pic! If u wanna, pass by my profile, I lost my account recently and a'
                                          'like would be awesome. Thanks!')
                    comments += 1
                    sleep(1)
                comment_box.send_keys(Keys.ENTER)
                sleep(randint(22, 28))

                # Next picture
                if counter != 1:
                    webdriver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div/a[2]").click()
                else:
                    webdriver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div/a").click()

                sleep(randint(25, 29))
            else:
                print("User already followed!")
                counter += 1
                if counter != 1:
                    sleep(2)
                    webdriver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div/a[2]").click()
                else:
                    sleep(2)
                    webdriver.find_element_by_xpath("/html/body/div[4]/div[1]/div/div/a").click()
                sleep(randint(20, 26))
    except Exception as e:
        print(e)
        continue

with open('followed.txt', 'r+') as f:
    for item in prev_user_list:
        f.write("%s\n" % item)

webdriver.get('https://www.instagram.com/' + USERNAME + '/')
nof = webdriver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span').text
with open('followers.txt', 'a+') as f:
    f.write(f"{get_date()}: {nof} followers\n")

print('Liked {} photos.'.format(likes))
print('Commented {} photos.'.format(comments))
print('Followed {} new people.'.format(followed))
