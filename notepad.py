import bottle
from bottle import get, post, request, error
import sqlite3
import html

import bottle
from bottle import get, post, request, error
import sqlite3
import html


class NotesManager:
    def __init__(self, db_name="bloc_notes.db"):
        try:
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
            self.create_table()
        except Exception as e:
            print(f"Error: {e}")

    def create_table(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    type TEXT NOT NULL
                )
            ''')
            self.conn.commit()
        except Exception as e:
            print(f"Error creating table: {e}")

    def add_note(self, note):
        try:
            self.cursor.execute("INSERT INTO notes (title, content, type) VALUES (?, ?, ?)",
                                (note.title, note.content, note.type))
            self.conn.commit()
            print("Note added successfully!")
        except Exception as e:
            print(f"Error adding note: {e}")

    def display_notes(self):
        try:
            self.cursor.execute("SELECT * FROM notes")
            notes = self.cursor.fetchall()
            return notes
        except Exception as e:
            print(f"Error displaying notes: {e}")
            return []

    def display_note(self, note_id):
        try:
            self.cursor.execute("SELECT title, content FROM notes WHERE id=?", (note_id,))
            note = self.cursor.fetchone()
            if note:
                return f"Title: {note[0]} <br> Content: {note[1]}"
            else:
                return "Note not found."
        except Exception as e:
            print(f"Error displaying note: {e}")
            return "Error displaying note."

    def delete_note(self, note_id):
        try:
            self.cursor.execute("DELETE FROM notes WHERE id=?", (note_id,))
            self.conn.commit()
            return "Note deleted successfully!"
        except Exception as e:
            print(f"Error deleting note: {e}")
            return "Error deleting note."


class Note:
    def __init__(self, title, content, note_type):
        self.title = title
        self.content = content
        self.type = note_type


class ImageNote(Note):
    def __init__(self, title, content):
        super().__init__(title, content, note_type="image")


class AnonymousNote(Note):
    def __init__(self, content):
        super().__init__(title="Anonymous", content=content, note_type="anonymous")


@get('/notepad')
def notepad():
    return '''
        <form action="/notepad" method="post">
            Enter your text: <input name="text" type="text" />
            <input value="Save" type="submit" />
        </form>
    '''


@get('/note')
def note():
    return '''
        <form action="/note" method="post">
            Enter the name of your note: <input name="title" type="text" />
            <br>
            Enter the text of your note: <input name="content" type="text" />
            <br>
            <input value="Save" type="submit" />
        </form>
    '''


@post('/note')
def add_note():
    try:
        title = html.escape(request.forms.get('title'))
        content = html.escape(request.forms.get('content'))
        note_type = request.forms.get('type')

        if note_type == "image":
            notes_manager.add_note(ImageNote(title, content))
        elif note_type == "anonymous":
            notes_manager.add_note(AnonymousNote(content))
        else:
            notes_manager.add_note(Note(title, content, note_type))

        return "Note added successfully!"
    except Exception as e:
        return f"Error adding note: {e}"


@get('/notepad')
def notepad():
    return '''
        <form action="/notepad" method="post">
            Enter your text: <input name="text" type="text" />
            <input value="Save" type="submit" />
        </form>
    '''


@get('/note')
def note():
    return '''
        <form action="/note" method="post">
            Enter the name of your note: <input name="title" type="text" />
            <br>
            Enter the text of your note: <input name="content" type="text" />
            <br>
            Note Type:
            <select name="type">
                <option value="text">Text Note</option>
                <option value="image">Image Note</option>
                <option value="anonymous">Anonymous Note</option>
            </select>
            <br>
            <input value="Save" type="submit" />
        </form>
    '''


@post('/note')
def add_note():
    try:
        title = html.escape(request.forms.get('title'))
        content = html.escape(request.forms.get('content'))
        note_type = request.forms.get('type')

        if note_type == "image":
            notes_manager.add_note(ImageNote(title, content))
        elif note_type == "anonymous":
            notes_manager.add_note(AnonymousNote(content))
        else:
            notes_manager.add_note(Note(title, content, note_type))

        return "Note added successfully!"
    except Exception as e:
        return f"Error adding note: {e}"


@get('/')
def notepad():
    return '''
        <button onclick="window.location.href='/note'">Add note</button>
        <button onclick="window.location.href='/display-all-notes'">Display all notes</button>
        <button onclick="window.location.href='/display-a-note'">Display a note</button>
        <button onclick="window.location.href='/delete-a-note'">Delete a note</button>
    '''

@get('/display-all-notes')
def display_all_notes():
    try:
        notes = notes_manager.display_notes()
        html_content = ""
        for note in notes:
            html_content += f"Note n°{note[0]} : {note[1]} | {note[2]}<br>"
        return html_content
    except Exception as e:
        return f"Error displaying notes: {e}"

@get('/display-a-note')
def display_a_note():
    return '''
        <form action="/display-a-note" method="post">
            Enter the id of the note you want to display: <input name="id" type="text" />
            <br>
            <input value="Display" type="submit" />
        </form>
    '''

@post('/display-a-note')
def display_a_note():
    try:
        note_id = int(request.forms.get('id'))
        return notes_manager.display_note(note_id)
    except ValueError:
        return "Invalid input. Please enter a valid note ID."

@get('/delete-a-note')
def delete_a_note():
    return '''
        <form action="/delete-a-note" method="post">
            Enter the id of the note you want to delete: <input name="id" type="text" />
            <br>
            <input value="Delete" type="submit" />
        </form>
    '''

@post('/delete-a-note')
def delete_a_note():
    try:
        note_id = int(request.forms.get('id'))
        return notes_manager.delete_note(note_id)
    except ValueError:
        return "Invalid input. Please enter a valid note ID."


if __name__ == '__main__':
    notes_manager = NotesManager()
    bottle.run(host='localhost', port=8080)
