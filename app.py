from flask import Flask, render_template
from emails import companies, links, locations, notes
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', companies=companies,
    links=links, locations=locations, notes=notes
)
    
# @app.route('/signup')
# def signup():
#     pass


if __name__ == "__main__":
    app.run()