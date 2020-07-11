import os, sqlite3,tkinter
#class library baraye gharar dadan e music ha dar library in kar ba copy kardan ahang anjam mishavad
class library:
    #dastor __init__ adrese music ra daryaft mikonad
    def __init__(self, MusicAdrress):
        self.MusicAdrress=MusicAdrress
        self.__Add()
    #ba dastore add music dar adresse e gherefte shode copy mishavad va dar library ba hamon name gharar dade mishavad
    #in function ba ejraye dastore __init__ va ijad object ejra mishavad
    def __Add(self):
        file=open(self.MusicAdrress, 'rb')
        list=self.MusicAdrress.split('\\')
        Musicname=list[len(list)-1]
        newMusic=open(os.getcwd()+"\\library"+"\\"+Musicname, 'wb')
        newMusic.write(file.read())
    @staticmethod
    #ba methode Delete music dar file e library hazf mishavad
    def Delete(FileName):
        os.remove(os.getcwd()+"\\library"+"\\"+FileName)
#class play list ke esm ahang ha ra dar PLAYLIST ke yek data base hast gharar midahad
class play_list:

    #method ahang ra be playlist ezafeh mikonad
    def __Add(self):
        try:
            Connection = sqlite3.connect(os.getcwd() + "\\PLAYLIST.db")
            Curser = Connection.cursor()
            Curser.execute("""CREATE TABLE IF NOT EXISTS PLAYLIST(
                 music char PRIMARY KEY,
                 TimeAdd char
                 );""")
            Query= """INSERT INTO PLAYLIST
                    (music, TimeAdd)
                    VALUES
                    (?,?)"""
            Curser.execute(Query, (self.MusicName, datetime.datetime.now()))
            Connection.commit()
            Curser.close()
            Connection.close()
        except:
            print("music already added")
    #method list mojod dar PLAYLIST ra bar migardanad
    def Show(self):
        try:
            Connection = sqlite3.connect(os.getcwd() + "\\PLAYLIST.db")
            Curser = Connection.cursor()
            Queray="select * from PLAYLIST;"
            Curser.execute(Queray)
            x=Curser.fetchall()
            Curser.close()
            Connection.close()
            return x
        except:
            print(f"eror: {sqlite3.Error}")
    #method ahang ra az PLAYLIST hazf mikonad
    def Delete(self, MusicName):
        try:
            Connection = sqlite3.connect(os.getcwd() + "\\PLAYLIST.db")
            Curser = Connection.cursor()
            Curser.execute('DELETE FROM PLAYLIST WHERE music=?', (MusicName,))
            Connection.commit()
            Curser.close()
            Connection.close()
        except:
            print(sqlite3.Error)

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

#ijade window
window = tkinter.Tk()
window.iconbitmap('image\\icon.ico')
window.geometry('800x700')
window.resizable(False, False)
#ijad image haye lazeme barname

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