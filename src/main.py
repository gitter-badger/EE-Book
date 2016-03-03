# -*- coding: utf-8 -*-
import sqlite3

from src import guide
from src.book import Book
from src.tools.config import Config
from src.tools.debug import Debug
from src.tools.http import Http
from src.tools.path import Path
from src.tools.db import DB
from login import Login
from read_list_parser import ReadListParser
from src.worker import worker_factory
from src.tools.type import Type


class EEBook(object):
    def __init__(self):
        u"""
        配置文件使用$符区隔，同一行内的配置文件归并至一本电子书内
        """
        Path.init_base_path()
        Path.init_work_directory()
        self.init_database()
        Config._load()
        return

    @staticmethod
    def init_config():
        login = Login()
        if Config.remember_account:
            print u'检测到有设置文件，是否直接使用之前的设置？(帐号、密码、图片质量)'
            print u'按回车使用之前设置，敲入任意字符后点按回车进行重新设置'
            # if raw_input():
            login.start()
            # Config.picture_quality = guide.set_picture_quality()
            Config.picture_quality = 1
            # else:
            #     Http.set_cookie()
        else:
            login.start()
            # Config.picture_quality = guide.set_picture_quality()
            Config.picture_quality = 1

        # 储存设置
        Config._save()
        return

    def begin(self):
        if Config.debug is not True:         # 不是debug的时候才检查更新
            print "Config debug?"
            print Config.debug
            self.check_update()
        else:
            Debug.logger.info(u"#Debug模式#: 不检查更新")
        self.init_config()
        Debug.logger.info(u"开始读取ReadList.txt的内容????")
        print Path.pwd()     # TODO hard code
        with open('/Users/Frank/PycharmProjects/EE-Book/ReadList.txt', 'r') as read_list:
            print "WTF??"
            counter = 1
            print str(read_list)
            for line in read_list:
                print "line???" + str(line)
                line = line.replace(' ', '').replace('\r', '').replace('\n', '').replace('\t', '')  # 移除空白字符
                self.create_book(line, counter)  # 一行内容代表一本电子书
                counter += 1
        return

    @staticmethod
    def create_book(command, counter):
        Path.reset_path()

        Debug.logger.info(u"开始制作第 {} 本电子书".format(counter))
        Debug.logger.info(u"对记录 {} 进行分析".format(command))
        task_package = ReadListParser.get_task(command)  # 分析命令
        Debug.logger.info(u"#Debug:#task_package是:" + str(task_package))

        Debug.logger.info(u"task_package的book_list的长度为:" + str(len(task_package.book_list)))
        Debug.logger.info(u"task_package:" + str(task_package))
        Debug.logger.info(u"task_package.work_list:" + str(task_package.work_list))
        # Debug.logger.info(u"task_package.book_list.kind:" + str((task_package.book_list[Type.question][0]).kind))
        # Debug.logger.info(u"task_package.book_list.info:" + str((task_package.book_list[Type.question][0]).info))
        # Debug.logger.info(u"task_package.book_list.article_list:" + str((task_package.book_list[Type.question][0]).article_list))
        # Debug.logger.info(u"task_package.book_list.page_list:" + str((task_package.book_list[Type.question][0]).page_list))
        # Debug.logger.info(u"task_package.book_list.sql.question:" + str((task_package.book_list[Type.question][0]).sql.question))
        # Debug.logger.info(u"task_package.book_list.sql.answer:" + str((task_package.book_list[Type.question][0]).sql.answer))
        # Debug.logger.info(u"task_package.book_list.sql.info:" + str((task_package.book_list[Type.question][0]).sql.info))
        # Debug.logger.info(u"task_package.book_list.epub.article_count:" + str((task_package.book_list[Type.question][0]).epub.article_count))
        # Debug.logger.info(u"task_package.book_list.epub.answer_count:" + str((task_package.book_list[Type.question][0]).epub.answer_count))
        # Debug.logger.info(u"task_package.book_list.epub.agree_count:" + str((task_package.book_list[Type.question][0]).epub.agree_count))
        # Debug.logger.info(u"task_package.book_list.epub.title:" + str((task_package.book_list[Type.question][0]).epub.title))

        if not task_package.is_work_list_empty():

            # Debug.logger.debug(u"task_package.book_list.sql.info:" + str((task_package.book_list[Type.question])))  #.sql.info))
            # Debug.logger.debug(u"task_package.book_list.sql.article:" + str((task_package.book_list[Type.question][0]).sql.article))
            worker_factory(task_package.work_list)  # 执行抓取程序
            Debug.logger.info(u"网页信息抓取完毕")

        if not task_package.is_book_list_empty():
            Debug.logger.info(u"开始自数据库中生成电子书数据")
            # Debug.logger.info(u"task_package.book_list的类型为:" + str(type(task_package.book_list)))
            # Debug.logger.info(u"task_package.book_list的长度为:" + str(len(task_package.book_list)))
            # Debug.logger.info(u"task_package.book_list['question'][0].kind为:" + str((task_package.book_list['question'])[0].kind))
            # Debug.logger.info(u"task_package.book_list.sql.info:" + str((task_package.book_list['question'][0]).sql.info))
            # Debug.logger.info(u"task_package.book_list.sql.answer:" + str((task_package.book_list['question'][0]).sql.answer))
            # Debug.logger.info(u"task_package.book_list.sql.question:" + str((task_package.book_list['question'][0]).sql.question))
            # Debug.logger.info(u"task_package.book_list.sql.get_answer_sql:" + str((task_package.book_list['question'][0]).sql.get_answer_sql()))
            # Debug.logger.info(u"task_package.book_list.info:" + str((task_package.book_list['question'][0]).info))
            # Debug.logger.info(u"task_package.book_list.article_list:" + str((task_package.book_list['question'][0]).article_list))
            # Debug.logger.info(u"task_package.book_list.page_list:" + str((task_package.book_list['question'][0]).page_list))
            book = Book(task_package.book_list)
            book.create()
        return

    @staticmethod
    def init_database():
        if Path.is_file(Path.db_path):
            DB.set_conn(sqlite3.connect(Path.db_path))
        else:
            DB.set_conn(sqlite3.connect(Path.db_path))
            # 没有数据库就新建一个出来
            with open(Path.sql_path) as sql_script:
                DB.cursor.executescript(sql_script.read())
            DB.commit()

    @staticmethod
    def check_update():  # 强制更新
        u"""
            *   功能
                *   检测更新。
                *   若在服务器端检测到新版本，自动打开浏览器进入新版下载页面
                *   网页请求超时或者版本号正确都将自动跳过
            *   输入
                *   无
            *   返回
                *   无
        """
        print u"检查更新。。。"
        try:
            # example:
            # 2016-01-02
            # http://www.dwz.cn/helperupgrade
            content = Http.get_content(u"http://zhihuhelpbyyzy-zhihu.stor.sinaapp.com/ZhihuHelpUpdateTime.txt")
            if not content:
                raise Exception('HttpError')
        except:
            return
        time, url = [x.strip() for x in content.split('\n')]
        if time == Config.update_time:
            return
        else:
            print u"发现新版本，\n更新日期:{} ，点按回车进入更新页面".format(time)
            print u'新版本下载地址:' + url
            raw_input()
            import webbrowser
            webbrowser.open_new_tab(url)
        return
