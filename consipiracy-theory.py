from tkinter import *
from tkinter import messagebox
import random
import praw
reddit = praw.Reddit(client_id='fefs8RsWfUhpjmb1jOz8ng', client_secret='_rrgQ5wHyAlhmoVC13Uzv7Nm-u485Q', user_agent='Jai')



topics_dict = {
    "Space": [],
    "MH370": [],
    "Aliens": [],
    "Mummies": [],
    "Secret Societies": [],
    "Illuminati":[]
}

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOUR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

class ConspiracyApp:
    def __init__(self):
        self.window = Tk()
        self._setup_main_window()
        self.open_notes = {}  # Dictionary to track open notes

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("Beyond the Surface: A Web Scraping Odyssey")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=600, height=750, bg=BG_COLOR)

       
        self.head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOUR,
                                text="Conspiracy Theory Topics", font=FONT_BOLD, pady=10)
        self.head_label.place(relwidth=1)

        
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        
        self._show_topics()

    def _show_topics(self):

        
        # Destroy the back button if it exists
        for widget in self.window.winfo_children():
            if isinstance(widget, Button) and widget.cget("text") == "Back":
             widget.destroy()

    # Update the header label
        self.head_label.config(text="Conspiracy Theory Topics")

    # Create and display shuffled topic buttons
        shuffled_topics = random.sample(list(topics_dict.keys()), len(topics_dict))
        for i, topic in enumerate(shuffled_topics):
            topic_button = Button(self.window, text=topic, font=FONT_BOLD, width=50, bg=BG_GRAY, command=lambda t=topic: self._show_theories(t))
            topic_button.place(relx=0.5, rely=0.2 + i * 0.1, anchor="center")

    def _show_full_content(self, topic, theory):

        # Create a unique key using topic and theory
        key = f"{topic}_{theory}"

        # Check if the note is already open
        if key in self.open_notes:
         # Alert that the note is already open
         messagebox.showinfo("Note Alert", f"The note is already open!")
         return  # Exit the function if note is already open

        # If the note is not open, then add it to the open_notes dictionary
        self.open_notes[key] = True  # You can use any value or True here

        print(topic)

        full_content_window = Toplevel(self.window)
        full_content_window.title(f"{theory} - Full Content")
        full_content_window.geometry("600x400")

        print(topic[theory])
        full_content = topic[theory]

        # Create a Text widget with vertical scrollbar
        text_widget = Text(full_content_window, wrap=WORD)
        text_widget.insert(END, full_content)
        text_widget.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(full_content_window, command=text_widget.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Configure the Text widget to use the scrollbar
        text_widget.config(yscrollcommand=scrollbar.set)


    def _show_theories(self, topic):
        # Update the header label
        self.head_label.config(text=f"Theories related to {topic}")

        # Create and place the back button
        back_button = Button(self.window, text="Back", font=FONT_BOLD, width=5, bg=BG_GRAY,
                             command=self._show_topics)
        back_button.place(relx=0.05, rely=0.05, anchor="center")

        # Hide the theory buttons
        for widget in self.window.winfo_children():
            if isinstance(widget, Button) and widget != back_button:
                widget.place_forget()

        # Fetch theories related to the selected topic from Reddit
        hot_posts = reddit.subreddit(topic.replace(" ", "")).hot(limit=100)
        contents = {}
        flag = 0
        for post in hot_posts:
            if len(post.selftext) != 0:
                flag += 1
                contents[post.title] = post.selftext
                topics_dict[topic].append(post.title)
            if flag == 5:
                break

        theories = topics_dict[topic]
        
        for i, theory in enumerate(theories):
            font_size = max(12, int(180 / len(theory)))
            theory_button = Button(self.window, text=theory, font=f"Helvetica {font_size} bold", width=50, bg=BG_GRAY,
                                   command=lambda t=theory: self._show_full_content(contents, t))
            theory_button.place(relx=0.5, rely=0.2 + i * 0.1, anchor="center")

if __name__ == "__main__":
    app = ConspiracyApp()
    app.run()
