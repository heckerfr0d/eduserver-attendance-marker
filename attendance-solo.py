#!/usr/bin/python3

import http.cookiejar as cookielib
import mechanize
import os
import datetime
import time

# italeem login details
username = "username"
password = "password"

i = 0

def createBr():
    br = mechanize.Browser()
    cookiejar = cookielib.LWPCookieJar()
    br.set_cookiejar(cookiejar)
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    return br

def login(br, username, password):
    br.open("https://italeemc.iium.edu.my/login/index.php")
    br.select_form(action="https://italeemc.iium.edu.my/login/index.php")
    br.form.set_all_readonly(False)
    br.form['username'] = username
    br.form['password'] = password
    br.submit()

def submit(br):
    br.follow_link(text="Submit attendance")
    br.select_form(action="https://italeemc.iium.edu.my/mod/attendance/attendance.php")
    br.form.set_all_readonly(False)
    br.form.find_control(name="status").get(nr=0).selected = True
    br.submit(id="id_submitbutton")

def init():
    global i
    while True:
        x = datetime.datetime.now()
        day = x.strftime("%A").lower()
        if day=="friday" or day=="sunday" or day=="saturday":
            pass
        elif x.hour == 11 and 30 <= x.minute <= 32:
            mark()
            time.sleep(82800)
        time.sleep(60)

# function to try to mark attendance during specified intervals
def mark():
    global i
    br = createBr()
    login(br, username, password)
    x = datetime.datetime.now()
    while x.hour == 11 and 30 <= x.minute <= 32:
        br.open("https://italeemc.iium.edu.my/calendar/view.php?view=day")
        try:
            br.follow_link(url_regex="https://italeemc\.iium\.edu\.my/mod/attendance/view\.php*", nr=i)
            try:
                submit(br)
                print(f"Marked attendance at {x.hour}:{x.minute}")
                return
            except:
                print("link not ready yet")
                time.sleep(60)
        except:
            print("no links here lol")
            time.sleep(60)

init()
