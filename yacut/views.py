from flask import render_template

from . import app
from .forms import URLMapForm


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    # opinion = random_opinion()
    # if opinion is not None:
    return render_template('index.html', form=form)
    # abort(404)
