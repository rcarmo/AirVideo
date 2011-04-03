import json
import time

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

		import time

class Retry(object):
    default_exceptions = (Exception,)
    def __init__(self, tries, exceptions=None, delay=0):
        """
        Decorator for retrying a function if exception occurs

        tries -- num tries 
        exceptions -- exceptions to catch
        delay -- wait between retries
        """
        self.tries = tries
        if exceptions is None:
            exceptions = Retry.default_exceptions
        self.exceptions =  exceptions
        self.delay = delay

    def __call__(self, f):
        def fn(*args, **kwargs):
            exception = None
            for _ in range(self.tries):
                try:
                    return f(*args, **kwargs)
                except self.exceptions, e:
                    #print "Retry, exception: "+str(e)
                    time.sleep(self.delay)
                    exception = e
            #if no success after tries, raise last exception
            raise exception
        return fn		