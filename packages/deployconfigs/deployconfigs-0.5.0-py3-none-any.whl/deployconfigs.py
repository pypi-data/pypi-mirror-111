#
"""
    DeployConfigs

    to lower the pip overhead, I include dj-database-url and dj-cache-url inline
"""

import configparser
import contextlib
import os
import re
import urllib.parse as urlparse
from pathlib import Path
from typing import List, Union

BOOLEAN_STATES = dict(configparser.RawConfigParser.BOOLEAN_STATES)  # force copy

try:  # no strict dependency on django. in case it exist we use ImproperlyConfigured from it
    from django.core.exceptions import ImproperlyConfigured
except ImportError:
    class ImproperlyConfigured(Exception):
        pass

DATABASE_SCHEMES = {
    'postgres': 'django.db.backends.postgresql',
    'postgresql': 'django.db.backends.postgresql',
    'pgsql': 'django.db.backends.postgresql',
    'postgis': 'django.contrib.gis.db.backends.postgis',
    'mysql': 'django.db.backends.mysql',
    'mysql2': 'django.db.backends.mysql',
    'mysqlgis': 'django.contrib.gis.db.backends.mysql',
    'mysql-connector': 'mysql.connector.django',
    'spatialite': 'django.contrib.gis.db.backends.spatialite',
    'sqlite': 'django.db.backends.sqlite3',
    'oracle': 'django.db.backends.oracle',
    'oraclegis': 'django.contrib.gis.db.backends.oracle',
    'redshift': 'django_redshift_backend',
}

CACHE_SCHEMES = {
    'db': 'django.core.cache.backends.db.DatabaseCache',
    'dummy': 'django.core.cache.backends.dummy.DummyCache',
    'file': 'django.core.cache.backends.filebased.FileBasedCache',
    'locmem': 'django.core.cache.backends.locmem.LocMemCache',
    'uwsgicache': 'uwsgicache.UWSGICache',
    'memcached': 'django.core.cache.backends.memcached.PyLibMCCache',
    'djangopylibmc': 'django_pylibmc.memcached.PyLibMCCache',
    'pymemcached': 'django.core.cache.backends.memcached.MemcachedCache',
    'redis': 'django_redis.cache.RedisCache',
    'hiredis': 'django_redis.cache.RedisCache',
}

EMAIL_SCHEMES = {
    'smtp': 'django.core.mail.backends.smtp.EmailBackend',
    'smtps': 'django.core.mail.backends.smtp.EmailBackend',
    'console': 'django.core.mail.backends.console.EmailBackend',
    'file': 'django.core.mail.backends.filebased.EmailBackend',
    'memory': 'django.core.mail.backends.locmem.EmailBackend',
    'dummy': 'django.core.mail.backends.dummy.EmailBackend',
    'celery+smtp': 'djcelery_email.backends.CeleryEmailBackend',
    'celery+smtps': 'djcelery_email.backends.CeleryEmailBackend',
}

STORAGE_SCHEMES = {
    'local': 'django.core.files.storage.FileSystemStorage',
    's3': '',
    'asure': '',
}

# Register database, cache, email schemes in URLs.
urlparse.uses_netloc.extend(DATABASE_SCHEMES.keys())
urlparse.uses_netloc.extend(CACHE_SCHEMES.keys())
urlparse.uses_netloc.extend(EMAIL_SCHEMES.keys())
urlparse.uses_netloc.extend(STORAGE_SCHEMES.keys())

DEFAULT_ENV = 'DJANGO_CONF'
DEFAULT_SECTION = 'DJANGO'
TEST_SECTION = 'TEST'
DEFAULT_DATABASE_ENV = 'DATABASE_URL'
DEFAULT_CACHE_ENV = 'CACHE_URL'
DEFAULT_EMAIL_ENV = 'EMAIL_URL'
DEFAULT_STORAGE_ENV = 'STORAGE_URL'


