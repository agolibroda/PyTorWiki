#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2015 Alec Goliboda
#
# WikiException.py




from .constants.data_base import *


class Error():
    """
    просто класс для описания ошибок - 
    ч бы было удобнее их отдавать получателю.
    
    """
    def __init__(self, code, message):
        self.code = code
        self.message = message


class WikiException(Exception):
    def __init__(self, value):
        self.value = value
        
    def getCode(self):
        if hasattr(self.value, 'code'):
            return self.value.code
        else:
            return None
    
    def getMessage(self):
        if hasattr(self.value, 'message'):
            return self.value.message
        else:
            return None

    def getValue(self):
        return self.value
    
    def __str__(self):
        return repr(self.value)


class LoginIsEmpty(WikiException):
    def __init__(self):
        WikiException.__init__(self, Error(100001, 'field login is empty'))

# PASSWD_IS_ENPTY             = '100002, field login is empty'
# LOGIN_ERROR                 = '100003, login error'
# LOAD_ONE_VALUE_ERROR        = '100004, load one value error'
# LINK_OR_ARTICLE_NOT_UNIQ    = '100005, Link or article is not unique'
# 
# FILE_NOT_FOUND              = '100007, File not found'
# LOAD_PRIVATE_KEY_ERROR      = '100008, Loading private Key Error'
# OLD_PASSWORD_IS_BAD         = '100009, Old Password is bad'
# 
# NOT_PERMISSION_TO_VIEW      = '403, No permission to view '

class ArticleNotFound(WikiException):
    def __init__(self):
        WikiException.__init__(self, Error(100006, 'Article not found'))







