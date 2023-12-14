from spotify_proj import *

tok = get_token()

print(tok)


drake_id = get_artist_info(tok, "Drake")


get_artists_top_tracks(tok, drake_id)
