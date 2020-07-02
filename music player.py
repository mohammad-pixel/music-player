import os, sqlite3, datetime
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
    #method esm ahang ke ezafe mishavad ra migirad
    def __init__(self, MusicName):
        self.MusicName=MusicName
        self.__Add()
    #method ahang av zamane gharar dadan ra be PLAYLIST add mikonad
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