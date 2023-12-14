from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
from flask import Flask, render_template, request, jsonify


load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


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

    return json_result["artists"]["items"][0]["id"]


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

    result_content = json.loads(result.content)

    return result_content


def print_album_songs(album_tracks):
    for idx, value in enumerate(album_tracks):
        print(idx + 1, value["name"])


# print(album_2_tracks[1]["id"])
# print_album_songs(album_2)


def song_id_dic_maker(track_info):
    obj = {}
    for idx, song in enumerate(track_info):
        obj[f'{track_info[idx]["id"]}'] = song["name"]
        # print(album_2_tracks[idx]["id"], song["name"])
    return obj


def top_track_info(top_tracks, metric):
    result = {}
    for song in top_tracks["tracks"]:
        result[f'{song['name']}'] = f'{metric} is {song[metric]}'

    return result

# print(top_track_info)


# def audio_features_dictionary(top_track_info):
#     audio_dict = dict()
#     for key, value in top_track_info.items():
#         audio_dict[key] = get_audio_features(token, value)
#     return audio_dict








app = Flask(__name__, static_url_path="/static")


@app.route("/")
def home():
    return render_template("sample_page.html")

@app.route("/form_submit", methods = ["POST"])
def form_submit():
    token = get_token()
    name1 = request.form.get("name")
    id1 = get_artist_info(token, name1)['id']
    tracks = get_artists_top_tracks(token, id1)

    response_data = json.loads(tracks)
    return jsonify(response_data)


@app.route("/album_info")
def album_link():
    return render_template('album_info.html')


if __name__ == "__main__":
    app.run(debug = True)
