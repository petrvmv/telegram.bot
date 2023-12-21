from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' and 'sqlite:///notes.db' with your actual bot token and SQLite database URI
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
#DB_URI = 'sqlite:///notes.db'
DB_URI = 'sqlite:///C:/temp/notes.db'
Base = declarative_base()

class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, Sequence('note_id_seq'), primary_key=True)
    text = Column(String(255))

engine = create_engine(DB_URI, echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to the Notes Bot! Use /add [note text] to add a new note, /getall to view all notes or /deleteall to delete all notes.')

def add_note(update: Update, context: CallbackContext) -> None:
    note_text = context.args
    if not note_text:
        update.message.reply_text('Please provide a note text. Usage: /add [note text]')
        return

    new_note = Note(text=' '.join(note_text))
    session.add(new_note)
    session.commit()
    update.message.reply_text('Note added successfully!')

def get_all_notes(update: Update, context: CallbackContext) -> None:
    all_notes = session.query(Note).all()
    if all_notes:
        notes_text = '\n'.join([f'{note.id}. {note.text}' for note in all_notes])
        update.message.reply_text(f'All Notes:\n{notes_text}')
    else:
        update.message.reply_text('No notes found.')

def delete_all_notes(update: Update, context: CallbackContext) -> None:
    session.query(Note).delete()
    session.commit()
    update.message.reply_text('All notes deleted successfully!')

def main() -> None:
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('add', add_note, pass_args=True))
    dp.add_handler(CommandHandler('getall', get_all_notes))
    dp.add_handler(CommandHandler('deleteall', delete_all_notes))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()