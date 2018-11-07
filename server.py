from flask import Flask, render_template
app = Flask(__name__)
app.add_url_rule('/node_modules/<path:filename>', endpoint='node_modules',
                 view_func=app.send_static_file)

@app.route("/")
def hello():
	return render_template("index.html")

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)
