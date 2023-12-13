from flask import Flask, render_template


app = Flask(__name__, static_url_path="/static")


@app.route("/")
def home():
    return render_template("sample_page.html")


# @app.route("/static")
# def static():
#     return


if __name__ == "__main__":
    app.run()
