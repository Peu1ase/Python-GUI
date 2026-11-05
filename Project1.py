
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os


class MemoApp:

    def __init__(self, root):
        self.root = root
        self.current_file = None
        self.is_modified = False
        self.extension_window = None

        self.setup_window()
        self.setup_menu()
        self.setup_editor()
        self.setup_statusbar()
        self.setup_shortcuts()

        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    # ==============================
    # 메인 창 설정
    # ==============================

    def setup_window(self):
        self.root.title("메모장")
        self.root.geometry("1200x800")
        self.root.minsize(700, 500)

    # ==============================
    # 메뉴바 설정
    # ==============================

    def setup_menu(self):

        mnu_bar = tk.Menu(self.root)

        # 파일 메뉴
        file_mnu = tk.Menu(mnu_bar, tearoff=0)

        file_mnu.add_command(
            label="새 파일",
            command=self.new_file,
            accelerator="Ctrl+N"
        )

        file_mnu.add_command(
            label="열기",
            command=self.open_file,
            accelerator="Ctrl+O"
        )

        file_mnu.add_separator()

        file_mnu.add_command(
            label="저장",
            command=self.save_file,
            accelerator="Ctrl+S"
        )

        file_mnu.add_command(
            label="다른 이름으로 저장",
            command=self.save_as,
            accelerator="Ctrl+Shift+S"
        )

        file_mnu.add_separator()

        file_mnu.add_command(
            label="종료",
            command=self.close_app
        )

        mnu_bar.add_cascade(
            label="파일",
            menu=file_mnu
        )

        # 편집 메뉴
        edit_mnu = tk.Menu(mnu_bar, tearoff=0)

        edit_mnu.add_command(
            label="실행 취소",
            command=lambda: self.edit_command("undo"),
            accelerator="Ctrl+Z"
        )

        edit_mnu.add_separator()

        edit_mnu.add_command(
            label="잘라내기",
            command=lambda: self.edit_command("cut"),
            accelerator="Ctrl+X"
        )

        edit_mnu.add_command(
            label="복사",
            command=lambda: self.edit_command("copy"),
            accelerator="Ctrl+C"
        )

        edit_mnu.add_command(
            label="붙여넣기",
            command=lambda: self.edit_command("paste"),
            accelerator="Ctrl+V"
        )

        edit_mnu.add_command(
            label="삭제",
            command=self.delete_selection
        )

        edit_mnu.add_separator()

        edit_mnu.add_command(
            label="전체 선택",
            command=self.select_all,
            accelerator="Ctrl+A"
        )

        mnu_bar.add_cascade(
            label="편집",
            menu=edit_mnu
        )

        # 확장 기능 메뉴
        extension_mnu = tk.Menu(mnu_bar, tearoff=0)

        extension_mnu.add_command(
            label="가계부 도구",
            command=self.open_extension
        )

        mnu_bar.add_cascade(
            label="확장 기능",
            menu=extension_mnu
        )

        self.root.config(menu=mnu_bar)

    # ==============================
    # 메모장 편집 영역
    # ==============================

    def setup_editor(self):

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        editor_frame = ttk.Frame(self.root)
        editor_frame.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        editor_frame.columnconfigure(0, weight=1)
        editor_frame.rowconfigure(0, weight=1)

        self.editor = tk.Text(
            editor_frame,
            wrap="word",
            undo=True,
            autoseparators=True,
            maxundo=-1,
            font=("맑은 고딕", 11),
            padx=10,
            pady=10
        )

        self.editor.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scrollbar = ttk.Scrollbar(
            editor_frame,
            orient="vertical",
            command=self.editor.yview
        )

        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        self.editor.config(
            yscrollcommand=scrollbar.set
        )

        self.editor.bind(
            "<<Modified>>",
            self.on_modified
        )

        self.editor.bind(
            "<KeyRelease>",
            self.update_status
        )

        self.editor.bind(
            "<ButtonRelease-1>",
            self.update_status
        )

    # ==============================
    # 상태 표시줄
    # ==============================

    def setup_statusbar(self):

        self.statusbar = ttk.Label(
            self.root,
            text="줄 1, 열 1",
            anchor="w",
            relief="sunken",
            padding=(5, 3)
        )

        self.statusbar.grid(
            row=1,
            column=0,
            sticky="ew"
        )

    def update_status(self, event=None):

        position = self.editor.index("insert")

        line, column = position.split(".")

        self.statusbar.config(
            text=f"줄 {line}, 열 {int(column) + 1}"
        )

    # ==============================
    # 키보드 단축키
    # ==============================

    def setup_shortcuts(self):

        self.root.bind(
            "<Control-n>",
            lambda event: self.new_file()
        )

        self.root.bind(
            "<Control-o>",
            lambda event: self.open_file()
        )

        self.root.bind(
            "<Control-s>",
            lambda event: self.save_file()
        )

        self.root.bind(
            "<Control-Shift-S>",
            lambda event: self.save_as()
        )

        self.editor.bind(
            "<Control-a>",
            self.select_all
        )

    # ==============================
    # 파일 관리 기능
    # ==============================

    def on_modified(self, event=None):

        if self.editor.edit_modified():

            self.is_modified = True

            self.update_title()

            self.editor.edit_modified(False)

    def update_title(self):

        filename = (
            os.path.basename(self.current_file)
            if self.current_file
            else "제목 없음"
        )

        mark = "*" if self.is_modified else ""

        self.root.title(f"{mark}{filename} - 메모장")

    def confirm_save(self):

        if not self.is_modified:
            return True

        result = messagebox.askyesnocancel(
            "저장 확인",
            "변경된 내용을 저장하시겠습니까?"
        )

        if result is None:
            return False

        if result:
            return self.save_file()

        return True

    def new_file(self):

        if not self.confirm_save():
            return

        self.editor.delete("1.0", "end")

        self.current_file = None
        self.is_modified = False

        self.editor.edit_modified(False)

        self.update_title()
        self.update_status()

    def open_file(self):

        if not self.confirm_save():
            return

        filepath = filedialog.askopenfilename(
            title="파일 열기",
            filetypes=[
                ("텍스트 파일", "*.txt"),
                ("모든 파일", "*.*")
            ]
        )

        if not filepath:
            return

        try:
            with open(
                filepath,
                "r",
                encoding="utf-8"
            ) as file:

                content = file.read()

            self.editor.delete("1.0", "end")
            self.editor.insert("1.0", content)

            self.current_file = filepath
            self.is_modified = False

            self.editor.edit_modified(False)

            self.update_title()
            self.update_status()

        except (OSError, UnicodeError) as error:

            messagebox.showerror(
                "파일 열기 오류",
                str(error)
            )

    def save_file(self):

        if self.current_file is None:
            return self.save_as()

        return self.write_file(self.current_file)

    def save_as(self):

        filepath = filedialog.asksaveasfilename(
            title="다른 이름으로 저장",
            defaultextension=".txt",
            filetypes=[
                ("텍스트 파일", "*.txt"),
                ("모든 파일", "*.*")
            ]
        )

        if not filepath:
            return False

        return self.write_file(filepath)

    def write_file(self, filepath):

        content = self.editor.get(
            "1.0",
            "end-1c"
        )

        try:
            with open(
                filepath,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(content)

            self.current_file = filepath
            self.is_modified = False

            self.editor.edit_modified(False)

            self.update_title()

            return True

        except OSError as error:

            messagebox.showerror(
                "저장 오류",
                str(error)
            )

            return False

    # ==============================
    # 편집 기능
    # ==============================

    def edit_command(self, command):

        try:
            self.editor.focus_set()

            self.editor.event_generate(
                f"<<{command.capitalize()}>>"
            )

        except tk.TclError:
            pass

    def delete_selection(self):

        try:
            self.editor.delete("sel.first", "sel.last")

        except tk.TclError:
            pass

    def select_all(self, event=None):

        self.editor.tag_add(
            "sel",
            "1.0",
            "end-1c"
        )

        self.editor.mark_set(
            "insert",
            "1.0"
        )

        self.editor.see("insert")

        return "break"

    # ==============================
    # 확장 프로그램 실행
    # ==============================

    def open_extension(self):

        # 이미 창이 열려 있다면 기존 창 활성화
        if (
            self.extension_window is not None
            and self.extension_window.winfo_exists()
        ):

            self.extension_window.deiconify()
            self.extension_window.lift()
            self.extension_window.focus_force()

            return

        self.extension_window = tk.Toplevel(
            self.root
        )

        self.extension_window.title(
            "가계부 도구"
        )

        self.extension_window.geometry(
            "1200x640"
        )

        self.extension_window.minsize(
            700,
            450
        )

        self.extension_window.protocol(
            "WM_DELETE_WINDOW",
            self.extension_window.destroy
        )

        self.setup_extension_gui(
            self.extension_window
        )

    # ==============================
    # 가계부 GUI
    # ==============================

    def setup_extension_gui(self, window):

        window.columnconfigure(0, weight=1)
        window.columnconfigure(1, weight=1)
        window.rowconfigure(0, weight=1)

        # 왼쪽 입력 영역
        left_frame = ttk.LabelFrame(
            window,
            text="입력 내용",
            padding=5
        )

        left_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(10, 5),
            pady=10
        )

        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=1)

        self.txt = tk.Text(
            left_frame,
            wrap="word",
            font=("맑은 고딕", 11),
            padx=8,
            pady=8
        )

        self.txt.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        left_scroll = ttk.Scrollbar(
            left_frame,
            orient="vertical",
            command=self.txt.yview
        )

        left_scroll.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        self.txt.config(
            yscrollcommand=left_scroll.set
        )

        # 오른쪽 결과 영역
        right_frame = ttk.LabelFrame(
            window,
            text="분석 결과",
            padding=5
        )

        right_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(5, 10),
            pady=10
        )

        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)

        self.excel = tk.Text(
            right_frame,
            wrap="word",
            font=("맑은 고딕", 11),
            padx=8,
            pady=8
        )

        self.excel.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        right_scroll = ttk.Scrollbar(
            right_frame,
            orient="vertical",
            command=self.excel.yview
        )

        right_scroll.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        self.excel.config(
            yscrollcommand=right_scroll.set
        )

        # 변환 버튼 영역
        button_frame = ttk.Frame(window)

        button_frame.grid(
            row=1,
            column=0,
            columnspan=2,
            pady=(0, 15)
        )

        convert_btn = ttk.Button(
            button_frame,
            text="변환",
            command=self.change
        )

        convert_btn.pack(
            padx=10,
            ipadx=25,
            ipady=5
        )

    # ==============================
    # 문장 변환 기능
    # ==============================

    def change(self):

        a = self.txt.get(
            "1.0",
            "end-1c"
        )

        print(a)

        self.excel.delete(
            "1.0",
            "end"
        )

        self.excel.insert(
            "1.0",
            "문장 분석 기능은 2단계에서 구현됩니다."
        )

    # ==============================
    # 프로그램 종료
    # ==============================

    def close_app(self):

        if not self.confirm_save():
            return

        self.root.destroy()


# ==============================
# 프로그램 시작
# ==============================

if __name__ == "__main__":

    root = tk.Tk()

    app = MemoApp(root)

    root.mainloop()
