import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict

# first argument is blueprints name
# second argument is it's import_name
song = Blueprint('songs', 'song')

# INDEX ROUTE
@song.route('/', methods=["GET"])
def get_all_songs():
    try:
      songs = [model_to_dict(song) for song in models.Song.select()]
      print(songs)
      return jsonify(data=songs, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
      return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

# POST ROUTE
@song.route('/', methods=["POST"])
def create_songs():
    payload = request.get_json()
    
    song = models.Song.create(**payload)
    song_dict = model_to_dict(song)
    return jsonify(data=song_dict, status={"code": 201, "message": "Success"})

# SHOW ROUTE 
@song.route('/<id>', methods=["GET"])
def get_one_song(id):
    try:
        print(id, 'reserved word?')
        # get_by_id(...) is a peewee method
        song = models.Song.get_by_id(id)
        # print dictionary type of response
        print(song.__dict__)
        return jsonify(data=model_to_dict(song), status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
      return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})


# UPDATE ROUTE
@song.route('/<id>', methods=["PUT"])
def update_song(id):
    try:
        payload = request.get_json()
        query = models.Song.update(**payload).where(models.Song.id==id)
        query.execute()
        return jsonify(data=model_to_dict(models.Song.get_by_id(id)), status={"code": 200, "message": "resource updated successfully"})
    except models.DoesNotExist:
      return jsonify(data={}, status={"code": 401, "message": "Error updating the resources"})

# DELETE ROUTE
@song.route('/<id>', methods=["Delete"])
def delete_song(id):
    query = models.Song.delete().where(models.Song.id==id)
    query.execute()
    return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})

