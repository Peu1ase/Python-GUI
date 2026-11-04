import tkinter as tk

root = tk.Tk()

root.title("test")
root.geometry("1200x640")

# ========== 메뉴바 ==========
mnu_bar = tk.Menu(root)

# 파일
file_mnu = tk.Menu(mnu_bar, tearoff=0)
file_mnu.add_command(label="열기", command=lambda: print("열기 클릭"))
file_mnu.add_separator()
file_mnu.add_command(label="저장", command=None)
file_mnu.add_command(label="다른 이름으로 저장", command=None)
file_mnu.add_separator()
file_mnu.add_command(label="종료", command=root.destroy)

mnu_bar.add_cascade(label="파일", menu=file_mnu)

# 편집
edit_mnu = tk.Menu(mnu_bar, tearoff=0)

edit_mnu.add_command(label="실행취소", command=None)
edit_mnu.add_separator()
edit_mnu.add_command(label="잘라내기", command=None)
edit_mnu.add_command(label="복사", command=None)
edit_mnu.add_command(label="붙여넣기", command=None)
edit_mnu.add_command(label="삭제", command=None)

mnu_bar.add_cascade(label="편집", menu=edit_mnu)

root.config(menu=mnu_bar)

# ========== 텍스트창 ==========
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)

txt = tk.Text(root)
txt.grid(row=0, column=0, sticky="nsew")
excel = tk.Text(root)
excel.grid(row=0, column=1, sticky="nsew")

root.mainloop()