from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sys
import random
import mysql.connector
from mysql.connector import Error

playername = ""
colname = ""
index = 0
score = 0
widgets = {
    "question": [],
    "answers": [],
    "option1": [],
    "option2": [],
    "option3": [],
    "option4": [],
    "score": [],
    "nextBtn": []
}
parameter = {
    "question": [],
    "option_one": [],
    "option_two": [],
    "option_three": [],
    "option_four": [],
    "correct_ans": [],
}

def t_catch(t):
    t = t.lower()
    t = t.replace(" ", "")
    global colname
    colname = t

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='test2',
            user='root',
            password='sql123'  # Replace with your root password
        )
        if connection.is_connected():
            print("Connected to MySQL database")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def insert_or_update_score(player_name, topic, score):
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            # Sanitize the topic name to replace spaces with underscores
            sanitized_topic = topic.replace(" ", "_").lower()
            
            # Check if the user already has a score for the topic
            query = f"SELECT {sanitized_topic} FROM scores WHERE username = %s"
            cursor.execute(query, (player_name,))
            result = cursor.fetchone()
            
            if result and result[0] is not None:
                current_score = result[0]
                if score > current_score:
                    # Update the score if the new score is higher
                    update_query = f"UPDATE scores SET {sanitized_topic} = %s WHERE username = %s"
                    cursor.execute(update_query, (score, player_name))
            else:
                # Insert a new record for the user
                insert_query = f"INSERT INTO scores (username, {sanitized_topic}) VALUES (%s, %s) ON DUPLICATE KEY UPDATE {sanitized_topic} = GREATEST({sanitized_topic}, %s)"
                cursor.execute(insert_query, (player_name, score, score))
            
            connection.commit()
            print("Score updated successfully")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

def qa(fname):
    clear_parameters()
    pq = []
    q = []
    a = []
    for i in range(0, 10):
        with open(fname, "r") as qa_file:
            while True:
                r = random.randint(0, 98)
                if pq.count(r) == 0 and r % 2 == 0:
                    pq.append(r)
                    break
            qna = qa_file.readlines()
            q.append(qna[r].strip())  # Remove newline characters
            a.append(qna[r + 1].strip())  # Remove newline characters
    return q, a

def match(t):
    filen = t + ".txt"
    q, a = qa(filen)
    ans = []
    qus = []
    a2 = []
    for i in range(0, 10):
        ai = a[i].split("|")
        qi = q[i]
        ans.append(ai[0])
        qus.append(qi)
        a3 = []
        for j in range(0, 4):
            if ai[j] != "":
                a3.append(ai[j])
        random.shuffle(a3)
        a2.append(a3)
    parameter["question"] = qus
    parameter["correct_ans"] = ans
    for i in a2:
        parameter["option_one"].append(i[0])
        parameter["option_two"].append(i[1])
        parameter["option_three"].append(i[2])
        parameter["option_four"].append(i[3])

def clear_parameters():
    for parm in parameter:
        if parameter[parm] != []:
            for i in range(0, len(parameter[parm])):
                parameter[parm].pop()

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
win.setGeometry(100, 100, 600, 600)
win.setWindowTitle("Quiz Program")
win.setStyleSheet("font-family: Lato; background: #FAFAFA;")
grid = QGridLayout()
win.setLayout(grid)

"""
===========================================
            MAIN MENU FUNCTION
===========================================
"""
# Window displaying the Main Menu of the Game
def main_menu():
    clearLayout(grid)
    title = QLabel()
    title.setText("Quiz Program")
    title.setAlignment(Qt.AlignCenter)
    title.setObjectName("title")
    title.setStyleSheet("QLabel#title { font-size:75px; margin-top: 100px;font-family:Times New Roman;font-weight:bold; background:none;}")
    grid.addWidget(title, 0, 0)
    
    # Add subtitle
    subtitle = QLabel()
    subtitle.setText("A guide for Comprehensive Course Work!")
    subtitle.setAlignment(Qt.AlignCenter)
    subtitle.setObjectName("subtitle")
    subtitle.setStyleSheet("QLabel#subtitle { font-size:20px; font-style:italic;  margin-top: 0px; background:none;}")
    grid.addWidget(subtitle, 1, 0)
    
    playBtn = QPushButton("PLAY")
    playBtn.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
    playBtn.setObjectName("playbtn")
    playBtn.setStyleSheet("QPushButton#playbtn{font-size:20px; color:white; border-radius:10px; padding:25px 70px; margin-bottom:20px; background:#0E1428; max-width:300px;} QPushButton#playbtn:hover{background:#4281A4;}")
    playBtn.clicked.connect(user_name)
    grid.addWidget(playBtn, 2, 0)
    
    scoresBtn = QPushButton("SCORES")
    scoresBtn.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
    scoresBtn.setObjectName("scoresbtn")
    scoresBtn.setStyleSheet("QPushButton#scoresbtn{font-size:20px; color:white; border-radius:10px; padding:25px 70px; margin-bottom:20px; background:#0E1428; max-width:300px;} QPushButton#scoresbtn:hover{background:#4281A4;}")
    scoresBtn.clicked.connect(display_scores)
    grid.addWidget(scoresBtn, 3, 0)
    
    quitBtn = QPushButton("QUIT")
    quitBtn.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
    quitBtn.setObjectName("replaybtn")
    quitBtn.setStyleSheet("QPushButton#replaybtn{font-size:20px; color:white; border-radius:10px; padding:25px 70px; margin-bottom:20px; background:#0E1428; max-width:300px;} QPushButton#replaybtn:hover{background:#4281A4}")
    quitBtn.clicked.connect(lambda: sys.exit())
    grid.addWidget(quitBtn, 4, 0)

