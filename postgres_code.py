import psycopg2
from dotenv import load_dotenv
import os 


load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD =os.getenv("DB_PASSWORD")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def insert_category(category_id,category_name):
    conn=get_connection()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO categories (category_id ,name)
        VALUES (%s, %s)""", (category_id,category_name))
    conn.commit()
    cursor.close()
    conn.close()

def insert_threads(category_id,thread_id ,title, question,author,posted_at):
    conn=get_connection()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO threads (category_id,thread_id ,title, question,author,posted_at)
        VALUES (%s,%s, %s, %s, %s,%s)""", (category_id,thread_id ,title, question,author,posted_at))
    conn.commit()
    cursor.close()
    conn.close()

def insert_answers(category_id,thread_id,id_msg,answer, author,posted_at):
    conn=get_connection()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO answers (category_id,thread_id, answer_id,answer_text,author,posted_at)
        VALUES (%s,%s,%s, %s, %s, %s)""", (category_id,thread_id,id_msg,answer, author,posted_at))
    conn.commit()
    cursor.close()
    conn.close()