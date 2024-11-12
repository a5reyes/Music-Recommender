from flask import Flask, request, render_template
import project
import re

app = Flask(__name__)

@app.route("/", methods=["POST","GET"])
def home():
    results = None
    if request.method == "GET":
        return render_template("index.html")
    else:
        if "track" in request.form:
            track = request.form["track name"]
            track_artist = request.form["track artist"]
            results = project.just_like_track(track, track_artist)
            results_str = "\n".join((result for result in results))
            return render_template("index.html", results=results_str)
        elif "album" in request.form:
            album = request.form["album name"]
            album_artist = request.form["album artist"]
            results = project.just_like_album(titlecase(album), titlecase(album_artist).casefold())
            results_str = "\n".join((result for result in results))
            return render_template("index.html", results=results_str)
        elif "artist" in request.form:
            artist = request.form["artist name"]
            result = project.search_artist(titlecase(artist).casefold())
            if result:
                recs = project.get_artists_recs(result)
                recs_str = "\n".join((rec for rec in recs))
                return render_template("index.html", results=recs_str)
            else:
                artist = "\n".join("Can't find artist")
                return render_template("index.html", results=artist)
        else:
            results = project.just_like_genre()
            results_str = "\n".join((result for result in results))
            return render_template("index.html", results=results_str)
            
def titlecase(s):
    return re.sub(r"[^\W\d_]+(?:['’][^\W\d_]+)?", lambda mo: mo.group(0).capitalize(), s)

if __name__ == "__main__":
    app.run(debug=True)