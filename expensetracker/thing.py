from flask import Flask,render_template,url_for,redirect
from forms import ExpenseForm
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SECRET_KEY"] = 'fis'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///expenses.db'

db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    category = db.Column(db.String, nullable = False)
    amount = db.Column(db.Integer, nullable = False)
    date = db.Column(db.String, nullable = False)

    def __repr__(self):
        return f"Expense('{self.name}','{self.category}','{self.amount}','{self.date}')"


@app.route("/")
def hello():
    return redirect(url_for('home'))

@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/expensecreate",methods=["GET","POST"])
def expensecreate():
    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense(name=form.expensename.data, category=form.category.data, amount=form.amount.data, date=form.date.data)
        db.session.add(expense)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('expensecreate.html',form=form)

if __name__ == '__main__':
    app.run(debug=True)

