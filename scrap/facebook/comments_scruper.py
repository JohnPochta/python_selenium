import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup as soup
import json
from pprint import pprint

browser = webdriver.Chrome("C:/Users/johnp/chromedriver_win32/chromedriver.exe")

def login_facebook1(email, password): #this function was made for login in facebook.
    url = u'https://www.facebook.com/login.php'
    browser.get(url)
    time.sleep(1)
    email_log_field = browser.find_element_by_id('email')
    email_log_field.send_keys(email)
    password_log_field = browser.find_element_by_id('pass')
    password_log_field.send_keys(password)
    login_button = browser.find_element_by_id('loginbutton')
    login_button.click()
def facebook_go(id_):#this function was made for making a requests to facebook from webdriver, so it takes a part of url which will be pasted after facebook.com in request path
    user_id = id_
    url = u'https://www.facebook.com/'
    browser.get(url+user_id) 
    browser.find_element_by_tag_name('body').click()
def read_login_info(): #this function was made for reading user login and password data from file in some path. File must have two lines: first line is email, second is password 
    f = open('path_to_file', 'r')
    email = f.readline()
    email = email.replace("\r","")
    email = email.replace("\n","")
    password = f.readline()
    password = password.replace("\r","")
    password = password.replace("\n","")
    f.close()
    return [email,password]
def items_analizator(items):#
    reactions = {}
    topics = []
    for elem in items:
        topic = elem.find_element_by_tag_name('span').find_element_by_tag_name('span').get_attribute("aria-label").split(' ')[-1]
        count = elem.find_element_by_tag_name('span').find_element_by_tag_name('span').text
        topic_info = {}
        topic_info['count'] = count
        elem.click()
        time.sleep(0.8)
        if topic=='post':
            topic='all'
            count = count.split(" ")[1]
            topic_info['count'] = count
            topic_info['people'] = browser.execute_script(
                "var people = []; document.querySelector('ul#reaction_profile_browser').querySelectorAll('li').forEach((elem)=>{people.push(elem.querySelector('a').href)});"+
                "return people;"
            )
        elif(topic=="Like"):
            topic_info['people'] = browser.execute_script(
                "var people = []; document.querySelector('ul#reaction_profile_browser1').querySelectorAll('li').forEach((elem)=>{people.push(elem.querySelector('a').href)});"+
                "return people;"
            )
        elif(topic=="Haha"):
            topic_info['people'] = browser.execute_script(
                "var people = []; document.querySelector('ul#reaction_profile_browser4').querySelectorAll('li').forEach((elem)=>{people.push(elem.querySelector('a').href)});"+
                "return people;"
            )
        elif(topic=="Love"):
            topic_info['people'] = browser.execute_script(
                "var people = []; document.querySelector('ul#reaction_profile_browser2').querySelectorAll('li').forEach((elem)=>{people.push(elem.querySelector('a').href)});"+
                "return people;"
            )
        elif(topic=="Wow"):
            topic_info['people'] = browser.execute_script(
                "var people = []; document.querySelector('ul#reaction_profile_browser3').querySelectorAll('li').forEach((elem)=>{people.push(elem.querySelector('a').href)});"+
                "return people;"
            )
        elif(topic=="Sad"):
            topic_info['people'] = browser.execute_script(
                "var people = []; document.querySelector('ul#reaction_profile_browser7').querySelectorAll('li').forEach((elem)=>{people.push(elem.querySelector('a').href)});"+
                "return people;"
            )
        elif(topic=="Angry"):
            topic_info['people'] = browser.execute_script(
                "var people = []; document.querySelector('ul#reaction_profile_browser8').querySelectorAll('li').forEach((elem)=>{people.push(elem.querySelector('a').href)});"+
                "return people;"
            ) 
        reactions[topic] = topic_info
    return reactions
def read_dataset():#this function read a dataset, which in this example consist of list, which elements is id's of facebook posts for analysis
    f1 = open('C:/Users/johnp/Downloads/saakashvili_post_ids_01_09_16_28_02_17_01_ (1).json')
    data = json.loads(f1.read())
    return data
def comment_object_builder(elem):
    actions = ActionChains(browser)
    actions.move_to_element(elem).perform()
    comment={}
    comment['author'] = elem.find_element_by_class_name('UFICommentActorName').get_attribute("href")
    comment['date'] = elem.find_element_by_class_name('livetimestamp').get_attribute("title")
    try:
        comment['text'] = elem.find_element_by_class_name('UFICommentBody').text
    except:
        comment['text'] = ''
    try:
        comment['img'] = elem.find_element_by_class_name('_2rn3').get_attribute("href")
    except:
        comment['img'] = ''
    try:
        actions = ActionChains(browser)
        actions.move_to_element(elem.find_element_by_class_name('UFICommentReactionsBling')).perform()
        elem.find_element_by_class_name('UFICommentReactionsBling').click()
        time.sleep(2)
        reactions = {}
        items = browser.execute_script("return document.querySelector('ul._4470').querySelectorAll('li')")
        comment['reactions'] = items_analizator(items)
        browser.execute_script("document.querySelector('a.layerCancel').click()")
    except Exception as e:
        comment['reactions'] = None
    return comment
def replies(list_):
#The main task of this script it's to Collect the information. 
#And one of the most important things in collection information try to save association between collected data
#So, when we process the comments we have to process replies to this comments too,
#and have to highlight affiliation between list of replies and particular comment.
#So, this function was made for processing all replies for particular comment 
#and returning results of their processing like a list of replies, every element of which - 
#has a same structure to structure of processed comment, but withoul field "replies")))0
#Try to understand this!
    comments = []
    for elem in list_:
        comment = comment_object_builder(elem)
        comments.append(comment)
    return comments
def scrub_all_comments():
    comments = []
    list_ = []
    time.sleep(5)
    for elem in browser.execute_script("return document.querySelector('._3ccb').querySelectorAll('.UFIComment')"):
        if (elem.get_attribute("aria-label")=="Comment"):
            list_.append([elem])
        elif (elem.get_attribute("aria-label")=="Comment reply"):
            list_[len(list_)-1].append(elem)
    try:
        actions = ActionChains(browser)
        actions.move_to_element(elem.find_element_by_class_name('UFICommentReactionsBling')).perform()
    except:
        pass
    for elem in list_:
        comment = comment_object_builder(elem[0])
        comment['replies'] = replies(elem[1:])
        comments.append(comment)
    return comments
    #time.sleep(15)
def show_all_comments():
    actions = ActionChains(browser)
    actions.move_to_element(browser.find_element_by_id('pagelet_bluebar')).perform()
    try:
        browser.execute_script(
            "document.querySelector('a._xlt').click()"
        )
    except:
        pass
    while True:
        try:
            load = browser.find_element_by_class_name('UFILastCommentComponent')
            actions.move_to_element(load).perform()
            load.click()
        except Exception as e:
            break
    browser.execute_script("document.querySelector('._3ccb').querySelectorAll('.UFICommentLink').forEach((elem)=>{elem.click()})")

def scrub_posts_info(dataset):
    result = {}
    comments = []
    for post in dataset:
        facebook_go(str(post))
        show_all_comments()
        for elem in scrub_all_comments():
            comments.append(elem)
        result[post] = comments
    with open('C:/Users/johnp/Desktop/Postcomments.json', 'w') as outfile:
        json.dump(result, outfile)
    print(json.dumps(result, sort_keys=True, indent=4))
        
        
    

emailpass = read_login_info()
email = emailpass[0]
password = emailpass[1]
login_facebook1( str(email), str(password) )
scrub_posts_info(read_dataset())