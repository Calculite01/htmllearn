from main import app,db,Expense,Account

with app.app_context():
    print(Account.query.all())
