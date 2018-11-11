from flask import Flask, render_template, request

app = Flask(__name__)
app.add_url_rule('/node_modules/<path:filename>', endpoint='node_modules',
                 view_func=app.send_static_file)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/save", methods=['POST'])
def save():
    return "saved !"

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)
