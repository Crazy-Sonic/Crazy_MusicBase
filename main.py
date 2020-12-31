
import moduls.MySQL_Mbase as MDB

test = MDB.MySQL_Database('localhost', 'Musicbase', 'MB', 'Musicbase')

test.insert_track('Hey You', 'The Singer', '1840','High Tones','Folk', 2, '''D:\Musik\Hey You - The Singer.mp3''')# <--------- Slasches werden nicht mit eingetragen!