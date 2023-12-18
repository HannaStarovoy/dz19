from flask import Flask, Response, request,  render_template, redirect, url_for
from sqlalchemy import exc

from crud import get_note, create_note,get_all_notes
from models import create_tables, drop_tables

# Создаем приложение Flask
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static-files/",
)


drop_tables()
create_tables()

@app.route( "/", methods=["GET"])
def home_page_view():
    all_notes = get_all_notes()
    return render_template("home.html", notes=all_notes)  # HTML

@app.route("/create_note", methods=["GET"])
def get_create_notes():
    return render_template("create_note.html")

@app.route("/create_note", methods=["POST"])
def create_note_view():
    note_data = request.form

    note = create_note(
            title=note_data["title"],
            content=note_data["content"],
        )

    return redirect(url_for("note_view", uuid = note.uuid))

@app.route("/<uuid>", methods=["GET"])
def note_view(uuid: str):
    try:
        note = get_note(uuid)
    except exc.NoResultFound:
        return Response("Note not found.", status=404)

    return render_template(
        "note.html",
        uuid = note.uuid,
        title = note.title,
        content = note.content,
        create_at = note.created_at
    )

