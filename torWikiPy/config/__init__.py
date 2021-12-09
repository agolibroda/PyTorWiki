#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2015 Alec Golibroda
#



""" Config."""

# from __future__ import absolute_import, division, print_function, with_statement

from tornado.options import define, options, parse_config_file 

import os
import os.path
import logging
dirModule = os.path.dirname(__file__)
nameModule = __file__
logger = logging.getLogger(nameModule)
logger.setLevel(logging.DEBUG)

# # create console handler and set level to debug
# ch = logging.StreamHandler()
# ch.setLevel(logging.INFO)
# # formatter = logging.Formatter('%(clientip)s - %(name)s - %(levelname)s: %(message)s')
# formatter = logging.Formatter('%(name)s - %(levelname)s: %(message)s')
# ch.setFormatter(formatter)
# # add ch to logger
# logger.addHandler(ch)
# # logger.info(dirModule)


define("logFileName", default = os.path.join(os.path.dirname(__file__) + '/../../log/torWikiPy_211203.log'), help="log File Name")
define("formatter", default = '%(name)s - %(levelname)s : %(message)s', help="log Formater")
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')

# define("logFileName", default =  'torWikiPy_211203.log'), help="log File Name")
# define("logLevel", default= 'logging.INFO', help="Log Level")
# define("logLevel", default= 'logging.DEBUG', help="Log Level")
# define("logLevel", default= 'logging.ERROR', help="Log Level")


# define("log_to_stderr", type=bool, default=None,
#                 help=("Send log output to stderr (colorized if possible). "
#                         "By default use stderr if --log_file_prefix is not set and "
#                         "no other logging is configured."))
# define("log_file_prefix", type=str, default=None, metavar="PATH",
#                 help=("Path prefix for log files. "
#                         "Note that if you are running multiple tornado processes, "
#                         "log_file_prefix must be different for each of them (e.g. "
#                         "include the port number)"))
# define("log_file_max_size", type=int, default=100 * 1000 * 1000,
#                 help="max size of log files before rollover")
# define("log_file_num_backups", type=int, default=10,
#                 help="number of log files to keep")

# define("log_rotate_when", type=str, default='midnight',
#                 help=("specify the type of TimedRotatingFileHandler interval "
#                         "other options:('S', 'M', 'H', 'D', 'W0'-'W6')"))
# define("log_rotate_interval", type=int, default=1,
#                 help="The interval value of timed rotating")

# define("log_rotate_mode", type=str, default='size',
#                 help="The mode of rotating files(time or size)")

# add_parse_callback(lambda: enable_pretty_logging(options))

#########################################################
 
# define("logging", default= 'info', help="Logging Level")
#--logging=debug|info|warning|error|none

define("Project_Name", default= 'pyTorWiki', help="Project name")
define("DomenName", default= 'pyTorWiki.org', help="Domen Name")

define("Project_Description", default= 'Вики система, реализованная на языке Python & FW Tornado', help="Project Description")
define("Project_Keywords", default= 'Вики система, язык Python, FW Tornado', help="Project_Keywords")

define("Project_Start_Data", default= '2016', help="Project Start Data")

define("wikiTitleAdmin", default= 'pyTorWiki Admin layer', help="TorWiki Admin layer")

define("sidName", default= 'wiki_author', help="wiki author")

define("main_port", default="8888", help="Main port 8888")
define("main_addr", default='127.0.0.1', help="Main addr 127.0.0.1")


define("main_title", default="Main WIKI Title", help="Main Wiki Title ")


# define("uploud_path", default="static/filestorage/", help="Path to upload")
# define("to_out_path", default="filestorage/", help="Path to upload")

# define("adminPath", default=r"/admin", help="Path to Admin Area")
# define("adminTplPath", default=r"admin/", help="Path to Admin Area")

define("projectDir", default=os.path.join(os.path.dirname(__file__), '../../'), help="Path to Project (vedogon.local) ")

# define("staticDir", default=r"static", help="Static Dir")

define("mediaDir", default=os.path.join(options.projectDir, 'torWikiMedia'), help="Static Dir")

# define("siteDir", default=r"site_templates", help="Catalog for site files")
 

# define("templateDir", default=r"templates", help="Template Dir")
# define("tmpTplPath", default=r"tmp", help="Path to user`s Template Area")

# define("tplExtension", default=r"html", help="Template file Extension")

# define("list_categofy_id", default=1, help="Information Page Category")

# define("info_page_categofy_id", default=3, help="Information Page Category")
# define("tpl_categofy_id", default=4, help="Template Page Category")

# define("main_info_template", default=5, help="Main tmplate of inforation page")
# define("main_page_id", default=6, help="Id of Main User Page")

define("salt", default= 'super_Salt', help="Main salt")

define("cookieName", default= 'pyTorWikiCookie', help="Main cookie name")
define("cookieSecret", default= 'cookieSecretBy_pyTorWiki', help="Main cookie secret")

define("sessionLifetime", default= 1800, help="Session Lifetime")
define("sessionLongLifetime", default= 3600*24*365, help="Session Lifetime")


########################################################################
define("postgreHost",   default="localhost",        help="postgreHost")
define("postgrePort",   default="5432",             help="postgrePort")

define("postgreBase",   default="baseName",         help="postgreBase")

define("postgreUser",   default="baseUser",         help="postgreUser")
define("postgrePwd",    default="passwordUser",     help="postgrePwd")
########################################################################

########################################################################
define("redis_host",             default="localhost",    help="redisHost")
define("redis_port",             default="6379",         help="redisPort")
define("redis_db",               default="1",            help="redisDb")
define("redis_default_db",       default="1",            help="redisredis_default_dbDb")
define("redis_session_db",       default="1",            help="redisDb")
define("redisMaxConnections",    default="1024",         help="redisMaxConnections")
########################################################################


options.parse_config_file(os.path.join( os.path.dirname(__file__), "dbase.conf"))

options.parse_config_file(os.path.join( os.path.dirname(__file__), "redis.conf"))

options.parse_config_file(os.path.join( os.path.dirname(__file__), "main.conf"))



