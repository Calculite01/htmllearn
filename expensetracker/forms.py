from flask_wtf import FlaskForm
from wtforms import StringField,SelectField,DateField,SubmitField,IntegerField
from wtforms.validators import DataRequired,NumberRange,Length,EqualTo,Email

categories = ["Essentials","Lifestyle","Health","Financial Obligation","Other"]

class ExpenseForm(FlaskForm):
    expensename = StringField('Expense Name',validators=[DataRequired()])
    category = SelectField('Expense Category',choices=categories)
    amount = IntegerField('Expense Amount',validators=[NumberRange(min=0),DataRequired()])
    date = DateField('Expense Date',validators=[DataRequired()])
    submit = SubmitField('Create')

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=3,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = StringField('Password',validators=[DataRequired(),Length(min=8,max=100)])
    confirm_password = StringField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=3,max=20)])
    password = StringField('Password',validators=[DataRequired(),Length(min=8,max=100)])
    submit = SubmitField('Login')



