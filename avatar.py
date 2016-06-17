import gi
gi.require_version ('Astroid', '0.1')
from gi.repository import GObject
from gi.repository import Astroid
from urllib.parse import urlencode
from hashlib import md5
from urllib.request import urlopen
from os.path import exists, expanduser
from os import unlink, makedirs
from base64 import b64encode
try:
	from libravatar import libravatar_url
except ImportError:
	libravatar_url = None

CACHE_DIR = expanduser('~/.cache/astroid/avatar/')

class AvatarPlugin (GObject.Object, Astroid.Activatable):
	object = GObject.property (type=GObject.Object)

	def do_activate (self):
		if not exists(CACHE_DIR):
			makedirs(CACHE_DIR)
		print ('avatar: activated')

	def do_deactivate (self):
		print ('avatar: deactivated')

	def _load(self, url, filename):
		with urlopen(url) as response:
			data = response.read()
		with open(filename, 'wb') as f:
			f.write(data)
		return b64encode(data).decode()

	def _load_preinstalled(self, n):
		filename = expanduser('~/.config/astroid/plugins/avatar/avatar_{}.png').format(n)
		print('avatar: filename=', filename)
		with open(filename, 'rb') as f:
			data = f.read()
		return b64encode(data).decode()

	def do_get_avatar_uri (self, email, type_, size):
		print('avatar:', email, type_, size)
		email = email.lower()
		for n in ('cron', 'nagios', 'root', ): # TODO determine dynamic
			if email.startswith('{}@'.format(n)):
				data = self._load_preinstalled(n)
				break
		else:
			filename = '{}{}.jpg'.format(CACHE_DIR, email, type_, size)
			print('avatar: filename=', filename)
			if exists(filename):
				# TODO check age
				with open(filename, 'rb') as f:
					data = f.read()
				if not data: # has no avatar, give default
					data = self._load_preinstalled('default')
				else:
					data = b64encode(data).decode()
			else:
				try:
					if libravatar_url: # we have the libravatar library
						url = libravatar_url(email,
							https=True,
							size=size,
							default='404',
							)
						print('avatar: libravatar_url=', url)
						data = self._load(url, filename)
					else: # do gravatar:
						url = 'https://www.gravatar.com/avatar/{}?{}'.format(
							md5(email.encode('ascii', 'replace')).hexdigest(),
							urlencode({'d':'404', 's':str(size)}))
						print('avatar: gravatar=', url)
						data = self._load(url, filename)
				except Exception as e:
					print('_load: e=', e)
					with open(filename, 'wb') as f: # we had an error, do neg cache (empty file)
						pass
					data = self._load_preinstalled('default')
		url = 'data:image/jpeg;base64,{}'.format(data)
		print('avatar: url=', url)
		return url

	def do_get_allowed_uris (self):
		print('do_get_allowed_uris:')
		return ['data:image/jpeg;base64,', ]

print ('avatar: plugin loaded')
