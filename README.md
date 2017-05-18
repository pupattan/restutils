.. restutils documentation master file, created by
   sphinx-quickstart on Thu May 18 19:23:46 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. module:: restutils
	:synopsis: restutils module
.. moduleauthor:: Pulak Pattanayak' <pulak.pattanayak@gmail.com>

Welcome to restutils's documentation!
=====================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

About
-----
restutils is a python library provides you easy methods to work with REST APIs.
Its provides client side methods to interact with your REST server

Future Enhancements
-------------------
We will add libraries for creating simple REST API servers also in upcoming releases.

Install
-------
The easiest way to install restutils is via ``pip``::

	pip install restutils




Classes
----------

.. class:: RESTClient(base_url, content_type="application/json", username=None, password=None, session=None, log=sys.stderr)

  provides a simple way to interact with HTTP/HTTPs RESTful resources.
  
  .. method:: get(url_path, **kwargs)
  
		Perform an HTTP(s) GET to the resource specified in url_path. Takes an optional ref of custom request headers.
  
  .. method:: post(self, url_path, request_body="", **kwargs)
  
		Perform an HTTP(s) POST to the resource specified. Takes an optional body content and reference of custom request headers.
  
  .. method:: put(self, url_path, request_body="", **kwargs)
  
		Perform an HTTP(s) PUT to the resource specified. Takes an optional body content and ref of custom request headers.
  
  .. method:: delete(self, url_path, **kwargs)
  
		Perform an HTTP(s) DELETE to the resource specified. Takes an optional ref of custom request headers.
		
  .. method:: create_session(auth_url, body="", status=httplib.ACCEPTED, username=None, password=None)
  
		If your API supports session handling feature you can create a session using this method and use it in other methods

  .. method:: delete_session(self, auth_url, status=httplib.NO_CONTENT)
  
		This method helps in deleting the exists session and creared by create_session method
		

Usage
------
How to use classes
	>>> from restutils import RESTClient
	>>> client = RESTClient()
