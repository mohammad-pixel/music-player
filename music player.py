#pip install pygame
#pip install tinytag
#pip install PIL
import os, tkinter, tinytag, time, threading, random, pygame, sqlite3
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
#library listi baraye neghahdashtane esme ahang ha
import mutagen.mp3
library = os.listdir(r'library')
#playlist listi baraye neghah dashtane esme ahang haye zakhire dar playlist
playlist = []
#baraye neghahdashtane ahang ha tahte yek genre
genre = []
#baraye neghahdashtane ahang ha tahte yek artist
artist = []
#baraye neghahdashtane ahang ha tahte yek album
album = []

#method insert baraye poor kardan list haye genre artist va album
def insert():
    #in ghesmat library ra migardad va baraye har genre(ya artist ya album) yek list(zir list) dar list() genre ijad mikonad. aghar genre ahang vojod dasht be on ezafe mishavad dar gheir in sorat
    #list jadid dar genre(ya artist ya album) ijad mishavad
    for i in range(len(library)):
        flag = True
        x = tinytag.TinyTag.get('library\\' + library[i]).genre
        for j in range(len(genre)):
            if x in genre[j]:
                genre[j].append(library[i])
                flag = False
                break
        if flag:
            new = []
            new.append(x)
            new.append(library[i])
            genre.append(new)
        flag = True
        x = tinytag.TinyTag.get('library\\' + library[i]).artist
        for j in range(len(artist)):
            if x in artist[j]:
                artist[j].append(library[i])
                flag = False
                break
        if flag:
            new = []
            new.append(x)
            new.append(library[i])
            artist.append(new)
        flag = True
        x = tinytag.TinyTag.get('library\\' + library[i]).album
        for j in range(len(album)):
            if x in album[j]:
                album[j].append(library[i])
                flag = False
                break
        if flag:
            new = []
            new.append(x)
            new.append(library[i])
            album.append(new)


# class LIBRARY baraye gharar dadan e musicha dar library in kar ba copy kardan ahang anjam mishavad
class LIBRARY:
    #in ghesmat address ahang ra az karbar mighirad va yek copy dar library gharar midahad
    def Add(self):
        self.MusicAdrress = filedialog.askopenfilename()
        if self.MusicAdrress:
            file = open(self.MusicAdrress, 'rb')
            #in bakhsh esme ahang ra az akhare addresse ahang migirad
            s = self.MusicAdrress.split('/')
            Musicname = s[len(s) - 1]
            #in ghesmat check mikonad ke ahang dar lib
            if not Musicname in library:
                #ahang jadid ijad va motaviat ahang gherefte shode rikhte mishavad
                NewMusic = open(f'library\\{Musicname}', 'wb')
                NewMusic.write(file.read())
                #esme ahang jadid be library ezafe mishavad
                library.append(Musicname)
                #method baraye ezafeh kardan ahang ezafeh shodeh be genre, artist va album
                insert()
                #baraye ezafeh kardan ahang be listbox pakhsh
                Play.listbox.insert(len(library) - 1, Musicname)
                #pegham baraye namayesh anajam shodan amalyat
                messagebox.showinfo(message='music inserted to library')
            else:
                #pegham inke ahang ghablan ezafeh shode
                messagebox.showerror(message='music already added to library!')

    @staticmethod
    # ba methode Delete music dar file e library hazf mishavad
    def Delete():
        #ebtedah check mikonad ke ahang darhal pakhsh ast ya kheir
        if Play.Start:
            messagebox.showerror(message='please play a music')

        else:
            #az karbar darkhaste anjame amalyat ra darad
            answer = messagebox.askyesno(message='are you sure to delete this music?')
            if answer:
                #ebteda aghar ahang dar playlist hast on ra az playlist barmidarad
                Playlist.Delete()
                #chon nahveye hzf ahang az library ba yek ozv ba chand ozv fargh darad be do dste taghsim mishavad
                if len(library) > 1:
                    #indexe ahang feli ra daryaft mikonad
                    index = library.index(Play.list[Play.Track])
                    #pakhsh ra be ahang badi montaghel mikonad
                    buttonNext.invoke()
                    #ahang ra az library hzf mikonad
                    os.remove('library\\' + library[index])
                    library.remove(library[index])

                elif len(library) == 1:
                    #baraye inke betavan tanha ahang ra hzf krd bayad in dastor anjam shavad dar gheyre insorat nemitavan hzf krd
                    pygame.mixer.quit()
                    pygame.mixer.init()
                    #hzf kardan
                    os.remove('library\\' + library[0])
                    library.remove(library[0])
                    #barname ra be halat aval barghara mikonad
                    pygame.mixer.init()
                    Play.duration=0
                    Play.Start=True
                    Play.Play=True
                    Play.Running=False
                    button.config(image=ImagePlay)
                    Play.show_list()
                    Play.show_image()


