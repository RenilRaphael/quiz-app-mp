from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sys
import time
import random





playername=""

def qa():
    pq=[]
    q = []
    a = []
    for i in range(0,10):
        qa = open("qna.txt","r")                                       
        while True:
            r = random.randint(0,442)
            if pq.count(r)==0 and r%2 == 0:
                pq.append(r)
                break
        qna = qa.readlines()
        q.append(qna[r])
        a.append(qna[r+1])
    return q,a


        



index = 0

score = 0

widgets = {
    "question":[],
    "answers":[],
    "option1":[],
    "option2":[],
    "option3":[],
    "option4":[],
    "score":[]
}


parameter = {
    "question":[],
    "option_one":[],
    "option_two":[],
    "option_three":[],
    "option_four":[],
    "correct_ans":[],
}
def match():
    q,a = qa()
    ans = []
    qus = []
    a2 = []
    for i in range(0,10):
        ai = a[i].split("|")
        qi = q[i].split("\n")
      
        ans.append(ai[0])
        qus.append(qi[0])
        a3 = []
        for i in range(0,5):
            if ai[i] != "\n":
                a3.append(ai[i])
        random.shuffle(a3)
        a2.append(a3)
    parameter["question"] = qus
    parameter["correct_ans"]= ans
    for i in a2:
        parameter["option_one"].append(i[0])
        parameter["option_two"].append(i[1])
        parameter["option_three"].append(i[2])
        parameter["option_four"].append(i[3])





#clear the global dictionary of parameters
def clear_parameters():
    for parm in parameter:
        if parameter[parm] != []:
            for i in range(0, len(parameter[parm])):
                parameter[parm].pop()


#function to clear existing widgets
def clearLayout(layout):
    if layout is not None:
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                clearLayout(child.layout())

# Essential Boilerplate Code to configure the Window
app = QApplication(sys.argv)



win = QWidget()
win.setGeometry(100,100,600,600)    
win.setWindowTitle("Quiz Program")  
  

win.setStyleSheet("font-family: Lato; background: #FAFAFA;")


grid = QGridLayout()
win.setLayout(grid)

"""
===========================================
            MAIN MENU FUNCTION
===========================================
"""
#Window displaying the Main Menu of the Game
def main_menu():
    clearLayout(grid)

    
    title = QLabel()
    title.setText("Quiz Program")  
    title.setAlignment(Qt.AlignCenter)  
    title.setObjectName("title")   
    title.setStyleSheet("QLabel#title { font-size:35px; margin-top: 0px; background:none;}")

    grid.addWidget(title, 0, 0)


    
    btn = QPushButton("PLAY")
    btn.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
    btn.setObjectName("playbtn")
    btn.setStyleSheet("QPushButton#playbtn{font-size:20px; color:white; border-radius:10px; padding:25px 10px; margin-bottom:20px; background:#0E1428; max-width:300px;} QPushButton#playbtn:hover{background:#4281A4;}")
    grid.addWidget(btn, 1, 0)
    btn.clicked.connect(user_name)

    scoresBtn = QPushButton("SCORES")
    scoresBtn.setCursor(QtGui.QCursor(Qt.PointingHandCursor)) 
    scoresBtn.setObjectName("playbtn")
    scoresBtn.setStyleSheet("QPushButton#playbtn{font-size:20px; color:white; border-radius:10px; padding:25px 10px; margin-bottom:20px; background:#0E1428; max-width:300px;} QPushButton#playbtn:hover{background:#4281A4}")
    grid.addWidget(scoresBtn, 2, 0)
    scoresBtn.clicked.connect(sql_ui)
    
    quitBtn = QPushButton("QUIT")
    quitBtn.setCursor(QtGui.QCursor(Qt.PointingHandCursor)) 
    quitBtn.setObjectName("replaybtn")
    quitBtn.setStyleSheet("QPushButton#replaybtn{font-size:20px; color:white; border-radius:10px; padding:25px 10px; margin-bottom:20px; background:#0E1428; max-width:300px;} QPushButton#replaybtn:hover{background:#4281A4}")
    
    quitBtn.clicked.connect(lambda: sys.exit())
    grid.addWidget(quitBtn, 3,0)


