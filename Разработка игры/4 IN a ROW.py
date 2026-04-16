import tkinter as tk
from tkinter import messagebox, colorchooser, simpledialog
import random

# Константы
ROWS = 6
COLS = 7
PLAYER1 = 1
PLAYER2 = 2
EMPTY = 0
AI_PIECE = PLAYER2
HUMAN_PIECE = PLAYER1

class ModernButton(tk.Button):
    """Современная кнопка с эффектами"""
    def __init__(self, parent, text, command, **kwargs):
        super().__init__(parent, text=text, command=command,
                        font=("Segoe UI", 12, "bold"),
                        relief=tk.FLAT, borderwidth=0, padx=20, pady=10,
                        cursor="hand2", **kwargs)
        
        self.configure(bg="#530c26", fg="white", activebackground="#690E5B",
                      activeforeground="white")
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def on_enter(self, e):
        self.configure(bg="#690E5B")
    
    def on_leave(self, e):
        self.configure(bg="#530c26")

class FourInRow:
    def __init__(self, root):
        self.root = root
        self.root.title("4 в ряд")
        self.root.configure(bg='#1a0b2e')
        
        # Полноэкранный режим
        self.root.attributes('-fullscreen', True)
        
        # Привязка клавиш
        self.root.bind('<Escape>', self.toggle_fullscreen)
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.bind('<Key>', self.key_press)
        
        self.mode = None
        self.current_player = PLAYER1
        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.input_buffer = ""
        
        # Настройки дизайна по умолчанию
        self.custom_design = {
            'player1_symbol': '●',
            'player1_color': '#FF6B6B',
            'player1_bg': '#ffffff',
            'player1_name': 'Игрок 1',
            'player2_symbol': '●',
            'player2_color': '#4ECDC4',
            'player2_bg': '#ffffff',
            'player2_name': 'Игрок 2'
        }
        
        self.show_design_selection()
    
    def toggle_fullscreen(self, event=None):
        is_fullscreen = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not is_fullscreen)
        return "break"
    
    def key_press(self, event):
        if not hasattr(self, 'game_active') or not self.game_active:
            return
        if event.char.isdigit():
            num = int(event.char)
            if 1 <= num <= COLS:
                self.make_move(num - 1)
    
    def on_mousewheel(self, event):
        if hasattr(self, 'canvas'):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def on_shift_mousewheel(self, event):
        if hasattr(self, 'canvas'):
            self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")
    
    def on_cell_click(self, col):
        if hasattr(self, 'game_active') and self.game_active:
            self.make_move(col)
    
    def show_design_selection(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.game_active = False
        
        main_frame = tk.Frame(self.root, bg='#1a0b2e')
        main_frame.place(x=0, y=0, width=self.root.winfo_screenwidth(), 
                        height=self.root.winfo_screenheight())
        
        center_frame = tk.Frame(main_frame, bg='#1a0b2e')
        center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        title_label = tk.Label(center_frame, text="4 в ряд", 
                              font=("Segoe UI", 64, "bold"),
                              bg='#1a0b2e', fg='#FF6B6B')
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(center_frame, text="Выберите дизайн игры", 
                                 font=("Segoe UI Light", 20), bg='#1a0b2e', fg='#e0e0e0')
        subtitle_label.pack(pady=10)
        
        standard_btn = ModernButton(center_frame, "🎨 Стандартный дизайн", 
                                   self.show_main_menu)
        standard_btn.pack(pady=15)
        
        custom_btn = ModernButton(center_frame, "✨ Создать свой дизайн", 
                                 self.custom_design_menu)
        custom_btn.pack(pady=15)
        
        exit_btn = ModernButton(center_frame, "🚪 Выход", self.root.quit)
        exit_btn.pack(pady=15)
        
        info_label = tk.Label(self.root, text="F11/Esc - полноэкранный режим", 
                             font=("Segoe UI", 10), fg='#888888', bg='#1a0b2e')
        info_label.place(relx=0.01, rely=0.98, anchor='sw')
    
    def custom_design_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        main_frame = tk.Frame(self.root, bg='#1a0b2e')
        main_frame.place(x=0, y=0, width=self.root.winfo_screenwidth(), 
                        height=self.root.winfo_screenheight())
        
        canvas = tk.Canvas(main_frame, bg='#1a0b2e', highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        content_frame = tk.Frame(canvas, bg='#1a0b2e')
        canvas_window = canvas.create_window((0, 0), window=content_frame, anchor="nw")
        
        def configure_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        content_frame.bind("<Configure>", configure_scroll)
        
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind('<Configure>', on_canvas_configure)
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        title_label = tk.Label(content_frame, text="Создайте свой дизайн", 
                              font=("Segoe UI", 36, "bold"), bg='#1a0b2e', fg='#FF6B6B')
        title_label.pack(pady=20)
        
        # Предпросмотр
        preview_frame = tk.Frame(content_frame, bg='#2a0a3a', relief=tk.FLAT, padx=20, pady=20)
        preview_frame.pack(pady=20)
        
        preview_container1 = tk.Frame(preview_frame, bg='#FF6B6B', padx=3, pady=3)
        preview_container1.grid(row=0, column=0, padx=20, pady=10)
        
        preview_container2 = tk.Frame(preview_frame, bg='#4ECDC4', padx=3, pady=3)
        preview_container2.grid(row=0, column=1, padx=20, pady=10)
        
        preview_inner1 = tk.Frame(preview_container1, bg=self.custom_design['player1_bg'], 
                                 padx=20, pady=20)
        preview_inner1.pack()
        
        preview_inner2 = tk.Frame(preview_container2, bg=self.custom_design['player2_bg'],
                                 padx=20, pady=20)
        preview_inner2.pack()
        
        self.preview_piece1 = tk.Label(preview_inner1, 
                                      text=self.custom_design['player1_symbol'],
                                      font=("Segoe UI", 60), 
                                      bg=self.custom_design['player1_bg'],
                                      fg=self.custom_design['player1_color'])
        self.preview_piece1.pack()
        
        name_label1 = tk.Label(preview_inner1, text=self.custom_design['player1_name'],
                              font=("Segoe UI", 12, "bold"), bg=self.custom_design['player1_bg'],
                              fg=self.custom_design['player1_color'])
        name_label1.pack(pady=(10,0))
        
        self.preview_piece2 = tk.Label(preview_inner2, 
                                      text=self.custom_design['player2_symbol'],
                                      font=("Segoe UI", 60),
                                      bg=self.custom_design['player2_bg'],
                                      fg=self.custom_design['player2_color'])
        self.preview_piece2.pack()
        
        name_label2 = tk.Label(preview_inner2, text=self.custom_design['player2_name'],
                              font=("Segoe UI", 12, "bold"), bg=self.custom_design['player2_bg'],
                              fg=self.custom_design['player2_color'])
        name_label2.pack(pady=(10,0))
        
        # Панели настроек
        settings_frame = tk.Frame(content_frame, bg='#1a0b2e')
        settings_frame.pack(pady=20)
        
        player1_frame = tk.LabelFrame(settings_frame, text="Игрок 1", 
                                     font=("Segoe UI", 14, "bold"),
                                     bg='#2a0a3a', fg='#FF6B6B', padx=15, pady=10)
        player1_frame.grid(row=0, column=0, padx=10, pady=10)
        
        btn_style = {"font": ("Segoe UI", 10), "bg": "#530c26", "fg": "white",
                    "activebackground": "#690E5B", "relief": tk.FLAT, "padx": 10, "pady": 5}
        
        tk.Button(player1_frame, text="✏️ Изменить имя", 
                 command=lambda: self.change_player_name(1), **btn_style).pack(pady=5)
        tk.Button(player1_frame, text="🔣 Выбрать символ", 
                 command=lambda: self.choose_symbol(1), **btn_style).pack(pady=5)
        tk.Button(player1_frame, text="🎨 Выбрать цвет", 
                 command=lambda: self.choose_color(1), **btn_style).pack(pady=5)
        tk.Button(player1_frame, text="🖌️ Выбрать фон", 
                 command=lambda: self.choose_bg_color(1), **btn_style).pack(pady=5)
        
        player2_frame = tk.LabelFrame(settings_frame, text="Игрок 2",
                                     font=("Segoe UI", 14, "bold"),
                                     bg='#2a0a3a', fg='#4ECDC4', padx=15, pady=10)
        player2_frame.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Button(player2_frame, text="✏️ Изменить имя", 
                 command=lambda: self.change_player_name(2), **btn_style).pack(pady=5)
        tk.Button(player2_frame, text="🔣 Выбрать символ", 
                 command=lambda: self.choose_symbol(2), **btn_style).pack(pady=5)
        tk.Button(player2_frame, text="🎨 Выбрать цвет", 
                 command=lambda: self.choose_color(2), **btn_style).pack(pady=5)
        tk.Button(player2_frame, text="🖌️ Выбрать фон", 
                 command=lambda: self.choose_bg_color(2), **btn_style).pack(pady=5)
        
        nav_frame = tk.Frame(content_frame, bg='#1a0b2e')
        nav_frame.pack(pady=30)
        
        reset_btn = ModernButton(nav_frame, "🔄 Сбросить", self.reset_design)
        reset_btn.pack(side=tk.LEFT, padx=10)
        
        back_btn = ModernButton(nav_frame, "◀ Назад", self.show_design_selection)
        back_btn.pack(side=tk.LEFT, padx=10)
        
        continue_btn = ModernButton(nav_frame, "Продолжить ▶", self.show_main_menu)
        continue_btn.pack(side=tk.LEFT, padx=10)
    
    def change_player_name(self, player):
        current_name = self.custom_design[f'player{player}_name']
        new_name = simpledialog.askstring("Изменение имени", 
                                          f"Введите новое имя для Игрока {player}\n(текущее: {current_name}):",
                                          parent=self.root,
                                          initialvalue=current_name)
        if new_name and new_name.strip():
            self.custom_design[f'player{player}_name'] = new_name.strip()
            self.custom_design_menu()
    
    def choose_symbol(self, player):
        symbol = simpledialog.askstring("Выбор символа", 
                                        f"Введите символ для {self.custom_design[f'player{player}_name']}\n(например: ●, ★, ♥, ♦, ♠, ♣, ☺, ☻):",
                                        parent=self.root)
        if symbol and len(symbol) == 1:
            self.custom_design[f'player{player}_symbol'] = symbol
            self.custom_design_menu()
    
    def choose_color(self, player):
        color = colorchooser.askcolor(title=f"Выберите цвет для {self.custom_design[f'player{player}_name']}", 
                                      parent=self.root)[1]
        if color:
            self.custom_design[f'player{player}_color'] = color
            self.custom_design_menu()
    
    def choose_bg_color(self, player):
        color = colorchooser.askcolor(title=f"Выберите цвет фона для {self.custom_design[f'player{player}_name']}",
                                      parent=self.root)[1]
        if color:
            self.custom_design[f'player{player}_bg'] = color
            self.custom_design_menu()
    
    def reset_design(self):
        self.custom_design = {
            'player1_symbol': '●',
            'player1_color': '#FF6B6B',
            'player1_bg': '#ffffff',
            'player1_name': 'Игрок 1',
            'player2_symbol': '●',
            'player2_color': '#4ECDC4',
            'player2_bg': '#ffffff',
            'player2_name': 'Игрок 2'
        }
        self.custom_design_menu()
    
    def show_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.game_active = False
        
        main_frame = tk.Frame(self.root, bg='#1a0b2e')
        main_frame.place(x=0, y=0, width=self.root.winfo_screenwidth(), 
                        height=self.root.winfo_screenheight())
        
        center_frame = tk.Frame(main_frame, bg='#1a0b2e')
        center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        title_label = tk.Label(center_frame, text="4 в ряд", 
                              font=("Segoe UI", 64, "bold"),
                              bg='#1a0b2e', fg='#FF6B6B')
        title_label.pack(pady=30)
        
        start_btn = ModernButton(center_frame, "🎮 Начать игру", self.show_mode_selection)
        start_btn.pack(pady=15)
        
        settings_btn = ModernButton(center_frame, "⚙️ Настройки", self.show_settings)
        settings_btn.pack(pady=15)
        
        redesign_btn = ModernButton(center_frame, "🎨 Изменить дизайн", self.custom_design_menu)
        redesign_btn.pack(pady=15)
        
        exit_btn = ModernButton(center_frame, "🚪 Выход", self.root.quit)
        exit_btn.pack(pady=15)
        
        info_label = tk.Label(self.root, text="F11/Esc - полноэкранный режим", 
                             font=("Segoe UI", 10), fg='#888888', bg='#1a0b2e')
        info_label.place(relx=0.01, rely=0.98, anchor='sw')
    
    def show_settings(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        main_frame = tk.Frame(self.root, bg='#1a0b2e')
        main_frame.place(x=0, y=0, width=self.root.winfo_screenwidth(), 
                        height=self.root.winfo_screenheight())
        
        canvas = tk.Canvas(main_frame, bg='#1a0b2e', highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        content_frame = tk.Frame(canvas, bg='#1a0b2e')
        canvas_window = canvas.create_window((0, 0), window=content_frame, anchor="nw")
        
        def configure_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        content_frame.bind("<Configure>", configure_scroll)
        
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind('<Configure>', on_canvas_configure)
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        center_frame = tk.Frame(content_frame, bg='#1a0b2e')
        center_frame.pack(expand=True)
        
        title_label = tk.Label(center_frame, text="Настройки", 
                              font=("Segoe UI", 48, "bold"),
                              bg='#1a0b2e', fg='#FF6B6B')
        title_label.pack(pady=30)
        
        info_text = """
        ═══════════════════════════════════════
               ПРАВИЛА ИГРЫ
        ═══════════════════════════════════════
        • Цель - собрать 4 фишки в ряд
        • По горизонтали, вертикали или диагонали
        
        ═══════════════════════════════════════
              УПРАВЛЕНИЕ
        ═══════════════════════════════════════
        • Мышь: нажмите на кнопку над колонкой
        • Мышь: кликните на любую ячейку в колонке
        • Клавиатура: нажмите цифру 1-7
        • Колесико мыши: вертикальная прокрутка
        • Shift + колесико: горизонтальная прокрутка
        • F11/Esc - полноэкранный режим
        
        ═══════════════════════════════════════
                РЕЖИМЫ ИГРЫ
        ═══════════════════════════════════════
        • Против компьютера - игра с ИИ
        • Игра с другом - два игрока
        """
        
        info_label = tk.Label(center_frame, text=info_text, 
                             font=("Segoe UI", 12), justify=tk.LEFT,
                             bg='#1a0b2e', fg='#e0e0e0')
        info_label.pack(pady=20)
        
        back_btn = ModernButton(center_frame, "◀ Назад", self.show_main_menu)
        back_btn.pack(pady=20)
    
    def show_mode_selection(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        main_frame = tk.Frame(self.root, bg='#1a0b2e')
        main_frame.place(x=0, y=0, width=self.root.winfo_screenwidth(), 
                        height=self.root.winfo_screenheight())
        
        center_frame = tk.Frame(main_frame, bg='#1a0b2e')
        center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        title_label = tk.Label(center_frame, text="Выберите режим", 
                              font=("Segoe UI", 48, "bold"),
                              bg='#1a0b2e', fg='#FF6B6B')
        title_label.pack(pady=30)
        
        ai_btn = ModernButton(center_frame, "🤖 Против компьютера", 
                             lambda: self.start_game('ai'))
        ai_btn.pack(pady=15)
        
        friend_btn = ModernButton(center_frame, "👥 Игра с другом", 
                                 lambda: self.start_game('friend'))
        friend_btn.pack(pady=15)
        
        back_btn = ModernButton(center_frame, "◀ Назад", self.show_main_menu)
        back_btn.pack(pady=20)
    
    def start_game(self, mode):
        self.mode = mode
        self.current_player = PLAYER1
        self.board = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.game_active = True
        self.create_game_board()
    
    def create_game_board(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        main_frame = tk.Frame(self.root, bg='#1a0b2e')
        main_frame.place(x=0, y=0, width=self.root.winfo_screenwidth(), 
                        height=self.root.winfo_screenheight())
        
        self.canvas = tk.Canvas(main_frame, bg='#1a0b2e', highlightthickness=0)
        scrollbar_v = tk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        scrollbar_h = tk.Scrollbar(main_frame, orient="horizontal", command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
        
        content_frame = tk.Frame(self.canvas, bg='#1a0b2e')
        self.canvas_window = self.canvas.create_window((0, 0), window=content_frame, anchor="nw")
        
        def center_content(event):
            canvas_width = self.canvas.winfo_width()
            frame_width = content_frame.winfo_reqwidth()
            if canvas_width > frame_width:
                x_offset = (canvas_width - frame_width) // 2
                self.canvas.coords(self.canvas_window, x_offset, 0)
            else:
                self.canvas.coords(self.canvas_window, 0, 0)
        
        def configure_scroll(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            center_content(event)
        
        self.canvas.bind('<Configure>', lambda e: configure_scroll(e))
        content_frame.bind("<Configure>", configure_scroll)
        
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind_all("<Shift-MouseWheel>", self.on_shift_mousewheel)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar_v.pack(side="right", fill="y")
        scrollbar_h.pack(side="bottom", fill="x")
        
        # Верхняя панель
        info_frame = tk.Frame(content_frame, bg='#1a0b2e')
        info_frame.pack(pady=20)
        
        status_frame = tk.Frame(info_frame, bg='#2a0a3a', relief=tk.FLAT, padx=20, pady=10)
        status_frame.pack()
        
        self.turn_label = tk.Label(status_frame, text="", font=("Segoe UI", 20, "bold"),
                                  bg='#2a0a3a', fg='#FF6B6B')
        self.turn_label.pack()
        
        input_label = tk.Label(status_frame, text="⌨️ Цифры 1-7 | 🖱️ Клик по ячейке", 
                              font=("Segoe UI", 11), bg='#2a0a3a', fg='#e0e0e0')
        input_label.pack(pady=5)
        
        menu_btn = ModernButton(status_frame, "🏠 Главное меню", self.show_main_menu)
        menu_btn.pack(pady=10)
        
        # Игровое поле
        game_container = tk.Frame(content_frame, bg='#2a0a3a', relief=tk.FLAT, padx=20, pady=20)
        game_container.pack(pady=10)
        
        # # Кнопки колонок
        # button_frame = tk.Frame(game_container, bg='#2a0a3a')
        # button_frame.pack(pady=10)
        
        # self.buttons = []
        # for col in range(COLS):
        #     btn = tk.Button(button_frame, text=f"▼ {col+1} ▼", 
        #                   font=("Segoe UI", 12, "bold"),
        #                   bg='#530c26', fg='white', width=6, height=1,
        #                   activebackground='#690E5B', cursor='hand2',
        #                   relief=tk.FLAT, bd=0,
        #                   command=lambda c=col: self.make_move(c))
        #     btn.grid(row=0, column=col, padx=3, pady=5)
        #     self.buttons.append(btn)
        
        # Игровая сетка
        board_frame = tk.Frame(game_container, bg='#3a0a4a', padx=5, pady=5)
        board_frame.pack()
        
        # Размер ячейки в пикселях
        cell_size = 80  
        
        self.labels = []
        self.cell_frames = []  # Для хранения фреймов ячеек
        
        for row in range(ROWS):
            row_labels = []
            row_frames = []
            for col in range(COLS):
                # Создаем фрейм для ячейки с фиксированным размером
                cell_container = tk.Frame(board_frame, width=cell_size, height=cell_size,
                                         bg='#4a0a5a')
                cell_container.grid(row=row, column=col, padx=2, pady=2)
                cell_container.grid_propagate(False)  # Запрещаем изменение размера
                
                # Создаем кнопку внутри фрейма, которая заполнит весь фрейм
                cell_button = tk.Button(cell_container, text="○", 
                                       font=("Segoe UI", cell_size // 2),
                                       relief=tk.FLAT, bd=0,
                                       bg='#ffffff', fg='#95a5a6', cursor='hand2',
                                       activebackground='#f0f0f0',
                                       command=lambda c=col: self.on_cell_click(c))
                cell_button.place(relx=0.5, rely=0.5, anchor='center', 
                                relwidth=0.95, relheight=0.95)
                
                row_labels.append(cell_button)
                row_frames.append(cell_container)
            self.labels.append(row_labels)
            self.cell_frames.append(row_frames)
        
        bottom_spacer = tk.Frame(content_frame, height=50, bg='#1a0b2e')
        bottom_spacer.pack()
        
        self.update_board_display()
        self.update_turn_label()
        
        self.root.after(100, lambda: configure_scroll(None))
        
        if self.mode == 'ai' and self.current_player == AI_PIECE:
            self.root.after(500, self.ai_move)
    
    def update_turn_label(self):
        if self.current_player == PLAYER1:
            self.turn_label.config(text=f"{self.custom_design['player1_symbol']} Ход: {self.custom_design['player1_name']} {self.custom_design['player1_symbol']}")
        else:
            if self.mode == 'ai':
                self.turn_label.config(text=f"{self.custom_design['player2_symbol']} Ход: Компьютер ({self.custom_design['player2_name']}) {self.custom_design['player2_symbol']}")
            else:
                self.turn_label.config(text=f"{self.custom_design['player2_symbol']} Ход: {self.custom_design['player2_name']} {self.custom_design['player2_symbol']}")
    
    def update_board_display(self):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece == EMPTY:
                    self.labels[row][col].config(text="○", fg="#95a5a6", bg="#ffffff")
                elif piece == PLAYER1:
                    self.labels[row][col].config(text=self.custom_design['player1_symbol'],
                                                fg=self.custom_design['player1_color'],
                                                bg=self.custom_design['player1_bg'])
                else:
                    self.labels[row][col].config(text=self.custom_design['player2_symbol'],
                                                fg=self.custom_design['player2_color'],
                                                bg=self.custom_design['player2_bg'])
    
    def make_move(self, col):
        if self.board[0][col] != EMPTY:
            messagebox.showwarning("Невозможный ход", f"Колонка {col+1} заполнена!")
            return False
        
        for row in range(ROWS-1, -1, -1):
            if self.board[row][col] == EMPTY:
                self.board[row][col] = self.current_player
                self.update_board_display()
                
                if self.check_win(row, col):
                    winner = self.custom_design['player1_name'] if self.current_player == PLAYER1 else (self.custom_design['player2_name'] if self.mode == 'friend' else "Компьютер")
                    if self.mode == 'ai' and self.current_player == PLAYER2:
                        winner = "Компьютер"
                    messagebox.showinfo("Победа!", f"🏆 {winner} победил! 🏆")
                    self.show_main_menu()
                    return True
                
                if self.is_full():
                    messagebox.showinfo("Ничья", "🤝 Ничья! 🤝")
                    self.show_main_menu()
                    return True
                
                self.current_player = PLAYER2 if self.current_player == PLAYER1 else PLAYER1
                self.update_turn_label()
                
                if self.mode == 'ai' and self.current_player == AI_PIECE:
                    self.root.after(500, self.ai_move)
                return True
        return False
    
    def ai_move(self):
        if self.current_player != AI_PIECE or not self.game_active:
            return
        
        available_cols = []
        for col in range(COLS):
            if self.board[0][col] == EMPTY:
                available_cols.append(col)
        
        if available_cols:
            for col in available_cols:
                for row in range(ROWS-1, -1, -1):
                    if self.board[row][col] == EMPTY:
                        self.board[row][col] = AI_PIECE
                        if self.check_win(row, col):
                            self.board[row][col] = EMPTY
                            self.make_move(col)
                            return
                        self.board[row][col] = EMPTY
                        break
            
            for col in available_cols:
                for row in range(ROWS-1, -1, -1):
                    if self.board[row][col] == EMPTY:
                        self.board[row][col] = HUMAN_PIECE
                        if self.check_win(row, col):
                            self.board[row][col] = EMPTY
                            self.make_move(col)
                            return
                        self.board[row][col] = EMPTY
                        break
            
            col = random.choice(available_cols)
            self.make_move(col)
    
    def check_win(self, row, col):
        piece = self.board[row][col]
        if piece == EMPTY:
            return False
        
        # Горизонталь
        count = 1
        c = col - 1
        while c >= 0 and self.board[row][c] == piece:
            count += 1
            c -= 1
        c = col + 1
        while c < COLS and self.board[row][c] == piece:
            count += 1
            c += 1
        if count >= 4:
            return True
        
        # Вертикаль
        count = 1
        r = row - 1
        while r >= 0 and self.board[r][col] == piece:
            count += 1
            r -= 1
        r = row + 1
        while r < ROWS and self.board[r][col] == piece:
            count += 1
            r += 1
        if count >= 4:
            return True
        
        # Диагональ \
        count = 1
        r, c = row - 1, col - 1
        while r >= 0 and c >= 0 and self.board[r][c] == piece:
            count += 1
            r -= 1
            c -= 1
        r, c = row + 1, col + 1
        while r < ROWS and c < COLS and self.board[r][c] == piece:
            count += 1
            r += 1
            c += 1
        if count >= 4:
            return True
        
        # Диагональ /
        count = 1
        r, c = row - 1, col + 1
        while r >= 0 and c < COLS and self.board[r][c] == piece:
            count += 1
            r -= 1
            c += 1
        r, c = row + 1, col - 1
        while r < ROWS and c >= 0 and self.board[r][c] == piece:
            count += 1
            r += 1
            c -= 1
        if count >= 4:
            return True
        
        return False
    
    def is_full(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] == EMPTY:
                    return False
        return True

if __name__ == "__main__":
    root = tk.Tk()
    game = FourInRow(root)
    root.mainloop()