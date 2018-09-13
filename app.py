import urllib.request
import urllib.parse
import youtube_dl
import asyncio
import re
import os
from moviepy.audio.io.AudioFileClip import AudioFileClip



class InvalidSong(BaseException):
    '''Raised when the song is invalid.'''

class Song:
    '''Classifies input song name/link as song with several attr.'''
    def __init__(self, id):
        self.options = {'format': 'bestaudio/best', 'quiet':True}
        self.id = id
        
    def download(self):
        '''Download the song.'''

        #Get the song
        if "http" in self.id:
            self.song = self.id
        else:
            query_string = urllib.parse.urlencode({"search_query" : self.id})
            html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
            search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
            self.song = "http://www.youtube.com/watch?v=" + search_results[0]
        with youtube_dl.YoutubeDL(self.options) as ydl:
            info = ydl.extract_info(self.song, download=False)
        self.title = info["title"].replace(" x ", ", ").replace(" & ", ", ").replace(" X ", ", ")
        self.format = info["ext"]
        self.display = "{}.{}".format(self.title, self.format)
        self.options.update({"outtmpl":"temp\\" + self.display})

        #Download
        with youtube_dl.YoutubeDL(self.options) as ydl:
            ydl.download([self.song])

    def convert(self, dir):
        '''Convert to the right format.'''
        music = AudioFileClip("temp\\"+self.display)
        music.write_audiofile("{}\\{}.mp3".format(dir, self.title))






