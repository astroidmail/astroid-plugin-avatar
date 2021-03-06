Avatar loader plugin
====================

Intro
-----

Astroid loads by default avatars from gravatar by embedding the URL into the
mailthread view. This has some obvious drawbacks:

-	avatars are not cached and retrieved too frequently

-	gravatar may learn your contacts

-	internal or system mail adresses are grabbed too

this plugin adds the following features:

-	instead of gravatar the avatars will be retreived from libravatar if the
	library python3-libravatar is installed

-	the images are persisted to not be retrieved again

-	the url is a base64 url containing all image data (out of security reasons)

-	avatars for system/internal mailaddresses are supported (for example for
	mailaddresses starting with root@)

TODOs
-----

-	there is no expiry of the cache

-	the image type (mime type) is ignored (assumed jpeg)

Installation
------------

the installation is simple as:

```sh
mkdir -p ~/.config/astroid/plugins/
cd ~/.config/astroid/plugins/
git clone https://github.com/astroidmail/astroid-plugin-avatar
```
...and restart astroid.

Licensing
---------

See [LICENSE](./LICENSE) for licensing information.
