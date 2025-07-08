import tkinter as tk
from tkinter import messagebox
import random

def play(choice):
    if not game_active[0]:
        return

    user_choice.set(f"You chose: {choice}")
    comp = random.choice(options)
    comp_choice.set(f"Computer chose: {comp}")

    if choice == comp:
        result.set("It's a Tie! 🤝")
    elif (choice == "Rock" and comp == "Scissors") or \
         (choice == "Paper" and comp == "Rock") or \
         (choice == "Scissors" and comp == "Paper"):
        result.set("You Win! 🎉")
        scores["user"] += 1
    else:
        result.set("Computer Wins! 😢")
        scores["comp"] += 1

    update_score()

    rounds[0] += 1
    round_label.config(text=f"Round {rounds[0]} of {max_rounds}")
    if rounds[0] > max_rounds:
        end_game()

def update_score():
    score_label.config(text=f"Score → You: {scores['user']} | Computer: {scores['comp']}")

def end_game():
    game_active[0] = False
    if scores["user"] > scores["comp"]:
        messagebox.showinfo("Game Over", "🏆 You are the Winner!")
    elif scores["user"] < scores["comp"]:
        messagebox.showinfo("Game Over", "💔 Computer Wins!")
    else:
        messagebox.showinfo("Game Over", "🤝 It's a Draw!")

def restart():
    scores["user"] = 0
    scores["comp"] = 0
    rounds[0] = 1
    game_active[0] = True
    user_choice.set("You chose: ")
    comp_choice.set("Computer chose: ")
    result.set("")
    update_score()
    round_label.config(text=f"Round {rounds[0]} of {max_rounds}")

# --- GUI setup ---
root = tk.Tk()
root.title("Rock Paper Scissors Premium")
root.geometry("500x500")
root.config(bg="#1E1E2F")  # Dark premium background
root.resizable(False, False)

# Variables
options = ["Rock", "Paper", "Scissors"]
scores = {"user": 0, "comp": 0}
rounds = [1]
max_rounds = 5
game_active = [True]
user_choice = tk.StringVar(value="You chose: ")
comp_choice = tk.StringVar(value="Computer chose: ")
result = tk.StringVar()

# Labels
tk.Label(root, text="Rock ✊ Paper ✋ Scissors ✌️", font=("Arial", 20, "bold"),
         fg="white", bg="#1E1E2F").pack(pady=20)

round_label = tk.Label(root, text=f"Round {rounds[0]} of {max_rounds}",
                       font=("Arial", 14), fg="#F9F871", bg="#1E1E2F")
round_label.pack()

score_label = tk.Label(root, text="Score → You: 0 | Computer: 0",
                       font=("Arial", 14, "bold"), fg="#00C9A7", bg="#1E1E2F")
score_label.pack(pady=10)

tk.Label(root, textvariable=user_choice, font=("Arial", 12), fg="#F9F871", bg="#1E1E2F").pack()
tk.Label(root, textvariable=comp_choice, font=("Arial", 12), fg="#F9F871", bg="#1E1E2F").pack()
tk.Label(root, textvariable=result, font=("Arial", 16, "bold"), fg="#3E64FF", bg="#1E1E2F").pack(pady=10)

# Buttons
btn_frame = tk.Frame(root, bg="#1E1E2F")
btn_frame.pack(pady=20)

colors = {"Rock": "#3E64FF", "Paper": "#00C9A7", "Scissors": "#F9F871"}

for i, opt in enumerate(options):
    tk.Button(btn_frame, text=opt, width=10, font=("Arial", 12, "bold"),
              bg=colors[opt], fg="black",
              command=lambda choice=opt: play(choice)).grid(row=0, column=i, padx=10)

tk.Button(root, text="🔄 Restart", font=("Arial", 12, "bold"), width=12,
          bg="#FF6B6B", fg="white", command=restart).pack(pady=15)

# Run app
root.mainloop()