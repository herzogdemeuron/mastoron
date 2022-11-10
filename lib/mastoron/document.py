import json
import revitron

class ConfigStorage:
	"""
	The `ConfigStorage`` allows for easily storing project configuration items.
	
	Getting configuration items::
	   
	   config = mastoron.DocumentConfigStorage().get('namespace.item')
	   
	The returned ``config`` item can be a **string**, a **number**, a **list** or a **dictionary**. 
	It is also possible to define a default value in case the item is not defined in the config::

		from collections import defaultdict
		config = mastoron.DocumentConfigStorage().get('namespace.item', defaultdict())
		
	Setting configuration items works as follows::
	
		mastoron.DocumentConfigStorage().set('namespace.item', value)
	
	"""

	def __init__(self):
		"""
		Inits a new ``ConfigStorage`` object.
        """
		self.configPath = revitron.DocumentConfigStorage().get('mastoron.configpath')
		with open(self.configPath, 'r') as f:
			self.config = json.load(f)

	def get(self, key, default=None):
		"""
		Returns config entry for a given key.

		Example::

			config = mastoron.ConfigStorage()
			item = config.get('name')
			
		Args:
			key (string): The key of the config entry
			default (mixed, optional): An optional default value. Defaults to None.

		Returns:
			mixed: The stored value 
		"""
		return self.config.get(key, default)

	def set(self, key, data):
		"""
		Updates or creates a config config entry.

		Example::
		
			config = mastoron.ConfigStorage()
			config.set('name', value)
			
		Args:
			key (string): The config entry key
			data (mixed): The value of the entry
		"""
		self.config[key] = data
		# Remove empty items.
		self.config = dict((k, v) for k, v in self.config.iteritems() if v)
		raw = json.dumps(self.config, sort_keys=True, ensure_ascii=False)
		with open(self.configPath, 'w') as f:
			f.write(raw)

	@staticmethod
	def setPath(path):
		revitron.DocumentConfigStorage().set('mastoron.configpath', path)