# class play list ke esm ahang ha ra dar PLAYLIST ke yek data base hast gharar midahad
class play_list:
    #dar in ghesmat PLAYLIST.db ijad va aghar vojod darad vasl mishavad
    Connection = sqlite3.connect("PLAYLIST.db")
    Curser = Connection.cursor()
    #dar in ghesmat table PLAYLIST ighar vojod nadarad ijad mishavad
    Curser.execute("""CREATE TABLE IF NOT EXISTS PLAYLIST(
         music char PRIMARY KEY
         );""")
    Curser.close()
    Connection.close()

    # method ahang ra be PLAYLIST add mikonad
    def Add(self):
        #esme ahang ra az ahang jari library daryaft mikonad
        MusicName = Play.list[Play.Track]
        #aghar ahangi ejra nashode bashad az karbar mikhahad ke ejra konad
        if Play.Start:
            messagebox.showerror(message='please play a music')

        else:
            try:
                #dar in ghesmat esme ahang be playlist ezafe mishavad
                Connection = sqlite3.connect("PLAYLIST.db")
                Curser = Connection.cursor()

                Query = """INSERT INTO PLAYLIST
                          (music)
                          VALUES
                          (?)"""
                Curser.execute(Query, (MusicName,))
                Connection.commit()
                Curser.close()
                Connection.close()
                playlist.append(MusicName)
                messagebox.showinfo(message="song added to playlist")
                #aghar khata ijad shod yani ahang dar playlist gharar darad ya khataii digar vojod darad
            except:
                messagebox.showinfo(message="song alreay added to playlist or database removed")

    # method list mojod dar PLAYLIST ra bar migardanad
    def Show(self):
        try:
            Connection = sqlite3.connect("PLAYLIST.db")
            Curser = Connection.cursor()
            Queray = "select * from PLAYLIST;"
            Curser.execute(Queray)
            ShowPlayList = Curser.fetchall()
            Curser.close()
            Connection.close()
            return ShowPlayList
        #aghar khata ijad shod dar in sorat ya playlist khali hast ya vojod nadarad
        except:
            messagebox.showinfo(message='playlist is empty! or database removed')

    # method ahang ra az PLAYLIST hazf mikonad
    def Delete(self):
        if Play.Start:
            messagebox.showinfo(message="please play a music")
        else:
            #check mikonad ahang dar playlist hast ya kheir
            if Play.list[Play.Track] in playlist:
                Connection = sqlite3.connect("PLAYLIST.db")
                Curser = Connection.cursor()
                Curser.execute('DELETE FROM PLAYLIST WHERE music=?', (Play.list[Play.Track],))
                Connection.commit()
                Curser.close()
                Connection.close()
                #aghar karbar khodash ahang ra az playlist hazf karde bashad be o khabar midahad(aghar ahangi az library hzf shavad az playlist ham hzf mishavad)
                if Switch.switch:
                    messagebox.showinfo(message="song removed from playlist")
                #ahang az list playlist ham hzf mishavad
                playlist.remove(Play.list[Play.Track])
                #agahr playlist kamel khali shode bashad pakhsh be library montaghel mishavad
                if len(playlist) == 0:
                    Switch.switch = False
                    Switch.choose()
            elif Switch.switch:
                messagebox.showinfo(message='music is not added to playlist')

