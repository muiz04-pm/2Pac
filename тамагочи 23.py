import tkinter as tk
from tkinter import messagebox
import os
import time


class Tamagotchi:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Тамагочи")
        self.window.geometry("300x420")  # Увеличена высота для новых элементов


        self.hunger = 10
        self.happiness = 10
        self.energy = 10
        self.last_action_time = time.time()
        self.current_display_state = "normal"  # normal, eating, playing, sleeping, sad


        self.name_label = tk.Label(self.window, text="Твой питомец: Пики", font=("Arial", 14, "bold"))
        self.name_label.pack(pady=5)


        self.pet_image_label = tk.Label(self.window)
        self.pet_image_label.pack(pady=5)


        self.pet_images = {}
        self.load_all_pet_images()
        self.update_pet_image()


        status_frame = tk.Frame(self.window)
        status_frame.pack(pady=5)

        self.hunger_label = tk.Label(status_frame, text=f"Сытость: {self.hunger}", font=("Arial", 10))
        self.hunger_label.pack(anchor="w", padx=10)

        self.happy_label = tk.Label(status_frame, text=f"Счастье: {self.happiness}", font=("Arial", 10))
        self.happy_label.pack(anchor="w", padx=10)

        self.energy_label = tk.Label(status_frame, text=f"Энергия: {self.energy}", font=("Arial", 10))
        self.energy_label.pack(anchor="w", padx=10)


        self.state_hint = tk.Label(self.window, text="Пики чувствует себя отлично!",
                                   font=("Arial", 9, "italic"), fg="#4CAF50")
        self.state_hint.pack(pady=3)


        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="🍽 Покормить", command=self.feed, width=15, bg="#FFD700").pack(pady=3)
        tk.Button(button_frame, text="🎮 Поиграть", command=self.play, width=15, bg="#4CAF50").pack(pady=3)
        tk.Button(button_frame, text="💤 Отдыхать", command=self.rest, width=15, bg="#2196F3").pack(pady=3)


        self.update()
        self.window.mainloop()

    def load_all_pet_images(self):
        """Загружает изображения для всех состояний питомца с резервными смайликами"""
        states = {
            "normal": ("pet_normal.png", "🐶", 48, "#FFA500"),
            "eating": ("pet_eating.png", "🍖", 40, "#FF6B6B"),
            "playing": ("pet_playing.png", "🎾", 40, "#4CAF50"),
            "sleeping": ("pet_sleeping.png", "😴", 48, "#90CAF9"),
            "sad": ("pet_sad.png", "🥺", 48, "#9E9E9E")
        }

        for state, (filename, emoji, size, color) in states.items():
            try:
                if os.path.exists(filename):
                    img = tk.PhotoImage(file=filename)
                    # Масштабирование под размер окна
                    max_size = 100
                    if img.width() > max_size or img.height() > max_size:
                        scale_x = max(1, img.width() // max_size)
                        scale_y = max(1, img.height() // max_size)
                        img = img.subsample(scale_x, scale_y)
                    self.pet_images[state] = ("image", img)
                else:
                    self.pet_images[state] = ("emoji", emoji, size, color)
                    print(f"Файл {filename} не найден. Используется резерв: {emoji}")
            except Exception as e:
                self.pet_images[state] = ("emoji", emoji, size, color)
                print(f"Ошибка загрузки {filename}: {e}. Используется резерв: {emoji}")

    def update_pet_image(self):
        """Обновляет изображение питомца в зависимости от текущего состояния"""
        if self.current_display_state not in self.pet_images:
            self.current_display_state = "normal"

        content = self.pet_images[self.current_display_state]

        if content[0] == "image":
            self.pet_image_label.config(image=content[1], text="")
            # Сохраняем ссылку на изображение, чтобы оно не удалилось сборщиком мусора
            self.pet_image_label.image = content[1]
        else:  # emoji fallback
            _, emoji, size, color = content
            self.pet_image_label.config(image="", text=emoji, font=("Arial", size), fg=color)

    def determine_auto_state(self):
        """Определяет состояние питомца на основе параметров"""
        if self.energy <= 2:
            return "sleeping"
        elif self.hunger <= 3 or self.happiness <= 3:
            return "sad"
        else:
            return "normal"

    def set_temporary_state(self, state, duration=1500):
        """Устанавливает временное состояние (например, во время еды) с автоматическим возвратом"""
        self.current_display_state = state
        self.update_pet_image()
        # Возвращаемся к автоматическому определению состояния через duration миллисекунд
        self.window.after(duration, self.restore_auto_state)

    def restore_auto_state(self):
        """Восстанавливает состояние на основе текущих параметров"""
        self.current_display_state = self.determine_auto_state()
        self.update_pet_image()
        self.update_state_hint()

    def update_state_hint(self):
        """Обновляет текстовую подсказку о состоянии питомца"""
        if self.energy <= 2:
            text, color = "Пики очень устал и хочет спать 😴", "#90CAF9"
        elif self.hunger <= 3:
            text, color = "Пики голоден... дай ему еды! 🦴", "#FF6B6B"
        elif self.happiness <= 3:
            text, color = "Пики грустит... поиграй с ним! 🎾", "#FFA726"
        elif self.hunger == 10 and self.happiness == 10 and self.energy == 10:
            text, color = "Пики в полном восторге! 😍", "#4CAF50"
        else:
            text, color = "Пики чувствует себя отлично!", "#4CAF50"

        self.state_hint.config(text=text, fg=color)

    def feed(self):
        if self.hunger < 10:
            self.hunger = min(10, self.hunger + 2)
            self.set_temporary_state("eating", 1800)  # Показываем состояние "еда" 1.8 сек
            self.update_status()
            self.last_action_time = time.time()
        else:
            messagebox.showinfo("Тамагочи", "Пики сыт и доволен! 😊")

    def play(self):
        if self.energy > 0:
            self.happiness = min(10, self.happiness + 2)
            self.energy = max(0, self.energy - 1)
            self.hunger = max(0, self.hunger - 1)
            self.set_temporary_state("playing", 1800)  # Показываем состояние "игра" 1.8 сек
            self.update_status()
            self.last_action_time = time.time()
        else:
            messagebox.showinfo("Тамагочи", "Пики слишком устал для игр 😴\nСначала дай ему отдохнуть!")

    def rest(self):
        self.energy = min(10, self.energy + 3)
        self.hunger = max(0, self.hunger - 1)
        self.set_temporary_state("sleeping", 2000)  # Показываем состояние "сон" 2 сек
        self.update_status()
        self.last_action_time = time.time()

    def update_status(self):
        self.hunger_label.config(text=f"Сытость: {self.hunger}")
        self.happy_label.config(text=f"Счастье: {self.happiness}")
        self.energy_label.config(text=f"Энергия: {self.energy}")
        self.update_state_hint()

    def update(self):
        current_time = time.time()

        if current_time - self.last_action_time >= 3.0:
            self.hunger = max(0, self.hunger - 1)
            self.happiness = max(0, self.happiness - 1)
            self.energy = max(0, self.energy - 1)
            self.last_action_time = current_time
            self.update_status()


        if self.current_display_state not in ["eating", "playing", "sleeping"]:
            self.current_display_state = self.determine_auto_state()
            self.update_pet_image()
            self.update_state_hint()


        if self.hunger <= 0 or self.happiness <= 0 or self.energy <= 0:
            self.current_display_state = "sad"
            self.update_pet_image()
            self.window.after(500, lambda: messagebox.showwarning(
                "Тамагочи",
                "Пики ушел в мир иной... 😢\nТы не заботился о нем должным образом.\nИгра окончена."
            ))
            self.window.after(2000, self.window.destroy)
        else:
            self.window.after(300, self.update)



print("=" * 50)
print("Для улучшения внешнего вида добавьте в папку с игрой изображения:")
print("  🐶 pet_normal.png    - обычное состояние")
print("  🦴 pet_eating.png    - во время еды")
print("  🎾 pet_playing.png   - во время игры")
print("  😴 pet_sleeping.png  - во время сна")
print("  🥺 pet_sad.png       - грустное состояние")
print("\nРекомендуемый размер: 100x100 пикселей")
print("Если изображения не найдены, будут использованы смайлики-резервы.")
print("=" * 50)


if __name__ == "__main__":
    Tamagotchi()