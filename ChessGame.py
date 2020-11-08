import tkinter
from tkinter import messagebox
from tkinter.ttk import Separator
import pymysql
import json
import sqlite3


# =================================  Constant =======================================
DB_HOST = "47.101.217.179"
DB_USER = "rocks"
DB_PASS = "Qy123456."
DB_DB = "chess"

# BLUE_CIRCLE_COLOR = "aqua"
# RED_CIRCLE_COLOR = "deeppink"
BLUE_CIRCLE_COLOR = "blue"
RED_CIRCLE_COLOR = "red"
BASE_COLOR = "LightBlue"
CANVAS_COLOR = "White"
BUTTON_BG_COLOR = "Navy"
BUTTON_FG_COLOR = "White"
SEPARATOR_COLOR = "LimeGreen"
WINDOWS_TITLE = "蜘蛛记录器"

CURRENT_USER_ID = None
CURRENT_USER_NAME = None
CURRENT_USER_PASS = None
CURRENT_USER_LOGOUT_POS = None

COL_N = 40
ITEM_SIZE = 15

INIT_SUCCESS = True

USER_IS_LOGIN = False
# ===================================================================================


class DBOperator(object):
    """"
    数据库操作类
    """
    def __init__(self):
        super().__init__()
        # self.db = pymysql.connect(DB_HOST, DB_USER, DB_PASS, DB_DB)
        global INIT_SUCCESS
        try:
            self.db = sqlite3.connect(r'.\ChessGame.db')
            self.cursor = self.db.cursor()
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS "chess" (
              "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
              "blue_pos" TEXT,
              "red_pos" TEXT,
              "user_id" INTEGER
            );
            """)
            self.cursor.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS "union"
            ON "chess" (
              "blue_pos" ASC,
              "red_pos" ASC,
              "user_id" ASC
            );
            """)
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS "user" (
              "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
              "name" TEXT,
              "pass" TEXT
            );
            """)
            self.db.commit()
        except Exception as e:
            print(e)
            INIT_SUCCESS = False

    def is_user_exist(self, username):
        query_sql = "select * from user where name = '{}'".format(username)
        print(query_sql)
        self.cursor.execute(query_sql)
        return self.cursor.fetchone()

    def save_user(self, username, password):
        try:
            insert_sql = "insert into user (name, pass) values ('{}', '{}')".format(username, password)
            print(insert_sql)
            self.cursor.execute(insert_sql)
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def is_login_success(self, username, password):
        query_sql = "select * from user where name = '{}' and pass = '{}'".format(username, password)
        print(query_sql)
        self.cursor.execute(query_sql)
        return self.cursor.fetchone()

    def query_all_records(self):
        global CURRENT_USER_ID
        query_sql = "select id,blue_pos,red_pos from chess where user_id = '{}'".format(CURRENT_USER_ID)
        print(query_sql)
        self.cursor.execute(query_sql)
        return self.cursor.fetchall()

    def get_first_item(self, item):
        return item[0]

    def save_record(self, blue_pos, red_pos):
        try:
            global CURRENT_USER_ID
            save_sql = "insert into chess (blue_pos, red_pos, user_id) values ('{}','{}', '{}')".format(blue_pos, red_pos, CURRENT_USER_ID)
            print(save_sql)
            self.cursor.execute(save_sql)
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            return False


class Home(object):
    """
    首页 用户注册登录
    """
    def __init__(self):
        super().__init__()
        # 创建主窗口
        self.windows = tkinter.Tk()
        # 设置窗口信息
        global WINDOWS_TITLE
        self.windows.title(WINDOWS_TITLE)
        # windows.geometry(800, 600)
        self.windows.resizable(True, True)
        self.windows.configure(bg="white")

        # 添加组件
        self.add_component()
        # 开启事件循环
        self.windows.mainloop()

    def add_component(self):
        # self.frame1 = tkinter.Frame(master=self.windows, bg=BASE_COLOR)
        # self.frame2 = tkinter.Frame(master=self.windows, bg=BASE_COLOR)
        # self.frame3 = tkinter.Frame(master=self.windows, bg=BASE_COLOR)
        # self.label_username = tkinter.Label(master=self.frame1, text='用户名', bg='White', font='Helvetic 20 bold')
        # self.label_username.pack(side=tkinter.LEFT, padx=10)
        # self.text_name = tkinter.Text(master=self.frame1, width=20, height=20)
        # self.text_name.pack(side=tkinter.RIGHT, padx=10)
        # self.label_password = tkinter.Label(master=self.frame2, text='密码', bg='White', font='Helvetic 20 bold')
        # self.label_password.pack(side=tkinter.LEFT, padx=10)
        # self.text_pass = tkinter.Text(master=self.frame2, width=20, height=20)
        # self.text_pass.pack(side=tkinter.RIGHT, padx=10)
        # self.frame1.pack(side=tkinter.TOP, pady=100, padx=50)
        # self.frame2.pack(side=tkinter.TOP, pady=100, padx=50)

        self.label_username = tkinter.Label(master=self.windows, text='用户名', bg='White')
        self.label_username.grid(row=0, column=0)
        self.text_username = tkinter.Entry(master=self.windows)
        self.text_username.grid(row=0, column=1)
        self.label_password = tkinter.Label(master=self.windows, text='密码', bg='White')
        self.label_password.grid(row=1, column=0)
        self.text_password = tkinter.Entry(master=self.windows, show='*')
        self.text_password.grid(row=1, column=1)
        self.button_register = tkinter.Button(master=self.windows, comman=self.register, text="                  注册                  ")
        self.button_register.grid(row=2, column=0)
        self.button_login = tkinter.Button(master=self.windows, comman=self.login, text="                    登录                  ")
        self.button_login.grid(row=2, column=1)

        global INIT_SUCCESS
        if not INIT_SUCCESS:
            messagebox.showerror('程序初始化失败!', '数据库初始化失败，请重新检查环境!')

    def register(self):
        """
        用户注册
        :return:
        """
        username = str(self.text_username.get()).strip()
        password = str(self.text_password.get()).strip()
        if username == '' or password == '':
            messagebox.showerror('注册失败！', '用户名或密码为空，请重新输入!')
            return
        res = db.is_user_exist(username=username)
        if not res:
            res2 = db.save_user(username, password)
            if res2:
                messagebox.showinfo('注册成功！', '恭喜您，注册成功!')
            else:
                # messagebox.showerror('注册失败！', '数据库状态异常!')
                messagebox.showerror('注册失败！', '用户名已存在，请重新输入!')
        else:
            messagebox.showerror('注册失败！', '用户名已存在，请重新输入!')

    def login(self):
        """
        用户登录
        :return:
        """
        username = str(self.text_username.get()).strip()
        password = str(self.text_password.get()).strip()
        if username == '' or password == '':
            messagebox.showerror('登录失败！', '用户名或密码为空，请重新输入!')
            return
        user = db.is_login_success(username, password)
        if user:
            print("登录成功...{}".format(user))
            # 更新用户信息
            global CURRENT_USER_ID, CURRENT_USER_NAME, CURRENT_USER_PASS
            CURRENT_USER_ID, CURRENT_USER_NAME, CURRENT_USER_PASS = user
            # 进入游戏
            self.windows.destroy()
            ChessGame(home=self)
        else:
            messagebox.showerror('登录失败！', '用户名或密码错误，请重新输入!')

    def back_home(self):
        """
        用户退回登录页面
        :return:
        """
        # 创建主窗口
        self.windows = tkinter.Tk()
        # 设置窗口信息
        global WINDOWS_TITLE
        self.windows.title(WINDOWS_TITLE)
        # windows.geometry(800, 600)
        self.windows.resizable(True, True)
        self.windows.configure(bg="white")

        # 添加组件
        self.add_component()
        # 开启事件循环
        self.windows.mainloop()


class ChessGame(object):
    """
    游戏主程序
    """
    def __init__(self, home=None):
        super().__init__()
        # home实例
        self.home = home
        # 创建主窗口
        self.windows = tkinter.Tk()
        # 设置窗口信息
        global WINDOWS_TITLE
        self.windows.title(WINDOWS_TITLE)
        # windows.geometry(800, 600)
        self.windows.resizable(True, True)
        self.windows.configure(bg="white")
        # 添加组件
        self.add_component()
        # 开启事件循环
        self.windows.mainloop()

    def add_component(self):
        # 添加左侧用户信息
        global CURRENT_USER_ID, CURRENT_USER_NAME, CURRENT_USER_PASS, ITEM_SIZE, CURRENT_USER_LOGOUT_POS
        # self.user_info = tkinter.Canvas(master=self.windows, width=21*ITEM_SIZE, height=7*ITEM_SIZE, bg=BASE_COLOR)
        # self.user_info.configure(highlightthickness=0)
        # self.user_info.create_text(ITEM_SIZE*4, ITEM_SIZE*4, text="用户名: {}".format(CURRENT_USER_NAME))
        # # self.user_info.create_text(ITEM_SIZE*4, ITEM_SIZE*4, text="密码: {}".format(CURRENT_USER_PASS))
        # self.user_info.create_rectangle(ITEM_SIZE*12, ITEM_SIZE*2.5, ITEM_SIZE*16, ITEM_SIZE*5.5, outline='Black', fill="gray")
        # self.user_info.create_text(ITEM_SIZE*14, ITEM_SIZE*4, text="  登出  ", fill="Black")
        # CURRENT_USER_LOGOUT_POS = ITEM_SIZE*12, ITEM_SIZE*2.5, ITEM_SIZE*16, ITEM_SIZE*5.5
        # self.user_info.create_rectangle(ITEM_SIZE*0, ITEM_SIZE*2, ITEM_SIZE*18, ITEM_SIZE*6, outline='Black')
        # # 绑定用户登出事件
        # self.user_info.bind(sequence='<Button-1>', func=self.user_clicked)
        # self.user_info.grid(row=0, column=0)
        self.user_info = UserInfo(master=self.windows)
        self.user_info.pack(fill=tkinter.X, padx=3)
        # 添加窗口1
        self.window1 = SmallWindow(master=self.windows, width=ITEM_SIZE, height=ITEM_SIZE, match_degree=None,
                                   button_text="查询", game=self, button_two="清除", button_three="确认", col_num=COL_N)
        self.window1.pack(fill=tkinter.X, padx=3)

        # 分割线
        # self.separator = Separator(master=self.windows, orient=tkinter.HORIZONTAL, style='Red.TSeparator')
        # self.separator.pack(fill=tkinter.X, pady=5, padx=3)
        self.sperator = tkinter.Canvas(master=self.windows, height=2, bg=SEPARATOR_COLOR)
        self.sperator.pack(fill=tkinter.X, pady=0)
        # self.sperator.create_line(0, 0, 0, 100, fill='Red')

        # 添加窗口2
        self.windows2_1 = SmallWindow(master=self.windows, width=ITEM_SIZE, height=ITEM_SIZE, col_num=COL_N, button_two="清除")
        self.windows2_1.pack(fill=tkinter.X, padx=3)
        self.windows2_2 = SmallWindow(master=self.windows, width=ITEM_SIZE, height=ITEM_SIZE, col_num=COL_N, button_two="清除")
        self.windows2_2.pack(fill=tkinter.X, padx=3)
        self.windows2_3 = SmallWindow(master=self.windows, width=ITEM_SIZE, height=ITEM_SIZE, col_num=COL_N, button_two="清除")
        self.windows2_3.pack(fill=tkinter.X, padx=3)
        self.windows2_4 = SmallWindow(master=self.windows, width=ITEM_SIZE, height=ITEM_SIZE, col_num=COL_N, button_two="清除")
        self.windows2_4.pack(fill=tkinter.X, padx=3)
        self.windows2_5 = SmallWindow(master=self.windows, width=ITEM_SIZE, height=ITEM_SIZE, col_num=COL_N, button_two="清除")
        self.windows2_5.pack(fill=tkinter.X, padx=3)
        self.windows2_6 = SmallWindow(master=self.windows, width=ITEM_SIZE, height=ITEM_SIZE, col_num=COL_N, button_two="清除")
        self.windows2_6.pack(fill=tkinter.X, padx=3)

    def user_clicked(self, event):
        """
        用户点击用户信息
        :return:
        """
        global CURRENT_USER_LOGOUT_POS
        x1, y1, x2, y2 = CURRENT_USER_LOGOUT_POS
        print("用户点击用户信息:{},{}".format(event.x, event.y))
        if event.x >= x1 and event.x <= x2 and event.y >= y1 and event.y <= y2:
            print("用户点击登出...")
            self.windows.destroy()
            self.home.back_home()

    def show_match_info(self, top_match_info):
        """
        先清空窗口2之前的所有数据 然后窗口2绘制匹配度最高的展示结果
        :param top_match_info:
        :return:
        """
        not_show_windows = {self.windows2_1, self.windows2_2, self.windows2_3, self.windows2_4, self.windows2_5, self.windows2_6}
        for window in not_show_windows:
            window.my_grid.recovery_grid()
        for match_degree, blue_pos, red_pos in top_match_info.values():
            not_show_windows.pop().my_grid.draw_circle(match_degree, blue_pos, red_pos)


class UserInfo(tkinter.Frame):
    """
    用户信息
    """
    def __init__(self, master=None):
        super().__init__(master=master, bg=BASE_COLOR)
        self.label_name = tkinter.Label(master=self, text="用户名:", bg=BASE_COLOR)
        self.label_name.pack(side=tkinter.LEFT)
        self.text_name = tkinter.Entry(master=self)
        self.text_name.pack(side=tkinter.LEFT)
        self.label_pass = tkinter.Label(master=self, text="密码:", bg=BASE_COLOR)
        self.label_pass.pack(side=tkinter.LEFT)
        self.text_pass = tkinter.Entry(master=self, show="*")
        self.text_pass.pack(side=tkinter.LEFT)
        self.button_login = tkinter.Button(master=self, text="登录", command=self.login, width=10, bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR)
        self.button_login.pack(side=tkinter.LEFT, padx=20)
        self.button_register = tkinter.Button(master=self, text="注册", command=self.register, width=10, bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR)
        self.button_register.pack(side=tkinter.LEFT)

    def register(self):
        """
        用户注册
        :return:
        """
        username = str(self.text_name.get()).strip()
        password = str(self.text_pass.get()).strip()
        if username == '' or password == '':
            messagebox.showerror('注册失败！', '用户名或密码为空，请重新输入!')
            return
        res = db.is_user_exist(username=username)
        if not res:
            res2 = db.save_user(username, password)
            if res2:
                messagebox.showinfo('注册成功！', '恭喜您，注册成功!')
            else:
                # messagebox.showerror('注册失败！', '数据库状态异常!')
                messagebox.showerror('注册失败！', '用户名已存在，请重新输入!')
        else:
            messagebox.showerror('注册失败！', '用户名已存在，请重新输入!')

    def logout(self):
        """
        用户登出
        :return:
        """
        global CURRENT_USER_ID, CURRENT_USER_NAME, CURRENT_USER_PASS, USER_IS_LOGIN
        CURRENT_USER_ID = None
        CURRENT_USER_NAME = None
        CURRENT_USER_PASS = None
        USER_IS_LOGIN = False
        self.button_logout.destroy()
        self.label_pass = tkinter.Label(master=self, text="密码:", bg=BASE_COLOR)
        self.label_pass.pack(side=tkinter.LEFT)
        self.text_pass = tkinter.Entry(master=self, show="*")
        self.text_pass.pack(side=tkinter.LEFT)
        self.button_login = tkinter.Button(master=self, text="登录", command=self.login, bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR)
        self.button_login.pack(side=tkinter.LEFT, padx=20)
        self.button_register = tkinter.Button(master=self, text="注册", command=self.register, bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR)
        self.button_register.pack(side=tkinter.LEFT)

    def login(self):
        """
        用户登录
        :return:
        """
        global CURRENT_USER_ID, CURRENT_USER_NAME, CURRENT_USER_PASS, USER_IS_LOGIN
        username = str(self.text_name.get()).strip()
        password = str(self.text_pass.get()).strip()
        if username == '' or password == '':
            messagebox.showerror('登录失败！', '用户名或密码为空，请重新输入!')
            return
        user = db.is_login_success(username, password)
        if user:
            print("登录成功...{}".format(user))
            # 更新用户信息
            CURRENT_USER_ID, CURRENT_USER_NAME, CURRENT_USER_PASS = user
            # 进入游戏
            USER_IS_LOGIN = True
            self.text_pass.destroy()
            self.label_pass.destroy()
            self.button_register.destroy()
            self.button_login.destroy()
            self.button_logout = tkinter.Button(master=self, text="登出", command=self.logout, bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR)
            self.button_logout.pack(side=tkinter.LEFT, padx=40)
        else:
            messagebox.showerror('登录失败！', '用户名或密码错误，请重新输入!')


class MyGrid(tkinter.Canvas):
    """
    表格
    """
    def __init__(self, master=None, width=50, height=50, col_num=20, row_num=6, match_degree=None):
        # 供方法使用的属性
        self.width = width
        self.height = height
        self.col_num = col_num
        self.row_num = row_num
        self.mouse_move_flag = None
        self.mouse_move_start_pos = None
        self.is_checked = False
        self.checked_pos = None

        self.pos = []
        # 红圈坐标
        self.red_circle = set()
        # 蓝圈坐标
        self.blue_circle = set()
        super().__init__(master=master, width=width*(col_num+1), height=height*(row_num+1), bg=BASE_COLOR)
        # 取消边框
        self.configure(highlightthickness=0)
        for x in range(col_num):
            for y in range(row_num):
                self.pos.append(((x+0.5)*width, (y+0.5)*height, (x + 1.5)*width, (y + 1.5)*width, x, y))
                self.create_rectangle((x+0.5)*width, (y+0.5)*height, (x + 1.5)*width, (y + 1.5)*width, fill=CANVAS_COLOR)
        if match_degree:
            global ITEM_SIZE
            # 展示匹配度
            self.create_text(width*(col_num-0.5), height*(row_num-0.5), text=str(match_degree)+"%", fill='Red', font="Helvetic {} bold".format(ITEM_SIZE), tag='text')
        # 绑定表格鼠标点击事件
        self.bind(sequence='<Button-1>', func=self.left_clicked)
        self.bind(sequence='<Double-Button-1>', func=self.left_double_clicked)
        self.bind(sequence='<Button-3>', func=self.right_clicked)
        self.bind(sequence='<Key>', func=self.key_clicked)
        # self.bind(sequence='<BackSpace>', func=self.del_clicked)
        # 绑定鼠标拖动事件
        self.bind(sequence='<B1-Motion>', func=self.left_move_start)
        self.bind(sequence='<ButtonRelease-1>', func=self.left_move_end)

    def get_pos_by_xy(self, x, y):
        """
        根据鼠标点击的xy坐标计算点击的表格坐标
        :param x:
        :param y:
        :return:
        """
        for x1, y1, x2, y2, x_num, y_num in self.pos:
            if x1<x and y1<y and x2>x and y2>y:
                return x1, y1, x2, y2, x_num, y_num

    def get_pos_by_xy_num(self, x_num, y_num):
        """
        根据表格的行和列计算表格的坐标
        :param x_num:
        :param y_num:
        :return:
        """
        return (x_num + 0.5) * self.width, (y_num + 0.5) * self.height, (x_num + 1.5) * self.width, (y_num + 1.5) * self.width

    def key_clicked(self, event):
        """
        键盘被点击 ==> del删除选中的圆圈
        :return:
        """
        global USER_IS_LOGIN
        if USER_IS_LOGIN:
            if str(event.char).strip() == "":
                print("del")
                if self.is_checked:
                    # 删除红框 如果存在圆圈则移除圆圈
                    for x_num, y_num in self.red_circle.copy():
                        if self.checked_pos == self.get_pos_by_xy_num(x_num=x_num, y_num=y_num):
                            print("选中是红圈...")
                            print("删除前:{}".format(self.red_circle))
                            self.red_circle.remove((x_num, y_num))
                            self.create_rectangle(self.checked_pos, fill='White')
                            print("删除后:{}".format(self.red_circle))
                    for x_num, y_num in self.blue_circle.copy():
                        if self.checked_pos == self.get_pos_by_xy_num(x_num=x_num, y_num=y_num):
                            print("选中是蓝圈...")
                            print("删除前:{}".format(self.blue_circle))
                            self.blue_circle.remove((x_num, y_num))
                            self.create_rectangle(self.checked_pos, fill='White')
                            print("删除后:{}".format(self.blue_circle))
                    self.is_checked = False
                    self.checked_pos = None
                    self.delete('red_box')
            else:
                print(event.char)

    def right_clicked(self, event):
        """
        鼠标右键被点击 ==> 给选中的位置加红框
        :return:
        """
        global USER_IS_LOGIN
        if USER_IS_LOGIN:
            print("鼠标右键点击:{}", self.get_pos_by_xy(event.x, event.y))
            if not self.is_checked:
                self.is_checked = True
                self.create_rectangle(self.get_pos_by_xy(event.x, event.y)[0:4], outline='Red', tag='red_box')
                self.checked_pos = self.get_pos_by_xy(event.x, event.y)[0:4]
                self.focus_set()
            elif self.checked_pos != self.get_pos_by_xy(event.x, event.y)[0:4]:
                self.checked_pos = self.get_pos_by_xy(event.x, event.y)[0:4]
                self.delete('red_box')
                self.create_rectangle(self.get_pos_by_xy(event.x, event.y)[0:4], outline='Red', tag='red_box')
            else:
                self.is_checked = False
                self.checked_pos = None
                self.delete('red_box')
                # self.focus_displayof()

    def left_move_start(self, event):
        """
        鼠标左键开始拖动 ==> 复制圆圈到别的位置
        :return:
        """
        global USER_IS_LOGIN
        if USER_IS_LOGIN:
            if not self.mouse_move_flag:
                self.mouse_move_flag = True
                self.mouse_move_start_pos = self.get_pos_by_xy(event.x, event.y)
                print("鼠标拖动开始位置:{}".format(self.mouse_move_start_pos))

    def left_move_end(self, event):
        """
        鼠标左键拖动停止 ==> 复制圆圈到别的位置
        :return:
        """
        global USER_IS_LOGIN
        if USER_IS_LOGIN:
            print("鼠标拖动结束位置：{}".format(self.get_pos_by_xy(event.x, event.y)))
            if (self.get_pos_by_xy(event.x, event.y) == self.mouse_move_start_pos) or not self.get_pos_by_xy(event.x, event.y) or not self.mouse_move_start_pos:
                print("return ==== ")
                return
            # 判断鼠标拖动开始位置是否有圆圈
            for x, y in self.red_circle:
                print(self.get_pos_by_xy_num(x, y))
                if self.mouse_move_start_pos[0:4] == self.get_pos_by_xy_num(x, y):
                    print("复制红圈:{}".format(self.get_pos_by_xy(event.x, event.y)))
                    x1, y1, x2, y2 = self.get_pos_by_xy(event.x, event.y)[0:4]
                    x1 = x1 + (x2 - x1) / 4
                    y1 = y1 + (y2 - y1) / 4
                    x2 = x2 - (x2 - x1) / 4
                    y2 = y2 - (y2 - y1) / 4
                    self.create_oval(x1, y1, x2, y2, fill=RED_CIRCLE_COLOR, tag="red_circle", width=1)
            for x, y in self.blue_circle:
                print(self.get_pos_by_xy_num(x, y))
                if self.mouse_move_start_pos[0:4] == self.get_pos_by_xy_num(x, y):
                    print("复制蓝圈:{}".format(self.get_pos_by_xy(event.x, event.y)))
                    x1, y1, x2, y2 = self.get_pos_by_xy(event.x, event.y)[0:4]
                    x1 = x1 + (x2 - x1) / 4
                    y1 = y1 + (y2 - y1) / 4
                    x2 = x2 - (x2 - x1) / 4
                    y2 = y2 - (y2 - y1) / 4
                    self.create_oval(x1, y1, x2, y2, fill=BLUE_CIRCLE_COLOR, tag="blue_circle", width=1)
            self.mouse_move_flag = False
            self.mouse_move_start_pos = None

    def left_clicked(self, event):
        """
        鼠标左键点击表格
        :return:
        """
        global USER_IS_LOGIN
        if USER_IS_LOGIN:
            print("鼠标单击位置:{},{}".format(event.x, event.y))
            x1, y1, x2, y2, x, y = self.get_pos_by_xy(event.x, event.y)
            if (x, y) in self.blue_circle:
                self.blue_circle.remove((x, y))
            if (x, y) in self.red_circle:
                self.red_circle.remove((x, y))
            # 记录画蓝色圆圈的坐标
            self.blue_circle.add((x, y))
            # 格子画蓝色圆圈
            x1 = x1 + (x2-x1)/4
            y1 = y1 + (y2-y1)/4
            x2 = x2 - (x2-x1)/4
            y2 = y2 - (y2-y1)/4
            self.create_oval(x1, y1, x2, y2, fill=BLUE_CIRCLE_COLOR, tag="blue_circle", width=1)

    def left_double_clicked(self, event):
        """
        鼠标左键双击表格 ==> 会先触发单击 然后触发双击
        :return:
        """
        global USER_IS_LOGIN
        if USER_IS_LOGIN:
            print("鼠标双击位置:{},{}".format(event.x, event.y))
            x1, y1, x2, y2, x, y = self.get_pos_by_xy(event.x, event.y)
            if (x, y) in self.blue_circle:
                self.blue_circle.remove((x, y))
            if (x, y) in self.red_circle:
                self.red_circle.remove((x, y))
            # 记录画红色圆圈的坐标
            self.red_circle.add((x, y))
            # 格子画红色圆圈
            x1 = x1 + (x2-x1)/4
            y1 = y1 + (y2-y1)/4
            x2 = x2 - (x2-x1)/4
            y2 = y2 - (y2-y1)/4
            self.create_oval(x1, y1, x2, y2, fill=RED_CIRCLE_COLOR, tag="red_circle", width=1)

    def recovery_grid(self):
        """
        恢复表格 ==> 删除绘制的红色和蓝色圆圈 匹配度 删除对应的set
        :return:
        """
        global USER_IS_LOGIN
        if USER_IS_LOGIN:
            self.delete("red_circle")
            self.delete("blue_circle")
            self.delete("text")
            self.red_circle.clear()
            self.blue_circle.clear()

    def draw_circle(self, match_degree, blue_pos, red_pos):
        """
        根据给定的红蓝圈位置画图
        :return:
        """
        global USER_IS_LOGIN
        if USER_IS_LOGIN:
            # 绘制匹配度
            global ITEM_SIZE
            self.create_text(self.width * (self.col_num - 0.5), self.height * (self.row_num - 0.5), text=str(match_degree)+"%", fill='Red',
                             font="Helvetic {} bold".format(ITEM_SIZE), tag='text')
            # 绘制红蓝圈
            for x, y in blue_pos:
                x1, y1, x2, y2 = self.get_pos_by_xy_num(x, y)
                x1 = x1 + (x2 - x1) / 4
                y1 = y1 + (y2 - y1) / 4
                x2 = x2 - (x2 - x1) / 4
                y2 = y2 - (y2 - y1) / 4
                self.create_oval(x1, y1, x2, y2, fill=BLUE_CIRCLE_COLOR, tag="blue_circle", width=1)
            for x, y in red_pos:
                x1, y1, x2, y2 = self.get_pos_by_xy_num(x, y)
                x1 = x1 + (x2 - x1) / 4
                y1 = y1 + (y2 - y1) / 4
                x2 = x2 - (x2 - x1) / 4
                y2 = y2 - (y2 - y1) / 4
                self.create_oval(x1, y1, x2, y2, fill=RED_CIRCLE_COLOR, tag="red_circle", width=1)
            # 将红蓝圈保存到set
            for item in blue_pos:
                self.blue_circle.add(tuple(item))
            for item in red_pos:
                self.red_circle.add(tuple(item))


class SmallWindow(tkinter.Frame):
    """
    小窗口 ： 表格 + 右边的红蓝圆圈和按钮
    """
    def __init__(self, master=None, button_text="确认", width=50, height=50, col_num=20, row_num=6, match_degree=None, game=None, button_two=None, button_three=None):
        # 方法需要参数
        self.button_type = None
        if button_text == '确认':
            self.button_type = 1
        elif button_text == '查询':
            self.button_type = 2
        elif button_text == '清除':
            self.button_type = 3
        self.width = width
        self.height = height
        self.col_num = col_num
        self.row_num = row_num
        self.match_degree = match_degree
        self.game = game

        super().__init__(master=master, bg=BASE_COLOR)
        # 创建表格
        self.my_grid = MyGrid(master=self, width=width, height=height, col_num=col_num, row_num=row_num, match_degree=match_degree)
        self.my_grid.pack(side=tkinter.LEFT)
        # # 创建两个圆圈的画布
        # self.circle = tkinter.Canvas(master=self, width=width*3, height=height*3, bg=BASE_COLOR)
        # # self.circle = tkinter.Canvas(master=self, bg=BASE_COLOR)
        # self.circle.configure(highlightthickness=0)
        # # 画圆
        # self.circle.create_oval(width*1, height*0.5, width*2, height*1.5, fill='aqua')
        # self.circle.create_oval(width*1, height*1.8, width*2, height*2.8, fill='deeppink')
        # self.circle.pack()
        # 创建按钮
        if button_three:
            self.button = tkinter.Button(master=self, text=button_text, command=self.button_clicked, height=1, bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR)
            self.button.pack(pady=2)
            self.button2 = tkinter.Button(master=self, text=button_two, command=self.button_clicked_clear, height=1, bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR)
            self.button2.pack(pady=2)
            self.button3 = tkinter.Button(master=self, text=button_three, command=self.button_clicked_save, height=1, bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR)
            self.button3.pack(pady=2)
        else:
            self.button = tkinter.Button(master=self, text=button_text, command=self.button_clicked_save, height=1, bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR)
            self.button.pack(pady=10)
            self.button2 = tkinter.Button(master=self, text=button_two, command=self.button_clicked_clear, height=1, bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR)
            self.button2.pack(pady=3)

    def button_clicked_clear(self):
        global USER_IS_LOGIN
        if USER_IS_LOGIN:
            self.my_grid.recovery_grid()

    def button_clicked_save(self):
        global USER_IS_LOGIN
        if USER_IS_LOGIN:
            # 确认按钮
            if len(self.my_grid.blue_circle) == 0 and len(self.my_grid.red_circle) == 0:
                messagebox.showerror(title='保存错误!', message='请在窗口中输入内容再进行保存!')
                return
            if (len(self.my_grid.blue_circle) + len(self.my_grid.red_circle)) < 25:
                messagebox.showerror(title='保存错误!', message='窗口中的圆圈数量不足25，无法保存!')
                return

            # 排序blue_pos和red_pos
            self.my_grid.blue_circle = list(self.my_grid.blue_circle)
            self.my_grid.red_circle = list(self.my_grid.red_circle)
            self.my_grid.blue_circle.sort()
            self.my_grid.red_circle.sort()

            res = db.save_record(json.dumps(tuple(self.my_grid.blue_circle)), json.dumps(tuple(self.my_grid.red_circle)))
            print(res)
            if res:
                messagebox.showinfo('保存成功!', '记录存储成功!')
            else:
                messagebox.showinfo('保存失败!', '记录存储失败,存在相同的记录!')
            self.my_grid.recovery_grid()

    def button_clicked(self):
        """
        按钮点击事件  ==>  查询按钮则根据数据库查询并展示在窗口2  确认按钮则将数据存储到数据库并刷新表格
        :return:
        """
        global USER_IS_LOGIN
        if USER_IS_LOGIN:
            print(self.button_type)
            if self.button_type == 2:
                # 如果窗口1未绘制任何圆圈 抛出异常
                if len(self.my_grid.blue_circle) == 0 and len(self.my_grid.red_circle) == 0:
                    messagebox.showerror(title='查询错误!', message='请在窗口1中输入内容再进行查询!')
                    return
                # 查询按钮
                records = db.query_all_records()
                # 计算匹配度并排序前6个展示
                top_record = {}
                min_match_degree = 100
                circle_sum = len(self.my_grid.red_circle) + len(self.my_grid.blue_circle)
                for record_id, blue_pos_str, red_pos_str in records:
                    blue_pos = json.loads(blue_pos_str)
                    red_pos = json.loads(red_pos_str)
                    same_num = 0
                    for red_circle in self.my_grid.red_circle:
                        if list(red_circle) in red_pos:
                            same_num = same_num + 1
                    for blue_circle in self.my_grid.blue_circle:
                        if list(blue_circle) in blue_pos:
                            same_num = same_num + 1
                    match_degree = int(str(same_num/circle_sum*100).split(".")[0])
                    if len(top_record) < 6:
                        # 要展示的小于6个
                        top_record[record_id] = (match_degree, blue_pos, red_pos)
                        min_match_degree = min(min_match_degree, match_degree)
                    elif match_degree > min_match_degree:
                        # 当前的匹配度高于top_record中的 删除当前最小的 然后将新的加进去
                        deleted_id = None
                        new_match_degree = [match_degree]
                        for record_id_t, (match_degree_t, blue_pos_t, red_pos_t) in top_record.items():
                            if match_degree_t == min_match_degree:
                                deleted_id = record_id_t
                            new_match_degree.append(match_degree_t)
                        top_record.pop(deleted_id)
                        new_match_degree.remove(min_match_degree)
                        top_record[record_id] = (match_degree, blue_pos, red_pos)
                        min_match_degree = min(new_match_degree)
                # 绘制窗口2的表格 展示数据
                for item in top_record.items():
                    print(item)
                self.game.show_match_info(top_record)
            elif self.button_type == 1:
                # 确认按钮
                if len(self.my_grid.blue_circle) == 0 and len(self.my_grid.red_circle) == 0:
                    messagebox.showerror(title='保存错误!', message='请在窗口中输入内容再进行保存!')
                    return
                if (len(self.my_grid.blue_circle) + len(self.my_grid.red_circle)) < 25:
                    messagebox.showerror(title='保存错误!', message='窗口中的圆圈数量不足25，无法保存!')
                    return
                if db.save_record(json.dumps(tuple(self.my_grid.blue_circle)), json.dumps(tuple(self.my_grid.red_circle))):
                    messagebox.showinfo('保存成功!', '记录存储成功!')
                else:
                    messagebox.showinfo('保存失败!', '记录存储失败,存在相同的记录!')
                self.my_grid.recovery_grid()
            elif self.button_type == 3:
                self.my_grid.recovery_grid()


if __name__ == '__main__':
    db = DBOperator()
    chess_game = ChessGame()
    # Home()
    # 创建主窗口
    # windows = tkinter.Tk()
    # # 设置窗口信息
    # windows.title("Demo")
    # # windows.geometry(800, 600)
    # windows.resizable(True, True)
    # windows.configure(bg="white")
    #
    # # 添加组件
    # user = UserInfo(master=windows)
    # user.pack()
    # # 开启事件循环
    # windows.mainloop()