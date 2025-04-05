from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "pomodoro_secret"
app.permanent_session_lifetime = timedelta(minutes=60)

class Pomodoro:
    def __init__(self):
        self.sessions_completed = 0
        self.current_mode = "Work"
        self.time_left = 0
        self.session_running = False

    def start_session(self, mode):
        self.session_running = True
        if mode == "Work":
            self.current_mode = "Work"
            self.time_left = 1 * 60
        elif mode == "Break":
            self.current_mode = "Break"
            self.time_left = 5 * 60
        elif mode == "Long Break":
            self.current_mode = "Long Break"
            self.time_left = 15 * 60

    def complete_session(self):
        if self.current_mode == "Work":
            self.sessions_completed += 1
        self.start_session("Break" if self.current_mode == "Work" else "Work")

    def end_session(self):
        self.session_running = False
        self.time_left = 0

pomodoro = Pomodoro()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "start_work":
            pomodoro.start_session("Work")
        elif action == "start_break":
            pomodoro.start_session("Break")
        elif action == "start_long_break":
            pomodoro.start_session("Long Break")
        elif action == "complete":
            pomodoro.complete_session()
        elif action == "end_session":
            pomodoro.end_session()
            flash("Session ended before completion.")

        return redirect(url_for("index"))

    return render_template("index.html",
                           mode=pomodoro.current_mode,
                           time=pomodoro.time_left,
                           sessions=pomodoro.sessions_completed,
                           session_running=pomodoro.session_running)

if __name__ == "__main__":
    app.run(debug=True)
