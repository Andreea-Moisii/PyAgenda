import json
import sqlite3 as sql


class SqlDataBase:
    conn = sql.connect('list.db')

    # singleton
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SqlDataBase, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def add_item(self, item):
        # insert title, description and datetime into the database
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO shop_items (title, description, date_added) VALUES (?, ?, datetime())",
                       (item["title"], item["description"]))
        self.conn.commit()
        # get the id of the last inserted item
        cursor.execute("Select last_insert_rowid()")
        item['id'] = cursor.fetchone()[0]

    def get_items(self):
        # get all items from the database
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM shop_items")
        rows = cursor.fetchall()
        items = []
        for row in rows:
            items.append({"id": row[0], "title": row[1], "description": row[2], "date_added": row[3]})
        return items

    def delete_item(self, item):
        # delete item from the database
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM shop_items WHERE id = ?", (item["id"],))
        self.conn.commit()

    def update_item(self, item):
        # update item in the database
        cursor = self.conn.cursor()
        cursor.execute("UPDATE shop_items SET title = ?, description = ?, date_added = datetime() WHERE id = ?",
                       (item["title"], item["description"], item["id"]))
        self.conn.commit()
