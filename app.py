from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "attendance.csv")

# Create CSV if not exists or empty
if not os.path.exists(CSV_FILE) or os.stat(CSV_FILE).st_size == 0:
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Name", "Status", "In Time", "Out Time", "Learnings"])


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                request.form["date"],
                request.form["name"],
                request.form["status"],
                request.form.get("inTime", "-"),
                request.form.get("outTime", "-"),
                request.form.get("learnings", "-")
            ])
        return redirect("/")

    records = []
    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None)  # skip header
        records = list(reader)

    return render_template("index.html", records=records)


@app.route("/delete/<int:row_id>", methods=["POST"])
def delete(row_id):
    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
        reader = list(csv.reader(file))

    header = reader[0]
    data = reader[1:]

    if 0 <= row_id < len(data):
        data.pop(row_id)

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
