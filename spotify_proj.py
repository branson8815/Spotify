from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json


load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# print(client_id, client_secret)


def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def get_album_info(token, album_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={album_name}&type=album&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    # print(json_result)
    return json_result["albums"]["items"][0]


def get_artist_info(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    # print(json_result)
    return json_result["artists"]["items"][0]


def get_album_tracks(token, album_id):
    url = "https://api.spotify.com/v1/albums"
    headers = get_auth_header(token)
    query = f"/{album_id}/tracks"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    # print(json_result)
    return json_result["items"]


def get_audio_features(token, track_id):
    url = "https://api.spotify.com/v1/audio-features"
    headers = get_auth_header(token)
    query = f"?ids={track_id}"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    # print(json_result)
    return json_result


def get_artists_top_tracks(token, artist_id):
    url = "https://api.spotify.com/v1/artists"
    headers = get_auth_header(token)
    query = f"/{artist_id}/top-tracks?country=US"
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    return json_result
    # return json_result


token = get_token()
album1 = get_album_info(token, "Ye")
# print(album1)
album1_tracks = get_album_tracks(token, album1["id"])


def print_album_songs(album_tracks):
    for idx, value in enumerate(album_tracks):
        print(idx + 1, value["name"])


album_2 = get_album_info(token, "The College Dropout")
album_2_tracks = get_album_tracks(token, album_2["id"])

# print(album_2_tracks[1]["id"])
# print_album_songs(album_2)


def song_id_dic_maker(track_info):
    obj = {}
    for idx, song in enumerate(track_info):
        obj[f'{track_info[idx]["id"]}'] = song["name"]
        # print(album_2_tracks[idx]["id"], song["name"])
    return obj


# for i, j in enumerate(album_2_tracks):
#     print(i, j)

dic1 = song_id_dic_maker(album_2_tracks)
# print(obj)

# for i in dic1:
#     print(dic1[i])


td = get_artist_info(token, "Target Demographic")
print(td["id"])

top_tracks = get_artists_top_tracks(token, td["id"])



def top_track_info(top_tracks):
    result = {}
    for song in (top_tracks["tracks"]):
        result[f'{song['name']}'] = song['id']
    return result
# step2 = get_album_tracks(token, step1["id"])

# print(top_tracks["tracks"][1]["name"])

top_track_info = (top_track_info(top_tracks))

# print(top_track_info)


def audio_features_dictionary(top_track_info):
    audio_dict = dict()
    for key, value in top_track_info.items():
        audio_dict[key] = get_audio_features(token, value)
    return audio_dict


# get_audio_features(token, top_track_info['Dreaming About You'])

top_audio_features  = (audio_features_dictionary(top_track_info))

print(top_audio_features['Dreaming About You'])

print(top_audio_features)