"""
=======================================
            PLAY FUNCION
=======================================
"""

def user_name():
    clearLayout(grid)
    nameLabel = QLabel()
    nameLabel.setText('Enter Name:')
    nameLabel.setAlignment(Qt.AlignCenter)
    nameLabel.setStyleSheet("*{ max-height: 20px; font-size: 25px; margin: 0px; padding: 0px;}")
    
    line = QLineEdit()
    line.setAlignment(Qt.AlignCenter)
    line.setStyleSheet("* { max-width: 300px; margin: 0px; padding: 0px; max-height: 30px; font-size: 22px;}")

    def handleNameInput():
        global playername
        playername=line.text()
        play()
   
    btn = QPushButton("Enter")
    btn.setStyleSheet("*{font-size:20px; color:white; border-radius:10px; padding:25px 10px; margin-bottom:20px; background:#0E1428;} *:hover:hover{background:#4281A4;}")
    btn.clicked.connect(handleNameInput)
    btn.setEnabled(False)

    def textboxChange():
        if line.text != "":
            btn.setEnabled(True)

    line.textChanged.connect(textboxChange)
        
    grid.addWidget(nameLabel, 0, 0)
    grid.addWidget(line, 1, 0)
    grid.addWidget(btn, 2, 0)
 
    
def play():

    clearLayout(grid)
    score = 0
    
   
    scoreTxt = QLabel()
    scoreTxt.setText("SCORE : "+str(score))
    scoreTxt.setAlignment(Qt.AlignCenter)
    scoreTxt.setObjectName("scoreTxt")
    scoreTxt.setStyleSheet("QLabel#scoreTxt{font-size:32px; font-weight:bold; color:#F26419; max-height: 80px;background: none;}")
    widgets["score"].append(scoreTxt)

   
    questionTxt = QLabel(parameter["question"][index])
    questionTxt.setObjectName("qtext")
    questionTxt.setAlignment(Qt.AlignCenter)
    questionTxt.setStyleSheet("QLabel#qtext{ font-size: 20px;background:none;}")
    questionTxt.setWordWrap(True)
    widgets["question"].append(questionTxt)

    
    def create_btn(option):
        optionBtn = QPushButton(option)
        optionBtn.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        optionBtn.setFixedWidth(250)
        optionBtn.setObjectName("optionBtn")
        optionBtn.setStyleSheet("QPushButton#optionBtn{font-size:20px; color:white; border-radius:10px; padding:25px 10px; margin-bottom:20px; background:#0E1428;} QPushButton#optionBtn:hover{background:#4281A4;}")
        optionBtn.clicked.connect(lambda: is_correct(optionBtn))   
        return optionBtn

   
    option1 = create_btn(parameter["option_one"][index])
    option2 = create_btn(parameter["option_two"][index])
    option3 = create_btn(parameter["option_three"][index])
    option4 = create_btn(parameter["option_four"][index])
    
    widgets["option1"].append(option1)
    widgets["option2"].append(option2)
    widgets["option3"].append(option3)
    widgets["option4"].append(option4)

    
    grid.addWidget(widgets["score"][-1], 0, 0, 1, 2)
    grid.addWidget(widgets["question"][-1], 1,0, 1, 2)
    grid.addWidget(widgets["option1"][-1], 2,0)
    grid.addWidget(widgets["option2"][-1], 2,1)
    grid.addWidget(widgets["option3"][-1], 3,0)
    grid.addWidget(widgets["option4"][-1], 3,1)

    def is_correct(btn):
        global index
        
        if btn.text() == parameter["correct_ans"][index]:
            global score
            score += 10

            widgets["score"][-1].setText("SCORE : "+str(score))
            

        if index >= 9:
            index = 0
            over()
        else:
            index +=1           
            widgets["question"][-1].setText(parameter["question"][index])
            widgets["option1"][-1].setText(parameter["option_one"][index])
            widgets["option2"][-1].setText(parameter["option_two"][index])
            widgets["option3"][-1].setText(parameter["option_three"][index])
            widgets["option4"][-1].setText(parameter["option_four"][index])
 
       

