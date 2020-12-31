import mysql.connector


class MySQL_Database:

    def __init__(self, db_host="localhost", db_user="Musicbase", db_pwd="MB", db_name="Musicbase"):
        self.db_host = db_host
        self.db_user = db_user
        self.db_pwd = db_pwd
        self.db_name = db_name
        self.db_Handle = [mysql.connector.connect(host=self.db_host, user=self.db_user, password=self.db_pwd, database=self.db_name)]
        self.db_Handle.append(self.db_Handle[0].cursor())

        self.dbcmd_crt_genres = '''CREATE TABLE IF NOT EXISTS `genres` (
                                `Genre_ID` int(11) NOT NULL AUTO_INCREMENT,
                                `Genre_Name` varchar(255) COLLATE latin1_general_cs NOT NULL,
                                PRIMARY KEY (`Genre_ID`)
                                ) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_cs;'''

        self.dbcmd_crt_artists = '''CREATE TABLE IF NOT EXISTS `artists` (
                                `Artist_ID` int(11) NOT NULL AUTO_INCREMENT,
                                `Artist_Name` varchar(255) COLLATE latin1_general_cs NOT NULL,
                                PRIMARY KEY (`Artist_ID`)
                                ) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_cs; '''

        self.dbcmd_crt_playl = '''CREATE TABLE IF NOT EXISTS `playlists` (
                                `Playlist_ID` int(11) NOT NULL AUTO_INCREMENT,
                                `Playlist_Name` varchar(255) COLLATE latin1_general_cs NOT NULL,
                                `Playlist_Createdate` date NOT NULL,
                                `Playlist_Comment` varchar(255) COLLATE latin1_general_cs NOT NULL,
                                `Playlist_Rating` int(11) NOT NULL,
                                `Source_ID` int(11) NOT NULL,
                                PRIMARY KEY (`Playlist_ID`),
                                KEY `Source_ID` (`Source_ID`),
                                CONSTRAINT `playlists_ibfk_1` FOREIGN KEY (`Source_ID`) REFERENCES `sources` (`Source_ID`)
                                ) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_cs; '''

        self.dbcmd_crt_playl_cont = '''CREATE TABLE IF NOT EXISTS `playlist_content` (
                                    `Playlist_content_ID` int(11) NOT NULL AUTO_INCREMENT,
                                    `Playlist_ID` int(11) NOT NULL,
                                    `Track_ID` int(11) DEFAULT NULL,
                                    `Playlist_content_Track` varchar(255) COLLATE latin1_general_cs NOT NULL,
                                    `Playlist_content_Artist` varchar(255) COLLATE latin1_general_cs NOT NULL,
                                    PRIMARY KEY (`Playlist_content_ID`),
                                    KEY `Playlist_ID` (`Playlist_ID`),
                                    KEY `Track_ID` (`Track_ID`),
                                    CONSTRAINT `playlist_content_ibfk_1` FOREIGN KEY (`Track_ID`) REFERENCES `tracks` (`Track_ID`),
                                    CONSTRAINT `playlist_content_ibfk_2` FOREIGN KEY (`Playlist_ID`) REFERENCES `playlists` (`Playlist_ID`)
                                    ) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_cs;'''

        self.dbcmd_crt_playl_track = '''CREATE TABLE IF NOT EXISTS `tracks` (
                                        `Track_ID` int(11) NOT NULL AUTO_INCREMENT,
                                        `Track_Name` varchar(255) COLLATE latin1_general_cs NOT NULL,
                                        `Artist_ID` int(11) NOT NULL,
                                        `Releasedate` date NOT NULL,
                                        `Genre_ID` int(11) NOT NULL,
                                        `Track_Rating` int(11) NOT NULL,
                                        `Track_Path` varchar(512) COLLATE latin1_general_cs NOT NULL,
                                        `Album` varchar(255) COLLATE latin1_general_cs NOT NULL,
                                        PRIMARY KEY (`Track_ID`),
                                        KEY `Genre_ID` (`Genre_ID`),
                                        KEY `Artist_ID` (`Artist_ID`),
                                        CONSTRAINT `tracks_ibfk_1` FOREIGN KEY (`Genre_ID`) REFERENCES `genres` (`Genre_ID`) ON DELETE NO ACTION ON UPDATE CASCADE,
                                        CONSTRAINT `tracks_ibfk_2` FOREIGN KEY (`Artist_ID`) REFERENCES `artists` (`Artist_ID`)
                                        ) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_cs;'''

        self.dbcmd_crt_sources = '''CREATE TABLE IF NOT EXISTS `sources` (
                                        `Source_ID` int(11) NOT NULL AUTO_INCREMENT,
                                        `Source_Name` int(11) NOT NULL,
                                        `Source_comment` varchar(512) COLLATE latin1_general_cs NOT NULL,
                                        `Source_Adress` varchar(255) COLLATE latin1_general_cs NOT NULL,
                                        PRIMARY KEY (`Source_ID`)
                                        ) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_cs'''

        self.db_Handle[1].execute(self.dbcmd_crt_genres)
        self.db_Handle[1].execute(self.dbcmd_crt_artists)
        self.db_Handle[1].execute(self.dbcmd_crt_playl)
        self.db_Handle[1].execute(self.dbcmd_crt_playl_cont)
        self.db_Handle[1].execute(self.dbcmd_crt_playl_track)
        self.db_Handle[1].execute(self.dbcmd_crt_sources)
        self.db_Handle[0].commit()

    def insert_genre(self, name):
        dbcmd_cnt = """SELECT count(*) FROM Genres WHERE Genre_Name = '%s';""" % (name.capitalize(),)
        dbcmd_ins = """INSERT INTO Genres VALUES (NULL, '%s');""" % (name.capitalize(),)
        dbcmd_chk = """SELECT Genre_ID FROM Genres WHERE Genre_Name = '%s';""" % (name.capitalize(),)
        self.db_Handle[1].execute(dbcmd_cnt)
        if (self.db_Handle[1].fetchall()[0][0] < 1):
            self.db_Handle[1].execute(dbcmd_ins)
            self.db_Handle[0].commit()
        self.db_Handle[1].execute(dbcmd_chk)
        return int(self.db_Handle[1].fetchall()[0][0])

    def get_genre_id(self, name):
        dbcmd_chk = """SELECT Genre_ID FROM Genres WHERE Genre_Name = '%s';""" % (name.capitalize(),)
        self.db_Handle[1].execute(dbcmd_chk)
        return int(self.db_Handle[1].fetchall()[0][0])

    def insert_artist(self, name):
        dbcmd_cnt = """SELECT count(*) FROM artists WHERE Artist_Name = '%s';""" % (name.capitalize(),)
        dbcmd_ins = """INSERT INTO artists VALUES (NULL,'%s');""" % (name.capitalize(),)
        dbcmd_chk = """SELECT Artist_ID FROM artists WHERE Artist_Name = '%s';""" % (name.capitalize(),)
        self.db_Handle[1].execute(dbcmd_cnt)
        if (self.db_Handle[1].fetchall()[0][0] < 1):
            self.db_Handle[1].execute(dbcmd_ins)
            self.db_Handle[0].commit()
        self.db_Handle[1].execute(dbcmd_chk)
        return int(self.db_Handle[1].fetchall()[0][0])

    def get_artist_id(self, name):
        dbcmd_chk = """SELECT Artist_ID FROM artists WHERE Artist_Name = '%s';""" % (name.capitalize(),)
        self.db_Handle[1].execute(dbcmd_chk)
        return int(self.db_Handle[1].fetchall()[0][0])

    def insert_playlist(self, name, create_date, comment, source, rate):
        dbcmd_cnt = """SELECT count(*) FROM Playlist WHERE Playlist_Name = '%s';""" % (name,)
        dbcmd_ins = """INSERT INTO Playlist VALUES (NULL, '%s', '%s', '%s', '%s', '%s');""" % (name, create_date, comment, rate, source)
        dbcmd_chk = """SELECT Playlist_ID FROM Playlist WHERE Playlist_Name = '%s';""" % (name,)
        self.db_Handle[1].execute(dbcmd_cnt)
        if (self.db_Handle[1].fetchall()[0][0] < 1):
            self.db_Handle[1].execute(dbcmd_ins)
            self.db_Handle[0].commit()
        self.db_Handle[1].execute(dbcmd_chk)
        return self.db_Handle[1].fetchall()[0][0]


    def get_playlistid(self, name):
        dbcmd_chk = """SELECT Playlist_ID FROM Playlist WHERE Playlist_Name = '%s';""" % (name,)
        self.db_Handle[1].execute(dbcmd_chk)
        return self.db_Handle[1].fetchall()[0][0]

    def insert_track(self, name, artist, releasedate, album, genre, rate, path):
        tmp_artist = self.insert_artist(artist)
        tmp_genre = self.insert_genre(genre)
        dbcmd_ins = """INSERT INTO tracks VALUES (NULL, '%s', '%s', '%s', '%s', '%s', '%s', '%s');""" % (name, tmp_artist, releasedate, tmp_genre, rate, path, album)
        print(dbcmd_ins)
        self.db_Handle[1].execute(dbcmd_ins)
        self.db_Handle[0].commit()

    def get_track_id(self, name, artist):
        tmp_artist = self.get_artist_id(artist)
        dbcmd_chk = """SELECT track_id FROM tracks WHERE Artist_ID = '%s' AND Track_Name = '%s';""" % (tmp_artist, name.capitalize(),)
        self.db_Handle[1].execute(dbcmd_chk)
        return (self.db_Handle[1].fetchall()[0])

    def insert_playlist_content(self, playlist, track, artist):
        dbcmd_cnt = """SELECT count(*) FROM playlist_content WHERE Playlist_ID = '%s' AND Playlist_content_Track = '%s' AND Playlist_content_Artist = '%s' ;""" % (self.get_playlistid(playlist), track, artist)
        dbcmd_ins = """INSERT INTO playlist_content (Playlist_ID, Playlist_content_Track, Playlist_content_Artist) VALUES  ('%s', %s', '%s') ;""" % (self.get_playlistid(playlist), track, artist)
        dbcmd_chk = """SELECT Playlist_content_ID FROM playlist_content WHERE Playlist_ID = '%s' AND Playlist_content_Track = '%s' AND Playlist_content_Artist = '%s' ;""" % (self.get_playlistid(playlist), track, artist)
        self.db_Handle[1].execute(dbcmd_cnt)
        if (self.db_Handle[1].fetchall()[0][0] < 1):
            self.db_Handle[1].execute(dbcmd_ins)
            self.db_Handle[0].commit()
        self.db_Handle[1].execute(dbcmd_chk)
        return int(self.db_Handle[1].fetchall()[0][0])

    def get_track_path(self, name, interpret):
        pass

    def get_m3u_info(self, playlist):
        pass

    def __del__(self):
        pass