"""
=======================================
            USER NAME FUNCTION
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
        playername = line.text()
        topick()
    btn = QPushButton("Enter")
    btn.setStyleSheet("QPushButton{font-size:20px; color:white; border-radius:10px; padding:25px 10px; margin-bottom:20px; background:#0E1428;} QPushButton:hover{background:#4281A4;}")
    btn.clicked.connect(handleNameInput)
    btn.setEnabled(False)
    def textboxChange():
        if line.text():
            btn.setEnabled(True)
    line.textChanged.connect(textboxChange)
    grid.addWidget(nameLabel, 0, 0)
    grid.addWidget(line, 1, 0)
    grid.addWidget(btn, 2, 0)

"""
=======================================
            TOPIC SELECTION FUNCTION
=======================================
"""
def topick():
    clearLayout(grid)
    nameLabel = QLabel()
    nameLabel.setText('Pick Topic:')
    nameLabel.setAlignment(Qt.AlignCenter)
    nameLabel.setStyleSheet("*{ max-height: 27px; font-size: 25px; margin: 0px; padding: 0px;}")
    grid.addWidget(nameLabel, 0, 0)
    topics = ["Data Structures", "Operating Systems", "COA", "Database Management", "FLAT"]
    for i, topic in enumerate(topics):
        btn = QPushButton(topic)
        btn.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
        btn.setObjectName(f"topicBtn{i}")
        btn.setStyleSheet("QPushButton{font-size:20px; color:white; border-radius:10px; padding:25px 10px; margin-bottom:20px; background:#0E1428; max-width:300px;} QPushButton:hover{background:#4281A4;}")
        btn.clicked.connect(lambda checked, t=topic: play_with_topic(t))
        grid.addWidget(btn, i + 1, 0)

def play_with_topic(topic):
    print(topic)
    print(f"Playing quiz on {topic}")
    match(topic)
    t_catch(topic)
    play()

"""
=======================================
            CREATE BUTTON FUNCTION
=======================================
"""
def create_btn(option):
    optionBtn = QPushButton(option)
    optionBtn.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
    optionBtn.setFixedWidth(300)  # Increased width
    optionBtn.setObjectName("optionBtn")
    optionBtn.setStyleSheet("QPushButton#optionBtn{font-size:20px; color:white; border-radius:10px; padding:25px 10px; margin-bottom:20px; background:#0E1428;} QPushButton#optionBtn:hover{background:#4281A4;}")
    optionBtn.clicked.connect(lambda: is_correct(optionBtn))
    return optionBtn

"""
=======================================
            PLAY FUNCTION
