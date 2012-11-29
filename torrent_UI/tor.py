import re
import base64
import httplib
import json
import time

defaults = {
    'host': '127.0.0.1',
    'port': 7755,
    'path': '/gui/',
    'username': 'admin',
    'password': '1',
    'caching': True,
    }

STATUS = {
    1: "Started",
    2: "Checking",
    4: "Start after check",
    8: "Checked",
    16: "Error",
    32: "Paused",
    64: "Queued",
    128: "Loaded",
    }

TORRENT_PROPERTIES = [
    'trackers', 'ulrate', 'dlrate', 'superseed', 'dht',
    'pex', 'seed_override', 'seed_ratio', 'seed_time', 'ulslots',
    ]

PRIORITIES = {
    0: "Don't Download",
    1: "Low Priority",
    2: "Normal Priority",
    3: "High Priority",
    }

INITIAL_SEEDING_STATES = {
    -1: 'Not allowed',
    0: 'Disabled',
    1: 'Enabled',
    }

def resync(f):
    def new_f(obj, *args, **kwargs):
        result = f(obj, *args, **kwargs)
        obj._syncdata()
        return result
    return new_f

class UTorrentTorrent(object):
    def __init__(self, ut, data):
        self.ut = ut
        self.hash = data['hash']
        self._props = None
        self.data = data

    def __getattr__(self, key):
        if key == 'files':
            self._syncfiles()
            return self.files
        if key == 'props':
            self._syncprops()
            return self.props

        if key in self.data:
            return self.data[key]

        raise AttributeError('No attribute: %s' % key)

    def __getitem__(self, property):
        if property in self.props:
            return self.props[property]

        raise KeyError('No property: %s' % property)

    def __setitem__(self, property, value):
        if property in TORRENT_PROPERTIES:
            self._setprop(property, value)

        raise KeyError('No property: %s' % property)

    def __iter__(self):
        return self.data.__iter__()

    def _setprop(self, property, value):
        # Initialize the temporary properties (for bulk update)
        if self._props is None:
            self._props = {}

        # For trackers we break the list by a carriage return / newline
        if property == 'trackers':
            value = '\r\n'.join(value)

        # Set the specific proprty
        self._props[property] = value

    def _setprops(self, properties):
        for key, value in properties:
            self._setprop(property, value)

    def _syncfiles(self):
        response = self.ut(hash=self.hash, action='getfiles')

        files = response['files'][1]
        self.files = []
        for file in files:
            sane = {
                'name': file[0],
                'size': file[1],
                'downloaded': file[2],
                'priority': file[3],
                }
            self.files.append(sane)

    def _syncprops(self):
        if self._props:
            response = self.ut(
                hash=self.hash,
                action='setprops',
                s=self._props.keys(),
                v=self._props.values(),
            )

            # Remove the temporary property store because we have
            # saved our properties. We dont want to send
            # the same data on further syncs.
            self._props = None

        response = self.ut(action='getprops', hash=self.hash)

        self.props = {}
        # Look through the json response and update this objects properties
        properties = response['props'][0]
        for property, value in properties.iteritems():
            if property == 'trackers':
                value = value.split('\r\n')
                value = filter(lambda x: len(x) > 0, value)
            self.props[property] = value

    def _syncdata(self):
        # Synchronize the UTorrent instance.
        self.ut._synctorrents()

        # Pull the data from the UTorrent instance about this torrent into here.
        # If the torrent no longer exists, make sure we raise this.
        if self.hash not in self.ut._torrents:
            return False

        self.data = self.ut._torrents[self.hash]
        return True

    def set_file_priorities(self, priorities):
        params = []
        for index, priority in enumerate(priorities):
            params.append({
                'p': priority,
                'f': index
            })
        self.ut(action='setprio', hash=self.hash, grouped=params)
        self._syncfiles()

    def set_file_priority(self, index, priority):
        self.ut(action='setprio', hash=self.hash, p=priority, f=index)
        self._syncfiles()

    @resync
    def start(self):
        return self.ut.start([self.hash])

    @resync
    def stop(self):
        return self.ut.stop([self.hash])

    @resync
    def pause(self):
        return self.ut.pause([self.hash])

    @resync
    def forcestart(self):
        return self.ut.forcestart([self.hash])

    @resync
    def unpause(self):
        return self.ut.unpause([self.hash])

    @resync
    def recheck(self):
        return self.ut.recheck([self.hash])

    @resync
    def remove(self, data=False):
        return self.ut.remove([self.hash], data=data)

    def refresh(self):
        # Just refreshes the data for this torrent
        self._syncdata()

    def sync(self):
        # If we have to set some properties then we do this now.
        self._syncprops()
        self._syncdata()
        self._syncfiles()

    def fields(self):
        return self.data.keys()

    def values(self):
        return self.data.values()

    def __str__(self):
        return "<Torrent: %s / %s>" % (self.hash, self.name)

    def __unicode__(self):
        return str(self)

    def __repr__(self):
        return str(self)

