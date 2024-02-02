from flask import render_template, redirect, flash
import re

from . import app, db
from .forms import URLMapForm
from .models import URLMap
from .constants import CUSTOM_ID_REGEX


@app.route('/', methods=['GET', 'POST'])
def add_link_view():
    form = URLMapForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if custom_id:
            if (URLMap.query.filter_by(short=custom_id).first()
                    and re.match(CUSTOM_ID_REGEX, custom_id)):
                flash('Предложенный вариант короткой ссылки уже существует.')
                return render_template('index.html', form=form)
        urlmap = URLMap(
            original=form.original_link.data,
            short=custom_id,
        )
        db.session.add(urlmap)
        db.session.commit()
        return render_template('index.html', form=form, short=custom_id)
    return render_template('index.html', form=form)


@app.route('/<short>')
def link_view(short):
    link = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(link.original)
