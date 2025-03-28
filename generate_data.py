import sqlite3
import random
from datetime import datetime, timedelta

# 数据库路径
DB_PATH = 'library.db'

# 示例数据
book_titles = [
    "Python编程：从入门到实践", "Java核心技术", "C++程序设计语言", "算法导论",
    "数据结构与算法分析", "深入理解计算机系统", "计算机网络：自顶向下方法",
    "数据库系统概念", "操作系统概念", "软件工程：实践者的研究方法",
    "人工智能：一种现代方法", "机器学习实战", "深度学习", "统计学习方法",
    "计算机组成原理", "编译原理", "离散数学及其应用", "线性代数",
    "概率论与数理统计", "微积分", "数值分析", "图论算法",
    "并行计算", "分布式系统", "云计算与大数据", "网络安全基础",
    "密码学原理", "软件测试", "敏捷开发实践", "设计模式"
]

authors = [
    "张三", "李四", "王五", "赵六", "钱七", "孙八", "周九", "吴十",
    "郑十一", "王十二", "Robert C. Martin", "Martin Fowler", "Kent Beck",
    "Erich Gamma", "Donald E. Knuth", "Thomas H. Cormen", "Brian W. Kernighan"
]

publishers = [
    "清华大学出版社", "机械工业出版社", "电子工业出版社", "人民邮电出版社",
    "科学出版社", "高等教育出版社", "北京大学出版社", "O'Reilly Media",
    "Addison-Wesley", "Pearson", "Wiley", "Springer", "Manning Publications"
]

categories = [
    "计算机科学", "编程语言", "算法", "数据结构", "操作系统",
    "数据库", "网络", "人工智能", "机器学习", "软件工程",
    "数学", "安全", "云计算", "分布式系统", "编译原理"
]

def generate_isbn():
    """生成随机ISBN"""
    return f"978-{random.randint(0, 9)}-{random.randint(100, 999)}-{random.randint(10000, 99999)}-{random.randint(0, 9)}"

def generate_description(title, author, category):
    """生成书籍描述"""
    templates = [
        f"《{title}》是{author}编写的一本关于{category}的经典教材，深入浅出地讲解了相关概念和技术。",
        f"这本{category}领域的权威著作《{title}》由{author}精心编写，是学习该领域的必备参考书。",
        f"《{title}》是{author}多年研究{category}的心血结晶，内容全面且实用。",
        f"作为{category}方向的入门书籍，《{title}》由专家{author}编写，适合各层次读者阅读。",
        f"《{title}》是{author}在{category}领域的代表作，包含了大量实用案例和最佳实践。"
    ]
    return random.choice(templates)

def generate_book_data():
    """生成随机书籍数据"""
    title = random.choice(book_titles)
    author = random.choice(authors)
    publisher = random.choice(publishers)
    isbn = generate_isbn()
    publication_year = random.randint(2000, 2023)
    category = random.choice(categories)
    description = generate_description(title, author, category)
    
    # 创建时间在过去两年内随机
    days_ago = random.randint(0, 730)
    created_at = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d %H:%M:%S')
    updated_at = created_at
    
    return {
        "title": title,
        "author": author,
        "publisher": publisher,
        "isbn": isbn,
        "publication_year": publication_year,
        "category": category,
        "description": description,
        "created_at": created_at,
        "updated_at": updated_at
    }

def insert_book(cursor, book_data):
    """插入书籍数据到数据库"""
    cursor.execute(
        '''INSERT INTO books 
           (title, author, publisher, isbn, publication_year, category, description, created_at, updated_at) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (book_data["title"], book_data["author"], book_data["publisher"], book_data["isbn"], 
         book_data["publication_year"], book_data["category"], book_data["description"],
         book_data["created_at"], book_data["updated_at"])
    )

def main():
    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 检查books表是否存在，如果不存在则创建
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
    
    # 生成并插入30条书籍数据
    print("开始生成30条书籍数据...")
    for i in range(30):
        book_data = generate_book_data()
        insert_book(cursor, book_data)
        print(f"已生成第 {i+1} 条数据: {book_data['title']}")
    
    # 提交事务并关闭连接
    conn.commit()
    conn.close()
    
    print("数据生成完成！")

if __name__ == "__main__":
    main()