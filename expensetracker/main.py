from flask import Flask,render_template,url_for,redirect,request,session
from itsdangerous import URLSafeTimedSerializer as Serializer
from forms import ExpenseForm,LoginForm,RegistrationForm,ExpenseChangeForm
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from flask_login import LoginManager,UserMixin,login_user,current_user,logout_user,login_required
import validate_email
import uuid
from flask_mail import Message,Mail
import os
import random
import re

app = Flask(__name__)
app.config["SECRET_KEY"] = 'fis'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///expenses.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "saadwajid401@gmail.com"
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)

class Expense(db.Model):
    id = db.Column(db.String(36), primary_key = True)
    name = db.Column(db.String(), nullable = False)
    category = db.Column(db.String(), nullable = False)
    amount = db.Column(db.Integer, nullable = False)
    date = db.Column(db.String(), nullable = False)
    accountid = db.Column(db.Integer,db.ForeignKey('account.id'),nullable = False)

    def __repr__(self):
        return f"Expense('{self.name}','{self.category}','{self.amount}','{self.date}',{self.accountid})"

class Account(db.Model,UserMixin):
    id = db.Column(db.String(36), primary_key = True)
    username = db.Column(db.String(), nullable = False, unique = True)
    email = db.Column(db.String(), nullable = False)
    password = db.Column(db.String(), nullable = False)
    expenses = db.relationship('Expense',backref="author",lazy=True)

    def get_reset_token(self,expires_sec=600):
        s = Serializer(app.config["SECRET_KEY"])
        return s.dumps({"user_id":self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            user_id = None
        return Account.query.get(user_id)
    
    def __repr__(self):
        return f"Account('{self.username}','{self.email}')"

@login_manager.user_loader
def load_account(id):
    return Account.query.get(id)

@app.route("/")
def hello():
    session["code"] = None
    session["name"] = None
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
        expense = Expense(id=str(uuid.uuid4()),name=form.expensename.data, category=form.category.data, amount=form.amount.data, date=form.date.data, accountid = current_user.id)
        db.session.add(expense)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('expensecreate.html',form=form)


@app.route("/deleteexpense<id>",methods=["GET","POST"])
@login_required
def deleteexpense(id):
    if request.method == "POST":
        expense = Expense.query.get(id)
        db.session.delete(expense)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('deleteexpense.html')


@app.route("/expenseupdate<id>",methods=["GET","POST"])
@login_required
def expenseupdate(id):
    form = ExpenseChangeForm()
    expense = Expense.query.get(id)
    if form.validate_on_submit():
        expense.name = form.expensename.data
        expense.category = form.category.data
        expense.amount = form.amount.data
        expense.date = form.date.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('expenseupdate.html',form=form,expense=expense)

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
    if session["code"] != None or session["name"] != None:
        account = Account.query.filter_by(username=session["name"]).first()
        db.session.delete(account)
        db.session.commit()
        session["code"] = None
        session["name"] = None

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    message = ""
    form = RegistrationForm()
    if form.validate_on_submit():
        pattern = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")
        if Account.query.filter_by(username=form.username.data).first():
            message = "Username is already taken"
        elif not bool(pattern.match(form.password.data)):
            message = "Password must contain atleast 1 letter 1 number and one special character (@$!%*?&)"
        else:
            code = send_email(form.email.data)
            hashedpw = bcrypt.hashpw(form.password.data.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
            account = Account(id=str(uuid.uuid4()),username=form.username.data,email=form.email.data,password=hashedpw)
            db.session.add(account)
            db.session.commit()
            session["code"] = code
            session["name"] = account.username
            return redirect(url_for('verifyemail'))
    return render_template('register.html',form=form,message=message)

@app.route("/verifyemail",methods=["GET","POST"])
def verifyemail():
    message = ""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    name = session["name"]
    code = session["code"]
    if name == None or code == None:
        return redirect(url_for('register'))
    account = Account.query.filter_by(username=name).first()
    if request.method == "POST":
        codeEntered = request.form.get('code')
        if codeEntered == code:
            login_user(account)
            return redirect(url_for('home'))
        else:
            message = "Incorrect code"
    return render_template('verifyemail.html',message=message)
    









@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('hello'))

@app.route("/account")
@login_required
def account():
    session["code"] = None
    session["name"] = None
    return render_template("account.html")

@app.route("/deleteaccount<id>",methods=["GET","POST"])
@login_required
def deleteaccount(id):
    if request.method == "POST":
        account = Account.query.get(id)
        Expense.query.filter_by(accountid=id).delete()
        logout_user()
        db.session.delete(account)
        db.session.commit()
        return redirect(url_for('hello'))
    return render_template('deleteaccount.html')

@app.route("/updateusername<id>",methods=["GET","POST"])
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
    
@app.route("/updateemail<id>",methods=["GET","POST"])
@login_required
def updateemail(id):
    session["code"] = None
    session["name"] = None
    message = ""
    account = Account.query.get(id)
    if request.method == "POST":
        email = request.form.get('email')   
        if not validate_email.validate_email(email):
            message = "Invalid email"
        else:
            #account.email = email
            #db.session.commit()
            code = send_email(email)
            session["code"] = code
            session["name"] = email
            return redirect(f"/verifyupdateemail{id}")
    return render_template("updateemail.html",message=message)

@app.route("/verifyupdateemail<id>",methods=["GET","POST"])
@login_required
def verifyupdateemail(id):
    message = ""
    code = session["code"]
    email = session["name"]
    if email == None or code == None:
        return redirect(url_for(f'updateemail{id}'))
    account = Account.query.get(id)
    if request.method == "POST":
        codeEntered = request.form.get('code')
        if codeEntered == code:
            account.email = email
            db.session.commit()
            return redirect(url_for('account'))
        else:
            message = "Incorrect code" + str(codeEntered) + str(code)
    return render_template('verifyupdateemail.html',message=message)                           




@app.route("/updatepassword<id>",methods=["GET","POST"])
def updatepassword(id):
    message = ""
    account = Account.query.get(id)
    if request.method == "POST":
        currentpw = request.form.get("old_password")
        newpw = request.form.get("new_password")
        confirmpw = request.form.get("confirm_password")
        pattern = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")
        if bcrypt.checkpw(currentpw.encode('utf-8'),(account.password).encode('utf-8')):
            if not bool(pattern.match(newpw)):
                message = "Password must contain atleast 1 letter 1 number and one special character (@$!%*?&)"
            elif newpw == confirmpw:
                if newpw == currentpw:
                    message = "New password can't be same as old password"
                else:
                    account.password = bcrypt.hashpw(newpw.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
                    db.session.commit()
                    return redirect(url_for('account'))
            else:
                message = "Passwords should be equal"
        else:
            message = "Incorrect Password"

    return render_template("updatepassword.html",message=message)

def send_email(email):
    msg = Message('Verify Email',
                  sender='noreply@demo.com',
                  recipients=[str(email)])
    code = str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9))
    msg.body = f"Your one time verification code is {code}"
    mail.send(msg)
    return code

def send_reset_email(email,id):
    msg = Message('Reset Password',
                  sender='noreply@demo.com',
                  recipients=[str(email)])
    msg.body = f"Click on link to reset password: http://127.0.0.1:5000/resetpassword{id}"
    mail.send(msg)

@app.route("/resetpassword",methods=["GET","POST"])
def resetpassword():
    session["reset"] = False
    message = ""
    if request.method == "POST":
        email = request.form.get("email")
        account = Account.query.filter_by(email=email).first()
        if not validate_email.validate_email(email) or account == None:
            message = "Invalid email"
        else:
            session["reset"] = True
            send_reset_email(email,account.id)
            message = "Reset password email sent"

    return render_template('resetpassword.html',message=message)

@app.route("/resetpassword<id>",methods=["GET","POST"])
def resetpassword2(id):
    message = ""
    account = Account.query.get(id)
    if not session["reset"]:
        return redirect(url_for('hello'))
    if request.method == "POST":
        newpw = request.form.get("new_password")
        confirmpw = request.form.get("confirm_password") 
        pattern = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")
        if not bool(pattern.match(newpw)):
            message = "Password must contain atleast 1 letter 1 number and one special character (@$!%*?&)"
        elif newpw != confirmpw:
            message = "Passwords dont match"
        else:
            hashedpw = bcrypt.hashpw(newpw.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
            account.password = hashedpw
            db.session.commit()
            return redirect(url_for('login'))

    return render_template('resetpassword2.html',message=message)

if __name__ == '__main__':
    app.run(debug=True)

