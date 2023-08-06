# -*- coding: utf-8 -*-
__author__ = 'Erick Almeida and Masroor Ehsan'

import gc
import logging
import threading
import time


try:
    from psycopg2 import connect as postgresql_connect
    import psycopg2.extensions as postgresql_ext
except ModuleNotFoundError:
    postgresql_connect = None
    postgresql_ext = None


class PoolError(Exception):
    pass


class AbstractConnectionPool(object):
    """Generic key-based pooling code."""

    def __init__(self, max_conn, expiration, disable_pooling, *args, **kwargs):
        """Initialize the connection pool."""
        self._logger = kwargs.pop("logger", logging.getLogger('sqlify'))
        self._pool = []
        self._used = {}
        self._rused = {}  # id(conn) -> key map
        self._tused = {}  # last used timestamp
        self._keys = 0
        self._disposed = False
        self.expiration = expiration
        self.max_conn = max_conn
        self._disable_pooling = disable_pooling  # do not pool database connections
        self._db_args = args
        self._db_kwargs = kwargs

    def build_connection(self):
        if self._dsn:
            return psycopg2.connect(self._dsn)
        else:
            return psycopg2.connect(**self._db_config)

    def _connect(self, key=None):
        """Create a new connection and assign it to 'key' if not None."""
        conn = self.build_connection()

        if not self._disable_pooling:
            if key is not None:
                self._used[key] = conn
                self._rused[id(conn)] = key
                self._tused[id(conn)] = time.time()
            else:
                self._pool.append(conn)

        self._logger.debug('Connection created %s' % conn)
        return conn

    def _release(self, conn, remove_from_pool=False):
        if not self._disable_pooling and remove_from_pool and conn in self._pool:
            self._pool.remove(conn)
            del self._tused[id(conn)]
        conn.close()
        self._logger.debug('Connection closed: %s [pool: %d]' % (conn, len(self._pool)))

    def _get_key(self):
        """Return a new unique key."""
        self._keys += 1
        return self._keys

    def _get_conn(self, key=None):
        """Get a free connection and assign it to 'key' if not None."""
        if self._disposed:
            raise PoolError('Connection pool is disposed')

        if self._disable_pooling:
            return self._connect(key)

        if key is None:
            key = self._get_key()
        if key in self._used:
            return self._used[key]

        if self._pool:
            self._used[key] = conn = self._pool.pop()
            self._rused[id(conn)] = key
            self._tused[id(conn)] = time.time()
            return conn
        else:
            if len(self._used) == self.max_conn:
                raise PoolError('Connection pool exhausted')
            return self._connect(key)

    def _purge_expired_connections(self):
        if self._disable_pooling:
            return

        now = time.time()
        expiry_list = []
        for item in self._pool:
            conn_time = self._tused[id(item)]
            elapsed = now - conn_time
            if elapsed >= self.expiration:
                expiry_list.append(item)

        self._logger.debug('Purging... [pool: %d, expired: %d]' % (len(self._pool), len(expiry_list)))
        for item in expiry_list:
            self._release(item, True)

    def _put_conn(self, conn, key=None, close=False, fail_silently=False):
        """Stow away a connection."""
        if self._disable_pooling:
            self._release(conn)
            return

        self._logger.debug('Putting away %s%s' % (conn, ' key=' + key if key else ''))
        if self._disposed:
            if fail_silently:
                return
            raise PoolError('Connection pool is disposed')

        if key is None:
            key = self._rused.get(id(conn))
        if not key:
            raise PoolError('Trying to put un-keyed connection')

        if len(self._pool) < self.max_conn and not close:
            # Return the connection into a consistent state before putting
            # it back into the pool
            if not conn.closed:
                status = conn.get_transaction_status()
                if status == _ext.TRANSACTION_STATUS_UNKNOWN:
                    # server connection lost
                    self._logger.debug('Connection lost. Closing %s' % conn)
                    self._release(conn.close)
                elif status != _ext.TRANSACTION_STATUS_IDLE:
                    # connection in error or in transaction
                    self._logger.debug('Connection is in transaction. Rolling back %s' % conn)
                    conn.rollback()
                    self._pool.append(conn)
                else:
                    # regular idle connection
                    self._pool.append(conn)
                    # If the connection is closed, we just discard it.
        else:
            self._logger.debug('Closing (pool exhausted or explicit close requested) %s' % conn)
            self._release(conn)

        self._purge_expired_connections()

        # here we check for the presence of key because it can happen that a
        # thread tries to put back a connection after a call to close
        if not self._disposed or key in self._used:
            del self._used[key]
            del self._rused[id(conn)]

    def _release_all(self):
        """Release all connections.

        Note that this can lead to some code fail badly when trying to use
        an already closed connection. If you call .release_all() make sure
        your code can deal with it.
        """
        # Make sure that all connections lying about are collected before we go on.
        try:
            gc.collect()
        except (TypeError, AttributeError):
            # We've detected that we're being called in an incomplete
            # finalization state, we just bail out, leaving the connections
            # to take care of themselves.
            return

        if self._disposed:
            raise PoolError('Connection pool is disposed')

        if not self._disable_pooling:
            close_list = self._pool + list(self._used.values())
            self._logger.debug('Closing %d connection(s)' % len(close_list))

            for conn in close_list:
                try:
                    conn.close()
                except:
                    pass

        self._disposed = True
        self._pool = []
        self._used = {}

    @property
    def disposed(self):
        return self._disposed

    def __del__(self):
        self._release_all()


class SimpleConnectionPool(AbstractConnectionPool):
    """A connection pool that can't be shared across different threads."""

    get_conn = AbstractConnectionPool._get_conn
    put_conn = AbstractConnectionPool._put_conn
    release_all = AbstractConnectionPool._release_all
    purge_expired_connections = AbstractConnectionPool._purge_expired_connections


class ThreadedConnectionPool(AbstractConnectionPool):
    """A connection pool that works with the threading module."""

    def __init__(self, max_conn, expiration, **kwargs):
        """Initialize the threading lock."""
        super(ThreadedConnectionPool, self).__init__(max_conn, expiration, **kwargs)
        self._lock = threading.Lock()

    def get_conn(self, key=None):
        """Get a free connection and assign it to 'key' if not None."""
        self._lock.acquire()
        try:
            return self._get_conn(key)
        finally:
            self._lock.release()

    def put_conn(self, conn=None, key=None, close=False, fail_silently=False):
        """Put away an unused connection."""
        self._lock.acquire()
        try:
            self._put_conn(conn, key, close, fail_silently)
        finally:
            self._lock.release()

    def purge_expired_connections(self):
        """Purge all stale connections."""
        self._lock.acquire()
        try:
            self._purge_expired_connections()
        finally:
            self._lock.release()

    def release_all(self):
        """Release all connections (even the one currently in use.)"""
        self._lock.acquire()
        try:
            self._release_all()
        finally:
            self._lock.release()
