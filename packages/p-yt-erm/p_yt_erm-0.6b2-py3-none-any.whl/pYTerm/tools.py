import re
import vlc
import sys
import pafy
import time
import threading
import feedparser
from youtubesearchpython import VideosSearch, PlaylistsSearch






class Song():
    def __init__(self, url, length=None, channelname=None, title=None, id=None):
        """Song object that stores important song stuff
        Best constructed by calling `get_song_obj()` with either search terms or a youtube URL
        """
        self.pafyobj = None
        self.url = url
        self.length = length
        self.channel = channelname
        self.vidtitle = title
        self.id = id
        if None in [self.url, self.channel, self.vidtitle]:
            self.fill_details()
        elif length == None:
            self.length = 0
        self.extract_title_author()
    
    def __str__(self):
        return self.vidtitle
    
    def extract_title_author(self):
        """"Extracts real song title and artist from youtube title"""
        title = self.vidtitle
        artist = self.channel
        if ' - ' in title:
            title_list = title.split(' - ')
            title = exclude_from_string(title_list[1].strip())
            artist = title_list[0].strip()
            if not artist:
                artist = exclude_from_string(self.channel)
        elif ' by ' in title:
            # way less common but occasionally some titles will have "songname by artist"
            title_list = title.split(' by ')
            title = exclude_from_string(title_list[0].strip())
            artist = title_list[-1]
            if not artist:
                artist = exclude_from_string(self.channel)
        else:
            title = exclude_from_string(title)
            artist = exclude_from_string(artist)
        self.title = title
        self.artist = artist
    
    def fill_details(self):
        if None in [self.length, self.channel, self.vidtitle, self.id]:
            self.pafyobj = pafy.new(self.url)
            # if not self.length: self.length = timestamp_to_sec(self.pafyobj.duration)
            if not self.length: self.length = self.pafyobj.length
            if not self.channel: self.channel = self.pafyobj.author
            if not self.vidtitle: self.vidtitle = self.pafyobj.title
            if not self.id: self.id = self.pafyobj.videoid
    
    def get_stream(self, legacy=False):
        if self.pafyobj is None:
            self.pafyobj = pafy.new(self.url)
        if legacy:
            return self.pafyobj.streams[0].url
        else:
            return self.pafyobj.getbestaudio(preftype='m4a').url


exclude_list = ['\\(', '\\)', '\\[', '\\]', '\\"', "\\'", 'official audio', 'official video', 'official music video',
                'lyrics', 'lyric video', ' \\- topic']


def exclude_from_string(input_):
    for i in exclude_list:
        input_ = re.sub(i, '', input_, flags=re.IGNORECASE)
    return input_


def previous_line():
    """Move cursor to previous line"""
    sys.stdout.write("\033[F")


def clear_line():
    """Clear current line"""
    sys.stdout.write("\033[K")


def clear_previous_line():
    """Clear previous line"""
    previous_line()
    clear_line()


def get_song_obj(song):
    """
    Create a song object from either a youtube url or a search query

    args:
        song (str): the yt URL or search terms
    """
    if is_url(song) and is_youtube_url(song):
        song_obj = song_from_url(song)
        return song_obj
    else:
        song_obj = song_from_search(song)
        return song_obj


def timestamp_to_sec(timestamp):
    colcount = timestamp.count(':')
    if colcount == 1:
        minutes, seconds = timestamp.split(':')
        return int(minutes) * 60 + int(seconds)
    elif colcount == 2:
        hours, minutes, seconds = timestamp.split(':')
        return int(hours) * 3600 + int(minutes) * 60 + int(seconds)


def song_from_url(url):
    return Song(url)


def song_from_search(search):
    # """Looks up a song with search terms and returns a Song object"""
    result = VideosSearch(search, limit=1).result()['result'][0]
    return Song(result['link'], timestamp_to_sec(result['duration']), result['channel']['name'], result['title'],
                result['id'])


def url_from_playlist_search(search):
    result = PlaylistsSearch(search, limit=1).result()['result'][0]
    return result['link']


