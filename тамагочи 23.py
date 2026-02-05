import tkinter as tk
from tkinter import messagebox
import os

class Tamagotchi:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Тамагочи")
        self.window.geometry("300x380")  # Увеличена высота для изображения

        # Параметры
        self.hunger = 10
        self.happiness = 10
        self.energy = 10

        # Имя питомца
        self.name_label = tk.Label(self.window, text="Твой питомец: Пики", font=("Arial", 14, "bold"))
        self.name_label.pack(pady=5)

        # Изображение питомца
        self.pet_image_label = tk.Label(self.window)
        self.pet_image_label.pack(pady=5)
        self.load_pet_image()

        # Статусы
        status_frame = tk.Frame(self.window)
        status_frame.pack(pady=5)

        self.hunger_label = tk.Label(status_frame, text=f"Сытость: {self.hunger}", font=("Arial", 10))
        self.hunger_label.pack(anchor="w", padx=10)

        self.happy_label = tk.Label(status_frame, text=f"Счастье: {self.happiness}", font=("Arial", 10))
        self.happy_label.pack(anchor="w", padx=10)

        self.energy_label = tk.Label(status_frame, text=f"Энергия: {self.energy}", font=("Arial", 10))
        self.energy_label.pack(anchor="w", padx=10)

        # Кнопки
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="🍽 Покормить", command=self.feed, width=15).pack(pady=3)
        tk.Button(button_frame, text="🎮 Поиграть", command=self.play, width=15).pack(pady=3)
        tk.Button(button_frame, text="💤 Отдыхать", command=self.rest, width=15).pack(pady=3)

        # Запуск обновления
        self.update()
        self.window.mainloop()

    def load_pet_image(self):
        """Загружает изображение питомца или показывает смайлик-резерв"""
        try:
            # Пытаемся загрузить изображение из файла
            image_path = "pet.png"
            if os.path.exists(image_path):
                self.pet_image = tk.PhotoImage(file=image_path)
                # Масштабирование если изображение слишком большое
                if self.pet_image.width() > 100 or self.pet_image.height() > 100:
                    self.pet_image = self.pet_image.subsample(
                        max(1, self.pet_image.width() // 100),
                        max(1, self.pet_image.height() // 100)
                    )
                self.pet_image_label.config(image=self.pet_image)
            else:
                # Резервный вариант — смайлик
                self.pet_image_label.config(text="😊", font=("Arial", 48), fg="#FFA500")
                print(f"Файл {image_path} не найден. Используется смайлик-резерв.")
        except Exception as e:
            # Если ошибка при загрузке — показываем смайлик
            self.pet_image_label.config(text="😊", font=("Arial", 48), fg="#FFA500")
            print(f"Ошибка загрузки изображения: {e}. Используется смайлик-резерв.")

    def feed(self):
        if self.hunger < 10:
            self.hunger += 2
            if self.hunger > 10: self.hunger = 10
            self.update_status()
        else:
            messagebox.showinfo("Тамагочи", "Я не голоден!")

    def play(self):
        if self.energy > 0:
            self.happiness += 2
            self.energy -= 1
            self.hunger -= 1
            if self.happiness > 10: self.happiness = 10
            if self.hunger < 0: self.hunger = 0
            self.update_status()
        else:
            messagebox.showinfo("Тамагочи", "Я устал, давай отдохнём!")

    def rest(self):
        self.energy += 3
        if self.energy > 10: self.energy = 10
        self.hunger -= 1
        if self.hunger < 0: self.hunger = 0
        self.update_status()

    def update_status(self):
        self.hunger_label.config(text=f"Сытость: {self.hunger}")
        self.happy_label.config(text=f"Счастье: {self.happiness}")
        self.energy_label.config(text=f"Энергия: {self.energy}")

    def update(self):
        # Уменьшение параметров со временем
        if self.hunger > 0: self.hunger -= 1
        if self.happiness > 0: self.happiness -= 1
        if self.energy > 0: self.energy -= 1

        self.update_status()

        # Проверка смерти
        if self.hunger <= 0 or self.happiness <= 0 or self.energy <= 0:
            messagebox.showwarning("Тамагочи", "Питомец умер! Игра окончена.")
            self.window.destroy()
        else:
            self.window.after(3000, self.update)


# Запуск игры
if __name__ == "__main__":
    Tamagotchi()