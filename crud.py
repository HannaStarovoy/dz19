from sqlalchemy import select
from models import Note,session

def get_note(uuid: str)->Note:
    with session() as conn:
        query = select(Note).where(Note.uuid == uuid)
        return conn.execute(query).scalar_one()

def create_note(title: str, content: str)->Note:
    with session() as conn:
        note = Note(title=title,content=content)
        conn.add(note)
        conn.commit()
        conn.refresh(note)
    return note

def get_all_notes()-> list[Note]:
    with session() as conn:
        return conn.execute(select(Note)).scalars().all()