from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, validators, SelectField
from wtforms.validators import DataRequired
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'adsfuygh92q83y47yuhn'
Bootstrap(app)


class DynamicSelectForm(FlaskForm):
    dynamic_select = SelectField('Choose an option')


class CafeForm(FlaskForm):
    cafe_name = StringField(label='Cafe Name', validators=[DataRequired(),
                                                           validators.Length(min=2)],
                            render_kw={'autofocus': True})
    cafe_location = URLField(label='Cafe Location On Google Maps (URL)', validators=[DataRequired()])
    cafe_open_time = StringField(label='Opening Time ex: 9AM', validators=[DataRequired()])
    cafe_close_time = StringField(label='Closing time ex: 7PM', validators=[DataRequired()])
    cafe_coffe_rating = SelectField('Coffe Rating', choices=['☕️', '☕️☕️', '☕️☕️☕️', '☕️☕️☕️☕️'],
                                    validators=[DataRequired(),
                                                validators.InputRequired()])
    cafe_wifi_rating = SelectField('Wifi Rating', choices=['💪', '💪💪', '💪💪💪', '💪💪💪💪'], validators=[DataRequired(),
                                                                                                  validators.InputRequired()])
    cafe_power_rating = SelectField('Power Rating', choices=['🔌', '🔌', '🔌🔌🔌', '🔌🔌🔌🔌'], validators=[DataRequired(),
                                                                                                   validators.InputRequired()])
    submit = SubmitField('Add')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_row = [form.data[item] for item in form.data][:7]
        new_data = ','.join(new_row)
        with open('cafe-data.csv', mode='a') as file:
            file.write('\n' + new_data)
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
