Avatar loader plugin
====================

Astroid loads by default avatars from gravatar by embedding the URL into the
mailthread view. This has some obvios drawbacks:

-	avatars are not cached and gotten too frequently

-	gravatar learns your contacts

-	internal or system mail adresses are grabbed too

this plugin adds the following features:

-	instead of gravatar the avatars can be retreived from libravatar if the
	library python3-libravatar is installed

-	the images are persistet to not be retrieved again

-	the url is a base64 url containing all image data (out of security reasons)

-	avatars for system/internal mailaddresses are supported (for example for
	mailaddresses starting with root@)

TODOs:

-	there is no expirering of the cache

-	the image type (mime type) is ignored (assumed jpeg)