#mohemtarin class barname ke aksar karha ra manand play, pause, next, back,... va dar kol kar pakh va tanzim ahang va list kardan
class play:
    #baraye moshakhas kardan inke music darhal pakhsh hast ya kheir
    Play = True
    #baraye inke bebinad aya pakh ejra shode ya kheir
    Start = True
    #baraye ejraye nakh mojod dar barname
    StartT = True
    #baraye moshakhas kardan shuffle krd barname
    Repeat = False
    #ahang feli ke dar ebteda avali hast
    Track = 0
    #ahang tekrari pakhsh shavad ya kheir
    onRandom = False
    #ijad motaghayer ha va karhaye ebtedai barname baraye ejra
    def __init__(self):
        #say mikonad ke time e ahange aval ra bedast biarad
        try:
            self.duration = tinytag.TinyTag.get('library\\'+library[0]).duration
        except:
            self.duration = 0
        #moshakhasat e music
        self.title = ""
        self.artist = ""
        self.album = ""
        #list pakhsh pishfarz library hast
        self.list = library
        #nakh baraye ejraye seekbar barname
        self.t=threading.Thread(target=ScaleTime, daemon=True)

        mp3=mutagen.mp3.MP3('library\\'+self.list[self.Track])
        print(mp3.info.sample_rate)

        #init kardan mixer
        pygame.mixer.init()
        #neshan dadan list pakhsh barnameh
        self.show_list()
    #method baraye ejra avalie ya pause, play
    def play_pause(self):
        #dar ebteda check mikonad ke ahang dar listpakhsh hast ya kheyr
        if len(self.list) >= 1:
            #taghiir dadane Play ba click
            self.Play = not self.Play
            #aghar ahangh pause hast pakhsh mishavad
            if self.Play == True:
                #unpause kardan az ghesmati ke seekbar ghara darad chon momken hast kardar moghe pause seekbar ra jolo ya aghab karde bashad
                pygame.mixer.music.play(start=int(seek.get()))
                #taghiir aks dokme be pause
                button.config(image=ImagePause)
                button_ttp.text = 'pause'
            #aghar paksh shoro nashode ya pause hast
            else:
                #agahr pakhsh shoro nashode
                if self.Start == True:
                    #tasvir va text dokme be pause taghiir mikonad
                    button.config(image=ImagePause)
                    button_ttp.text = 'pause'
                    #Start az True(halat shoro pakhsh) bardashte mishavad
                    self.Start = False
                    #halat dar halate pakhsh True mishavad
                    self.Play = True
                    #agahr baraye avalin bar barname ejra mishavad nakhe t ejra mishavad
                    if self.StartT:
                        self.t.start()
                        self.StartT=False
                    #method insert seda zade mishavad
                    insert()
                    #ba in method ahang ejra mishavad
                    self.play()
                #aghar ahang darhal pakhsh hast pause mishavad
                else:
                    button.config(image=ImagePlay)
                    button_ttp.text = 'play'
                    pygame.mixer.music.pause()
        #ahangi dar listpakhsh nist
        else:

            answer = messagebox.askokcancel(message='Library is empty\ndo you want to add a music?')
            if answer:
                #ahang be library ezafe mishavad
                Library.Add()
                #liste pakhsh update mishavad
                Play.show_list()
    #method baraye pakhsh repeat
    def play_repeat(self):
        #taghiire halat ba click
        self.Repeat=not self.Repeat
        #aghar halat repeat bashad
        if self.Repeat:
            #dokme be halate cancel repeating taghiir mikonad
            buttonRepeat.config(image=ImageCancel)
            buttonRepeat_ttp.text = 'cancel repeating'
            #dokme be halat Repeat taghiir mikonad
        else:
            buttonRepeat.config(image=ImageRepeat)
            buttonRepeat_ttp.text = 'repeat'
    #baraye pakhsh ahang badi
    def play_next(self):
        if self.Play:
            #check mikonad ke halat shuffle hast ya kheir
            if self.onRandom and not self.Repeat:
                Shuffle = random.randint(0, len(self.list))
                while Shuffle == self.Track:
                    Shuffle = random.randint(0, len(self.list))
                self.Track = Shuffle
            #check mikonad ke halat Repeat hast ya kheir
            elif not self.Repeat:
                self.Track+=1
            #ahang pakhsh mishavad
            self.play()
    #baraye pakhshe ahange ghabli
    def play_pre(self):
        if self.Play:
            self.Track -= 1
            self.play()
    #baraye pakhshe halate shuffle
    def play_random(self):
        #taghiire halate onRandom ba click
        self.onRandom = not self.onRandom
        if self.onRandom:
            buttonRandom.config(image=ImageCancel)
        else:
            buttonRandom.config(image=ImageShuffle)
    #methode pakhshe ahang
    def play(self):
        #check mikonad ke Track az mahdode pakhsh kharej nashavad
        if self.Track >= len(self.list):
            self.Track = 0
        elif self.Track < 0:
            self.Track = len(self.list)-1
        #talash mikonad ke ahang ra load konad dar gheire insorat az karbar mikhahad in ahang hzf shavad
        try:
            pygame.mixer.music.load('library\\' + self.list[self.Track])
        except:
            answer = messagebox.askokcancel(message='this file cant play do you want to Delete it?')
            if answer:
                Library.Delete()
            else:
                self.Track += 1
                if self.Track >= len(self.list):
                    self.Track = 0
            pygame.mixer.music.load('library\\' + self.list[self.Track])
        #daryafte inform haye music
        self.__inform()
        #ejraye dobare seekbar
        seek.set(0)
        #update listbox(listpakhsh) chon momken hast liste pakhsh dochare taghiir shode bashad
        self.show_list()
        #neshan dadane ahange darhale pakhsh dar listbox
        self.listbox.yview_moveto(self.Track*self.listbox.yview()[1])
        self.highlight()
        #neshan dadane image album
        self.show_image()
        #va belakhare pakhshe ahang (cheghad tool keshid (:   )
        pygame.mixer.music.play()

    #metoode update informe ahange darhale pakhsh
    def __inform(self):

        try:
            self.duration = tinytag.TinyTag.get('library\\' + self.list[self.Track]).duration
        except:
            self.duration = 0
        try:
            self.title = tinytag.TinyTag.get('library\\' + self.list[self.Track]).title
        except:
            pass
        try:
            self.artist = tinytag.TinyTag.get('library\\' + self.list[self.Track]).artist
        except:
            pass
        try:
            self.album = tinytag.TinyTag.get('library\\' + self.list[self.Track]).album
        except:
            pass
        try:
            labeltotal.config(
                text=f'{int((self.duration // 60) // 10)}{int((self.duration // 60) % 10)} : {int((self.duration % 60) // 10)}{int((self.duration % 60) % 10)}')
        except:
            labeltotal.config(text='-- : --')
        label2.config(text=f'{self.title}___{self.artist}___{self.album}')

        seek.config(to=self.duration)
    #methode ijade listbox
    def show_list(self):
        #frame baraye gharar dadane listbox
        self.frame = tkinter.Frame(window)
        #ijade listbox
        self.listbox = tkinter.Listbox(self.frame, width=35, height=3, font=('arial', 15))
        #ijade scrolle listbox
        self.scroll = tkinter.Scrollbar(self.frame, orient='vertical')
        #ghara dadane frame
        self.frame.place(x=200, y=26)
        #etesale listbox va scroll
        self.scroll.config(command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scroll.set)
        # aghar liste pakhsh poor bashad, esme music be list box ezafe mishavad
        if len(self.list)>0:
            for i in range(1, len(self.list) + 1):
                self.listbox.insert(i, self.list[i - 1])
        #baraye entekhabe music dar listbox ke bayad double click shavad
        self.listbox.bind('<Double-1>', self.__choose)
        #mogheyade listbox va scroll
        self.listbox.pack(side='right', fill='y')
        self.scroll.pack(side='left', fill='y')
        #meghdare motagheyere listbox ke ba yek bar taghiire mogheyate do satre jari be dast mi ayad
        self.para = self.listbox.yview()[1]

    #methode entekhabe ahang az listbox
    def __choose(self, _):
        #ghereftane Track az radife entekhabie listbox(chon listbox tuple midahad meghdare listbox gherefte mishavad)
        self.Track = self.listbox.curselection()[0]
        #pakhshe music ba Track be daste amade
        self.play()
    #method baraye moshakhas kardane ahange dar hale pakhshe listbox
    def highlight(self):
        #bg ahange dar hale pakhsh black va fg ahang white mishavad
        self.listbox.itemconfig(self.Track, {'bg' : 'black'})
        self.listbox.itemconfig(self.Track, {'fg' : 'white'})
        #check mikanad baghie ahangh ha ra va fg ra black va bg ra white
        for i in range(len(self.list)):
            if i != self.Track:
                try:
                    self.listbox.itemconfig(i, {'bg': 'white'})
                    self.listbox.itemconfig(i, {'fg': 'black'})
                except:
                    pass
    #methode namayeshe album image
    def show_image(self):
        #agahr image ahang mojod bod dar gheire insorat image asli
        try:
            #chon image asli music ra nemitavan namayesh dad yek image dighar ba methode Image va ImageTk ba size e dorost va pasvande png ijad mishavad
            self.ImageData = tinytag.TinyTag.get('library\\' + self.list[self.Track], image=True).get_image()
            self.file = open('image\\ImageAlbum.png', 'wb')
            self.file.write(self.ImageData)
            self.Image = Image.open('image\\ImageAlbum.png')
            self.Image = self.Image.resize((800, 700), Image.ANTIALIAS)
            self.Image = ImageTk.PhotoImage(self.Image)
            label.config(image=self.Image)
        except:
            label.config(image=Imagebg)
