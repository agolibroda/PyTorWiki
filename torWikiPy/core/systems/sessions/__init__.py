# -*- coding: UTF-8 -*-
# Copyright 2014 Cole Maclean

"""Tornado sessions, stored in Redis.
"""

import os
import os.path
################
import logging

dirModule = os.path.dirname(__file__)
nameModule = __file__
logger = logging.getLogger(nameModule)
logger.setLevel(logging.DEBUG)
###################################


import datetime
import uuid
import json
from functools import wraps

import config

try:
    from collections import MutableMapping #py2
except ImportError:
    from collections.abc import MutableMapping #py3
try:
    import cPickle as pickle #py2
except ImportError:
    import pickle #py3

import redis
from tornado.web import RequestHandler
from tornado.options import options, define


# if not hasattr(options, 'redis_host'):
#     define("redis_host", default="localhost", help="Redis host")
# if not hasattr(options, 'redis_port'):
#     define("redis_port", default=6379, help="Redis port number")
# if not hasattr(options, 'redis_session_db'):
#     try:
#         redis_default_db = options.redis_db
#     except AttributeError:
#         redis_default_db = 8
#     define("redis_session_db", default=redis_default_db, help="Redis sessions database")
# if not hasattr(options, 'session_length_sec'):
#     define("session_length_sec", default=1800, help="Session length in sec")


class Session(MutableMapping):
    """Simple session, stored in redis.
    sess_id = uuid.uuid4().hex
    s = Session(sess_id)
    s['foo'] = 'bar'
    s.save()
        
    s = Session.load(sess_id)
    s['foo']
    > 'bar'
    """
    store = redis.StrictRedis(host=options.redis_host,
                port=options.redis_port, db=options.redis_session_db)
    length = options.sessionLifetime # * 86400 # in seconds
 
    def __init__(self, id, *args, **kwargs):
        self._id = id
        self._data = dict(*args, **kwargs)
        self._loaded = False
        self._dirty = False
        self._pipe = self.store.pipeline()
 
    @classmethod
    def load(cls, id, preload=False):
        """Load the given session id from redis. If there's nothing for the
        id given, returns an empty session.
        If preload is True, load and unpickle all data.
        
        returns Session object.
        """
        session = Session(id)
        if preload:
            session._load_data()
            
        return session
    
    def _load_data(self, key=None):
        if self._loaded:
            return
        if key is None:
            # load everything
            for key, val in self.store.hgetall(self.id).items():
                # hgetall returns bytes
                key = key.decode('utf-8')
                self._data[key] = pickle.loads(val)
            self._loaded = True
        elif key in self:
            val = self.store.hget(self.id, key)
            self._data[key] = pickle.loads(val)
                
    @property
    def id(self):
        """Prefix the session id for storage."""
        return 'session:{0}'.format(self._id) if self._id else None

    def clear(self):
        """Delete the session and all data."""
        self._data.clear()
        self._pipe = self.store.pipeline()
        self.store.delete(self.id)
 
    def touch(self, remote_ip=None):
        """Update the session expiry and set the last access time
        and IP (if provided).
        """
        if remote_ip is not None:
            self['last_ip_address'] = remote_ip
        self['last_access_time'] = '{0}'.format(datetime.datetime.now())
        self._pipe.expire(self.id, self.length)
 
    def save(self, force=False):
        """Execute piped session commands."""
        if self._dirty or force:
            self._pipe.execute()
        self._dirty = False
 
    def __getitem__(self, key):
        try:
            return self._data[key]
        except KeyError:
            self._load_data(key=key)
            return self._data[key]
 
    def __setitem__(self, key, value):
        self._dirty = True
        self._pipe.hset(self.id, key, pickle.dumps(value))
        self._data[key] = value
 
    def __delitem__(self, key):
        # We save immediately here to prevent
        # autoloading of the key on next access
        if key in self:
            self._pipe.hdel(self.id, key)
            self.save(force=True)
            if key in self._data:
                del self._data[key]
        else:
            raise KeyError(key)
        
    def __iter__(self):
        self._load_data()
        return iter(self._data)
        
    def __len__(self):
        self._load_data()
        return len(self._data)
        
    def __repr__(self):
        self._load_data()
        return "<{0}, {1}>".format(self.id, repr(self._data))
        
    def __contains__(self, key):
        if key in self._data:
            return True
        elif not self._loaded:
            return self.store.hexists(self.id, key)
        else:
            return False
    
    def to_json(self):
        self._load_data()
        return json.dumps(self, default=lambda o: o._data,
            sort_keys=True, indent=4)
            
    def copy(self):
        self._load_data()
        return Session(self._id, **self._data.copy())

def setup_session(handler):
    """
    Setup a new session (or retrieve the existing one)
    
    """
    cookieName = config.options.cookieName
    logger.info( ' Session setup_session cookieName :: '+ str(cookieName))
    # session_id = handler.get_secure_cookie("pyTorWikiCookie")
    session_id = handler.get_secure_cookie(setup_session)

    if session_id is not None:
        session_id = session_id.decode('utf-8')
        handler.session = Session.load(session_id)
    else:
        new_id = uuid.uuid4().hex
        handler.session = Session(new_id)
        handler.set_secure_cookie(config.options.cookieName, new_id)

    handler.session.touch(remote_ip=handler.request.remote_ip)

def save_session(handler):
    """Store the session to redis."""
    if hasattr(handler, config.options.cookieName) and handler.session is not None:
        handler.session.save()

class SessionHandler(RequestHandler):
    """Handlers inheriting from this class get session access (self.session).
    """
    def prepare(self):
        setup_session(self)
            
    def on_finish(self, *args, **kwargs):
        save_session(self)
        
    def clear_session(self):
        self.session.clear()
        self.clear_cookie(config.options.cookieName)
            
def session(method):
    """Decorator for handler methods. Loads the session prior to method
    execution and saves it after.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        setup_session(self)
        result = method(self, *args, **kwargs)
        save_session(self)
        return result
    return wrapper