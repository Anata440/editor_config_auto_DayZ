import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import re

class ConfigEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Редактор конфигурации")
        self.geometry("800x600")

        # Создание контейнера с холстом и скроллбаром
        self.create_scrollable_area()

        self.fields = {}
        self.original_lines = []  # Сохраняем исходный текст файла
        self.create_fields()

        # Кнопки для загрузки/сохранения
        self.load_button = ttk.Button(self, text="Загрузить файл", command=self.load_file)
        self.load_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.save_button = ttk.Button(self, text="Сохранить изменения", command=self.save_file)
        self.save_button.pack(side=tk.LEFT, padx=10, pady=10)

    def create_scrollable_area(self):
        """Создает область с прокруткой."""
        container = ttk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(container)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def create_fields(self):
        """Создает текстовые поля для параметров."""
        parameters = [
            ("Steering", ["maxSteeringAngle", "increaseSpeed", "decreaseSpeed", "centeringSpeed"]),
            ("Throttle", ["reactionTime", "defaultThrust", "gentleThrust", "turboCoef", "gentleCoef"]),
            ("Brake", ["pressureBySpeed", "reactionTime", "driverless"]),
            ("Aerodynamics", ["frontalArea", "dragCoefficient"]),
            ("Engine", ["torqueCurve", "inertia", "frictionTorque", "rollingFriction", "viscousFriction", "rpmIdle", "rpmMin", "rpmClutch", "rpmRedline"]),
            ("Clutch", ["maxTorqueTransfer", "uncoupleTime", "coupleTime"]),
            ("Gearbox", ["type", "reverse", "ratios"]),
            ("CentralDifferential", ["ratio", "type"]),
        ]

        row = 0
        for group, params in parameters:
            label = ttk.Label(self.scrollable_frame, text=f"{group}:", font=("Arial", 12, "bold"))
            label.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
            row += 1
            for param in params:
                label = ttk.Label(self.scrollable_frame, text=f"{param}:")
                label.grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
                entry = ttk.Entry(self.scrollable_frame)
                entry.grid(row=row, column=1, sticky=tk.EW, padx=5, pady=2)
                self.fields[f"{group}_{param}"] = entry
                row += 1

    def load_file(self):
        """Загрузка файла конфигурации и заполнение полей."""
        file_path = filedialog.askopenfilename(title="Выберите файл config.cpp", filetypes=[("CPP Files", "*.cpp"), ("All Files", "*.*")])
        if not file_path:
            return

        try:
            with open(file_path, "r") as file:
                self.original_lines = file.readlines()

            # Парсинг секций и заполнение текстовых полей
            for line in self.original_lines:
                for field_key in self.fields.keys():
                    group, param = field_key.split("_", 1)
                    pattern = rf"{param}\s*=\s*(.*?);"
                    match = re.search(pattern, line)
                    if match:
                        value = match.group(1).strip()
                        self.fields[field_key].delete(0, tk.END)
                        self.fields[field_key].insert(0, value)

            messagebox.showinfo("Успех", "Файл успешно загружен!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

    def save_file(self):
        """Сохранение изменений в файл."""
        try:
            updated_lines = []
            for line in self.original_lines:
                updated_line = line
                for field_key, field_widget in self.fields.items():
                    group, param = field_key.split("_", 1)
                    pattern = rf"({param}\s*=\s*)(.*?)(;)"
                    match = re.search(pattern, line)
                    if match:
                        # Проверяем, изменилось ли значение
                        new_value = field_widget.get()
                        old_value = match.group(2).strip()
                        if new_value != old_value:
                            updated_line = re.sub(pattern, rf"\1{new_value}\3", line)
                        break
                updated_lines.append(updated_line)

            save_path = filedialog.asksaveasfilename(title="Сохранить файл как", defaultextension=".cpp", filetypes=[("CPP Files", "*.cpp"), ("All Files", "*.*")])
            if save_path:
                with open(save_path, "w") as file:
                    file.writelines(updated_lines)

                messagebox.showinfo("Успех", "Файл успешно сохранен!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")

if __name__ == "__main__":
    app = ConfigEditor()
    app.mainloop()
