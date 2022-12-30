import validators
import json
from flask import Flask, redirect, render_template, request


app = Flask(__name__)


# Setting shortlinks
@app.route("/", methods=['POST', 'GET'])
def hello_world():
    with open("links.json", "r") as f:
        try:
            links_dict = json.load(f)
        except:
            links_dict = {}
                    
    if request.method == 'POST':
        original_link = request.form['originallink']
        short_link = request.form['shortlink']
        
        if short_link and original_link and validators.url(original_link):
            links_dict.setdefault(short_link, original_link) 
                
            with open('links.json', 'w') as f:
                json.dump(links_dict, f)
            
        return render_template("homepage.html", data = links_dict)
        
    else:
        return render_template("homepage.html", data = links_dict)
        


# Rerouting
@app.route("/<shortlink>")
def reroute(shortlink):
    with open('links.json', 'r') as f:
        links_dict = json.loads(f.read())
        
    return redirect(links_dict[shortlink])


if __name__ == "__main__":
    app.run(debug=True)