from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    search_query = StringField('Search for Agents', validators=[DataRequired()])

class ImportForm(FlaskForm):
    csv_file = FileField('CSV File', validators=[DataRequired()])
    submit = SubmitField('Import Agents')

class ContactForm(FlaskForm):
    # Define your contact form fields here
    pass
