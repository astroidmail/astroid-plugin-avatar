import gi
gi.require_version ('Astroid', '0.1')
gi.require_version ('Gtk', '3.0')
gi.require_version ('WebKit', '3.0')
gi.require_version ('GMime', '2.6')
from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import WebKit
from gi.repository import Astroid
from gi.repository import GMime
from urllib.parse import urlencode
from hashlib import md5
from urllib.request import urlopen
from os.path import exists, expanduser, dirname
from os import unlink, makedirs
from base64 import b64encode
try:
	from libravatar import libravatar_url as avatar_url
	print('avatar: using libravatar')
except ImportError:
	# fallback to home grown gravatar url
	def avatar_url(email, https=True, size=48, default='404', ):
		return 'https://www.gravatar.com/avatar/{}?{}'.format(
			md5(email.encode('ascii', 'replace')).hexdigest(),
			urlencode(dict(
				d=default,
				s=str(size),
				)))
	print('avatar: using gravatar')

class AvatarPlugin (GObject.Object, Astroid.ThreadViewActivatable):
	object = GObject.property (type=GObject.Object)
	thread_view = GObject.property (type = Gtk.Box)
	web_view = GObject.property (type = WebKit.WebView)

	def do_activate (self):
		self.cache_dir = expanduser('~/.cache/astroid/avatar/')
		self.config_dir = dirname(__file__)
		if not exists(self.cache_dir):
			makedirs(self.cache_dir)
		print ('avatar: activated', __file__)

	def do_deactivate (self):
		print ('avatar: deactivated')

	def _load(self, url, filename):
		with urlopen(url) as response:
			data = response.read()
		with open(filename, 'wb') as f:
			f.write(data)
		return b64encode(data).decode()

	def _load_preinstalled(self, name):
		filename = '{}/avatar_{}.png'.format(self.config_dir, name)
		if exists(filename):
			print('avatar: filename=', filename)
			with open(filename, 'rb') as f:
				data = f.read()
			return b64encode(data).decode()

	def do_get_avatar_uri (self, email, type_, size, message):
		# Check if message is from GitHub
		github_user = message.get_header ('X-GitHub-Sender')
		if github_user:
			email = github_user
			mime_type = 'image/png'
			ext				= 'png'
		else:
			email = email.lower()
			mime_type = 'image/jpeg'
			ext				= 'jpg'


		print('avatar:', email, type_, size)

		data = self._load_preinstalled(email.split('@')[0])
		if not data:
			filename = '{}{}.{}'.format(self.cache_dir, email, ext)
			print('avatar: filename=', filename)
			if exists(filename):
				# TODO check age
				with open(filename, 'rb') as f:
					data = f.read()
				if not data: # has no avatar, give default
					data = self._load_preinstalled('default')
					mime_type = 'image/jpeg'
					ext				= 'jpg'
				else:
					data = b64encode(data).decode()
			else:
				try:
					if github_user:
						url = "https://github.com/%s.png" % github_user
						print ('avatar: github url=', url)
						data = self._load(url, filename)

					else:
						url = avatar_url(email, https=True, size=size, default='404', )
						print('avatar: libravatar_url=', url)
						data = self._load(url, filename)
				except Exception as e:
					print('_load: e=', e)
					with open(filename, 'wb') as f: # we had an error, do neg cache (empty file)
						pass
					data = self._load_preinstalled('default')
		else:
			# pre-installed
			mime_type = 'image/jpeg'
			ext				= 'jpg'


		url = 'data:{};base64,{}'.format(mime_type, data)
		return url

	def do_get_allowed_uris (self):
		print('do_get_allowed_uris:')
		return [] # our uris are always allowed

print ('avatar: plugin loaded')
