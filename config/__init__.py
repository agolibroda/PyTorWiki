#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
#
# Copyright 2015 Alec Golibroda
#

""" Config."""

# from __future__ import absolute_import, division, print_function, with_statement


from tornado.options import define, options, parse_config_file
# options.logging = debug #None

define("logFileName", default= 'test.log', help="log File Name")
#
define("Project_Name", default= 'pyTorWiki', help="Project name")

define("wikiTitleAdmin", default= 'pyTorWiki Admin layer', help="TorWiki Admin layer")

define("sidName", default= 'wiki_author', help="wiki author")

define("salt", default= 'saltBy_pyTorWiki', help="Main salt")

define("cookieSecret", default= 'cookieSecretBy_pyTorWiki', help="Main cookie secret")

# Выбираем одну из стратегий работы с сессиями :-) 
# define("sessionsStrategy", default= 'memory', help="Session strategy")
# define("sessionsStrategy", default= 'file', help="Session strategy")
define("sessionsStrategy", default= 'redis', help="Session strategy")
define("sessionLifetime", default= 1800, help="Session Lifetime")


########################################################################
define("postgreHost", default="localhost", help="postgreHost")
define("postgrePort", default="5432", help="postgrePort")

define("postgreBase", default="baseName", help="postgreBase")

define("postgreUser", default="baseUser", help="postgreUser")
define("postgrePwd", default="passwordUser", help="postgrePwd")
########################################################################

define("main_port", default="8888", help="Main port 8888")
define("main_title", default="Main WIKI Title", help="Main Wiki Title ")


define("uploud_path", default="static/filestorage/", help="Path to upload")
define("to_out_path", default="filestorage/", help="Path to upload")

define("adminPath", default=r"/admin", help="Path to Admin Area")
define("adminTplPath", default=r"admin/", help="Path to Admin Area")

define("projectDir", default=r"", help="Path to Project")
define("staticDir", default=r"static", help="Static Dir")
define("templateDir", default=r"templates", help="Template Dir")

define("tmpTplPath", default=r"tmp", help="Path to user`s Template Area")
define("tplExtension", default=r".html", help="Template file Extension")

define("list_categofy_id", default=1, help="Information Page Category")

define("info_page_categofy_id", default=3, help="Information Page Category")
define("tpl_categofy_id", default=4, help="Template Page Category")

define("main_info_template", default=5, help="Main tmplate of inforation page")
define("main_page_id", default=6, help="Id of Main User Page")




# Эти параметры переопределим на "боевые" в файле dbase.conf
# postgreHost = 'localhost'
# postgrePort = '5432'
# postgreBase = '?'
# postgreUser ='?'
# postgrePwd = '?'
parse_config_file("./config/dbase.conf")


# Эти параметры переопределим на "боевые" в файле main.conf
# main_port = '8888' 
# main_title ='titile'
# Project_Name='TorWiki'
# wikiTitleAdmin='TorWiki Admin layer'
# salt = "?"
# cookieSecret="?"

parse_config_file("./config/main.conf")



