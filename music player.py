import os
#class library baraye gharar dadan e ahang ha dar library proje in kar ba copy kardan ahang anjam mishavad
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