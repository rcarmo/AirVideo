FOLDER_RETURNTYPES = ["air.video.DiskRootFolder", "air.video.Folder"]
VIDEO_RETURNTYPES = ["air.video.VideoItem"]

def client_map_avdict(client, avd):
	if avd.name in FOLDER_RETURNTYPES:
		return FolderObject(client,
							avd.data['name'], 
							avd.data['itemId'])
	elif avd.name in VIDEO_RETURNTYPES:
		if avd.data['detail']:
			detail = avd.data['detail'].data
		else:
			detail = None
			
		return VideoObject(client,
							avd.data['name'], 
							avd.data['itemId'],
							detail)
	else:
		print "unknown return type: %s" % avd.name

class FolderObject:
	def __init__(self, client, name, itemId):
		self.client = client
		self.name = name
		self.path = itemId
		self.isFolder = True
	
	def __getattr__(self, name):
		if name == "contents":
			return self.client.browse(self)
		else:
			return object.__getattr__(self, name)
		
	def search(self, search_term):
		#TODO - implement search
		pass
		
class VideoObject:
	def __init__(self, client, name, itemId, detail = None):	
		self.client = client
		self.name = name
		self.path = itemId
		self.isFolder = False
		
		if detail:
			self.detail = detail
			self.hydrated = True
		else:
			self.hydrated = False
	
	def __getattr__(self, name):
		if name == "detail":
			self._fetch_details()
			return self.detail
		elif name == "thumbnail_image":
			self._fetch_details()
			return self.detail['videoThumbnail']
		elif name == "video_stream":	
			self._fetch_details()
			#TODO - figure out which stream is which
			return self.detail['streams'][0]
		else:
			return object.__getattr__(self, name)
	
	def _fetch_details(self):
		if self.hydrated:
			return
		
		self.detail = self.client.get_detail(self)
		self.hydrated = True
		
	def url(self):
		return self.client.get_url(self, False)	
	
	def live_url(self):
		return self.client.get_url(self, True)	