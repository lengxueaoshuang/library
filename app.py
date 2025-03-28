import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from models import init_db, User, Book

class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("图书管理系统")
        self.geometry("800x600")
        self.resizable(True, True)
        
        # 初始化数据库
        init_db()
        
        # 设置当前用户
        self.current_user = None
        
        # 显示登录页面
        self.show_login_page()
    
    def show_login_page(self):
        # 清除当前页面
        for widget in self.winfo_children():
            widget.destroy()
        
        # 创建登录框架
        login_frame = tk.Frame(self)
        login_frame.pack(pady=100)
        
        # 标题
        title_label = tk.Label(login_frame, text="图书管理系统", font=("Arial", 24, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # 用户名
        username_label = tk.Label(login_frame, text="用户名:")
        username_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.username_entry = tk.Entry(login_frame, width=30)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # 密码
        password_label = tk.Label(login_frame, text="密码:")
        password_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.password_entry = tk.Entry(login_frame, width=30, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # 按钮框架
        button_frame = tk.Frame(login_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        # 登录按钮
        login_button = tk.Button(button_frame, text="登录", width=10, command=self.login)
        login_button.grid(row=0, column=0, padx=10)
        
        # 注册按钮
        register_button = tk.Button(button_frame, text="注册", width=10, command=self.show_register_page)
        register_button.grid(row=0, column=1, padx=10)
    
    def show_register_page(self):
        # 清除当前页面
        for widget in self.winfo_children():
            widget.destroy()
        
        # 创建注册框架
        register_frame = tk.Frame(self)
        register_frame.pack(pady=100)
        
        # 标题
        title_label = tk.Label(register_frame, text="用户注册", font=("Arial", 24, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # 用户名
        username_label = tk.Label(register_frame, text="用户名:")
        username_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.reg_username_entry = tk.Entry(register_frame, width=30)
        self.reg_username_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # 密码
        password_label = tk.Label(register_frame, text="密码:")
        password_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.reg_password_entry = tk.Entry(register_frame, width=30, show="*")
        self.reg_password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # 确认密码
        confirm_label = tk.Label(register_frame, text="确认密码:")
        confirm_label.grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.confirm_entry = tk.Entry(register_frame, width=30, show="*")
        self.confirm_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # 按钮框架
        button_frame = tk.Frame(register_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        # 注册按钮
        register_button = tk.Button(button_frame, text="注册", width=10, command=self.register)
        register_button.grid(row=0, column=0, padx=10)
        
        # 返回按钮
        back_button = tk.Button(button_frame, text="返回", width=10, command=self.show_login_page)
        back_button.grid(row=0, column=1, padx=10)
    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("错误", "用户名和密码不能为空")
            return
        
        if User.authenticate(username, password):
            self.current_user = username
            self.show_main_page()
        else:
            messagebox.showerror("错误", "用户名或密码错误")
    
    def register(self):
        username = self.reg_username_entry.get().strip()
        password = self.reg_password_entry.get().strip()
        confirm = self.confirm_entry.get().strip()
        
        if not username or not password or not confirm:
            messagebox.showerror("错误", "所有字段都不能为空")
            return
        
        if password != confirm:
            messagebox.showerror("错误", "两次输入的密码不一致")
            return
        
        user = User(username, password)
        if user.save():
            messagebox.showinfo("成功", "注册成功，请登录")
            self.show_login_page()
        else:
            messagebox.showerror("错误", "用户名已存在")
    
    def show_main_page(self):
        # 清除当前页面
        for widget in self.winfo_children():
            widget.destroy()
        
        # 创建主框架
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 顶部框架 - 包含欢迎信息和搜索栏
        top_frame = tk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=5)
        
        # 欢迎信息
        welcome_label = tk.Label(top_frame, text=f"欢迎, {self.current_user}!", font=("Arial", 12))
        welcome_label.pack(side=tk.LEFT, padx=5)
        
        # 搜索框架
        search_frame = tk.Frame(top_frame)
        search_frame.pack(side=tk.RIGHT, padx=5)
        
        # 搜索输入
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        # 搜索按钮
        search_button = tk.Button(search_frame, text="搜索", command=self.search_books)
        search_button.pack(side=tk.LEFT)
        
        # 清除搜索按钮
        clear_search_button = tk.Button(search_frame, text="清除搜索", command=self.load_books)
        clear_search_button.pack(side=tk.LEFT, padx=5)
        
        # 退出登录按钮
        logout_button = tk.Button(top_frame, text="退出登录", command=self.show_login_page)
        logout_button.pack(side=tk.RIGHT, padx=5)
        
        # 中间框架 - 包含书籍列表
        middle_frame = tk.Frame(main_frame)
        middle_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 创建书籍表格
        columns = ("ID", "书名", "作者", "出版社", "ISBN", "出版年份", "分类", "描述")
        self.book_tree = ttk.Treeview(middle_frame, columns=columns, show="headings")
        
        # 设置列标题
        for col in columns:
            self.book_tree.heading(col, text=col)
            self.book_tree.column(col, width=100)
        
        # 设置列宽
        self.book_tree.column("ID", width=50)
        self.book_tree.column("书名", width=150)
        self.book_tree.column("描述", width=200)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(middle_frame, orient=tk.VERTICAL, command=self.book_tree.yview)
        self.book_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.book_tree.pack(fill=tk.BOTH, expand=True)
        
        # 绑定双击事件
        self.book_tree.bind("<Double-1>", self.edit_book)
        
        # 底部框架 - 包含操作按钮
        bottom_frame = tk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, pady=5)
        
        # 添加书籍按钮
        add_button = tk.Button(bottom_frame, text="添加书籍", command=self.add_book)
        add_button.pack(side=tk.LEFT, padx=5)
        
        # 删除书籍按钮
        delete_button = tk.Button(bottom_frame, text="删除书籍", command=self.delete_book)
        delete_button.pack(side=tk.LEFT, padx=5)
        
        # 导出按钮框架
        export_frame = tk.Frame(bottom_frame)
        export_frame.pack(side=tk.RIGHT)
        
        # 导出数据库按钮
        export_db_button = tk.Button(export_frame, text="导出数据库", command=self.export_db)
        export_db_button.pack(side=tk.LEFT, padx=5)
        
        # 导入数据库按钮
        import_db_button = tk.Button(export_frame, text="导入数据库", command=self.import_db)
        import_db_button.pack(side=tk.LEFT, padx=5)
        
        # 导出书籍按钮
        export_books_button = tk.Button(export_frame, text="导出书籍(JSON)", command=self.export_books_json)
        export_books_button.pack(side=tk.LEFT, padx=5)
        
        # 导入书籍按钮
        import_books_button = tk.Button(export_frame, text="导入书籍(JSON)", command=self.import_books_json)
        import_books_button.pack(side=tk.LEFT, padx=5)
        
        # 导出书籍列表按钮
        export_list_button = tk.Button(export_frame, text="导出书籍列表(CSV)", command=self.export_books_csv)
        export_list_button.pack(side=tk.LEFT, padx=5)
        
        # 导入书籍列表按钮
        import_list_button = tk.Button(export_frame, text="导入书籍(CSV)", command=self.import_books_csv)
        import_list_button.pack(side=tk.LEFT, padx=5)
        
        # 加载书籍数据
        self.load_books()
    
    def load_books(self):
        # 清空表格
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)
        
        # 获取所有书籍
        books = Book.get_all()
        
        # 填充表格
        for book in books:
            values = (
                book['id'],
                book['title'],
                book['author'] or "",
                book['publisher'] or "",
                book['isbn'] or "",
                book['publication_year'] or "",
                book['category'] or "",
                book['description'] or ""
            )
            self.book_tree.insert("", tk.END, values=values)
    
    def search_books(self):
        keyword = self.search_entry.get().strip()
        if not keyword:
            messagebox.showinfo("提示", "请输入搜索关键词")
            return
        
        # 清空表格
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)
        
        # 搜索书籍
        books = Book.search(keyword)
        
        # 填充表格
        for book in books:
            values = (
                book['id'],
                book['title'],
                book['author'] or "",
                book['publisher'] or "",
                book['isbn'] or "",
                book['publication_year'] or "",
                book['category'] or "",
                book['description'] or ""
            )
            self.book_tree.insert("", tk.END, values=values)
    
    def add_book(self):
        # 创建添加书籍窗口
        self.book_window = tk.Toplevel(self)
        self.book_window.title("添加书籍")
        self.book_window.geometry("500x400")
        self.book_window.resizable(False, False)
        self.book_window.transient(self)  # 设置为主窗口的子窗口
        self.book_window.grab_set()  # 模态窗口
        
        # 创建表单
        self.create_book_form()
        
        # 保存按钮
        save_button = tk.Button(self.book_window, text="保存", command=self.save_book)
        save_button.pack(pady=10)
    
    def edit_book(self, event):
        # 获取选中的项
        selected_item = self.book_tree.selection()
        if not selected_item:
            return
        
        # 获取书籍ID
        book_id = self.book_tree.item(selected_item[0], "values")[0]
        
        # 获取书籍信息
        book = Book.get_by_id(book_id)
        if not book:
            return
        
        # 创建编辑书籍窗口
        self.book_window = tk.Toplevel(self)
        self.book_window.title("编辑书籍")
        self.book_window.geometry("500x400")
        self.book_window.resizable(False, False)
        self.book_window.transient(self)  # 设置为主窗口的子窗口
        self.book_window.grab_set()  # 模态窗口
        
        # 创建表单
        self.create_book_form(book)
        
        # 保存按钮
        save_button = tk.Button(self.book_window, text="保存", command=self.save_book)
        save_button.pack(pady=10)
    
    def create_book_form(self, book=None):
        # 创建表单框架
        form_frame = tk.Frame(self.book_window)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 书籍ID（隐藏）
        self.book_id = tk.StringVar(value=book['id'] if book else "")
        
        # 书名
        title_label = tk.Label(form_frame, text="书名:")
        title_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.title_entry = tk.Entry(form_frame, width=40)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        if book:
            self.title_entry.insert(0, book['title'])
        
        # 作者
        author_label = tk.Label(form_frame, text="作者:")
        author_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.author_entry = tk.Entry(form_frame, width=40)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)
        if book and book['author']:
            self.author_entry.insert(0, book['author'])
        
        # 出版社
        publisher_label = tk.Label(form_frame, text="出版社:")
        publisher_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.publisher_entry = tk.Entry(form_frame, width=40)
        self.publisher_entry.grid(row=2, column=1, padx=5, pady=5)
        if book and book['publisher']:
            self.publisher_entry.insert(0, book['publisher'])
        
        # ISBN
        isbn_label = tk.Label(form_frame, text="ISBN:")
        isbn_label.grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.isbn_entry = tk.Entry(form_frame, width=40)
        self.isbn_entry.grid(row=3, column=1, padx=5, pady=5)
        if book and book['isbn']:
            self.isbn_entry.insert(0, book['isbn'])
        
        # 出版年份
        year_label = tk.Label(form_frame, text="出版年份:")
        year_label.grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.year_entry = tk.Entry(form_frame, width=40)
        self.year_entry.grid(row=4, column=1, padx=5, pady=5)
        if book and book['publication_year']:
            self.year_entry.insert(0, str(book['publication_year']))
        
        # 分类
        category_label = tk.Label(form_frame, text="分类:")
        category_label.grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.category_entry = tk.Entry(form_frame, width=40)
        self.category_entry.grid(row=5, column=1, padx=5, pady=5)
        if book and book['category']:
            self.category_entry.insert(0, book['category'])
        
        # 描述
        description_label = tk.Label(form_frame, text="描述:")
        description_label.grid(row=6, column=0, sticky="ne", padx=5, pady=5)
        self.description_text = tk.Text(form_frame, width=40, height=5)
        self.description_text.grid(row=6, column=1, padx=5, pady=5)
        if book and book['description']:
            self.description_text.insert("1.0", book['description'])
    
    def save_book(self):
        # 获取表单数据
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        publisher = self.publisher_entry.get().strip()
        isbn = self.isbn_entry.get().strip()
        year_str = self.year_entry.get().strip()
        category = self.category_entry.get().strip()
        description = self.description_text.get("1.0", tk.END).strip()
        
        # 验证必填字段
        if not title:
            messagebox.showerror("错误", "书名不能为空")
            return
        
        # 验证年份
        publication_year = None
        if year_str:
            try:
                publication_year = int(year_str)
            except ValueError:
                messagebox.showerror("错误", "出版年份必须是数字")
                return
        
        # 创建书籍对象
        book_id = self.book_id.get()
        book = Book(
            title=title,
            author=author if author else None,
            publisher=publisher if publisher else None,
            isbn=isbn if isbn else None,
            publication_year=publication_year,
            category=category if category else None,
            description=description if description else None,
            id=int(book_id) if book_id else None
        )
        
        # 保存书籍
        if book.save():
            messagebox.showinfo("成功", "保存成功")
            self.book_window.destroy()
            self.load_books()
        else:
            messagebox.showerror("错误", "保存失败")
    
    def delete_book(self):
        # 获取选中的项
        selected_item = self.book_tree.selection()
        if not selected_item:
            messagebox.showinfo("提示", "请先选择要删除的书籍")
            return
        
        # 获取书籍ID
        book_id = self.book_tree.item(selected_item[0], "values")[0]
        
        # 确认删除
        if messagebox.askyesno("确认", "确定要删除这本书吗？"):
            # 删除书籍
            if Book.delete(book_id):
                messagebox.showinfo("成功", "删除成功")
                self.load_books()
            else:
                messagebox.showerror("错误", "删除失败")
    
    def export_db(self):
        # 选择保存路径
        filename = filedialog.asksaveasfilename(
            defaultextension=".db",
            filetypes=[("SQLite数据库", "*.db")],
            title="导出数据库"
        )
        if not filename:
            return
        
        # 导出数据库
        if Book.export_db(filename):
            messagebox.showinfo("成功", f"数据库已导出到 {filename}")
        else:
            messagebox.showerror("错误", "导出失败")
    
    def import_db(self):
        # 选择文件
        filename = filedialog.askopenfilename(
            filetypes=[("SQLite数据库", "*.db")],
            title="导入数据库"
        )
        if not filename:
            return
        
        # 确认导入
        if messagebox.askyesno("确认", "导入将覆盖当前数据库，确定要继续吗？"):
            # 导入数据库
            if Book.import_db(filename):
                messagebox.showinfo("成功", "数据库导入成功")
                self.load_books()
            else:
                messagebox.showerror("错误", "导入失败")
    
    def export_books_json(self):
        # 选择保存路径
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON文件", "*.json")],
            title="导出书籍到JSON"
        )
        if not filename:
            return
        
        # 导出书籍
        if Book.export_to_json(filename):
            messagebox.showinfo("成功", f"书籍已导出到 {filename}")
        else:
            messagebox.showerror("错误", "导出失败")
    
    def import_books_json(self):
        # 选择文件
        filename = filedialog.askopenfilename(
            filetypes=[("JSON文件", "*.json")],
            title="从JSON导入书籍"
        )
        if not filename:
            return
        
        # 导入书籍
        if Book.import_from_json(filename):
            messagebox.showinfo("成功", "书籍导入成功")
            self.load_books()
        else:
            messagebox.showerror("错误", "导入失败")
    
    def export_books_csv(self):
        # 选择保存路径
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV文件", "*.csv")],
            title="导出书籍到CSV"
        )
        if not filename:
            return
        
        # 导出书籍
        if Book.export_to_csv(filename):
            messagebox.showinfo("成功", f"书籍列表已导出到 {filename}")
        else:
            messagebox.showerror("错误", "导出失败")
    
    def import_books_csv(self):
        # 选择文件
        filename = filedialog.askopenfilename(
            filetypes=[("CSV文件", "*.csv")],
            title="从CSV导入书籍"
        )
        if not filename:
            return
        
        # 导入书籍
        if Book.import_from_csv(filename):
            messagebox.showinfo("成功", "书籍导入成功")
            self.load_books()
        else:
            messagebox.showerror("错误", "导入失败")

if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()