#method baraye ijade Tooltip baraye widget ha(copy shode az internet :)    )
class CreateToolTip:
    """
    create a tooltip for a given widget
    """

    def __init__(self, widget, text):
        self.waittime = 50  # miliseconds
        self.wraplength = 100  # pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None
        self.lib = True

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 35
        y += self.widget.winfo_rooty() + 30
        # creates a toplevel window
        self.tw = tkinter.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tkinter.Label(self.tw, text=self.text, justify='left',
                              background="white", relief='solid', borderwidth=1,
                              wraplength=self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()

#class baraye taghiire meghdare seda
class click_volume:
    def __init__(self):
        #mogheiate inke seda tanzim shavad ya na
        self.on = True
        #meghdare pishfarze seda
        self.set = 100
    #methode taiine on
    def OpenClose(self):
        if self.on:
            #ijade scale baraye tanzim e seda
            self.scale = tkinter.Scale(window, from_=100, to=0, command=self.__volume)
            self.scale.set(self.set)
            self.scale.place(x=58, y=196)
            self.on = False
        else:
            #scale az safhe hazf mishavad
            self.set = self.scale.get()
            self.scale.destroy()
            self.on = True
    #methode taghiire meghdare volume
    def __volume(self, _):
        #meghdar ra az scale mighirad va tanzim mikonad
        Volume = int(self.scale.get())
        #tanzime image buttonVolume nesbat be sedaye tanzim shode
        if Volume == 0:
            buttonVolume.config(image=imgno)
        elif Volume >= 1 and Volume < 30:
            buttonVolume.config(image=imglow)
        elif Volume >= 30 and Volume < 70:
            buttonVolume.config(image=imgmid)
        elif Volume >= 70:
            buttonVolume.config(image=imgfull)
        #tanzim e seda
        pygame.mixer.music.set_volume(Volume / 100)
#class baraye menu samte chape barname(entekhabe playlist, library, hzf va ezafe kardan be library ya playlist)
class menu:

    def __init__(self):
        self.switch = False

    #taghiire vaziat be playlist ya library
    def Switch(self):
        self.switch = not self.switch
        #in button baraye pakhshe playlist ya library ijad mishavad
        self.buttonSwitch = tkinter.Button(window, image=ImageStart, command=self.choose, height=52, width=52,
                                           borderwidth=0)
        self.buttonSwitch_ttk = CreateToolTip(self.buttonSwitch, text="")
        self.buttonSwitch.place(x=56, y=22)

        #switch True ya False bashad(vaziat be library ya playlist) dokmehaye + va - va dokme e bala, nesbat be libarary ya playlist taghiir mikonad
        if self.switch:
            self.buttonSwitch_ttk.text = 'start playlist'
            buttonPlay.config(image=ImagePlaylist)
            buttonPlay_ttp.text = 'play list'
            buttonDelete_ttp.text = 'remove this music from play list'
            buttonPlus_ttp.text = 'add this  music to playlist'
            playlist = Playlist.Show()
            for i in range(len(playlist)):
                playlist[i] = playlist[i][0]

        else:

            self.buttonSwitch_ttk.text = 'start library'
            buttonPlay.config(image=ImageLibrary)
            buttonPlay_ttp.text = 'library'
            buttonDelete_ttp.text = 'delete this music from library'
            buttonPlus_ttp.text = 'add a music to library'
    #methode entekhabe pakhshe library ya playlist
    def choose(self):
        #aghar switch True bashad playlist pakhsh mishavad
        if Switch.switch:
            #check mikonad ke playlist poor hast ya kheir
            if len(playlist) >= 1:
                #talash mikonad musice dar playlist ra pakhsh konad dar gheir insorat music vojod nadarad pas peygham midahad
                try:
                    #taghiire liste pakhsh be playlist
                    Play.list = playlist
                    #taghiire Track be avale list
                    Play.Track = 0
                    #pakhshe music
                    Play.play()
                    #dokme switch hazf mishavad
                    Switch.buttonSwitch.destroy()
                except:
                    #choon playlist digar ghabele estenad nist az karbar mikhahad ke on ra hazf konad
                    answer = messagebox.askokcancel(
                        message='the music source music in play list\nnot exist maybe it deleted from\nother ways do you want to restore\n..........the play list')
                    if answer:
                        os.remove('PLAYLIST.db')
                        playlist.clear()
            else:
                messagebox.showerror(message='playlist is empty')
        #mesle bala faghat baraye library
        else:
            Play.list = library
            Play.Track = 0
            Play.play()
            Switch.buttonSwitch.destroy()
    #hazf kardan ke ya az library hazf mikonad ya az playlist remove mikonad
    def Delete(self):
        if self.switch:
            Playlist.Delete()

        else:
            Library.Delete()
    #add kardan ...
    def Add(self):
        if self.switch:
            Playlist.Add()

        else:
            Library.Add()
#ijad list box baraye entekhabe artist va pakhshe liste on artist
class showArtist:
    def __init__(self):
        #vaziat e ijad ya hazfe listboxe ijad shode
        self.on=False
        #methode ijad ya hazfe listbox
    def click(self):
        self.on=not self.on
        #aghar vaziat e on True bashad listbox ijad mishavad
        if self.on:
            #frame baraye gharar dadane listbox va scroll dar on
            self.frame=tkinter.Frame(window)
            self.frame.place(x=460, y=26)
            self.listbox = tkinter.Listbox(self.frame, width=35, height=4, font=('arial',9))
            #gharar dadane item haye liste artist dar list box
            for i in range(len(artist)):
                self.listbox.insert(i+1, artist[i][0])
            self.listbox.bind('<Double-1>', self.play)
            self.listbox.pack(side="left", fill="y")
            self.scroll=tkinter.Scrollbar(self.frame, command=self.listbox.yview, orient="vertical")
            self.scroll.pack(side="right", fill="y")
            self.listbox.config(yscrollcommand=self.scroll.set)
            #aghar dokme artist zade shavad ba click dobare mishavd listbox ra bardasht va image cancel bekhatere hamin gharar dade mishavad roye buttonArtist
            buttonArtist.config(image=ImageCancel)
        #aghar on False bashad listbox, scroll va frame haz mishavad
        else:
            self.frame.destroy()
            self.listbox.destroy()
            self.scroll.destroy()
            #update image e button be image asli
            buttonArtist.config(image=ImageArtist)
    #aghar yek radife listbox entekhab shavad music haye on artist pakhsh mishavad
    def play(self, _):
        #update liste pakhsh be on artist(choon ma esme ahang ha ra mikhahim va meghdare 0 artist esme Artist(esme list)
        # hast az indexe 1 ta akhar ra dar liste pakhsh rikhte mishavad)
        Play.list=artist[self.listbox.curselection()[0]][1:]
        #ebtedaye list
        Play.Track=0
        #update liste pakhsh
        Play.show_list()
        #aghar ahanghi hanoz pakhsh nashode dokme pakhsh zade shavad
        #dar gheire insorat ahang pakhsh shavad
        if Play.Start:
            button.invoke()
        else:
            Play.play()
        #ba entekhabe artist listbox va ... hazf shavad
        self.frame.destroy()
        self.listbox.destroy()
        self.scroll.destroy()
        self.on=False
        buttonArtist.config(image=ImageArtist)

class showAlbum:
    def __init__(self):
        self.on = False

    def click(self):
        self.on = not self.on
        if self.on:
            self.frame = tkinter.Frame(window)
            self.frame.place(x=460, y=26)
            self.listbox = tkinter.Listbox(self.frame, width=35, height=4, font=('arial', 9))
            for i in range(len(album)):
                self.listbox.insert(i + 1, album[i][0])
            self.listbox.bind('<Double-1>', self.play)
            self.listbox.pack(side="left", fill="y")
            self.scroll = tkinter.Scrollbar(self.frame, command=self.listbox.yview, orient="vertical")
            self.scroll.pack(side="right", fill="y")
            self.listbox.config(yscrollcommand=self.scroll.set)
            buttonAlbum.config(image=ImageCancel)
        else:
            self.frame.destroy()
            self.listbox.destroy()
            self.scroll.destroy()
            buttonAlbum.config(image=ImageAlbum)

    def play(self, _):
        Play.list = album[self.listbox.curselection()[0]][1:]
        Play.onRandom = False
        Play.show_list()
        Play.Track = 0
        if Play.Start:
            Play.play_pause()
        else:
            Play.play_next()
        self.frame.destroy()
        self.listbox.destroy()
        self.scroll.destroy()
        self.on = False
        buttonAlbum.config(image=ImageAlbum)

#mesle artist...
class showGenre:
    def __init__(self):
        self.on = False

    def click(self):
        self.on = not self.on
        if self.on:
            self.frame = tkinter.Frame(window)
            self.frame.place(x=460, y=26)
            self.listbox = tkinter.Listbox(self.frame, width=35, height=4, font=('arial', 9))
            for i in range(len(genre)):
                self.listbox.insert(i + 1, genre[i][0])
            self.listbox.bind('<Double-1>', self.play)
            self.listbox.pack(side="left", fill="y")
            self.scroll = tkinter.Scrollbar(self.frame, command=self.listbox.yview, orient="vertical")
            self.scroll.pack(side="right", fill="y")
            self.listbox.config(yscrollcommand=self.scroll.set)
            buttonGenre.config(image=ImageCancel)
        else:
            self.frame.destroy()
            self.listbox.destroy()
            self.scroll.destroy()
            buttonGenre.config(image=ImageGenre)

    def play(self, _):
        Play.list = genre[self.listbox.curselection()[0]][1:]
        Play.onRandom = False
        Play.show_list()
        Play.Track = 0
        if Play.Start:
            Play.play_pause()
        else:
            Play.play_next()
        self.frame.destroy()
        self.listbox.destroy()
        self.scroll.destroy()
        self.on = False
        buttonGenre.config(image=ImageGenre)
#in methode baraye namayeshe zaman va neshan dadane lahze pakhas
def ScaleTime():

    while True:
        #update duration music(aghar music avaz shod)
        duration = int(Play.duration)
        #check konad ke music dar hale pakhsh hast ya kheyr aghar pause hast jolo raftan time stop shavad
        if Play.Play:

            #meghdare seek bar har lahze az meghdare ghabli be ezafe yek bedast miayad
            seek.set(int(seek.get())+1)
            #bedast avardane min va sec e muisc baraye namayesh dadan
            mins, secs=divmod(int(seek.get()), 60)
            mins=int(mins)
            secs=int(secs)
            #namayesh dadane min va sec e music aghar musici pakhsh mishavad zaman neshan dadae shavad
            #dar gheire insorat zaman neshan dade nashavad
            if mins!=0 or secs!=0:
                labelcurrent.config(text='{:02d} : {:02d}'.format(mins, secs))
            else:
                labelcurrent.config(text='-- : --')
            #jolo raftan har yek sec
            time.sleep(1)
            #aghar music tamom shod music badi pakhsh shavad
            if int(seek.get())==int(duration):
                #aghar list khali shode bashad zamani neshan dade shavad
                if len(Play.list)==0:
                    labeltotal.config(text='-- : --')
                    labelcurrent.config(text='-- : --')
                    Play.play_pause()
                #dokme ahange badi zade shavad
                else:
                    buttonNext.invoke()
#method baraye raftan be lahze entekhabi dar seek bar
def goto(_):
    if Play.Play:
        pygame.mixer.music.play(start=int(seek.get()))
#ijade window
window = tkinter.Tk()
window.iconbitmap('image\\icon.ico')
window.geometry('800x700')
window.resizable(False, False)
#ijade object az class haye ijad shode
Library = LIBRARY()
Playlist = play_list()
Play = play()
Volume = click_volume()
Switch = menu()
Artist = showArtist()
Album = showAlbum()
Genre = showGenre()
#image haye lazem dar barname
Imagebg = tkinter.PhotoImage(file='image\\Imagebg.png')
imgfull = tkinter.PhotoImage(file='image\\full.png')
imgno = tkinter.PhotoImage(file='image\\empty.png')
imgmid = tkinter.PhotoImage(file='image\\mid.png')
imglow = tkinter.PhotoImage(file='image\\low.png')
ImagePlay = tkinter.PhotoImage(file='image\\play.png')
ImagePause = tkinter.PhotoImage(file='image\\pause.png')
ImageRepeat = tkinter.PhotoImage(file='image\\repeat.png')
ImageCancel = tkinter.PhotoImage(file='image\\cancel.png')
ImageLibrary = tkinter.PhotoImage(file='image\\library.png')
ImagePlaylist = tkinter.PhotoImage(file='image\\playlist.png')
ImagePlus = tkinter.PhotoImage(file='image\\plus.png')
ImageDelete = tkinter.PhotoImage(file='image\\delete.png')
ImageNext = tkinter.PhotoImage(file='image\\next.png')
ImagePrevious = tkinter.PhotoImage(file='image\\previous.png')
ImageStart = tkinter.PhotoImage(file='image\\start.png')
ImageList = tkinter.PhotoImage(file='image\\list.png')
ImageArtist = tkinter.PhotoImage(file='image\\artist.png')
ImageAlbum = tkinter.PhotoImage(file='image\\album.png')
ImageGenre = tkinter.PhotoImage(file='image\\genre.png')
ImageShuffle = tkinter.PhotoImage(file='image\\shuffle.png')
#label ha baraye namayesh e etelaat
label = tkinter.Label(window, image=Imagebg, width=800, height=700)
label.pack()

label2 = tkinter.Label(window, text='Title\t\t Artist\t\t Album', width=100, height=1, font=('arial', 10), bg='black',fg='white')
label2_ttp = CreateToolTip(label2, text='music info')
label2.place(x=0, y=0)

labeltotal = tkinter.Label(window, text=f'-- : --', font=('arial', 10), bg='black', fg='white')
labeltotal_ttp = CreateToolTip(labeltotal, text='total time')
labeltotal.place(x=416, y=530)

labelcurrent = tkinter.Label(window, text='-- : --', font=('arial', 10), bg='black', fg='white')
labelcurrent_ttp = CreateToolTip(labelcurrent, text='current time')
labelcurrent.place(x=346, y=530)
#seek bar
seek= tkinter.Scale(window, from_=0, to=Play.duration, bg='black', orient='horizontal', length=790, width=10 , sliderlength=10, troughcolor='white', highlightbackground='green', activebackground='green')
seek_ttp = CreateToolTip(seek, text='seek')
seek.place(x=1, y=550)
seek.bind('<B1-Motion>' , goto)
#dokme haye barname
button = tkinter.Button(window, image=ImagePlay, command=Play.play_pause, height=52, width=52, borderwidth=0)
button_ttp = CreateToolTip(button, text='play')
button.place(x=374, y=600)

buttonVolume = tkinter.Button(window, image=imgmid, command=Volume.OpenClose, height=52, width=52, borderwidth=0)
buttonVolume_ttp = CreateToolTip(buttonVolume, text='volume')
buttonVolume.place(x=0, y=196)

buttonRepeat = tkinter.Button(window, image=ImageRepeat, command=Play.play_repeat, height=52, width=52, borderwidth=0)
buttonRepeat_ttp = CreateToolTip(buttonRepeat, text='repeat')
buttonRepeat.place(x=530, y=600)

buttonPlay = tkinter.Button(window, image=ImageLibrary, command=Switch.Switch, height=52, width=52, borderwidth=0)
buttonPlay_ttp = CreateToolTip(buttonPlay, text='library')
buttonPlay.place(x=0, y=22)

buttonDelete = tkinter.Button(window, image=ImageDelete, command=Switch.Delete, height=52, width=52, borderwidth=0)
buttonDelete_ttp = CreateToolTip(buttonDelete, text='delete this music from library')
buttonDelete.place(x=0, y=80)

buttonPlus = tkinter.Button(window, image=ImagePlus, command=Switch.Add, height=52, width=52, borderwidth=0)
buttonPlus_ttp = CreateToolTip(buttonPlus, text='add a music to library')
buttonPlus.place(x=0, y=138)

buttonNext = tkinter.Button(window, image=ImageNext, command=Play.play_next, height=52, width=52, borderwidth=0)
buttonNext_ttp = CreateToolTip(buttonNext, text='next')
buttonNext.place(x=450, y=600)

buttonPrevious = tkinter.Button(window, image=ImagePrevious, command=Play.play_pre, height=52, width=52, borderwidth=0)
buttonPrevious_ttp = CreateToolTip(buttonPrevious, text='back')
buttonPrevious.place(x=300, y=600)

buttonArtist = tkinter.Button(window, image=ImageArtist, command=Artist.click, height=52, width=52, borderwidth=0)
buttonArtist_ttk = CreateToolTip(buttonArtist, text='artist')
buttonArtist.place(x=748, y=22)

buttonAlbum = tkinter.Button(window, image=ImageAlbum, command=Album.click, height=52, width=52, borderwidth=0)
buttonAlbum_ttk = CreateToolTip(buttonAlbum, text='album')
buttonAlbum.place(x=748, y=80)

buttonGenre = tkinter.Button(window, image=ImageGenre, command=Genre.click, height=52, width=52, borderwidth=0)
buttonGenre_ttk = CreateToolTip(buttonGenre, text='genre')
buttonGenre.place(x=748, y=138)

buttonRandom = tkinter.Button(window, image=ImageShuffle, command=Play.play_random, height=52, width=52, borderwidth=0)
buttonRandom_ttp = CreateToolTip(buttonRandom, text='random')
buttonRandom.place(x=225, y=600)

window.mainloop()