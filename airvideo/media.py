FOLDER_RETURNTYPES = ["air.video.DiskRootFolder", "air.video.Folder"]
VIDEO_RETURNTYPES = ["air.video.VideoItem"]

def client_map_avdict(client, avd):
	if avd.name in FOLDER_RETURNTYPES:
		return FolderObject(client,
							avd.data['name'], 
							avd.data['itemId'])
	elif avd.name in VIDEO_RETURNTYPES:
		return VideoObject(client,
							avd.data['name'], 
							avd.data['itemId'], 
							avd.data['detail'])
	else:
		print "unknown media type: %s" % avd.name

class FolderObject:
	def __init__(self, client, name, itemId):
		self.client = client
		self.name = name
		self.path = itemId
	
	def contents(self):
		return self.client.browse(self)
		
	def search(self, search_term):
		pass
		
class VideoObject:
	def __init__(self, client, name, itemId, detail):	
		self.client = client
		self.name = name
		self.path = itemId
		self.detail = detail.data
		
		self.thumbnail_image = self.detail['videoThumbnail']
		# TODO - Actually check which stream is which
		self.video_stream = self.detail['streams'][0]
		self.audio_stream = self.detail['streams'][1]
		
	def url(self):
		return self.client.get_url(self, False)	
	
	def live_url(self):
		return self.client.get_url(self, True)	