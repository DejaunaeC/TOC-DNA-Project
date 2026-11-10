import customtkinter as ctk
import tkinter as tk
from collections import deque
from diagram import draw_dfa

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# --- Member C: NFA → DFA Conversion Demo ---
nfa = {
    "q0": {"A": {"q1"}},
    "q1": {"T": {"q2"}},
    "q2": {"G": {"q3"}},
    "q3": {"A": {"q4"}},
    "q4": {"T": {"q3", "q5"}},   # (AT)+ loop, or finish and move to stop codon
    "q5": {"T": {"q6"}},         # the T of the stop codon
    "q6": {"A": {"q7"}, "G": {"q8"}},
    "q7": {"A": {"accept"}, "G": {"accept"}},   # TAA, TAG
    "q8": {"A": {"accept"}},                    # TGA
}

def subset_construction(nfa, alphabet={"A", "C", "G", "T"}):
    start = frozenset(["q0"])
    dfa_states = {start}
    transitions = {}
    queue = deque([start])
    accepting = set()

    while queue:
        current = queue.popleft()
        transitions[current] = {}
        for symbol in alphabet:
            next_states = set()
            for s in current:
                if symbol in nfa.get(s, {}):
                    next_states |= nfa[s][symbol]
            if next_states:
                next_set = frozenset(next_states)
                transitions[current][symbol] = next_set
                if next_set not in dfa_states:
                    dfa_states.add(next_set)
                    queue.append(next_set)
                if "accept" in next_set:
                    accepting.add(next_set)
    return transitions, accepting

dfa_transitions, dfa_accepting = subset_construction(nfa)
START = frozenset(["q0"])

# --- GUI Integration ---
def redraw(current=None):
    draw_dfa(canvas, dfa_transitions, dfa_accepting, START,
             current, ctk.get_appearance_mode() == "Dark")

def animate(states, i=0):
    if i < len(states):
        redraw(states[i])
        app.after(500, animate, states, i + 1)

def on_check():
    seq = entry.get().strip().upper()
    if not seq:
        result_label.configure(text="Please enter a sequence", text_color="orange")
        return

    trace_box.delete("1.0", "end")
    current = START
    visited = [current]
    path = [f"Start: {set(current)}"]
    for char in seq:
        if char in dfa_transitions.get(current, {}):
            current = dfa_transitions[current][char]
            visited.append(current)
            path.append(f"--{char}--> {set(current)}")
        else:
            path.append(f"--{char}--> dead")
            break
    result_label.configure(
        text="Accepted,DNA Seqence Match" if current in dfa_accepting else "Rejected,No DNA match can be found",
        text_color="#2ecc71" if current in dfa_accepting else "#e74c3c"
    )
    trace_box.insert("end", "\n".join(path))
    animate(visited)

def change_mode(choice):
    ctk.set_appearance_mode(choice.lower())
    redraw()

app = ctk.CTk()
app.title("DNA Sequence Analyzer - Member C")
app.geometry("640x800")

ctk.CTkLabel(app, text="DNA Sequence Analyzer",
             font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(25, 5))
ctk.CTkLabel(app, text="Enter DNA sequence to Check for a match",
             text_color="gray").pack(pady=(0, 15))

entry = ctk.CTkEntry(app, width=440, height=40, corner_radius=10,
                     placeholder_text="Enter sequence, e.g. ATGATATTAA")
entry.pack(pady=10)

ctk.CTkButton(app, text="Check sequence", width=200, height=40,
              corner_radius=10, command=on_check).pack(pady=10)

result_label = ctk.CTkLabel(app, text="", font=ctk.CTkFont(size=16))
result_label.pack(pady=5)

trace_box = ctk.CTkTextbox(app, width=500, height=150, corner_radius=10)
trace_box.pack(pady=15)

canvas = tk.Canvas(app, width=580, height=230, highlightthickness=0)
canvas.pack(pady=10)

row = ctk.CTkFrame(app, fg_color="transparent")
row.pack(pady=5)
ctk.CTkLabel(row, text="Theme:").pack(side="left", padx=(0, 10))
ctk.CTkOptionMenu(row, values=["Dark", "Light", "System"],
                  command=change_mode).pack(side="left")

redraw()
app.mainloop()