=======================================
"""
def play():
    clearLayout(grid)
    global score
    score = 0
    scoreTxt = QLabel()
    scoreTxt.setText("SCORE : " + str(score))
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
    option1 = create_btn(parameter["option_one"][index])
    option2 = create_btn(parameter["option_two"][index])
    option3 = create_btn(parameter["option_three"][index])
    option4 = create_btn(parameter["option_four"][index])
    widgets["option1"].append(option1)
    widgets["option2"].append(option2)
    widgets["option3"].append(option3)
    widgets["option4"].append(option4)
    nextBtn = QPushButton("Next")
    nextBtn.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
    nextBtn.setObjectName("nextBtn")
    nextBtn.setStyleSheet("QPushButton#nextBtn{font-size:20px; color:white; border-radius:10px; padding:25px 10px; margin-bottom:20px; background:#0E1428; max-width:300px;} QPushButton#nextBtn:hover{background:#4281A4;}")
    nextBtn.clicked.connect(next_question)
    nextBtn.setEnabled(False)  # Initially disabled
    widgets["nextBtn"].append(nextBtn)
    grid.addWidget(widgets["score"][-1], 0, 0, 1, 2)
    grid.addWidget(widgets["question"][-1], 1, 0, 1, 2)
    grid.addWidget(widgets["option1"][-1], 2, 0)
    grid.addWidget(widgets["option2"][-1], 2, 1)
    grid.addWidget(widgets["option3"][-1], 3, 0)
    grid.addWidget(widgets["option4"][-1], 3, 1)
    grid.addWidget(widgets["nextBtn"][-1], 4, 0, 1, 2, alignment=Qt.AlignCenter)

def is_correct(btn):
    global score
    if btn.text() == parameter["correct_ans"][index]:
        score += 10
        btn.setStyleSheet("QPushButton{font-size:20px; color:white; border-radius:10px; padding:25px 10px; margin-bottom:20px; background:green; max-width:300px;}")
    else:
        btn.setStyleSheet("QPushButton{font-size:20px; color:white; border-radius:10px; padding:25px 10px; margin-bottom:20px; background:red; max-width:300px;}")
        correct_btn = get_correct_button()
        correct_btn.setStyleSheet("QPushButton{font-size:20px; color:white; border-radius:10px; padding:25px 10px; margin-bottom:20px; background:green; max-width:300px;}")
    widgets["score"][-1].setText("SCORE : " + str(score))
    widgets["nextBtn"][-1].setEnabled(True)  # Enable the next button
    # Disable all option buttons
    for option in ["option1", "option2", "option3", "option4"]:
        widgets[option][-1].setEnabled(False)

def get_correct_button():
    options = ["option1", "option2", "option3", "option4"]
    for option in options:
        if widgets[option][-1].text() == parameter["correct_ans"][index]:
            return widgets[option][-1]

def next_question():
    global index
    if index >= 9:
        index = 0
        over()
    else:
        index += 1
        widgets["nextBtn"][-1].setEnabled(False)  # Disable the next button
        reset_button_styles()
        update_question_and_options()

def reset_button_styles():
    options = ["option1", "option2", "option3", "option4"]
    for option in options:
        widgets[option][-1].setStyleSheet("QPushButton{font-size:20px; color:white; border-radius:10px; padding:25px 10px; margin-bottom:20px; background:#0E1428; max-width:300px;} QPushButton:hover{background:#4281A4;}")
        widgets[option][-1].setEnabled(True)  # Re-enable the buttons

def update_question_and_options():
    widgets["question"][-1].setText(parameter["question"][index])
    widgets["option1"][-1].setText(parameter["option_one"][index])
    widgets["option2"][-1].setText(parameter["option_two"][index])
    widgets["option3"][-1].setText(parameter["option_three"][index])
    widgets["option4"][-1].setText(parameter["option_four"][index])

"""
=========================================
            OVER FUNCTION
=========================================
"""
def over():
    clearLayout(grid)
    thanksTxt = QLabel(f"Thanks for playing! {playername}'s Score was : {score}")
    thanksTxt.setAlignment(Qt.AlignCenter)
    thanksTxt.setStyleSheet("*{ font-size: 30px; background:none;}")
    grid.addWidget(thanksTxt, 0, 0)
    replayBtn = QPushButton("Replay")
    replayBtn.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
    replayBtn.setObjectName("replaybtn")
    replayBtn.setStyleSheet("QPushButton#replaybtn{font-size:20px; color:white; border-radius:10px; padding:25px 10px; margin-bottom:20px; background:#0E1428; max-width:300px;} QPushButton#replaybtn:hover{background:#4281A4;}")
    replayBtn.clicked.connect(user_name)
    grid.addWidget(replayBtn, 1, 0)
    backBtn = QPushButton("Back to Main Menu")
    backBtn.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
    backBtn.setObjectName("replaybtn")
    backBtn.setStyleSheet("QPushButton#replaybtn{font-size:20px; color:white; border-radius:10px; padding:25px 10px; margin-bottom:20px; background:#0E1428; max-width:300px;} QPushButton#replaybtn:hover{background:#4281A4;}")
    backBtn.clicked.connect(main_menu)
    grid.addWidget(backBtn, 2, 0)
    # Insert or update the score in the database
    insert_or_update_score(playername, colname, score)

def display_scores():
    clearLayout(grid)
    title = QLabel()
    title.setText("High Scores")
    title.setAlignment(Qt.AlignCenter)
    title.setObjectName("title")
    title.setStyleSheet("QLabel#title { font-size:35px; margin-top: 0px; background:none;}")
    grid.addWidget(title, 0, 0, 1, 2)
    
    scores_table = QTableWidget()
    scores_table.setColumnCount(6)
    scores_table.setHorizontalHeaderLabels(["Username", "COA", "DS", "DBMS", "FLAT", "OS"])
    scores_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    scores_table.verticalHeader().setVisible(False)
    
    connection = create_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM scores"
            cursor.execute(query)
            results = cursor.fetchall()
            scores_table.setRowCount(len(results))
            for row, result in enumerate(results):
                for col, value in enumerate(result):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignCenter)
                    scores_table.setItem(row, col, item)
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()
    
    grid.addWidget(scores_table, 1, 0, 1, 2)
    
    backBtn = QPushButton("Back to Main Menu")
    backBtn.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
    backBtn.setObjectName("replaybtn")
    backBtn.setStyleSheet("QPushButton#replaybtn{font-size:20px; color:white; border-radius:10px; padding:25px 10px; margin-bottom:20px; background:#0E1428; max-width:300px;} QPushButton#replaybtn:hover{background:#4281A4;}")
    backBtn.clicked.connect(main_menu)
    grid.addWidget(backBtn, 2, 0, 1, 2, alignment=Qt.AlignCenter)

if __name__ == '__main__':
    main_menu()
    win.show()
    sys.exit(app.exec())