class DeployConfigs(object):
    def __init__(
            self,
            deploy_conf_env=DEFAULT_ENV,
            section=DEFAULT_SECTION,
            required: Union[List, None] = None,
            check_environ: bool = True,
            use_conf_file: Union[str, Path, bool] = True,
            default_django_conf: Union[str, Path, bool] = None,
            auto_create_from_default: bool = False
    ):
        self.deploy_conf_env = deploy_conf_env
        self.section = section
        self.required = required or []
        self.check_environ = check_environ
        self.use_conf_file_env = False
        if use_conf_file is True:
            self.use_conf_file_env = True
            use_conf_file = os.environ.get(self.deploy_conf_env, None)
        self.conf_file = self.to_path(use_conf_file)

        if default_django_conf is True:
            raise ImproperlyConfigured('default_django_conf could not be True')
        self.default_file = self.to_path(default_django_conf)

        self.auto_create_from_default = auto_create_from_default
        self.ready = False
        self.cf = None

    def _configure(self):
        if self.conf_file and not self.conf_file.exists():
            if self.auto_create_from_default and self.default_file and self.default_file.exists():
                self.conf_file.write_text(self.default_file.read_text())
            else:
                raise ValueError('deployconfigs file `{}` not exists'.format(self.conf_file))

        filenames = filter(None, [self.default_file, self.conf_file])
        if self.use_conf_file_env and not filenames:
            raise ImproperlyConfigured('Please set `%s` environment' % self.deploy_conf_env)

        if filenames:
            self.cf = configparser.ConfigParser()
            read_filenames = self.cf.read(filenames)
            if len(read_filenames) == 0:
                self.cf = None

        self.ready = True

    def _get(self, option, default=None, section=None, check_environ=None, _convert_func=lambda x: x):
        if not self.ready:
            self._configure()

        if check_environ is None:
            check_environ = self.check_environ

        # let environment overwrite what is in\or not in the conf file.
        if check_environ and section is None:
            val = os.environ.get(option, Undefined)
            if val is not Undefined:
                return _convert_func(val)
        try:
            if self.cf:
                val = self.cf.get(section or self.section, option)
                return _convert_func(val)
            else:
                return default

        except configparser.NoOptionError as e:
            if option in self.required and default is None:
                raise e
            return default

    def get(self, option, default=None, section=None, check_environ=None):
        return self._get(option, default, section, check_environ)

    def getboolean(self, option, default=False, section=None, check_environ=None):
        if default not in (True, False):
            raise ValueError('default value for getboolean must be True or False')
        return self._get(option, default, section, check_environ, _convert_func=as_boolean)

    def get_path(self, key: str, default: Union[Path, str] = None) -> Union[Path, None]:
        value: str = self.get(key) or default
        return self.to_path(value)

    def to_path(self, value) -> Union[Path, bool]:
        return Path(value).resolve() if isinstance(value, (str, Path)) else bool(value)

    def general_dict(self, option, default=None, section=None):
        url = self.get(option, section=section, default=default)
        return self.parse_url(url).__dict__

    def database_dict(self, option=DEFAULT_DATABASE_ENV, engine=None, default=None, section=None):
        url = self.get(option, section=section, default=default)
        return self.parse_database_url(url, engine=engine)

    def cache_dict(self, option=DEFAULT_CACHE_ENV, default='locmem://', section=None):
        url = self.get(option, section=section, default=default)
        return self.parse_cache_url(url)

    def email_dict(self, option=DEFAULT_EMAIL_ENV, default=None, section=None, context=False):
        url = self.get(option, section=section, default=default)
        res = self.parse_email_url(url)
        if context:
            return contextlib.contextmanager(iter)([res, ])
        return res

    def storage_dict(self, option=DEFAULT_STORAGE_ENV, default=None, section=None):
        url = self.get(option, section=section, default=default)
        return self.parse_storage_url(url)

    def parse_url(self, url, schemes=None, upper=False, clean_path=True):
        if url is None:
            return self.Result()
        url = urlparse.urlparse(url)

        backend = None

        if schemes:
            try:
                backend = schemes[url.scheme]
            except KeyError:
                raise ImproperlyConfigured('Unknown scheme `%s`' % url.scheme)

        transport, scheme = None, url.scheme
        if scheme and '+' in scheme:
            transport, scheme = scheme.rsplit('+', 1)

        # Split query strings from path.
        path, query = url.path, url.query
        if '?' in path and not url.query:
            # Handle python 2.6 broken url parsing
            path, query = path.split('?', 1)

        query_dict = dict([((key.upper() if upper else key), ';'.join(val))
                           for key, val in urlparse.parse_qs(query).items()])
        if ',' in url.netloc:
            hostname = port = ''
        else:
            port = url.port or ''
            hostname = url.hostname or ''

        if clean_path:
            if path and path[0] == '/':
                path = path[1:]

        result = self.Result(
            backend=backend,
            transport=transport,
            scheme=scheme,
            netloc=url.netloc,
            username=urlparse.unquote(url.username or ''),
            password=urlparse.unquote(url.password or ''),
            hostname=hostname,
            port=port,
            path=path,
            query=query,
            query_dict=query_dict,
        )
        return result

    class Result(object):
        backend = transport = scheme = username = password = hostname = port = path = query_dict = None
        netloc = query = fragment = ''

        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
            self.__dict__.setdefault('query_dict', {})

        def is_empty(self):
            if len(self.query_dict.keys()) == 0 and len(self.__dict__) == 1:
                return True
            return False

        def __str__(self):
            return repr(self.__dict__)

    def parse_database_url(self, url, engine=None):
        if url == 'sqlite://:memory:':
            # this is a special case, because if we pass this URL into
            # urlparse, urlparse will choke trying to interpret "memory"
            # as a port number
            return {
                'ENGINE': DATABASE_SCHEMES['sqlite'],
                'NAME': ':memory:'
            }

        # otherwise parse the url as normal
        url = self.parse_url(url, DATABASE_SCHEMES)
        if url.backend is None:
            return {}

        # If we are using sqlite and we have no path, then assume we
        # want an in-memory database (this is the behaviour of sqlalchemy)
        if url.scheme == 'sqlite' and url.path == '':
            url.path = ':memory:'

        # Handle postgres percent-encoded paths.
        netloc = url.netloc
        if "@" in netloc:
            netloc = netloc.rsplit("@", 1)[1]
        if ":" in netloc:
            netloc = netloc.split(":", 1)[0]
        url.hostname = netloc or ''
        if '%2f' in url.hostname.lower():
            url.hostname = url.hostname.replace('%2f', '/').replace('%2F', '/')

        conn_max_age = int(url.query_dict.pop('conn_max_age', 0))

        config = {
            'ENGINE': engine or url.backend,
            'NAME': urlparse.unquote(url.path or ''),
            'USER': url.username,
            'PASSWORD': url.password,
            'HOST': url.hostname,
            'PORT': url.port,
            'CONN_MAX_AGE': conn_max_age,
        }

        if url.scheme == 'mysql' and 'ssl-ca' in url.query_dict:
            url.query_dict['ssl'] = {'ca': url.query_dict.pop('ssl-ca')}

        # Support for Postgres Schema URLs
        if 'currentSchema' in url.query_dict and config['ENGINE'] in (
            'django.contrib.gis.db.backends.postgis',
            'django.db.backends.postgresql',
            'django_redshift_backend',
        ):
            url.query_dict['options'] = '-c search_path={0}'.format(url.query_dict.pop('currentSchema'))

        # Pass the query string into OPTIONS if any
        if url.query_dict:
            config.setdefault('OPTIONS', {}).update(url.query_dict)
            connect_timeout = config['OPTIONS'].get('connect_timeout')
            if connect_timeout:
                config['OPTIONS']['connect_timeout'] = int(connect_timeout)
        return config

    def parse_cache_url(self, url):
        url = self.parse_url(url, CACHE_SCHEMES, upper=True, clean_path=False)
        config = {
            'BACKEND': url.backend,
        }

        redis_options = {}
        if url.scheme == 'hiredis':
            redis_options['PARSER_CLASS'] = 'redis.connection.HiredisParser'

        # File based
        if not url.netloc:
            if url.scheme in ('memcached', 'pymemcached', 'djangopylibmc'):
                config['LOCATION'] = 'unix:' + url.path

            elif url.scheme in ('redis', 'hiredis'):
                match = re.match(r'.+?(?P<db>\d+)', url.path)
                if match:
                    db = match.group('db')
                    url.path = url.path[:url.path.rfind('/')]
                else:
                    db = '0'
                config['LOCATION'] = 'unix:%s:%s' % (url.path, db)
            else:
                config['LOCATION'] = url.path

        # URL based
        else:
            # Handle multiple hosts
            config['LOCATION'] = ';'.join(url.netloc.split(','))

            if url.scheme in ('redis', 'hiredis'):
                if url.password:
                    redis_options['PASSWORD'] = url.password
                # Specifying the database is optional, use db 0 if not specified.
                db = url.path[1:] or '0'
                config['LOCATION'] = "redis://%s:%s/%s" % (url.hostname, url.port, db)

        if redis_options:
            config['OPTIONS'] = redis_options

        if url.scheme == 'uwsgicache':
            config['LOCATION'] = config.get('LOCATION') or 'default'

        # Pop special options from cache_args
        # https://docs.djangoproject.com/en/1.10/topics/cache/#cache-arguments
        options = {}
        for key in ('MAX_ENTRIES', 'CULL_FREQUENCY'):
            try:
                val = url.query_dict.pop(key)
                options[key] = int(val)
            except KeyError:
                pass

        if options:
            config.setdefault('OPTIONS', {}).update(options)

        config.update(url.query_dict)

        return config

    def parse_email_url(self, url):
        url = self.parse_url(url, EMAIL_SCHEMES)

        config = {
            'EMAIL_BACKEND': url.backend,
            'EMAIL_FILE_PATH': url.path,
            'EMAIL_HOST_USER': url.username,
            'EMAIL_HOST_PASSWORD': url.password,
            'EMAIL_HOST': url.hostname,
            'EMAIL_PORT': url.port,
            'SERVER_EMAIL': url.query_dict.get('error_from', url.username),
            'DEFAULT_FROM_EMAIL': url.query_dict.get('from', url.username),
            'EMAIL_SCHEME': url.scheme,
            'EMAIL_TRANSPORT': url.transport,
        }

        use_ssl = False
        use_tls = False
        if url.scheme == 'smtps':
            use_tls = True
        if as_boolean(url.query_dict.get('ssl')):
            use_ssl = True
            use_tls = False  # maybe user use smtps://?ssl=True
        elif as_boolean(url.query_dict.get('tls')):
            use_tls = True
        config['EMAIL_USE_SSL'] = use_ssl
        config['EMAIL_USE_TLS'] = use_tls

        if url.transport == 'celery':
            t = config['CELERY_EMAIL_TASK_CONFIG'] = url.query_dict.copy()
            for k in ('ssl', 'tls', 'from', 'error_from'):
                t.pop(k, None)

        return config

    def parse_storage_url(self, url):
        if url.startswith('local'):
            assert url.startswith('local:///'), \
                'please use local:/// to supress the parsing local path as netloc'

        url = self.parse_url(url, STORAGE_SCHEMES)
        config = url.__dict__

        return config

    def parse(self, url):
        if url == 'sqlite://:memory:':
            # this is a special case, because if we pass this URL into
            # urlparse, urlparse will choke trying to interpret "memory"
            # as a port number
            return {
                'ENGINE': DATABASE_SCHEMES['sqlite'],
                'NAME': ':memory:'
            }

        # otherwise parse the url as normal
        url2 = self.parse_url(url)
        if url2.scheme in DATABASE_SCHEMES:
            return self.parse_database_url(url)
        elif url2.scheme in CACHE_SCHEMES:
            return self.parse_cache_url(url)
        elif url2.scheme in EMAIL_SCHEMES:
            return self.parse_email_url(url)
        elif url2.scheme in STORAGE_SCHEMES:
            return self.parse_storage_url(url)
        else:
            raise ValueError('unknown scheme `%s`' % url2.scheme)


class Undefined(object):
    pass


def as_boolean(val):
    return BOOLEAN_STATES.get(str(val).lower()) is True
