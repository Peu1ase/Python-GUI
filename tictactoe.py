import tkinter as tk

LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
]
WIN_COLOR = "#8BD67A"
NORMAL_COLOR = "#F2F2F2"

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("틱택토")
        self.root.resizable(False, False)

        # 게임 상태 및 데이터 초기화
        self.turn = "X"
        self.over = False
        self.score = {"X": 0, "O": 0, "무승부": 0}
        self.board = [""] * 9

        self.create_widgets()

    def create_widgets(self):
        # 상단 상태 레이블
        self.status = tk.Label(
            self.root, text="X 차례입니다", font=("Arial", 18, "bold"), pady=10
        )
        self.status.grid(row=0, column=0, columnspan=3)

        # 3x3 버튼 생성
        self.buttons = []
        for i in range(9):
            b = tk.Button(
                self.root, text="", width=4, height=2, bg=NORMAL_COLOR,
                font=("Arial", 32, "bold"), command=lambda n=i: self.click(n)
            )
            b.grid(row=i // 3 + 1, column=i % 3, padx=3, pady=3)
            self.buttons.append(b)

        # 점수판 레이블
        self.score_label = tk.Label(self.root, text="", font=("Arial", 13))
        self.score_label.grid(row=4, column=0, columnspan=3, pady=(10, 0))
        self.update_score()

        # 새 게임 버튼
        tk.Button(
            self.root, text="새 게임", font=("Arial", 13), command=self.new_game
        ).grid(row=5, column=0, columnspan=3, pady=10)

    def find_winner(self):
        for a, b, c in LINES:
            if self.board[a] != "" and self.board[a] == self.board[b] == self.board[c]:
                return (a, b, c)
        return None

    def update_score(self):
        text = f"X: {self.score['X']}승   O: {self.score['O']}승   무승부: {self.score['무승부']}"
        self.score_label.config(text=text)

    def click(self, i):
        if self.over or self.board[i] != "":
            return

        player = self.turn
        color = "#D9534F" if player == "X" else "#337AB7"
        
        # 데이터 업데이트 및 UI 반영
        self.board[i] = player
        self.buttons[i].config(text=player, fg=color)

        line = self.find_winner()
        if line is not None:
            for n in line:
                self.buttons[n].config(bg=WIN_COLOR)
            self.status.config(text=f"{player} 승리!")
            self.score[player] += 1
            self.over = True
        elif "" not in self.board:
            self.status.config(text="무승부입니다!")
            self.score["무승부"] += 1
            self.over = True
        else:
            self.turn = "O" if player == "X" else "X"
            self.status.config(text=f"{self.turn} 차례입니다")
        
        self.update_score()

    def new_game(self):
        self.board = [""] * 9
        for b in self.buttons:
            b.config(text="", bg=NORMAL_COLOR)
        self.turn = "X"
        self.over = False
        self.status.config(text="X 차례입니다")

if __name__ == "__main__":
    window = tk.Tk()
    app = TicTacToeApp(window)
    window.mainloop()