class UTorrent(httplib.HTTPConnection):
    def __init__(self, config=None):
        # Ensure the configuration if not passed in is an empty dict.
        if config is None:
            config = {}

        # Merge the default configuration and the passed in configuration.
        self.config = dict(defaults.items() + config.items())

        if not self.config['path'].endswith('/'):
            self.config['path'] = self.config['path'] + '/'

        # Build a url string that is usable by the request framework.
        self.url = "/%(path)s" % self.config

        # Default values for cached properties.
        self._token = None
        self._authorization = None
        self._cache = None
        self._torrents = {}

        self.labels = {}

        self.debuglevel = 0

        # Connect to the client
        httplib.HTTPConnection.__init__(self, self.config['host'], self.config['port'])

    @property
    def authorization(self):
        if not self._authorization:
            self._authorization = base64.b64encode("%s:%s" % (self.config['username'], self.config['password']))

        return self._authorization

    @property
    def token(self):
        if not self._token:
            self.putrequest('GET', self.config['path'] + 'token.html')
            self.putheader('Authorization', 'Basic %s' % self.authorization)
            self.endheaders()

            response = self.getresponse()

            self._cookie = response.getheader('set-cookie').split(';')[0].split('=')[1]

            if response.status == 401:
                raise UTorrentError("Invalid login")

            body = response.read()
            match = re.search(r'>([^<]+)<', body)
            if not match:
                raise UTorrentError("Could not find a token in the request")

            self._token = match.group(1)

        return self._token

    def __call__(self, cookies=None, data=None, grouped=None, method='GET', params=None, **kwargs):
        url = self.config['path'] + '?token=%s' % self.token

        if params is None:
            params = []

        headers = {}
        headers['Authorization'] = 'Basic %s' % self.authorization
        headers['Cookie'] = 'GUID=%s' % self._cookie

        if len(kwargs) > 0:
            for key, value in kwargs.iteritems():
                if type(value) is list:
                    for member in value:
                        params.append((key, str(member)))
                else:
                    params.append((key, str(value)))

        for key, value in params:
            url += '&%s=%s' % (key, value)

        if cookies:
            url += ':COOKIE:'

            for key, value in cookies.iteritems():
                url += '&%s=%s' % (key, value)

        self.request(method, url, data, headers)

        response = self.getresponse()

        if response.status == 401:
            raise UTorrentError("Invalid login")

        body = response.read()

        return json.loads(body)

    def __getitem__(self, hash):
        if hash not in self._torrents:
            raise KeyError("Unknown torrent: %s" % hash)
        else:
            return UTorrentTorrent(self, self._torrents[hash])

    def iteritems(self):
        return self._torrents.iteritems()

    def __iter__(self):
        return self._torrents.__iter__()

    def _sanitize(self, data):
        return {
            'hash': data[0],
            'status': data[1],
            'name': data[2],
            'size': data[3],
            'progress': data[4],
            'downloaded': data[5],
            'uploaded': data[6],
            'ratio': data[7],
            'upload_speed': data[8],
            'download_speed': data[9],
            'eta': data[10],
            'label': data[11],
            'peers_connected': data[12],
            'peers_swarm': data[13],
            'seeds_connected': data[14],
            'seeds_swarm': data[15],
            'availability': data[16],
            'queue': data[17],
            'remaining': data[18],
            'created_at': data[20],
            'finished_at': data[21],
            'download_path': data[23]
        }

    def add(self, path):
        raise NotImplementedError()

    def sync(self):
        self._synctorrents()

    def _synctorrents(self):
        params = [('list',1)]
        if self.config['caching'] and self._cache:
            params.append(('cid', self._cache))

        response = self(params=params)

        self.labels = dict(response['label'])

        if self.config['caching'] and self._cache:
            torrents = response['torrentp']
            removed = response['torrentm']

            # Remove any of the torrents that no longer exist.
            for hash in removed:
                del(self._torrents[hash])
        else:
            torrents = response['torrents']

        if self.config['caching']:
            # Update the cache id.
            self._cache = response['torrentc']
        else:
            # If we arent caching we clear the list.
            self._torrents = {}

        # Add or update the new torrents.
        for torrent in torrents:
            torrent = self._sanitize(torrent)
            self._torrents[torrent['hash']] = torrent

    def list(self):
        return self._torrents

    def torrents(self):
        _torrents = []
        for hash in self._torrents:
            t = UTorrentTorrent(self, self._torrents[hash])
            _torrents.append(t)

        return _torrents

    def keys(self):
        return self._torrents.keys()

    def values(self):
        return self._torrents.values()

    def start(self, hashes):
        return self(action='start', hash=hashes)

    def stop(self, hashes):
        return self(action='stop', hash=hashes)

    def pause(self, hashes):
        return self(action='pause', hash=hashes)

    def forcestart(self, hashes):
        return self(action='forcestart', hash=hashes)

    def unpause(self, hashes):
        return self(action='unpause', hash=hashes)

    def recheck(self, hashes):
        return self(action='recheck', hash=hashes)

    def remove(self, hashes, data=False):
        if data:
            return self(action='removedata', hash=hashes)
        else:
            return self(action='remove', hash=hashes)

class UTorrentError(Exception):
    pass