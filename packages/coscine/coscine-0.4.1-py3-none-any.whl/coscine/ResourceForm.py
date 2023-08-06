###############################################################################
# Coscine Python3 Client
# Copyright (c) 2018-2021 RWTH Aachen University
# Contact: coscine@itc.rwth-aachen.de
# Git: https://git.rwth-aachen.de/coscine/docs/public/wiki/-/tree/master/
# Please direct bug reports, feature requests or questions at the URL above
# by opening an issue.
###############################################################################
# This python wrapper implements a client for the Coscine API.
# Coscine is an open source project at RWTH Aachen University for
# the management of research data.
# Visit https://coscine.rwth-aachen.de for more information.
###############################################################################

from collections.abc import MutableMapping
from .exceptions import *
from .FormFlags import FormFlags

###############################################################################

KEYS = [
	{
		"name": {
			"de": "Ressourcentyp",
			"en": "Resource Type"
		},
		"flags": FormFlags.REQUIRED | FormFlags.CONTROLLED,
		"field": "type"
	},
	{
		"name": {
			"de": "Ressourcengröße",
			"en": "Resource Size"
		},
		"flags": FormFlags.NONE,
		"field": "resourceTypeOption"
	},
	{
		"name": {
			"de": "Ressourcenname",
			"en": "Resource Name"
		},
		"flags": FormFlags.REQUIRED,
		"field": "ResourceName"
	},
	{
		"name": {
			"de": "Anzeigename",
			"en": "Display Name"
		},
		"flags": FormFlags.REQUIRED,
		"field": "DisplayName"
	},
	{
		"name": {
			"de": "Ressourcenbeschreibung",
			"en": "Resource Description"
		},
		"flags": FormFlags.REQUIRED,
		"field": "Description"
	},
	{
		"name": {
			"de": "Disziplin",
			"en": "Discipline"
		},
		"flags": FormFlags.REQUIRED | FormFlags.CONTROLLED,
		"field": "Disciplines"
	},
	{
		"name": {
			"de": "Ressourcenschlagwörter",
			"en": "Resource Keywords"
		},
		"flags": FormFlags.NONE,
		"field": "Keywords"
	},
	{
		"name": {
			"de": "Sichtbarkeit",
			"en": "Visibility"
		},
		"flags": FormFlags.REQUIRED | FormFlags.CONTROLLED,
		"field": "Visibility"
	},
	{
		"name": {
			"de": "Lizenz",
			"en": "License"
		},
		"flags": FormFlags.CONTROLLED,
		"field": "License"
	},
	{
		"name": {
			"de": "Verwendungsrechte",
			"en": "Usage Rights"
		},
		"flags": FormFlags.NONE,
		"field": "UsageRights"
	},
	{
		"name": {
			"de": "Applikationsprofile",
			"en": "Application Profiles"
		},
		"flags": FormFlags.REQUIRED | FormFlags.CONTROLLED,
		"field": "applicationProfile"
	}
]

###############################################################################

class ResourceForm(MutableMapping):

	"""
	Coscine Input Form for creating and editing resources
	"""

###############################################################################

	def __init__(self, handle):
		self.store = {}
		self._keys = {}
		self.handle = handle
		resource_types = handle.get_resource_types()
		profiles = handle.get_profiles()
		visibility = handle.get_visibility()
		licenses = handle.get_licenses()
		disciplines = handle.get_disciplines()
		self.vocabulary = {
			"type": resource_types,
			"applicationProfile": profiles,
			"Visibility": visibility,
			"License": licenses,
			"Disciplines": disciplines
		}
		self.reset()

###############################################################################

	def __getitem__(self, key):
		return self.store[key]

###############################################################################

	def __setitem__(self, key, value):
		if key not in self._keys:
			raise KeyError(key)
		elif self.is_controlled(key):
			vocabulary = self.get_vocabulary(key)
			if type(value) is list:
				self.store[key] = []
				for val in value:
					if val in vocabulary:
						self.store[key].append(vocabulary[val])
					else:
						raise VocabularyError(val)
			else:
				if value in vocabulary:
					self.store[key] = vocabulary[value]
				else:
					raise VocabularyError(value)
		else:
			self.store[key] = value

###############################################################################

	def __delitem__(self, key):
		del self.store[key]

###############################################################################

	def __iter__(self):
		return iter(self.store)

###############################################################################

	def __len__(self):
		return len(self.store)

###############################################################################

	def __repr__(self):
		entries = []
		for key in self._keys:
			R = " "
			C = " "
			value = ""
			if self.is_required(key):
				R = "R"
			if self.is_controlled(key):
				C = "C"
			if key in self.store:
				value = " = %s" % self.store[key]
			text = " [%s%s] %s%s" % (R, C, key, value)
			entries.append(text)

		format = \
			"_______________________________\n\n" \
			"    Coscine Resource Form\n" \
			"_______________________________\n\n" \
			" [R: Required] [C: Controlled]\n" \
			"-------------------------------\n" \
			+ "\n".join(entries) + \
			"\n_______________________________\n"
		return format

###############################################################################

	def is_required(self, key):

		"""
		Determines wether a key is required

		Parameters
		-----------
		key : str

		Returns
		--------
		bool
		"""

		if self._keys[key]["flags"] & FormFlags.REQUIRED:
			return True
		else:
			return False

###############################################################################

	def is_controlled(self, key):

		"""
		Determines wether a key is controlled by a vocabulary

		Parameters
		-----------
		key : str

		Returns
		--------
		bool
		"""

		if self._keys[key]["flags"] & FormFlags.CONTROLLED:
			return True
		else:
			return False

###############################################################################

	def get_vocabulary(self, key):

		"""
		Returns the vocabulary associated with a controlled key

		Parameters
		-----------
		key : str

		Returns
		--------
		dict
		"""

		if self.is_controlled(key):
			return self._keys[key]["vocabulary"]
		else:
			msg = "Key [%s] is not controlled by a vocabulary!" % key
			raise CoscineException(msg)

###############################################################################

	def keys(self):

		"""
		Enumerates the keys of the input form
		"""

		keys = []
		for key in self._keys:
			keys.append(key)
		return keys

###############################################################################

	def reset(self):

		"""
		Resets the input form to default
		"""

		self.store.clear()
		for key in KEYS:
			self._keys[key["name"][self.handle.lang]] = key
			if key["flags"] & FormFlags.CONTROLLED:
				key["vocabulary"] = self.vocabulary[key["field"]]

###############################################################################

	def generate(self):

		"""
		Generates JSON-LD formatted representation of resource data

		Raises
		-------
		RequirementError
			When one or more required fields have not been set
		
		Returns
		--------
		JSON-LD formatted resource data
		"""

		data = {}
		missing = []
		for key in self._keys:
			value = self._keys[key]
			if key not in self.store:
				if self.is_required(key):
					missing.append(key)
			else:
				data[value["field"]] = self.store[key]

		if missing:
			raise RequirementError(missing)

		size = {}
		if "resourceTypeOption" in data:
			size = {
				"Size": data["resourceTypeOption"]
			}
		data["resourceTypeOption"] = size

		return data

###############################################################################