# -*- coding: utf-8 -*-
import os
import shutil
import locale


class Path(object):
    u"""
    定义资源,生成的文件等的路径,以及关于路径操作的一些函数
    不能在开头from src.tools.debug import Debug
    """
    cwd_path = unicode(os.getcwd())    # 执行命令的路径
    in_base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))  # 项目路径

    config_path = u''     # 根据recipe_kind确定config_path
    db_path = u''         # 根据recipe_kind确定
    sql_path = u''        # 新建数据库的脚本路径
    image_pool_path = u''
    html_pool_path = u''
    result_path = u''
    www_css = u''

    read_list_path = cwd_path + '/ReadList.txt'

    @staticmethod
    def reset_path():
        Path.chdir(Path.cwd_path)
        return

    @staticmethod
    def pwd():
        u"""
        输出绝对路径
        :return:
        """
        print os.path.realpath('.')
        return

    @staticmethod
    def get_pwd():
        u"""
        :return: 绝对路径
        """
        path = unicode(os.path.abspath('.').decode(locale.getpreferredencoding()))
        return path

    @staticmethod
    def mkdir(path):
        try:
            os.mkdir(path)
        except OSError:
            from src.tools.debug import Debug
            Debug.logger.debug(u'directory ' + str(path) + str(u' already exists'))
            pass
        return

    @staticmethod
    def chdir(path):
        u"""
        换路径,如果路径不存在就新建一个
        :param path:
        :return:
        """
        try:
            os.chdir(path)
        except OSError:
            from src.tools.debug import Debug
            Debug.logger.debug(u'path does not exist，creating it....')
            Path.mkdir(path)
            os.chdir(path)
        return

    @staticmethod
    def rmdir(path):
        u"""
        删除整个目录,忽略错误
        :param path:
        :return:
        """
        if path:
            shutil.rmtree(path, ignore_errors=True)
        return

    @staticmethod
    def copy(src, dst):
        if not os.path.exists(src):
            from src.tools.debug import Debug
            Debug.logger.debug('{}does not exist，skip it'.format(src))
            return
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy(src=src, dst=dst)
        return

    @staticmethod
    def get_filename(src):
        return os.path.basename(src)

    @staticmethod
    def init_base_path(recipe_kind):
        u"""
        初始化路径,不需要实例化 Path 就能执行
        :return:
        """
        Path.cwd_path = Path.get_pwd()    # TODO 删掉Path这个函数

        Path.www_css = Path.in_base_path + str(u'/www/css')
        Path.www_image = Path.in_base_path + str(u'/www/images')

        if recipe_kind == 'jianshu':    # TODO: 用循环解决
            Path.config_path = Path.in_base_path + str(u'/config/jianshu_config.json')
            Path.sql_path = Path.in_base_path + str(u'/db/jianshu.sql')
            Path.db_path = Path.cwd_path + str(u'/db/jianshu_db_002.sqlite')
        elif recipe_kind == 'zhihu':
            Path.config_path = Path.in_base_path + str(u'/config/zhihu_config.json')
            Path.sql_path = Path.in_base_path + str(u'/db/zhihuhelp.sql')
            Path.db_path = Path.cwd_path + str(u'/db/zhihuDB_173.sqlite')
        elif recipe_kind == 'sinablog':
            Path.config_path = Path.in_base_path + str(u'/config/sinablog_config.json')
            Path.sql_path = Path.in_base_path + str(u'/db/sinablog.sql')
            Path.db_path = Path.cwd_path + str(u'/db/sinablog_db_001.sqlite')
        elif recipe_kind == 'csdnblog':
            Path.config_path = Path.in_base_path + str(u'/config/csdn_config.json')
            Path.sql_path = Path.in_base_path + str(u'/db/csdnblog.sql')
            Path.db_path = Path.cwd_path + str(u'/db/csdn_db_001.sqlite')

        Path.html_pool_path = Path.cwd_path + str(u'/e-books_tmp_source/html')
        Path.image_pool_path = Path.cwd_path + str(u'/e-books_tmp_source/picture')
        Path.result_path = Path.cwd_path + str(u'/e-books_produced')
        return

    @staticmethod
    def init_work_directory():
        Path.reset_path()
        Path.mkdir(u'./db')
        Path.mkdir(u'./e-books_tmp_source')
        Path.mkdir(u'./e-books_produced')
        Path.chdir(u'./e-books_tmp_source')
        Path.mkdir(u'./html')
        Path.mkdir(u'./picture')
        Path.reset_path()
        return

    @staticmethod
    def is_file(path):
        return os.path.isfile(path)


