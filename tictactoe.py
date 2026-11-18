# 파일: 22_tictactoe_gui.py
# 틱택토 GUI (tkinter)
import tkinter as tk

LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
]
WIN_COLOR = "#8BD67A"
NORMAL_COLOR = "#F2F2F2"

# 게임 상태를 딕셔너리 하나에 모아 둡니다.
state = {"turn": "X", "over": False}
score = {"X": 0, "O": 0, "무승부": 0}


def find_winner(board):
    for a, b, c in LINES:
        if board[a] != "" and board[a] == board[b] == board[c]:
            return (a, b, c)
    return None


def current_board():
    board = []
    for b in buttons:
        board.append(b["text"])
    return board


def update_score():
    score_label.config(text=f"X: {score['X']}승   O: {score['O']}승   무승부: {score['무승부']}")


def click(i):
    if state["over"] or buttons[i]["text"] != "":
        return

    player = state["turn"]
    color = "#D9534F" if player == "X" else "#337AB7"
    buttons[i].config(text=player, fg=color)

    board = current_board()
    line = find_winner(board)
    if line is not None:
        for n in line:
            buttons[n].config(bg=WIN_COLOR)
        status.config(text=f"{player} 승리!")
        score[player] += 1
        state["over"] = True
    elif "" not in board:
        status.config(text="무승부입니다!")
        score["무승부"] += 1
        state["over"] = True
    else:
        state["turn"] = "O" if player == "X" else "X"
        status.config(text=f"{state['turn']} 차례입니다")
    update_score()

def new_game():
    for b in buttons:
        b.config(text="", bg=NORMAL_COLOR)
    state["turn"] = "X"
    state["over"] = False
    status.config(text="X 차례입니다")

# ---------------- 화면 만들기 ----------------
window = tk.Tk()
window.title("틱택토")
window.resizable(False, False)

status = tk.Label(window, text="X 차례입니다", font=("Arial", 18, "bold"), pady=10)
status.grid(row=0, column=0, columnspan=3)

buttons = []
for i in range(9):
    b = tk.Button(window, text="", width=4, height=2, bg=NORMAL_COLOR,
                  font=("Arial", 32, "bold"), command=lambda n=i: click(n))
    b.grid(row=i // 3 + 1, column=i % 3, padx=3, pady=3)
    buttons.append(b)

score_label = tk.Label(window, text="", font=("Arial", 13))
score_label.grid(row=4, column=0, columnspan=3, pady=(10, 0))
update_score()

tk.Button(window, text="새 게임", font=("Arial", 13), command=new_game).grid(
    row=5, column=0, columnspan=3, pady=10)

window.mainloop()