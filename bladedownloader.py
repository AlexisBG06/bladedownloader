import tkinter as tk
from tkinter import messagebox as m
import tkinter.filedialog
import os
import json
try:
    import asyncio
    import time
    from PIL import ImageTk, Image
    import appdirs
    from urllib.request import urlretrieve
    import app as music
except Exception as e:
    m.showinfo("Error", '{}: {}'.format(type(e).__name__, str(e)) )
    os.system('exit')


    
    
class App(tk.Frame):
    '''Represent the app itself.'''

    def __init__(self, master=None):
        '''Init the main settings.'''
        super().__init__(master)
        self.data = AppData()
        sizes = self.data.get("appsizes")
        self.x = sizes[0]
        self.y = sizes[1]
        self.pack()
        root.geometry("{}x{}".format(self.x, self.y))
        root["bg"] = "#00bdff"
        root.iconbitmap(self.data.path+"\\assets\\blade.ico")
        self.dir = self.data.get("folder")
        root.title = "Blade Downloader"
        if self.y >= self.x:
            self.mode = "portrait"
        else:
            self.mode = "landscape"


        

    def create_widgets(self):
        '''Initialize the widgets.'''
        sizes = self.get_proportions(100, 17)
        self.header=tk.Canvas(self,width=sizes[0],height=sizes[1],bg="#0000ff")
        self.header.pack()

        self.menu = tk.Menu(self, bg="black", fg="#00bdff")
        self.menu.add_command(label="QUIT", command=root.destroy)
        self.menu.add_command(label="DOWNLOAD SONGS", command=self.download_songs)
        self.menu.add_command(label="SELECT FOLDER", command=self.choose_dir)
        
        root.config(menu=self.menu)

        self.logo_sizes = [self.get_proportions(y=13.5)]
        self.logo_sizes.extend(self.get_proportions(x=1.5, y=2))
        self.logo = Image.open(self.data.path+"\\assets\\logo_white_borders.png")
        image = self.logo.resize((self.logo_sizes[0], self.logo_sizes[0]), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(image)
        self.header_thumbnail = self.header.create_image(self.logo_sizes[1], self.logo_sizes[2], image=self.img, anchor=tk.NW) 

        self.reinit_entry()

    def reinit_entry(self):
        '''Init / Reinit the app.entry.'''
        sizes = self.get_proportions(x=100, y=55)
        my_font = "arial 10".format()
        try:
            self.entry.destroy()
            del self.entry
            self.entry = tk.Text(root, width=int(sizes[0]/10), height=30, font=my_font)
            self.entry.pack()
        except:
            self.entry = tk.Text(root, width=int(sizes[0]/10), height=30, font=my_font)
            self.entry.pack()
            pass

    def update_sizes(self):
        '''Update widget sizes according to window sizes.'''
        self.x = root.winfo_width()
        self.y = root.winfo_height()
        if self.x > self.y:
            self.mode = "landscape"
        else:
            self.mode = "portrait"
        app.entry['width'] = int(app.get_proportions(x=100)/10)
        app.header["width"] = int(app.get_proportions(x=100))
        app.header["height"] = int(app.get_proportions(y=17))

        self.logo_sizes = [self.get_proportions(y=13.5)]
        self.logo_sizes.extend(self.get_proportions(x=1.5, y=2))
        image = self.logo.resize((self.logo_sizes[0], self.logo_sizes[0]), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(image)
        self.header_thumbnail = self.header.create_image(self.logo_sizes[1], self.logo_sizes[2], image=self.img, anchor=tk.NW) 


    def get_proportions(self, x=0, y=0):
        '''Return the nb of pixels for x and y being window-size percentages.'''
        sizes = (int(x*self.x/100), int(y*self.y/100))
        if y <= 0 and x > 0:
            return sizes[0]
        elif x <= 0 and y > 0:
            return sizes[1]
        else:
            return sizes

    def choose_dir(self):
        self.dir = tkinter.filedialog.askdirectory()   
        self.data.write("folder", self.dir)    


    def download_songs(self):
        for line in app.entry.get('1.0', 'end-1c').split("\n"):
            song = music.Song(line)
            song.download()
            song.convert(self.dir)


    async def mainloop(self):
        '''The mainloop of the app to keep it running and check for events.'''

        SizeUpdater = AppEvents(desc="Updates size on entry element", condition="root.winfo_width() != app.x or root.winfo_height() != app.y", action="app.update_sizes()")
        SizeUpdater.start()

        self.create_widgets()

        while True:
            await root.update()
            for event in list(AppEvents()):
                event.check()

class AppData:
    '''The app data handler class.'''
    datafolder = appdirs.user_data_dir("Blade", "Izorr").split("\\Izorr\\Blade")[0]
    def __init__(self, reinit=False):
        self.path = AppData.datafolder+"\\Blade"
        try:
            if reinit:
                os.rmdir(self.path)
            os.chdir(self.path)  
        except:
            os.chdir(AppData.datafolder)
            os.mkdir("Blade")
            os.chdir(self.path)
            os.mkdir("temp")
            os.mkdir("music")
            os.mkdir("assets")
            os.mkdir("data")
            content = {"theme":"classic","folder":"{}\\music".format(self.path),"format":"mp3","tags":True,"appsizes":(1000, 750)}
            with open('data/index.json', 'w') as outfile:
                json.dump(content, outfile)
            os.chdir(self.path+"\\assets")
            urlretrieve("https://fv9-2.failiem.lv/down.php?i=grdyf27b&download_checksum=02f05e4ca26acbef8e4da39eae01d5357f488dea&download_timestamp=1536769635", "logo_white_borders.png")
            urlretrieve("https://fv9-2.failiem.lv/down.php?i=ana4cah4&n=blade.ico&download_checksum=8d20c1c5cd66dfc944bf6b8a2d068313026f582e&download_timestamp=1536769895", "blade.ico")
            os.chdir(self.path)
            
        

    def write(self, key, value):
        try:
            with open("data/index.json", "r+") as x:
                content = json.load(x)
                content[key] = value
                x.seek(0) 
                json.dump(content, x) 
                x.truncate()
        except FileNotFoundError:
            self.__init__(reinit=True)
            self.write(key, value)
    
    def get(self, key):
        try:
            with open("data/index.json", "r") as x:
                content = json.load(x)
                return content[key]
        except FileNotFoundError:
            self.__init__(reinit=True)
            self.write(key, value)

class AppEvents:
    '''The app event registering class.'''
    events = []
    def __init__(self, desc="", condition="False", action="pass"):
        self.desc = desc
        self.condition = condition
        self.action = action


    def start(self):
        AppEvents.events.append(self)

    def stop(self):
        AppEvents.events.remove(self)

    def check(self):
        if eval(self.condition):
            exec(self.action)

    def __iter__(self):
        return iter(AppEvents.events)
    

      
#Root everything into the app class, into an asynchronous loop.
try:
    root = tk.Tk()
    app = App(master=root)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.mainloop())
except Exception as e:
    m.showinfo("Error", '{}: {}'.format(type(e).__name__, str(e)) )
    os.system('exit')



