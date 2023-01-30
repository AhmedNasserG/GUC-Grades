# GUC-Grades

## Motivation
The main goal of this script is to apply what I learned in Python, learn more to achieve the script and finally to automate daily boring stuff which is checking new grades posted on GUC Admin system

## Script Description
It is a simple script based on web scraping idea to save your time while checking your grades
<img src="./SVGS/offline_mode.svg">

### Features
1. You don't need to log in every time to check your grades you can enable remember me feature
2. After loading your grades you can browse them very fast
3. **MY FAVORITE ONE** You don't need anymore to check all courses and midterm grades to know if there are any updates *As* if there are any updates in your grades a new option in navigation menu will be available then to check new updates in grades only 
<img src="./SVGS/grade_updates.svg">
   
4. **ANOTHER AWESOME ONE** There are offline mode to check your grades from your last session if you are offline or GUC servers are down
5. If any error occurred when connecting to GUC server or fetching your grades the script won't crash, you will be able to try again without closing the script or go to the offline mode or exit

## Installation

### For Linux
```bash
#if you don't have chrome use the following two commands
$ wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
$ sudo apt install ./google-chrome-stable_current_amd64.deb
#----------------------------------------------------------
$ sudo apt install git chromium-chromedriver python3-pip 
$ git clone https://github.com/AhmedNasserG/GUC-Grades.git
$ cd GUC-Grades
$ sudo pip3 install -r requirements.txt
```
### For Windows
if you don't have Python3 [install it from here](https://www.python.org/downloads/)
if you don't have git [install it from here](https://git-scm.com/download/win)
if you don't have chrome [install it from here](https://www.google.com/chrome/)
you will need to install chromedriver [check this](http://jonathansoma.com/lede/foundations-2018/classes/selenium/selenium-windows-install/)


```bash
> git clone https://github.com/AhmedNasserG/GUC-Grades.git
> cd GUC-Grades
> pip install -r  requirements.txt
```
## Usage

```
$ python3 GUC-Grades.py
```
> **⚠️ This script supports up to Python v3.9. Any newer versions of Python will not be able to run it due the changes in `Mapping` collection.**
> 
> **⚠️ This script is tested on Linux and Windows. It's not tested on Mac till now but soon**
> 
> **⚠️ If you face any problem with the script for example it crash in a certain case just add your issue in Github issues section**
## DISCLAIMER
Your login credentials are saved on your local machine. We have no access to them. They are only sent to GUC Admin System.

## Contribution
You are very welcome to contribute to this repository. Just create your Pull Request, I will review it & your updates will be merged ASAP insha'Allah.

## Credits ©
By [Ahmed Nasser](https://github.com/AhmedNasserG)
and I want to thank [Ibrahim Abou Elenein](https://github.com/aboueleyes) for inspiring and helping me 