"""
=========================================
            SQL FUNCTION
=========================================
"""
import mysql.connector as my
db=my.connect(host="localhost",user="root",password="deva",database="Quiz")
cur=db.cursor()

input_data_one = " INSERT INTO Score(Name, Score) VALUES (%s, %s)"
input_data_two = "UPDATE Score SET Score=Score +(%s) WHERE Name=(%s)"
input_data_three = "SELECT * FROM Score WHERE Name=(%s)"

def display_score():
    try:
        cur.execute("SELECT*FROM Score")
        data=cur.fetchall()
        return data
    except Exception as e:
        return e

def add_score_record(player_name,score):
    cur.execute(input_data_three, (player_name,))
    d = cur.fetchall()
    if d == []:
        cur.execute(input_data_one, (player_name, score))
        db.commit()
    else:
        cur.execute(input_data_two, (score, player_name))
        db.commit()

def sql_ui():
    clearLayout(grid)

    table = QTableWidget()

    data = display_score()

    
    table.setColumnCount(2)
    

    for i in data:
        row_no = table.rowCount()
        table.insertRow(row_no)
        table.setItem(row_no, 0, QTableWidgetItem(data[row_no][0]))
        table.setItem(row_no, 1, QTableWidgetItem(str(data[row_no][1])))
        

    

    table.setHorizontalHeaderLabels(["Player Name", "Score"])
    hheader = table.horizontalHeader()
    hheader.setSectionResizeMode(QHeaderView.Stretch)
    table.setEditTriggers(QTableWidget.NoEditTriggers)

    
    grid.addWidget(table, 0,0)

    backBtn = QPushButton("Back to Main Menu")
    backBtn.setCursor(QtGui.QCursor(Qt.PointingHandCursor)) 
    backBtn.setObjectName("replaybtn")
    backBtn.setStyleSheet("QPushButton#replaybtn{font-size:20px; color:white; border-radius:10px; padding:25px 10px; margin-bottom:20px; background:#0E1428; max-width:300px;} QPushButton#replaybtn:hover{background:#4281A4;} ")
    backBtn.clicked.connect(main_menu)

    grid.addWidget(backBtn, 1,0)

"""Function to Quit"""

def over():
    clearLayout(grid)
    

    add_score_record(playername, score)

    thanksTxt = QLabel("Thanks for playing! \n "+playername+"'s Score was : {}".format(score))
    thanksTxt.setAlignment(Qt.AlignCenter)
    thanksTxt.setStyleSheet("*{ font-size: 30px; background:none;}")
    grid.addWidget(thanksTxt, 0, 0)

    replayBtn = QPushButton("Replay")
    replayBtn.setCursor(QtGui.QCursor(Qt.PointingHandCursor)) 
    replayBtn.setObjectName("replaybtn")
    replayBtn.setStyleSheet("QPushButton#replaybtn{font-size:20px; color:white; border-radius:10px; padding:25px 10px; margin-bottom:20px; background:#0E1428; max-width:300px;} QPushButton#replaybtn:hover{background:#4281A4;}")
    replayBtn.clicked.connect(user_name)
    grid.addWidget(replayBtn, 1,0)

    backBtn = QPushButton("Back to Main Menu")
    backBtn.setCursor(QtGui.QCursor(Qt.PointingHandCursor)) 
    backBtn.setObjectName("replaybtn")
    backBtn.setStyleSheet("QPushButton#replaybtn{font-size:20px; color:white; border-radius:10px; padding:25px 10px; margin-bottom:20px; background:#0E1428; max-width:300px;} QPushButton#replaybtn:hover{background:#4281A4;} ")
    backBtn.clicked.connect(main_menu)
    grid.addWidget(backBtn, 2,0)


if __name__ == '__main__':
    clearLayout(grid)
    match()
    main_menu()



win.show()
sys.exit(app.exec())
