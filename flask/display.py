from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

@app.route('/<string:uid>')
def retrieval(uid):
    title = "title"
    sub_title = ["sub_title1", "sub_title2"]
    layout = [True, False]
    head = [[('a','h11'), ('b','h12')], [('a','h21'), ('b','h22')]]
    items = [[{'a':1, 'b':2}, {'a':3, 'b':4}], [{'a':1, 'b':2}, {'a':3, 'b':4}]]
    return render_template('table.html', num=len(sub_title), title=title, sub_title=sub_title, layout=layout, head=head, items=items)
