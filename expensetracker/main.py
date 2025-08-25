from flask import Flask,render_template,url_for,redirect,request
from forms import ExpenseForm,LoginForm,RegistrationForm
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from flask_login import LoginManager,UserMixin,login_user,current_user,logout_user,login_required
import validate_email


app = Flask(__name__)
app.config["SECRET_KEY"] = 'fis'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///expenses.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), nullable = False)
    category = db.Column(db.String(), nullable = False)
    amount = db.Column(db.Integer, nullable = False)
    date = db.Column(db.String(), nullable = False)
    accountid = db.Column(db.Integer,db.ForeignKey('account.id'),nullable = False)

    def __repr__(self):
        return f"Expense('{self.name}','{self.category}','{self.amount}','{self.date}',{self.accountid})"

class Account(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(), nullable = False, unique = True)
    email = db.Column(db.String(), nullable = False)
    password = db.Column(db.String(), nullable = False)
    expenses = db.relationship('Expense',backref="author",lazy=True)

    def __repr__(self):
        return f"Account('{self.username}','{self.email}')"

@login_manager.user_loader
def load_account(id):
    return Account.query.get(int(id))

@app.route("/")
def hello():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template("home.html")


@app.route("/home")
@login_required
def home():
    expenses = Expense.query.filter_by(accountid = current_user.id)
    return render_template('index.html',expenses=expenses)


@app.route("/expensecreate",methods=["GET","POST"])
@login_required
def expensecreate():
    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense(name=form.expensename.data, category=form.category.data, amount=form.amount.data, date=form.date.data, accountid = current_user.id)
        db.session.add(expense)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('expensecreate.html',form=form)


@app.route("/deleteexpense<int:id>",methods=["POST"])
@login_required
def deleteexpense(id):
    expense = Expense.query.get(id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/expenseupdate<int:id>",methods=["GET","POST"])
@login_required
def expenseupdate(id):
    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense.query.get(id)
        expense.name = form.expensename.data
        expense.category = form.category.data
        expense.amount = form.amount.data
        expense.date = form.date.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('expenseupdate.html',form=form)

@app.route("/login",methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    message = ""
    form = LoginForm()
    if form.validate_on_submit():
        account = Account.query.filter_by(username=form.username.data).first()
        if account and bcrypt.checkpw(form.password.data.encode('utf-8'),(account.password).encode('utf-8')):
            login_user(account)
            return redirect(url_for('home'))
        else:
            message = "Incorrect username or password"
    return render_template('login.html',form=form,message=message)

@app.route("/register",methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    message = ""
    form = RegistrationForm()
    if form.validate_on_submit():
        if Account.query.filter_by(username=form.username.data).first():
            message = "Username is already taken"
        else:
            hashedpw = bcrypt.hashpw(form.password.data.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
            account = Account(username=form.username.data,email=form.email.data,password=hashedpw)
            db.session.add(account)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html',form=form,message=message)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('hello'))

@app.route("/account")
@login_required
def account():
    return render_template("account.html")

@app.route("/deleteaccount<int:id>")
@login_required
def deleteaccount(id):
    account = Account.query.get(id)
    Expense.query.filter_by(accountid=id).delete()
    logout_user()
    db.session.delete(account)
    db.session.commit()
    return redirect(url_for('hello'))

@app.route("/updateusername<int:id>",methods=["GET","POST"])
@login_required
def updateaccount(id):
    message = ""
    account = Account.query.get(id)
    if request.method == "POST":
        username = request.form.get('username')
        if Account.query.filter_by(username=username).first():
            message = "Username is already taken"
        else:
            account.username = username
            db.session.commit()
            return redirect(url_for('account'))
    return render_template("updateusername.html",message=message)
    
@app.route("/updateemail<int:id>",methods=["GET","POST"])
@login_required
def updateemail(id):
    message = ""
    account = Account.query.get(id)
    if request.method == "POST":
        email = request.form.get('email')   
        if not validate_email.validate_email(email):
            message = "Invalid email"
        else:
            account.email = email
            db.session.commit()
            return redirect(url_for('account'))
    return render_template("updateemail.html",message=message)

@app.route("/updatepassword<int:id>",methods=["GET","POST"])
def updatepassword(id):
    message = ""
    account = Account.query.get(id)
    if request.method == "POST":
        currentpw = request.form.get("old_password")
        newpw = request.form.get("new_password")
        confirmpw = request.form.get("confirm_password")
        if bcrypt.checkpw(currentpw.encode('utf-8'),(account.password).encode('utf-8')):
            if newpw == confirmpw:
                account.password = bcrypt.hashpw(newpw.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
                db.session.commit()
                return redirect(url_for('account'))
            else:
                message = "Passwords should be equal"
        else:
            message = "Incorrect Password"

    return render_template("updatepassword.html",message=message)


if __name__ == '__main__':
    app.run(debug=True)

