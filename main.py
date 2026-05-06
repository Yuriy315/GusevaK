import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
import json
import random as rnd


class RandomTaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных задач")
        self.root.geometry("500x500")

        self.tasks = []
        self.history = []

        self.load_tasks()
        self.load_history()

        self.create_widgets()

    def load_tasks(self):
        """Загрузка задач из tasks.json"""
        try:
            with open('tasks.json', 'r', encoding='utf-8') as f:
                self.tasks = json.load(f)
            # Формируем список уникальных типов для фильтра (включая 'Все')
            self.types = list(set(task['type'] for task in self.tasks))
            self.types.insert(0, 'Все')
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл tasks.json не найден!")
            self.root.destroy()

    def load_history(self):
        """Загрузка истории из history.json"""
        try:
            with open('history.json', 'r', encoding='utf-8') as f:
                self.history = json.load(f)
        except FileNotFoundError:
            self.history = []

    def save_history(self):
        """Сохранение истории в history.json"""
        with open('history.json', 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def create_widgets(self):
        # Фрейм для фильтра и кнопки
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10, padx=10, fill=tk.X)

        # Фильтр по типу задачи (Combobox)
        tk.Label(top_frame, text="Фильтр по типу:").pack(side=tk.LEFT)

        self.filter_var = tk.StringVar(value=self.types[0])
        self.filter_combo = ttk.Combobox(top_frame, textvariable=self.filter_var,
                                         values=self.types, state="readonly", width=15)
        self.filter_combo.pack(side=tk.LEFT, padx=(5, 20))

        # Кнопка генерации задачи
        self.generate_btn = tk.Button(top_frame, text="Сгенерировать задачу",
                                      command=self.generate_task, bg="#4CAF50", fg="white")
        self.generate_btn.pack(side=tk.LEFT)

        # Поле для отображения текущей задачи
        self.task_label = tk.Label(self.root, text="Ваша задача появится здесь",
                                   font=("Arial", 14), wraplength=450, justify="center")
        self.task_label.pack(pady=20)

        # Фрейм для истории и скроллбара
        history_frame = tk.Frame(self.root)
        history_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        tk.Label(history_frame, text="История сгенерированных задач:", font=("Arial", 12, "bold")).pack(anchor="w")

        self.history_text = scrolledtext.ScrolledText(history_frame, wrap=tk.WORD,
                                                      width=55, height=12, state='disabled')
        self.history_text.pack(fill=tk.BOTH, expand=True)

        # Отобразить историю при запуске
        self.update_history_display()

    def generate_task(self):
        """Логика генерации случайной задачи"""
        selected_type = self.filter_var.get()

        if selected_type == 'Все':
            filtered_tasks = self.tasks.copy()
            filter_text = "(все типы)"
        else:
            filtered_tasks = [task for task in self.tasks if task['type'] == selected_type]
            filter_text = f"(тип: {selected_type})"

        if not filtered_tasks:
            messagebox.showwarning("Нет задач", f"В выбранной категории {filter_text} нет задач.")
            return

        task = rnd.choice(filtered_tasks)

        # Обновляем лейбл с задачей
        self.task_label.config(text=f"Задача: {task['name']}\nТип: {task['type']}")

        # Добавляем в историю и сохраняем
        self.history.append(task)
        self.save_history()

        # Обновляем виджет истории на экране (добавляем только новую строку)
        self.history_text.config(state='normal')
        self.history_text.insert(tk.END, f"- {task['name']} ({task['type']})\n")
        self.history_text.config(state='disabled')

    def update_history_display(self):
        """Полное обновление виджета истории (при запуске)"""
        self.history_text.config(state='normal')
        self.history_text.delete(1.0, tk.END)

        if not self.history:
            self.history_text.insert(tk.END, "История пока пуста.")
            return

        for task in self.history:
            self.history_text.insert(tk.END, f"- {task['name']} ({task['type']})\n")

        self.history_text.config(state='disabled')


if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTaskGenerator(root)
    root.mainloop()