import sqlite3


con = sqlite3.connect('gfg.db')


def create_tables():
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS questions(id text,question text)''')
    con.commit()


def save_question(id,question):
    cur = con.cursor()
    cur.execute('''INSERT INTO questions VALUES(?,?)''',(id,question))
    con.commit()

def find_question(id):
    cur = con.cursor()
    cur.execute('SELECT question from questions WHERE id=?',(id,))
    results = cur.fetchone()
    return results[0] if results else None




if __name__ == '__main__':
    find_question('shop-in-candy-store1145')
