import tkinter as tk
from tkinter import messagebox
import random

class HangmanGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Hangman - GUESS CITIES NAME")
        self.master.geometry("1600x750")
        self.master.configure(bg="white")  # Set background color to white

        self.create_front_page()

    def create_front_page(self):
        # Create a frame to hold the front page contents
        front_page_frame = tk.Frame(self.master, bg="white")
        front_page_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame in the window

        # Header label
        header_label = tk.Label(front_page_frame, text="Hangman", font=("Courier New", 45, "bold"), fg="black", bg="white")
        header_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Start button
        start_button = tk.Button(front_page_frame, text="Start", command=self.start_game, font=("Courier New", 20, "bold"), bg="lightblue", fg="black", relief="raised")
        start_button.grid(row=1, column=0, padx=10, pady=10)

        # Rules button
        rules_button = tk.Button(front_page_frame, text="Rules", command=self.display_rules, font=("Courier New", 20, "bold"), bg="lightgreen", fg="black", relief="raised")
        rules_button.grid(row=1, column=1, padx=10, pady=10)

    def start_game(self):
        # Clear front page widgets
        for widget in self.master.winfo_children():
            widget.destroy()

        # Proceed to game setup
        self.word_list = ['MUMBAI', 'DELHI', 'BANGALORE', 'HYDERABAD', 'AHMEDABAD', 'CHENNAI', 'KOLKATA', 'SURAT', 'PUNE', 'JAIPUR', 'AMRITSAR', 'ALLAHABAD', 'RANCHI', 'LUCKNOW', 'KANPUR', 'NAGPUR', 'INDORE', 'THANE', 'BHOPAL', 'PATNA', 'GHAZIABAD', 'AGRA', 'FARIDABAD', 'MEERUT', 'RAJKOT', 'VARANASI', 'SRINAGAR', 'RAIPUR', 'KOTA', 'JHANSI', 'BENGALURU', 'CHENNAI', 'HYDERABAD', 'MYSURU', 'KOCHI', 'COIMBATORE', 'VISAKHAPATNAM', 'VIJAYAWADA', 'MANGALORE', 'HUBLI', 'BELGAUM', 'GULBARGA', 'SHIVAMOGGA', 'TUMKUR', 'MANDYA']
        self.photos = [tk.PhotoImage(file=f"Hangman-main/hang{i}.png").zoom(1) for i in range(12)]

        self.create_widgets()
        self.new_game()
        self.counter = 0

    def create_widgets(self):
        # Header label
        header_label = tk.Label(self.master, text="Hangman", font=("Poppins", 45, "bold"), fg="black", bg="white")
        header_label.grid(row=0, column=0, columnspan=6, padx=10, pady=10)
        header_label = tk.Label(self.master, text="Guess The City", font=("Poppins", 30, "bold"), fg="black", bg="white")
        header_label.grid(row=0, column=3, columnspan=6, padx=10, pady=10)

        self.img_label = tk.Label(self.master)
        self.img_label.grid(row=1, column=0, rowspan=9, padx=10, pady=10)

        # Enlarged widget for displaying guessed dashes
        self.lbl_word = tk.StringVar()
        tk.Label(self.master, textvariable=self.lbl_word, font=('Chalkboard', 60, 'bold'), fg="black", bg="white").grid(row=1, column=3, columnspan=6, padx=10, pady=10)

        self.buttons_frame = tk.Frame(self.master, bg='grey')
        self.buttons_frame.grid(row=3, column=6, columnspan=3, pady=10)

        self.buttons = []
        for idx, letter in enumerate("QWERTYUIOPASDFGHJKLZXCVBNM0123456789"):
            btn = tk.Button(self.buttons_frame, text=letter, font=('Georgia', 14), width=7, height=3, command=lambda l=letter: self.guess(l), fg="black", bg="blue", activeforeground="white", activebackground="lightblue", bd=2)
            btn.grid(row=idx // 9, column=(idx % 9), padx=2, pady=2)

            if btn.cget("bg") == 'SystemButtonFace':
                btn.bind("<Enter>", lambda event, b=btn: b.config(bg="lightblue"))
                btn.bind("<Leave>", lambda event, b=btn: b.config(bg="SystemButtonFace"))

            btn.bind("<Button-1>", lambda event, b=btn: self.handle_button_click(b))
            self.buttons.append(btn)

        tk.Button(self.master, text="New Game", command=self.new_game, font=("Courier New", 20, "bold"), bg="yellow", fg="black", relief="raised").grid(row=0, column=8, sticky="ne", padx=10, pady=10)

        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

    def handle_button_click(self, btn):
        if self.counter == 0:
            if btn['text'] in self.the_word_withSpaces:
                btn.config(bg="green")
            else:
                btn.config(bg="red")
            for b in self.buttons:
                b.unbind("<Enter>")
            for b in self.buttons:
                b.unbind("<Leave>")

    def new_game(self):
        self.numberOfGuesses = 0
        self.counter=0
        for btn in self.buttons:
            btn.config(bg="SystemButtonFace")
            btn.bind("<Enter>", lambda event, b=btn: b.config(bg="light blue"))
            btn.bind("<Leave>", lambda event, b=btn: b.config(bg="SystemButtonFace"))

        # Reset hangman image
        self.img_label.config(image=self.photos[self.numberOfGuesses])

        the_word = random.choice(self.word_list)

        # Choose random positions for letters to display
        if len(the_word) <= 5:
            display_indices = random.sample(range(len(the_word)), 2)
        else:
            display_indices = random.sample(range(len(the_word)), 3)

        # Create the display word with underscores for other positions
        display_word = ['_' if i not in display_indices else the_word[i] for i in range(len(the_word))]
        self.lbl_word.set(' '.join(display_word))

        # Store the complete word with spaces for comparison
        self.the_word_withSpaces = " ".join(the_word)
        
        # Enable buttons for new game
        self.enable_buttons()


    def guess(self, letter):
        if self.numberOfGuesses < 11:
            txt = list(self.the_word_withSpaces)
            guessed = list(self.lbl_word.get())
            if self.the_word_withSpaces.count(letter) > 0:
                for c in range(len(txt)):
                    if txt[c] == letter:
                        guessed[c] = letter
                self.lbl_word.set("".join(guessed))
                if self.lbl_word.get() == self.the_word_withSpaces:
                    messagebox.showinfo("Hangman", "You guessed it!")
                    self.disable_buttons()
            else:
                self.numberOfGuesses += 1
                self.img_label.config(image=self.photos[self.numberOfGuesses])
                if self.numberOfGuesses == 11:
                    messagebox.showwarning("Hangman", f"Game Over! The correct word was: {self.the_word_withSpaces}")
                    self.disable_buttons()

    def enable_buttons(self):
        for btn in self.buttons:
            btn.config(state='normal')

    def disable_buttons(self):
        for btn in self.buttons:
            btn.config(state='disabled')

    def on_enter(self, btn):
        btn.config(bg="lightblue")

    def on_leave(self, btn):
        btn.config(bg="SystemButtonFace")

    def display_rules(self):
        messagebox.showinfo("Rules", "1. Guess the word by clicking the letters.\n2. You have 11 chances to guess the word correctly.\n3. If you fail to guess the word within 11 chances, you lose the game.")

def main():
    root = tk.Tk()
    app = HangmanGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()