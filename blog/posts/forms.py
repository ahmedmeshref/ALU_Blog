from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class AddPostForm(FlaskForm):
    """
    form for adding new posts
    """
    title = StringField("Title", validators=[DataRequired(), Length(min=2, max=50)])
    content = TextAreaField("Content", validators=[DataRequired(), Length(min=10, max=500)],
                            render_kw={"placeholder": "What new at ALU?"})
    submit = SubmitField("POST")
