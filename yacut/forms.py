from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional

from . import constants


class URLMapForm(FlaskForm):
    original_link = URLField(
        label='Введите полную ссылку',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(constants.MIN_ORIG_CUST_LENGTH,
                           constants.MAX_ORIGINAL_LENGTH)]
    )
    custom_id = URLField(
        label='Ваш вариант короткой ссылки',
        validators=[Length(constants.MIN_ORIG_CUST_LENGTH,
                           constants.MAX_CUSTOM_ID_LENGTH), Optional()]
    )
    submit = SubmitField('Создать')
