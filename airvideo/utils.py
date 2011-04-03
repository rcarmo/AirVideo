import json

def singleton(cls):
	instance_container = []
	def getinstance():
		if not len(instance_container):
			instance_container.append(cls())
		return instance_container[0]
	return getinstance

class AVEncoder(json.JSONEncoder):
	def default(self, obj):
		if hasattr(obj, 'name') and hasattr(obj, "data"):
			return ("AVObject: %s" % obj.name, obj.data)
		if hasattr(obj, 'read'):
			pos = obj.tell()
			obj.seek(0, 2)
			size = obj.tell()
			obj.seek(0)
			return "<Data size:%s>" % size
		return json.JSONEncoder.default(self, obj)