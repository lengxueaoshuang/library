import sqlite3
import os
import json
import csv
from datetime import datetime

DB_PATH = 'library.db'

def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """初始化数据库"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 创建用户表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 创建书籍表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT,
        publisher TEXT,
        isbn TEXT,
        publication_year INTEGER,
        category TEXT,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()

class User:
    """用户模型"""
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def save(self):
        """保存用户到数据库"""
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (self.username, self.password)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # 用户名已存在
            return False
        finally:
            conn.close()
    
    @staticmethod
    def authenticate(username, password):
        """验证用户"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM users WHERE username = ? AND password = ?',
            (username, password)
        )
        user = cursor.fetchone()
        conn.close()
        return user is not None

class Book:
    """书籍模型"""
    def __init__(self, title, author=None, publisher=None, isbn=None, 
                 publication_year=None, category=None, description=None, id=None):
        self.id = id
        self.title = title
        self.author = author
        self.publisher = publisher
        self.isbn = isbn
        self.publication_year = publication_year
        self.category = category
        self.description = description
    
    def save(self):
        """保存书籍到数据库"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            # 新增书籍
            cursor.execute(
                '''INSERT INTO books 
                   (title, author, publisher, isbn, publication_year, category, description) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (self.title, self.author, self.publisher, self.isbn, 
                 self.publication_year, self.category, self.description)
            )
            self.id = cursor.lastrowid
        else:
            # 更新书籍
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(
                '''UPDATE books SET 
                   title = ?, author = ?, publisher = ?, isbn = ?, 
                   publication_year = ?, category = ?, description = ?,
                   updated_at = ? 
                   WHERE id = ?''',
                (self.title, self.author, self.publisher, self.isbn, 
                 self.publication_year, self.category, self.description,
                 current_time, self.id)
            )
        
        conn.commit()
        conn.close()
        return True
    
    @staticmethod
    def delete(book_id):
        """删除书籍"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
        conn.commit()
        conn.close()
        return True
    
    @staticmethod
    def get_all():
        """获取所有书籍"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books ORDER BY title')
        books = cursor.fetchall()
        conn.close()
        return books
    
    @staticmethod
    def search(keyword):
        """搜索书籍"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''SELECT * FROM books 
               WHERE title LIKE ? OR author LIKE ? OR publisher LIKE ? 
               OR isbn LIKE ? OR category LIKE ? OR description LIKE ?''',
            ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%',
             '%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%')
        )
        books = cursor.fetchall()
        conn.close()
        return books
    
    @staticmethod
    def get_by_id(book_id):
        """根据ID获取书籍"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
        book = cursor.fetchone()
        conn.close()
        return book
    
    @staticmethod
    def export_to_json(filename):
        """导出所有书籍到JSON文件"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books')
        books = cursor.fetchall()
        conn.close()
        
        # 将查询结果转换为字典列表
        book_list = [dict(book) for book in books]
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(book_list, f, ensure_ascii=False, indent=4)
        
        return True
    
    @staticmethod
    def export_to_csv(filename):
        """导出所有书籍到CSV文件"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books')
        books = cursor.fetchall()
        conn.close()
        
        # 获取列名
        if books:
            fieldnames = books[0].keys()
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for book in books:
                    writer.writerow(dict(book))
            
            return True
        return False
    
    @staticmethod
    def import_from_json(filename):
        """从JSON文件导入书籍"""
        if not os.path.exists(filename):
            return False
        
        with open(filename, 'r', encoding='utf-8') as f:
            books_data = json.load(f)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        for book_data in books_data:
            # 移除id和时间戳字段，让数据库自动生成
            if 'id' in book_data:
                del book_data['id']
            if 'created_at' in book_data:
                del book_data['created_at']
            if 'updated_at' in book_data:
                del book_data['updated_at']
            
            # 构建插入语句
            fields = ', '.join(book_data.keys())
            placeholders = ', '.join(['?'] * len(book_data))
            values = list(book_data.values())
            
            cursor.execute(f'INSERT INTO books ({fields}) VALUES ({placeholders})', values)
        
        conn.commit()
        conn.close()
        return True
    
    @staticmethod
    def import_from_csv(filename):
        """从CSV文件导入书籍"""
        if not os.path.exists(filename):
            return False
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        with open(filename, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # 移除id和时间戳字段，让数据库自动生成
                if 'id' in row:
                    del row['id']
                if 'created_at' in row:
                    del row['created_at']
                if 'updated_at' in row:
                    del row['updated_at']
                
                # 构建插入语句
                fields = ', '.join(row.keys())
                placeholders = ', '.join(['?'] * len(row))
                values = list(row.values())
                
                cursor.execute(f'INSERT INTO books ({fields}) VALUES ({placeholders})', values)
        
        conn.commit()
        conn.close()
        return True
    
    @staticmethod
    def export_db(filename):
        """导出整个数据库"""
        if os.path.exists(DB_PATH):
            import shutil
            shutil.copyfile(DB_PATH, filename)
            return True
        return False
    
    @staticmethod
    def import_db(filename):
        """导入整个数据库"""
        if os.path.exists(filename):
            import shutil
            shutil.copyfile(filename, DB_PATH)
            return True
        return False