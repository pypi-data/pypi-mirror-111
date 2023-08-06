import os
import math
import time
import queue
import random

try:
    from . import tools
except:
    import tools


try:
    import ffpyplayer.player
except:
    pass

try:
    import vlc
except:
    pass


def get_best_backend():
    """returns a AudioBackend instance thats deemed best for the system"""
    try:
        import vlc
        vlc.Instance()
        return VLCBackend()
    except:
        return FFPyPlayerBackend()


class AudioBackend():
    """
    AudioBackend provides a standardised way of integrating an audio backend in pYTerm.
    You can use the constructor on runtime to create backends on the fly, in case you want that for some reason, or you can implemenent all the functions under here
    
    args:
        get_name (callable): function simply return the backend name as a str. If a song is already playing, stop it and play this one.
        play (callable): function to run when a song needs to be played, must accept a str argument of an audio URL
        stop (callable): called when the song needs to stop playing. Takes no arguments.
        pause (callable): called when pYTerm is paused or unpaused, must accept a bool argument indicating the pause state, where True is paused and False is unpaused
        set_volume (callable): called when volume needs to be changed, must accept an int argument indicating the volume level, where 0 is silent. Note that an int bigger than 100 may be given, if the backend doesnt support this make sure to clamp the number.
        is_paused (callable): must return True if the player is paused, or False if the player is unpaused
        is_alive (callable): must return True if the player is capable of playing music at this moment: it is either playing or paused. Return False if the backend isn't capable of doing that at this time, for example if it's not been given audio yet, or still loading a song. Rule of thumb is: return false if its not playing or paused (alternatively: return false if calling any of the other functions might raise an exception due to the current state of the backend.)
        get_current_time (callable): return the elapsed play time of the current song in ms as int. if no song is playing, you can return 0
        get_total_time (callable): return the total play time of the current song in ms as int. if no song is playing, you can return 0
        get_volume (callable): return the current backend volume as int, where 0 is lowest and 100 is considered "normal max volume", although you are allowed to exceed this.
        get_progress (callable): return the current progress within a song as a float between 0.0 and 1.0. For example: the song is currently midway through playing: return 0.5. This may be calculated from the get_total_time and get_current_time, or the other way around. you can return 0.0 if is_alive is False
        set_progress (callable): set the backend's progress of the current song to the given progress (a float between 0.0 and 1.0) where 0.0 is the start of the song and 1.0 is the end. A valueError may be raised if the float exceeds these bounds or is_alive is False. 
        set_time (callable): set the current song elapsed time to x milliseconds. Must take an argument of type int as the milliseconds. If the backend doesn't support this it can be calculated with get_total_time and passed to set_progress, or the other way around.
    """
    def __init__(self,
                get_name,
                play,
                set_pause,
                set_volume,
                stop,
                is_paused,
                is_alive,
                get_current_time,
                get_total_time,
                get_volume,
                get_progress,
                set_progress,
                set_time,
                ):
        self.get_name = get_name
        self.play = play
        self.stop = stop
        self.set_pause = set_pause
        self.set_volume = set_volume
        self.is_paused = is_paused
        self.is_alive = is_alive
        self.get_current_time = get_current_time
        self.get_total_time = get_total_time
        self.get_volume = get_volume
        self.get_progress = get_progress
        self.set_progress = set_progress
        self.set_time = set_time

class VLCBackend(): 
    """VLC audio backend for pYTerm. Highly recommended but requires VLC media player to be installed"""
    def __init__(self):
        os.environ['VLC_VERBOSE'] = '-1'
        self.instance = vlc.Instance('--no-video', '--quiet', 'vout=none')
        self.player = self.instance.media_player_new()

    def get_name(self):
        return 'VLC'

    def play(self, url: str):
        if self.is_alive():
            self.player.stop()
        media = self.instance.media_new(url, 'vout=none', '--no-video')
        self.player.set_media(media)
        self.player.play()
    
    def stop(self):
        self.player.stop()

    def set_pause(self, state: bool):
        self.player.set_pause(int(state))
    
    def set_volume(self, volume: int):
        self.player.audio_set_volume(volume)

    def is_paused(self):
        if self.is_alive():
            return self.player.is_playing()
        else:
            return False

    def is_alive(self):
        try:
            if str(self.player.get_state()) == 'State.Playing' or str(
                    self.player.get_state()) == 'State.Paused':
                return True
            else:
                return False
        except Exception:
            return False
    
    def get_current_time(self):
        return self.player.get_time()
    
    def get_total_time(self):
        return self.player.get_length()

    def get_volume(self):
        return self.player.audio_get_volume()
    
    def get_progress(self):
        return self.player.get_position()

    def set_progress(self, progress: float):
        self.player.set_position(progress)

    def set_time(self, ms: int):
        self.player.set_time(ms)


class FFPyPlayerBackend():
    """FFPyPlayer audio backend for pYTerm. Experimental and unstable, but requires no extra installation"""
    def __init__(self):
        self.player = None
        self.timer = tools.ThreadedSoftwareTimer(-3,start=False)
        # self.lockids = 0

    def get_name(self):
        return 'FFPyPlayer'

    def play(self, url: str):
        # print('play','called')
        # # print('hi!',url)
        if self.is_alive():
            # print('grrr')
            #  self.waitAcquire()
            self.stop()
            #  self.release()
        # print('lets goo')
        #  self.waitAcquire()
        self.player = ffpyplayer.player.MediaPlayer(url, autoexit=True, loglevel='quiet')
        self.timer.restart(-3)
        # print('uwu')
        #  self.release()
    
    def stop(self):
        # print('stop','called')
        #  self.waitAcquire()
        self.player.close_player()
        self.timer.stop()
        self.player = None
        #  self.release()

    def set_pause(self, state: bool):
        # print('set_pause','called')
        #  self.waitAcquire()
        self.player.set_pause(state)
        self.timer.set_pause(state)
        #  self.release()
    
    def set_volume(self, volume: int):
        # print('set_volume','called')
        #  self.waitAcquire()
        self.player.set_volume(tools.clip(volume/100, 0.0, 1.0))
        #  self.release()

    def is_paused(self):
        # print('is_paused','called')
        if self.is_alive():
            #  self.waitAcquire()
            out = self.player.get_pause()
            #  self.release()
        else:
            out = False
        return out

    def is_alive(self):
        # print('is_alive','called')
        try:
            if self.player != None:
                if self.get_progress() < 1.0:
                    return True
        except Exception:
            # print('ffpy:',e)
            pass
        return False
    
    def get_current_time(self):
        # print('get_current_time','called')
        out = self.timer.get()
        return int(out*1000)
    
    def get_total_time(self):
        # print('get_totalt_time','called')
        #  self.waitAcquire()
        out = int(self.player.get_metadata()['duration']*1000)
        #  self.release()
        return out

    def get_volume(self):
        # print('get_volume','called')
        #  self.waitAcquire()
        out = int(100 * self.player.get_volume())
        #  self.release()
        return out
    
    def get_progress(self):
        # print('get_progres','called')
        out = (self.get_current_time() / self.get_total_time())
        return out

    def set_progress(self, progress: float):
        # print('set_progress','called')
        val = self.get_total_time()*progress
        #  self.waitAcquire()
        self.player.set_time()
        #  self.release()

    def set_time(self, ms: int):
        # print('set_time','called')
        #  self.waitAcquire()
        self.player.seek(ms/1000)
        self.timer.set_time(ms/1000)
        # self.player.set_time(round(self.get_current_time() + ms))
        #  self.release()
