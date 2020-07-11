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