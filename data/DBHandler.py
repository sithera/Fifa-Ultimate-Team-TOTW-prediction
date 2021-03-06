import sqlite3


class DBHandler(object):
    def __init__(self):
        self.conn = sqlite3.connect('statistics.db')
        self.conn.execute('''CREATE TABLE IF NOT EXISTS player_statistics (
            player_id integer, 
            player_name text, 
            match_id integer,
            match_date text,
            fixture integer,
            minutes_played integer,
            goals integer, 
            assists integer, 
            shots integer,
            shots_on_target integer,
            head_shots integer,
            passes integer,
            success_passes integer,
            long_passes integer,
            success_long_passes integer,
            short_passes integer,
            success_short_passes integer,
            ball_possession integer,
            interceptions integer,
            tackles integer,
            clearances integer,
            fouls integer,
            shots_blocked integer,
            passes_blocked integer,
            red_card integer,
            yellow_card integer,
            saves integer,
            UNIQUE (player_id, match_id) ON CONFLICT REPLACE)''')

    def insert_player_statistics(self, player_stats):
        cur = self.conn.cursor()
        cur.execute('''INSERT INTO player_statistics VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                          (player_stats['personId'], player_stats['personNameEn'], player_stats['matchId'],
                           player_stats['match_date'], player_stats['fixture'], player_stats['minutesPlayed'],
                           player_stats['goals'], player_stats['assists'], player_stats['shots'],
                           player_stats['shotsOnTarget'], player_stats['headShots'], player_stats['passes'],
                           player_stats['succPasses'], player_stats['passLong'], player_stats['succPassLong'],
                           player_stats['passShorts'], player_stats['succPassShorts'], player_stats['ballPossession'],
                           player_stats['interceptions'], player_stats['tackles'], player_stats['clearances'],
                           player_stats['fouls'], player_stats['blocksShots'], player_stats['blocksPasses'],
                           player_stats['redCard'], player_stats['yellowCard'], player_stats['saves']))

        self.conn.commit()
        cur.close()

    def get_all_players_statistics(self):
        cur = self.conn.cursor()
        cur.execute('''SELECT * FROM player_statistics''')

        output = ''.join(str(cur.fetchone()))
        print output
        cur.close()
        return output

    def check_player_name(self, name):
        cur = self.conn.cursor()
        cur.execute('''SELECT * FROM player WHERE player_name LIKE ?''', (name,))
        if cur.fetchone() is None:
            print name
        cur.close()

    def get_all_players(self):
        cur = self.conn.cursor()
        cur.execute('''SELECT * FROM player''')
        result = cur.fetchall()
        cur.close()
        return result

    def update_player_position(self, position, player_id):
        cur = self.conn.cursor()
        cur.execute('''SELECT * FROM player WHERE player_id = ? AND position IS NOT NULL''', (player_id,))
        if cur.fetchone() is None:
            cur.execute('''UPDATE player SET position = ? WHERE player_id = ?''', (position, player_id))
            self.conn.commit()
        cur.close()

    def update_player_photo(self, url, player_id):
        cur = self.conn.cursor()
        cur.execute('''SELECT * FROM player WHERE player_id = ? AND photo IS NOT NULL''', (player_id,))
        if cur.fetchone() is None:
            cur.execute('''UPDATE player SET photo = ? WHERE player_id = ?''', (url, player_id))
            self.conn.commit()
        cur.close()

    def get_all_matches_ids(self):
        cur = self.conn.cursor()
        cur.execute('''SELECT DISTINCT match_id FROM player_statistics''')
        result = cur.fetchall()
        cur.close()
        return result

    def get_player_data_by_id(self, player_id):
        cur = self.conn.cursor()
        cur.execute('''SELECT player_name, photo FROM player WHERE player_id = ?''', (player_id,))
        result = cur.fetchone()
        cur.close()
        return result

    def get_all_players_with_positions_and_statistics(self, table1='player', table2='player_statistics'):
            cur = self.conn.cursor()
            cur.execute("SELECT {0}.position, {1}.* FROM {0} JOIN {1} USING(player_id);".format(str(table1), str(table2)))
            rows = []
            while True:
                row = cur.fetchone()
                if row is None:
                    break
                rows.append(row)
            return rows
