from datetime import datetime
from flask import Flask, render_template, request, redirect
from waitress import serve
import os
import json

app = Flask(__name__)
DATEI = "notizen.json"

if os.path.isfile(DATEI):
    with open(DATEI, "r", encoding="utf-8") as f:
        notizen = json.load(f)

else:
    notizen = []

notizen = []
if os.path.exists(DATEI):
    try:
        with open(DATEI, "r", encoding="utf-8") as f:
            notizen = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        notizen = []
else:
    notizen = []

#Notizen speichern
def speichere_notizen():
    with open(DATEI, "w", encoding="utf-8") as f:
        json.dump(notizen, f, ensure_ascii=False, indent=4)

@app.route("/", methods=["GET", "POST"])
def index():
    global notizen

    if request.method == "POST":
        aktion = request.form.get("aktion")

        # Neue Notiz hinzufügen
        if aktion == "hinzufuegen":
            neue_notiz = request.form.get("neue_notiz")
            if neue_notiz:
                notiz_objekt = {
                    "text": neue_notiz,
                    "datum": datetime.now().strftime("%m-%d %H:%M")}
                notizen.append(notiz_objekt)
                speichere_notizen()
        # Einzelne Notiz löschen
        elif aktion == "loeschen":
            index = int(request.form.get("index"))
            if 0 <= index < len(notizen):
                notizen.pop(index)
                speichere_notizen()
        # Alle Notizen löschen
        elif aktion == "alle_loeschen":
            notizen.clear()
            speichere_notizen()

        # Nach jeder Änderung neu laden (damit kein doppeltes Absenden)
        return redirect("/")

    # GET → Seite anzeigen
    return render_template("index.html", notizen=notizen)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)