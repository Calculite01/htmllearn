from flask_wtf import FlaskForm
from wtforms import StringField,SelectField,DateField,SubmitField,IntegerField
from wtforms.validators import DataRequired,NumberRange

categories = ["Essentials","Lifestyle","Health","Financial Obligation","Other"]

class ExpenseForm(FlaskForm):
    expensename = StringField('Expense Name',validators=[DataRequired()])
    category = SelectField('Expense Category',choices=categories)
    amount = IntegerField('Expense Amount',validators=[NumberRange(min=0),DataRequired()])
    date = DateField('Expense Date',validators=[DataRequired()])
    submit = SubmitField('Submit')



