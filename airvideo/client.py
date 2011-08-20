import urllib2
import avmap
from hashlib import sha1
from utils import Retry, hexdump, strdump
from avmap import AVDict, AVBitrateList
from media import client_map_avdict, FolderObject, VideoObject

class AVClient:
    
    udid = "89eae483355719f119d698e8d11e8b356525ecfb"
    allowed_bitrates = AVBitrateList(["2048"])

    def __init__(self, host, port=45631, password=None):
        self.endpoint = "http://%s:%d/service" % (host, port)
        if password:
            self.digest = sha1("S@17" + password + "@1r").hexdigest().upper()
        else:
            self.digest = None

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
        
        return [ii for ii in [client_map_avdict(self, i) for i in items] if ii]
    
    @Retry(3, delay=1)
    def get_item(self, path):
        item = self._request("browseService", 
                            "getItemsWithDetail", 
                                [path])['result'][0]
        
        return client_map_avdict(self, item)

    def get_queue(self):
        url_resp = self._request("conversionService", "getConversionSnapshot")
        """ queue lists pending items, convertedItem is the current conversion with an eta and a percentDone """
        return url_resp['result']
    
    def get_conversion_locations(self):
        """ TODO: missing arguments """
        url_resp = self._request("conversionService", "getConversionLocations")
        return url_resp['result']

    def convert_item(self, item):
        url_resp = self._request("conversionService", "convertItem", self._params_for_video_conversion(item))
        return url_resp['result']

    def pause_queue(self):
        url_resp = self._request("conversionService", "pause")
        return url_resp['result']

    def resume_queue(self):
        url_resp = self._request("conversionService", "resume")
        return url_resp['result']

    def remove_from_queue(self, item):
        """ TODO: missing arguments """
        url_resp = self._request("conversionService", "remove")
        return url_resp['result']
    
    def get_detail(self, video):
        item = self.get_item(video.path)
        return item.detail
    
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
            
    def _request(self, service, method, params = None):
        headers = { 
            'User-Agent' : "AirVideo/2.4.0 CFNetwork/459 Darwin/10.0.0d3",
            'Accept' : "*/*",
            'Accept-Language' : "en-us",
            'Accept-Encoding' : "gzip, deflate"
        }
        
        avrequest = {
            'parameters' : [params],
            'clientVersion' : 240, 
            'clientIdentifier' : self.udid,
            'serviceName' : service,
            'methodName' : method,
            'requestURL' : self.endpoint,
        }
        if params == None:
            avrequest['parameters'] = None
        if self.digest:                 
            avrequest['passwordDigest'] = self.digest

        #if method == "convertItem":
        #    avrequest['parameters'].append('clientVersion')
        #    avrequest['parameters'].append('2.4.9')
        
        post_body = avmap.dumps(AVDict("air.connect.Request", avrequest))

        print hexdump(post_body, 32)
        
        request = urllib2.Request(self.endpoint, post_body, headers)
        
        response = urllib2.urlopen(request).read()

        print strdump(response)

        return avmap.loads(response)
        
    def _params_for_video_conversion(self, video):
        convertreq = {
            'itemId' : video.path,
            # General
            'quality' : 0.0,
            'metaData': ['device','iPhone'],
            'subtitleInfo' : None,
            'offset' : 0.0,
            # Audio
            'audioStream' : 1,
            'audioBoost' : 0.0,
            # Video
            'videoStream' : 0,
            'allowedBitratesLocal' : self.allowed_bitrates,
            'allowedBitratesRemote' : AVBitrateList(['384']),
            'resolutionWidth' : min(video.video_stream['width'],720),   # scale down 1080p stuff, like what we get from camcorders
            'resolutionHeight' : min(video.video_stream['height'],480), # TODO: check if this affects ratios (shouldn't)
            'cropTop' : 0,
            'cropRight' : 0,
            'cropBottom' : 0,
            'cropLeft' : 0
        }
        
        return AVDict("air.video.ConversionRequest", convertreq)
        
