import urllib2
import avmap
from avmap import AVDict, AVBitrateList
from media import client_map_avdict, FolderObject, VideoObject

#urllib2.install_opener(
#    urllib2.build_opener(
#        urllib2.ProxyHandler({'http': '127.0.0.1:8888'})
#    )
#)

class AVClient:
	
	udid = "89eae483355719f119d698e8d11e8b356525ecfb"
	allowed_bitrates = AVBitrateList(["1280", "1536", "2048", "2560"])
	
	def __init__(self, host, port=45631):
	    self.endpoint = "http://%s:%d/service" % (host, port)
	
	def browse(self, path=None):
		if isinstance(path, FolderObject):
			path = path.path
		
		browsereq = { 
			"folderId" : path, 
			"preloadDetails" : False
		}
		
		browse_resp = self._request("browseService", 
						"getItems", 
						AVDict("air.video.BrowseRequest", browsereq))
		
		items = browse_resp['result']['items']
		
		return [client_map_avdict(self, i) for i in items]			
	
	def get_url(self, video, live):
		if live:
			url_resp = self._request("livePlaybackService", 
							"initLivePlayback", 
							self._params_for_video_conversion(video))
		else:
			url_resp = self._request("playbackService", 
							"initPlayback", 
							video.path)	
		
		return url_resp['result']['contentURL']									
	
	def get_detail(self, video):
		detail_resp = self._request("browseService", 
						"getItemsWithDetail", 
						[video.path])
		
		return detail_resp.data['result'][0].data['detail'].data
			
	def _request(self, service, method, params):
		headers = { 
			'User-Agent' : "AirVideo/2.4.0 CFNetwork/459 Darwin/10.0.0d3",
			'Accept' : "*/*",
			'Accept-Language' : "en-us",
			'Accept-Encoding' : "gzip, deflate"
		}
		
		avrequest = {
			'requestURL' : self.endpoint,
			'clientVersion' : 240, 
			'serviceName' : service,
			'methodName' : method,
			'clientIdentifier' : self.udid,
			'parameters' : [params]
		}
		
		post_body = avmap.dumps(AVDict("air.connect.Request", avrequest))
		
		request = urllib2.Request(self.endpoint, post_body, headers)
		
		response = urllib2.urlopen(request).read()

		return avmap.loads(response)
		
	def _params_for_video_conversion(self, video):
		convertreq = {
			'itemId' : video.path,
			# General
			'quality' : 0.699999988079071,
		    'subtitleInfo' : None,
		    'offset' : 0.0,
			# Audio
    		'audioStream' : 1,
			'audioBoost' : 0.0,
    		# Video
			'videoStream' : 0,
			'allowedBitratesLocal' : self.allowed_bitrates,
    		'allowedBitratesRemote' : self.allowed_bitrates,
    		'resolutionWidth' : video.video_stream['width'],
			'resolutionHeight' : video.video_stream['height'],
			'cropTop' : 0,
			'cropRight' : 0,
			'cropBottom' : 0,
			'cropLeft' : 0
		}
		
		return AVDict("air.video.ConversionRequest", convertreq)
		
			