BGCOLOR = "#21325E"
CORRECT_COLOR = "#F1D00A"
WRONG_COLOR = "#3E497A"
BTN_COLOR = "#F0F0F0"

import csv
from tkinter import *
import random
import os

# os.system("python english_web.py") #english_web 실행 
# os의 기능들은 동기적으로 실행되기 때문에 
# delay가 발생하면 결과가 도출될 때까지 기다렸다가 다음 기능을 순차적으로 실행합니다.

with open("out2.csv", "r", encoding="UTF-8-sig") as file:
        questions = list(csv.reader(file))

answer = 0
score = 0

#문제 생성
def next_question():
    global answer
    
    for i in range(4):
        buttons[i].config(bg=BTN_COLOR)
    
    multi_choice = random.sample(questions, 4) #questions 리스트에서 4개를 뽑아온다.
    answer = random.randint(0,3)
    cur_question = multi_choice[answer][0]
    
    question_label.config(text=cur_question)
    
    score_label.config(text= '점수 : ' + str(score), width = 20, font=("나눔바른펜", 15, "bold"), bg=BGCOLOR, fg="white")
    
    for i in range(4):
        buttons[i].config(text=multi_choice[i][1])
        
        
#정답 체크
def check_answer(idx):
    idx = int(idx)
    global score
    if answer == idx:
        buttons[idx].config(bg=CORRECT_COLOR)
        score = score+1
        window.after(100, next_question)
    else:
        buttons[idx].config(bg=WRONG_COLOR)


window = Tk()
window.title("영어 퀴즈")
window.config(padx=30, pady=10, bg=BGCOLOR)

question_label = Label(window, width=90, height=2, text="test", font=("나눔바른펜", 20, "bold"), bg=BGCOLOR, fg="white")
question_label.pack(pady=30)

#버튼 생성
buttons=[]
for i in range(4):
    btn = Button(window, text=f"{i}번", width=70, height=2, font=("나눔바른펜", 15, "bold"), bg=BTN_COLOR, command=lambda idx=i: check_answer(idx))
    btn.pack()
    buttons.append(btn)
    
next_btn = Button(window, text="다음 문제", width=15, height=2, command=next_question, font=("나눔바른펜", 15, "bold"), bg=CORRECT_COLOR)

next_btn.pack(pady=30)

score_label = Label(window, text = '점수 : ' + str(score), width = 20, font=("나눔바른펜", 15, "bold"), bg=BGCOLOR, fg="white")
score_label.pack(side = 'right', padx = 10, pady = 10)

next_question()

# window.itemconfig(score_label, text = str(score))

# score_label = Label(window, text=score)
# score_label.place(x=100,y=100)
# score_label.pack(pady=30)

window.mainloop()