import sqlite3


class MusicDB:

    def __init__(self, db_Path="music.lib"):
        self.db_Path = db_Path
        self.db_Handle = [sqlite3.connect(self.db_Path)]
        self.db_Handle.append(self.db_Handle[0].cursor())



        self.dbcmd_crt_genres = '''CREATE TABLE IF NOT EXISTS Genres (
                                "ID" INTEGER,
                                "Name"	TEXT,
                                PRIMARY KEY("ID" AUTOINCREMENT)); '''

        self.dbcmd_crt_interpr = '''CREATE TABLE IF NOT EXISTS "Interpreten" (
                                "ID"	INTEGER, 
                                "Name"	TEXT,
                                PRIMARY KEY("ID" AUTOINCREMENT));'''

        self.dbcmd_crt_playl = '''CREATE TABLE IF NOT EXISTS "Playlisten" (
                                "ID"	INTEGER,
                                "Name"	TEXT NOT NULL, 
                                "Erstellt am"	NUMERIC NOT NULL,
                                "Kommentar" TEXT,"Quelle"	TEXT,
                                "Bewertung" INTEGER,
                                PRIMARY KEY("ID" AUTOINCREMENT));'''

        self.dbcmd_crt_playl_inh = '''CREATE TABLE IF NOT EXISTS "Playlisten_Inhalt" (
                                    "ID"	INTEGER,
                                    "Playlist"	INTEGER,
                                    "Titel"	INTEGER,
                                    FOREIGN KEY("Titel") REFERENCES "Titel"("ID"),
                                    FOREIGN KEY("Playlist") REFERENCES "Playlisten"("ID"),
                                    PRIMARY KEY("ID" AUTOINCREMENT));'''

        self.dbcmd_crt_playl_titel = '''
                                    CREATE TABLE IF NOT EXISTS "Titel" (
                                    "ID"	INTEGER,
                                    "Titel_Name"	TEXT,
                                    "Interpret"	INTEGER,
                                    "Erscheinungsjahr"	INTEGER,
                                    "Album"	TEXT,
                                    "Genre"	INTEGER,
                                    "Bewertung"	INTEGER,
                                    "Path" TEXT,
                                    FOREIGN KEY("Genre") REFERENCES "Genres"("ID"),
                                    FOREIGN KEY("Interpret") REFERENCES "Interpreten"("ID"),
                                    PRIMARY KEY("ID" AUTOINCREMENT));'''

        self.db_Handle[1].execute(self.dbcmd_crt_genres)
        self.db_Handle[1].execute(self.dbcmd_crt_interpr)
        self.db_Handle[1].execute(self.dbcmd_crt_playl)
        self.db_Handle[1].execute(self.dbcmd_crt_playl_inh)
        self.db_Handle[1].execute(self.dbcmd_crt_playl_titel)
        self.db_Handle[0].commit()

    def insert_genre(self, name):
        dbcmd_cnt = """SELECT count(*) FROM Genres WHERE Name = '%s';""" % (name.capitalize(),)
        dbcmd_ins = """INSERT INTO Genres VALUES (NULL, '%s');""" % (name.capitalize(),)
        dbcmd_chk = """SELECT ID FROM Genres WHERE Name = '%s';""" % (name.capitalize(),)
        self.db_Handle[1].execute(dbcmd_cnt)
        if (self.db_Handle[1].fetchall()[0][0] < 1):
            self.db_Handle[1].execute(dbcmd_ins)
            self.db_Handle[0].commit()
        self.db_Handle[1].execute(dbcmd_chk)
        return int(self.db_Handle[1].fetchall()[0][0])

    def insert_interpret(self, name):
        dbcmd_cnt = """SELECT count(*) FROM Interpreten WHERE Name = '%s';""" % (name.capitalize(),)
        dbcmd_ins = """INSERT INTO Interpreten VALUES (NULL,'%s');""" % (name.capitalize(),)
        dbcmd_chk = """SELECT ID FROM Interpreten WHERE Name = '%s';""" % (name.capitalize(),)
        self.db_Handle[1].execute(dbcmd_cnt)
        if (self.db_Handle[1].fetchall()[0][0] < 1):
            self.db_Handle[1].execute(dbcmd_ins)
            self.db_Handle[0].commit()
        self.db_Handle[1].execute(dbcmd_chk)
        return int(self.db_Handle[1].fetchall()[0][0])

    def insert_playlist(self, name, create_date, comment, source, rate):
        dbcmd_cnt = """SELECT count(*) FROM Playlist WHERE Name = '%s';""" % (name,)
        dbcmd_ins = """INSERT INTO Playlist ('Name') VALUES (NULL, '%s', '%s', '%s', '%s', '%s');""" % (name, create_date, comment, source, rate)
        dbcmd_chk = """SELECT ID FROM Playlist WHERE Name = '%s';""" % (name,)
        self.db_Handle[1].execute(dbcmd_cnt)
        if (self.db_Handle[1].fetchall()[0][0] < 1):
            self.db_Handle[1].execute(dbcmd_ins)
            self.db_Handle[0].commit()
        self.db_Handle[1].execute(dbcmd_chk)
        return self.db_Handle[1].fetchall()[0][0]

    def get_playlistid(self, name):
        dbcmd_chk = """SELECT ID FROM Playlist WHERE Name = '%s';""" % (name,)
        self.db_Handle[1].execute(dbcmd_chk)
        return self.db_Handle[1].fetchall()[0][0]

    def insert_track(self, name, interpret, releaseyear, album, genre, rate, path):
        tmp_interpret = self.insert_interpret(interpret)
        tmp_genre = self.insert_genre(genre)
        dbcmd_ins = """INSERT INTO Titel VALUES (NULL, '%s', '%s', '%s', '%s', '%s', '%s', '%s');""" % (name, tmp_interpret, releaseyear, album, tmp_genre, rate, path)
        self.db_Handle[1].execute(dbcmd_ins)
        self.db_Handle[0].commit()

    def get_trackid(self, name, interpret):
        dbcmd_chk = """SELECT ID FROM Titel WHERE Name = '%s' AND Interpret = '%s';""" % (name,interpret)
        self.db_Handle[1].execute(dbcmd_chk)
        return self.db_Handle[1].fetchall()[0][0]

    def fill_playlist(self, playlist, titel, interpret):
        dbcmd_ins = """INSERT INTO Playlisten_Inhalt VALUES (NULL, '%s', '%s');""" % (self.get_playlistid(playlist), self.get_trackid(titel, interpret))
        self.db_Handle[1].execute(dbcmd_ins)
        self.db_Handle[0].commit()

    def get_track_path(self, name, interpret):
        dbcmd_chk = """SELECT ID FROM Titel WHERE Name = '%s' AND Interpret = '%s';""" % (name,interpret)
        self.db_Handle[1].execute(dbcmd_chk)
        return self.db_Handle[1].fetchall()[0][0]

    def get_m3u_info(self, playlist):
        pass

    def __del__(self):
        self.db_Handle[0].close()




