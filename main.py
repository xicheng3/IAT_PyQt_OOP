from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from basicSetting import submitConsent
from basicSetting import submitDemo
from basicSetting import recordDemo
from iat import *
import random
from keyboard import KeyboardWidget

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
app = QApplication([])
window = uic.loadUi("manyPages.ui")

# Please first read the ExperimentManual.pdf before proceed to this file :)

# This is the main pyfile for this experiment, which contains
# (1) materials (including iat category labels, stimuli, and keys to press)
# (2) the structure of experiment (presented in corresponds with the procedure)
# (3) how pages are connected

# For more information presented in this file,
# if related to iat -> 'iat.py'
# if related to consent and demographic -> 'basicSetting.py'
# if related to keyboard -> 'keyboard.py'
# if related to experiment setting -> 'ExperimentManual.docx'

# After collection of consent and demographic information, as well as given instruction, participants first go to the
# (1) 'Sexuality' block, for which they get to familiarize with the sexuality category;
# depending on the random sequence:
# (2) 'Congruent' or 'Incongruent' phase;
# (3) 'Incongruent' or 'Congruent' phase;
# and finally debrief.

# For congruent and incongruent phase, they each consist an attitude iat block and a combined iat block.
# For each of the iat block,
# it consists of a prepare page which tells participants the left and right categories,
# and then the iat page which participants press key to indicate categorization


# Materials (labels, stimuli, keys)-------------------------------------------------------------------------------------
# labels
# these sets of labels are used to change the category label according to different iat phase
sexualityLbls = [{"position": "left", "text": "Homosexuality", "prepareBtn": window.sexualityPrepareLeft, "iatBtn": window.sexualityIatLeft},
                 {"position": "right", "text": "Heterosexuality", "prepareBtn": window.sexualityPrepareRight, "iatBtn": window.sexualityIatRight}]
congruentAttitudeLbls = [{"position": "left", "text": "Negative", "prepareBtn": window.conAttPrepareLeft, "iatBtn": window.conAttIatLeft},
                         {"position": "right", "text": "Positive", "prepareBtn": window.conAttPrepareRight, "iatBtn": window.conAttIatRight}]
incongruentAttitudeLbls = [{"position": "left", "text": "Positive", "prepareBtn": window.inconAttPrepareLeft, "iatBtn": window.inconAttIatLeft},
                           {"position": "right", "text": "Negative", "prepareBtn": window.inconAttPrepareRight, "iatBtn": window.inconAttIatRight}]
congruentCombinedLbls = [{"position": "left", "text": "Homosexuality \nNegative", "prepareBtn": window.conCombinedPrepareLeft, "iatBtn": window.conCombinedIatLeft},
                         {"position": "right", "text": "Heterosexuality \nPositive", "prepareBtn": window.conCombinedPrepareRight, "iatBtn": window.conCombinedIatRight}]
incongruentCombinedLbls = [{"position": "left", "text": "Homosexuality \nPositive", "prepareBtn": window.inconCombinedPrepareLeft, "iatBtn": window.inconCombinedIatLeft},
                           {"position": "right", "text": "Heterosexuality \nNegative", "prepareBtn": window.inconCombinedPrepareRight, "iatBtn": window.inconCombinedIatRight}]

# stimuli
# The stimuli used in this study belong to one of the 4 categories: homosexuality, heterosexuality, positive, negative.
# In order to run the iat, we need to combine stimuli sets.
# (e.g., sexualityStimuli is used when we asked participants to categorize stimuli
# into either 'homosexuality' or 'heterosexuality' - which is combination of homoPics and heteroPics)

# These stimuli are also shuffled to ensure they're presented at random order

homoPics = ["Homosexuality", "homo1.png", "homo2.png", "homo3.png", "homo4.png", "homo5.png", "homo6.png", "homo7.png"]
heteroPics = ["Heterosexuality", "hetero1.png", "hetero2.png", "hetero3.png", "hetero4.png", "hetero5.png", "hetero6.png",
              "hetero7.png"]
positiveWords = ["Joy", "Love", "Peace", "Wonderful", "Pleasure", "Glorious", "Laughter", "Happy"]
negativeWords = ["Agony", "Terrible", "Horrible", "Nasty", "Evil", "Awful", "Failure", "Hurt"]

sexualityStimuli = homoPics + heteroPics               # combine stimuli
shuffle(sexualityStimuli)                              # shuffle the order of stimulus

attitudeStimuli = positiveWords + negativeWords
shuffle(attitudeStimuli)

combinedStimuli = sexualityStimuli + attitudeStimuli
shuffle(combinedStimuli)

# keys
# because iat requires participants pressing keys on keyboard to categorize stimuli,
# the keys are made for each iat phase
sexualityKey = KeyboardWidget(window.sexualityIatInstruction)
sexualityKey.setFocus()

conAttKey = KeyboardWidget(window.conAttIatInstruction)
conAttKey.setFocus()

conCombinedKey = KeyboardWidget(window.conCombinedIatInstruction)
conCombinedKey.setFocus()

inconAttKey = KeyboardWidget(window.inconAttIatInstruction)
inconAttKey.setFocus()

inconCombinedKey = KeyboardWidget(window.inconCombinedIatInstruction)
inconCombinedKey.setFocus()


# Experiment------------------------------------------------------------------------------------------------------------

# 0. Start with first page
window.stackedExp.setCurrentIndex(0)

