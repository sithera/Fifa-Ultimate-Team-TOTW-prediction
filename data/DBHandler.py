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

    def get_all_players(self):
        cur = self.conn.cursor()
        cur.execute('''SELECT * FROM player_statistics''')

        print cur.fetchone()

        cur.close()

