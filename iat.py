from random import *
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from keyboard import *
import time

# This file has everything about setting up IAT,
# includes (1) several functions setting up IAT, and (2) the materials needed to achieve that

# leftORright -> tells if current stimulus belongs to left or right category
# stimulusType -> if the stimulus is a picture, present picture; if it's a word, present text
# changeLbls -> change the category labels corresponds with each phase
# preparePage -> calls changeLbls and go to correct prepare page
# class ExperimentPage -> tells if participants are categorizing correctly, record their reaction time
# presentStimuli -> converge all of the above, and is imported into main file to run iat

# Materials-------------------------------------------------------------------------------------------------------------
# stimuli
homoPics = ["Homosexuality", "homo1.png", "homo2.png", "homo3.png", "homo4.png", "homo5.png", "homo6.png", "homo7.png"]
heteroPics = ["Heterosexuality", "hetero1.png", "hetero2.png", "hetero3.png", "hetero4.png", "hetero5.png", "hetero6.png",
              "hetero7.png"]
positiveWords = ["Joy", "Love", "Peace", "Wonderful", "Pleasure", "Glorious", "Laughter", "Happy"]
negativeWords = ["Agony", "Terrible", "Horrible", "Nasty", "Evil", "Awful", "Failure", "Hurt"]

conLeft = homoPics + negativeWords
inconLeft = homoPics + positiveWords

# a list to know whether a stimuli belong to which group
source = [{"category": "Homosexuality", "stimuli": homoPics},
          {"category": "Negative", "stimuli": negativeWords},
          {"category": "Positive", "stimuli": positiveWords},
          {"category": "Homosexuality \nNegative", "stimuli": conLeft},
          {"category": "Homosexuality \nPositive", "stimuli": inconLeft}]

# use the above source list to find out which category the stimulus belongs to
# this function will return either "left" or "right"
def leftORright(leftIatLbl, stimulus):

    belongsTo = ""

    for pair in source:

        # when a/some category is on the left
        if pair["category"] in leftIatLbl.text():

            # when the stimulus presented belongs to the left category
            if stimulus in pair["stimuli"]:

                # the stimulus belongs to left
                belongsTo = "left"

            # when the stimulus presented doesn't belong to the left category
            else:

                # the stimulus belongs to right
                belongsTo = "right"

    return belongsTo


# identify the type of stimuli (either a picture or a word)
# if it's a word, setText to the label
# if it's a picture, setPixmap to the label
def stimulusType(stimulusLbl, stimulus):
    # if it's a picture
    if ".png" in stimulus:

        # present pic
        stimulusLbl.setPixmap(QPixmap(stimulus))

        # picture fit the label size
        stimulusLbl.setScaledContents(True)

    # if it's a word
    elif ".png" not in stimulus:

        # set text
        stimulusLbl.setText(stimulus)


# set the labels according to its iat phase
# the argument 'labels' refers to the labels used in the current iat phase, as shown in Materials section in main.py
def changeLbls(labels):
    for label in labels:

        # make sure prepare label and iat label are the same according to its iat
        label["prepareBtn"].setText(label["text"])
        label["iatBtn"].setText(label["text"])


# a function that changes label and goes to current index at the same time
def preparePage(win, labels, index):
    win.stackedExp.setCurrentIndex(index)
    changeLbls(labels)

# This is a class that represents every iat page:
# they are different in the name of specific widgets, the key,
# the stimuli used, the category label, and the next page heading to.
# so these are arguments that experimenter could change for different iats
class ExperimentPage:

    def __init__(self, stimuli, keyname, redX, cross, stimulusLbl, leftIatLbl, goto_next_page):
        self.stimulus_index = 0
        self.show_pic_time = 0
        self.results = [leftIatLbl.text().replace('\n', ' ')]   # the left label of iat, which indicates its phase
        self.stimuli = stimuli
        self.goto_next_page = goto_next_page
        self.keyname = keyname
        self.redX = redX
        self.cross = cross
        self.stimulusLbl = stimulusLbl
        self.leftIatLbl = leftIatLbl

        self.keyname.eReleased.connect(lambda: self.check(True))
        self.keyname.iReleased.connect(lambda: self.check(False))

    # actual function that show the stimuli
    def show_next_image(self):

        # if all the stimulus are presented
        if len(self.stimuli) == self.stimulus_index:

            # proceed to the page as indicated by the input argument
            self.goto_next_page()

            # append reaction time
            resultsData = open("results.csv", 'a+')
            resultsData.write(",".join(self.results) + "\n")
            resultsData.close()
            print(self.results)
            return


        self.show_pic_time = time.time()

        # both central cross and red 'x' are hided first
        self.redX.hide()
        self.cross.hide()

        # stimulus presented begin by the first item in the stimuli list
        stimulus = self.stimuli[self.stimulus_index]
        print(len(self.stimuli))
        print(self.stimulus_index)

        # if it's a picture, present picture; if it's a word, present text
        stimulusType(self.stimulusLbl, stimulus)

        # go the next stimulus
        self.stimulus_index += 1

    # identify which key would be correct to press
    def check(self, isLeft: bool):

        stimulus = self.stimuli[self.stimulus_index - 1]

        # if the stimulus belongs to left, press left key would be correct
        if leftORright(self.leftIatLbl, stimulus) == "left":
            if isLeft:
                self.correct()
            else:
                self.incorrect()
        else:
            if isLeft:
                self.incorrect()
            else:
                self.correct()

    # when the participants correctly categorize the stimuli
    def correct(self):

        # only when they're correct, the reaction time is recorded
        # if they're wrong, the stimuli wouldn't disappear until they have done it correctly
        time_elapsed = time.time() - self.show_pic_time
        self.results.append(str(time_elapsed))

        # when correct, show the central cross and hide the red 'x'
        self.redX.hide()
        self.cross.show()
        QTimer.singleShot(1000, self.show_next_image)

    # when the participants incorrectly categorize the stimuli
    def incorrect(self):

        # show red 'x'
        self.redX.show()


# combine all the iat set-ups together
def presentStimuli(stimuli, keyname, redX, cross, stimulusLbl, leftIatLbl, goto_next_page):

    # create the above object
    page = ExperimentPage(stimuli, keyname, redX, cross, stimulusLbl, leftIatLbl, goto_next_page)

    # show stimuli
    page.show_next_image()