import tkinter as tk
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import *
from sys import exit
from tkinter import *


global userName
global password
global leechAccount
global num_toFollow
global num_toUnfollow

master = tk.Tk()
master.config(background="white")


def center(master):
    w = 280  # width for the Tk root
    h = 200  # height for the Tk root

    # get screen width and height
    ws = master.winfo_screenwidth()  # width of the screen
    hs = master.winfo_screenheight()  # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    # set the dimensions of the screen
    # and where it is placed
    master.geometry('%dx%d+%d+%d' % (w, h, x, y))


center(master)
master.title("InstaBot")
tk.Label(master, text="Username", background="white").grid(row=0)
tk.Label(master, text="Password", background="white").grid(row=1)
tk.Label(master, text="Account Name to find followers", background="white").grid(row=2)
tk.Label(master, text="Amount to follow", background="white").grid(row=3)
tk.Label(master, text="Amount to unfollow", background="white").grid(row=4)

eUsername = tk.Entry(master)
ePassword = tk.Entry(master, show="*")
eLeechAccount = tk.Entry(master)
eNumFollow = tk.Entry(master, width=5)
eNumUnfollow = tk.Entry(master, width=5)

eUsername.grid(row=0, column=1)
ePassword.grid(row=1, column=1)
eLeechAccount.grid(row=2, column=1)
eNumFollow.grid(row=3, column=1)
eNumUnfollow.grid(row=4, column=1)

tk.Label(master, text="*It will do both on default", background="white").grid(row=5, pady=(15, 0))
followOnlyBox = IntVar()
unfollowOnlyBox = IntVar()

Checkbutton(master, text="Only Follow", variable=followOnlyBox, background="white").grid(row=6)
Checkbutton(master, text="Only Un-Follow", variable=unfollowOnlyBox, background="white").grid(row=6, column=1)

followOnly = 1
unFollowOnly = 1


def submit():
    global userName
    global password
    global leechAccount
    global num_toFollow
    global num_toUnfollow
    userName = eUsername.get()
    password = ePassword.get()
    leechAccount = eLeechAccount.get()
    num_toFollow = eNumFollow.get()
    num_toUnfollow = eNumUnfollow.get()
    master.destroy()


def on_Closing():
    master.destroy()
    exit(0)


master.protocol("WM_DELETE_WINDOW", on_Closing)
tk.Button(master, text="Submit", background="white", command=lambda: submit()).grid(row=8)

master.mainloop()

if followOnlyBox.get() == 1:
    unFollowOnly = 0
if unfollowOnlyBox.get() == 1:
    followOnly = 0

browser = webdriver.Chrome("path to your web driver")
browser.implicitly_wait(5)

browser.get('https://www.instagram.com')

username_in = browser.find_element_by_name("username")
password_in = browser.find_element_by_css_selector("input[name='password']")

username_in.send_keys(userName)
password_in.send_keys(password)

login_button = browser.find_element_by_xpath("//button[@type='submit']")
try:
    login_button.click()
except WebDriverException as e:
    print("login or password not valid")
    print(e)
    browser.close()

if browser.find_element_by_xpath('//button[text()="Not Now"]'):
    saveInfo_button = browser.find_element_by_xpath('//button[text()="Not Now"]')
    saveInfo_button.click()

if browser.find_element_by_xpath('//button[text()="Not Now"]'):
    notification_button = browser.find_element_by_xpath('//button[text()="Not Now"]')
    notification_button.click()

if followOnly == 1:
    browser.get('https://www.instagram.com/%s/' % leechAccount)
    followers_button = browser.find_element_by_xpath('//a[@href="/%s/followers/"]' % leechAccount)
    followers_button.click()
    sleep(6)
    fBody = browser.find_element_by_xpath("//div[@class='isgrP']")

    i = 0
    for x in range(int(num_toFollow)):
        try:
            follow_button = browser.find_element_by_xpath("//button[@class='sqdOP  L3NKy   y3zKF     ']")
        except NoSuchElementException:
            browser.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
                                   fBody)
            sleep(0.5)
            continue

        follow_button.click()
        sleep(1)

if unFollowOnly == 1:
    browser.get('https://www.instagram.com/japan_2u/')

    followers_button = browser.find_element_by_xpath('//a[@href="/%s/following/"]' % userName)
    followers_button.click()

    fBody = browser.find_element_by_xpath("//div[@class='isgrP']")

    for x in range(int(num_toUnfollow)):
        try:
            following_button = browser.find_element_by_xpath('//button[text()="Following"]')
        except NoSuchElementException:
            browser.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
                                   fBody)
            sleep(0.5)
            continue
        following_button.click()
        sleep(1)
        try:
            unfollow_button = browser.find_element_by_xpath("//button[@class='aOOlW -Cab_   ']")
        except NoSuchElementException:
            browser.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
                                   fBody)
            sleep(1)
            continue
        unfollow_button.click()
        sleep(1)

browser.close()
