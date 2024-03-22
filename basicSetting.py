import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


# This file contains the basic things related to this experiment,
# Everything about (1) consent, and (2) demographic information are here.
# (e.g., print error message, record demographic information)

# Consent
# whether they've checked the consent box or not
def getConsent(win):

    # haveConsent is True if participant did check the box
    haveConsent = win.consentAgreeBox.isChecked()

    return haveConsent


# print error message
def consentErr(consent, win):

    errMessage = ""

    # if there's no consent, error message would be below
    if consent == False:
        errMessage = 'You must consent to continue'

    # if there is consent, no error message
    else:
        errMessage = ''

    # set the corresponds error message
    win.consentErrlbl.setText(errMessage)

    # if there is consent, would return True
    return errMessage == ""


# the below function is what happens when the 'Next' button on consent page is pressed
def submitConsent(win):

    consent = getConsent(win)

    # if True (which is when there is consent), go to demographic page
    if consentErr(consent, win):
        win.stackedExp.setCurrentIndex(1)


# Demographic

# get their demographic information
def getDemo(win):
    age = win.ageBox.value()
    gender = win.sexBox.currentText()
    isStudent = win.eduBox.currentText()
    return {"age": age, "gender": gender, "education": isStudent}


# error message if incomplete
def demoErr(win, demographic):
    demoErrMessage = ""
    if demographic["age"] == 0 or \
            demographic["age"] < 18 or \
            demographic["gender"] == "--choose--" or \
            demographic["education"] == "--choose--":
        demoErrMessage = "Please complete the above information"
        win.demoErrlbl.setText(demoErrMessage)

    return demoErrMessage == ""


# print the error message OR proceed to next page
def submitDemo(win):
    demographic = getDemo(win)
    if demoErr(win, demographic):
        win.stackedExp.setCurrentIndex(2)


# format their demographic information into ["age", "gender", "education"]
def saveDemo(win):

    demoInfo = []

    demographic = getDemo(win)  # {"age":age, "gender":gender, "education":isStudent}
    for demo in demographic:
        demoInfo.append(str(demographic[demo]))

    return demoInfo


# append the demographic information in a csv file
def recordDemo(win):
    demo = saveDemo(win)  # age, gender, education
    demoData = open("demographic.csv", 'a+')
    demoData.write(",".join(demo) + "\n")
    demoData.close()