def songs_from_yt_playlist(url):
    """Returns a list of song objects from a youtube playlist link
    
    args:
        urls (str): url to a youtube playlist
    """
    url = yt_playlist_to_rss_url(url)
    rss = feedparser.parse(url)
    out = []
    for item in rss['entries']:
        song = Song(item['link'], None, item['author'], item['title'], item['yt_videoid'])
        out.append(song)
    return out


def format_yt_title(title):
    return title


url_regex = '(?:(?:https?|ftp):\\/\\/|\\b(?:[a-z\\d]+\\.))(?:(?:[^\\s()<>]+|\\((?:[^\\s()<>]+|(?:\\([^\\s()<>]+\\)))?\\))+(?:\\((?:[^\\s()<>]+|(?:\\(?:[^\\s()<>]+\\)))?\\)|[^\\s`!()\\[\\]{};:\'".,<>?«»“”‘’]))?'


def is_url(url):
    """Checks if a given string is an URL using regular expression, returns a bool"""
    return bool(re.match(url_regex, url))


youtube_url_regex = '^((?:https?:)?\\/\\/)?((?:www|m)\\.)?((?:youtube\\.com|youtu.be))(\\/(?:[\\w\\-]+\\?v=|embed\\/|v\\/)?)([\\w\\-]+)(\\S+)?$'


def is_youtube_url(url):
    """Checks if a given string is a youtube url, returns a bool"""
    return bool(re.match(youtube_url_regex, url))


def ensure_list(input_object):
    """Returns any input as a list. Tuples and sets get converted to lists,
    lists are returned as-is, and all other types get returned as a single element list
    
    args:
        input_object (any): the object to get listified
    """
    input_type = type(input_object)
    if input_type == list:
        return input_object
    elif input_type in [tuple, set]:
        return list(input_object)
    else:
        return [input_object]


def yt_playlist_to_rss_url(playlist_url):
    """Gets the rss url from a youtube playlist"""
    url_prefix = 'https://www.youtube.com/feeds/videos.xml?playlist_id='
    playlist_id = playlist_url.split('?list=')[-1]
    return url_prefix + playlist_id


def secs_to_string(seconds):
    """Gets time from seconds to human readable"""
    hours = -1
    minutes = 0
    seconds = int(seconds)
    out = ""
    if seconds >= 3600:
        hours = int(seconds / 3600)
        seconds = seconds % 3600
    if seconds >= 60:
        minutes = int(seconds / 60)
        seconds = seconds % 60
    
    if hours != -1:
        out += f'{hours}:'
        if minutes < 10:
            out += f'0{minutes}:'
        else:
            out += f'{minutes}:'
    else:
        out += f'{minutes}:'
    
    if seconds < 10:
        out += f'0{seconds}'
    else:
        out += f'{seconds}'
    
    return out

    


def clip(value, lower, upper):
    return lower if value < lower else upper if value > upper else value



class ThreadedSoftwareTimer():
    def __init__(self, starttime = 0, start=True):
        self.counter = starttime
        self.paused = False
        self.x = threading.Thread(target=self.counter_, daemon=True)
        if start:
            self.x.start()
    
    def start(self):
        if not self.x.is_alive():
            self.x.start()
    
    def counter_(self):
        while True:
            if not self.paused:
                self.counter += 0.25
            time.sleep(0.25)

    def set_pause(self, state: bool):
        self.paused = state

    def restart(self, starttime: int=0):
        self.stop()
        while self.x.is_alive():
            time.sleep(0.01)
        self.counter = starttime
        self.x = threading.Thread(target=self.counter_, daemon=True)
        self.start()

    def set_time(self, seconds: int):
        self.counter = seconds
    
    def get(self):
        return self.counter
    
    def stop(self):
        if self.x.is_alive:
            self.x._stop()


    