# 0. randomly select either congruent or incongruent phase goes first
choice = random.choice(["conFirst", "inconFirst"])


# 1. Consent
# participants need to click consent box to indicate their consent to proceed
def submitConsentPage():
    submitConsent(window)


# 2. Demographic
# participants need to include all the demographic information to proceed
def submitDemographicPage():
    submitDemo(window)


# 3. Instruction
# This page is only used to inform participants about the detail of the experiment


# 4. Sexuality block
# Sexuality IAT: left category as 'Homosexuality' and right as 'Heterosexuality'.
def sexualityPrepare():

    # preparePage could be find in 'iat.py', it (1) sets to the correct prepare page, (2) set the category labels
    preparePage(window, sexualityLbls, 3)

def sexualityIat():

    # go to the correct iat page
    window.stackedExp.setCurrentIndex(4)

    # if congruent phase first, sexuality iat -> congruent phase
    if choice == "conFirst":

        # presentStimuli could be find in 'iat.py', for which it (1) set iat mechanism, (2) leads to next page
        presentStimuli(sexualityStimuli, sexualityKey, window.sexualityRedX, window.sexualityCross,
                       window.sexualityIatStimuli, window.sexualityIatLeft, conAttPrepare)

    # if incongruent phase first, sexuality iat -> incongruent phase
    else:
        presentStimuli(sexualityStimuli, sexualityKey, window.sexualityRedX, window.sexualityCross,
                       window.sexualityIatStimuli, window.sexualityIatLeft, inconAttPrepare)


# 5. Congruent phase
# Congruent Attitude IAT: left category as 'Negative' and right as 'Positive'
def conAttPrepare():
    preparePage(window, congruentAttitudeLbls, 5)

def conAttIat():
    window.stackedExp.setCurrentIndex(6)

    # congruent attitude iat -> congruent combined iat
    presentStimuli(attitudeStimuli, conAttKey, window.conAttRedX,window.conAttCross,
                   window.conAttIatStimuli, window.conAttIatLeft, conCombinedPrepare)

# Congruent Combined IAT: left category as 'Homosexuality \nNegative' and right as 'Heterosexuality \nPositive'
def conCombinedPrepare():
    preparePage(window, congruentCombinedLbls, 7)

def conCombinedIat():
    window.stackedExp.setCurrentIndex(8)

    # if congruent phase first, congruent combined iat -> incongruent phase
    if choice == "conFirst":
        presentStimuli(combinedStimuli, conCombinedKey, window.conCombinedRedX,window.conCombinedCross,
                       window.conCombinedStimuli, window.conCombinedIatLeft, inconAttPrepare)

    # if incongruent phase first, congruent combined iat -> debrief
    else:
        presentStimuli(combinedStimuli, conCombinedKey, window.conCombinedRedX,window.conCombinedCross,
                       window.conCombinedStimuli, window.conCombinedIatLeft, debrief)


# 5. incongruent phase
# Incongruent Attitude IAT: left category as 'Positive' and right as 'Negative'
def inconAttPrepare():
    preparePage(window, incongruentAttitudeLbls, 9)

def inconAttIat():
    window.stackedExp.setCurrentIndex(10)

    # incongruent attitude -> incongruent combined
    presentStimuli(attitudeStimuli, inconAttKey, window.inconAttRedX,window.inconAttCross,
                   window.inconAttStimuli, window.inconAttIatLeft, inconCombinedPrepare)

# Incongruent Combined IAT: left category as 'Homosexuality \nPositive' and right as 'Heterosexuality \nNegative'
def inconCombinedPrepare():
    preparePage(window, incongruentCombinedLbls, 11)

def inconCombinedIat():
    window.stackedExp.setCurrentIndex(12)

    # if congruent phase first, incongruent combined iat -> debrief
    if choice == "conFirst":
        presentStimuli(combinedStimuli, inconCombinedKey, window.inconCombinedRedX,window.inconCombinedCross,
                       window.inconCombinedStimuli, window.inconCombinedIatLeft, debrief)

    # if incongruent phase first, incongruent combined iat -> congruent phase
    else:
        presentStimuli(combinedStimuli, inconCombinedKey, window.inconCombinedRedX, window.inconCombinedCross,
                       window.inconCombinedStimuli, window.inconCombinedIatLeft,conAttPrepare)


# 6. debrief
def recordDemographic():
    recordDemo(window)

def debrief():

    # go to brief page
    window.stackedExp.setCurrentIndex(13)

    # when finish button clicked, close the window and record demographic information
    window.finishButton.clicked.connect(QCoreApplication.instance().quit)
    window.finishButton.clicked.connect(recordDemographic)


# connect pages---------------------------------------------------------------------------------------------------------
## By pushing buttons to proceed
## consent -> demographic -> instruction -> sexuality
window.consentNextButton.clicked.connect(submitConsentPage)
window.demoNextButton.clicked.connect(submitDemographicPage)
window.instructionNextButton.clicked.connect(sexualityPrepare)

## prepare page -> corresponding iat page
window.sexualityBtn.clicked.connect(sexualityIat)
window.conAttBtn.clicked.connect(conAttIat)
window.conCombinedBtn.clicked.connect(conCombinedIat)
window.inconAttBtn.clicked.connect(inconAttIat)
window.inconCombinedBtn.clicked.connect(inconCombinedIat)

window.show()
exit(app.exec_())