class mdict():
    """ fucked up little multiple dict class made by yours truly :)"""
    def __init__(self, startDict = None):
        self.__inside__ = {}
        self.__outside__ = {}
        self.__counter__ = 0
        if type(startDict) == dict:
            for key,item in startDict.items():
                self[key] = item


    def __makelist__(self,value):
        t = type(value)
        if t == list:
            return value
        elif t in [str,int,float]:
            return [value]
        elif t in [tuple,set]:
            return list(value)

    def __len__(self):
        return len(self.__inside__.values())

    def __str__(self):
        return str(self.export())

    def __setitem__(self,keys,value):
        keys = self.__makelist__(keys)
        exists = None
        for key in keys:
            if self.__iskey__(key):
                exists = key
                break
        if exists:
            siblings = self.keys(exists)
            for key in keys:
                if not key in siblings:
                    self.__addsibling__(exists,key)
            self.__updatevalue__(key,value)
        else:
            self.__newentry__(keys,value)

    def __delitem__(self, keys):
        self.__remove__(keys)

    def __getitem__(self,key):
        return self.__getval__(self.__getkey__(key))

    def __iter__(self):
        return self.__outside__.__iter__()

    def __clean__(self):
        insidekeys = set(self.__outside__.values())
        for key in insidekeys:
            if not self.__islinked__(key):
                self.__remove__(key)

    def __iskey__(self,key):
        return key in self.__outside__

    def __islinked__(self,insidekey):
        return insidekey in self.__outside__.values()

    def __getkey__(self,key):
        try:
            return self.__outside__[key]
        except Exception as e:
            raise e

    def __getval__(self,insidekey):
        try:
            return self.__inside__[insidekey]
        except Exception as e:
            raise e

    def get(self,key,fallback=None):
        try:
            return self.__getitem__(key)
        except Exception:
            return fallback

    def __newentry__(self,keys,value):
        # creates a new key and value link
        keys = self.__makelist__(keys)


        insidekey = str(self.__counter__) + str(keys[0])
        self.__counter__ += 1

        self.__inside__[insidekey] = value

        for item in keys:
            if self.__islinked__(item):
                self.pop(item)
            self.__outside__[item] = insidekey

    def __addsibling__(self,key,newkeys):
        # adds another key to an existing value
        insidekey = self.__getkey__(key)
        newkeys = self.__makelist__(newkeys)

        for item in newkeys:
            if self.__islinked__(item):
                self.pop(item)
            self.__outside__[item] = insidekey
        
    def add(self, *args, **kwargs):
        return self.__addsibling__(*args, **kwargs)

    def pop(self,keys):
        # removes single outside key
        # if its the last outside key, remove the value entirely
        keys = self.__makelist__(keys)

        for key in keys:
            insidekey = self.__getkey__(key)
            del self.__outside__[key]
            if not self.__islinked__(insidekey):
                del self.__inside__[insidekey]

    def __updatevalue__(self,key,newvalue):
        insidekey = self.__getkey__(key)
        self.__inside__[insidekey] = newvalue

    def __remove__(self,key):
        # deletes value and all its related keys
        if type(key) == list:
            key = key[0]

        insidekey = self.__getkey__(key)
        for item in self.keys(key):
            del self.__outside__[item]
        del self.__inside__[insidekey]
    

    def keys(self,siblingof=None):
        if siblingof != None:
            out = []
            insidekey = self.__getkey__(siblingof)
            for item in self.__outside__:
                if self.__outside__[item] == insidekey: out.append(item)
            return tuple(out)
        else:
            return tuple(self.__outside__.keys())
    
    def pairkeys(self):
        out = []
        for key in self.export(duplicates=False):
            out.append(self.keys(key))
        return tuple(out)

    def values(self):
        return self.__inside__.values()

    def export(self,duplicates=True):
        if duplicates:
            return dict(self)
        else:
            used = set()
            out = {}
            for item in self.__outside__:
                insidekey = self.__getkey__(item)
                if insidekey not in used:
                    # else:
                    #     used.__addsibling__(insidekey)
                    out[item] = self.__getval__(insidekey)
                    used.add(insidekey)
            return out
