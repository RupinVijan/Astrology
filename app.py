
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME="rupinvijan@gmail.com",
    MAIL_PASSWORD="xxx"

)
mail=Mail(app)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///appoint.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class appoint(db.Model):
    sno = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(50) , nullable=True)
    email = db.Column(db.String(50) , nullable=True)
    phone = db.Column(db.String(50) , nullable=True)
    message = db.Column(db.String(500) , nullable=True)
    date = db.Column(db.String(100) , nullable=True)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.name}"


@app.route("/")
def hello_world():
    return render_template("home.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/more")
def more_about_us():
    return render_template("more.html")
@app.route("/logout")
def logout():
    return render_template("admin.html")

@app.route("/admin" , methods=['GET','POST'])
def admin():
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        if username=="Rupin" and password=="password":
            dets=appoint.query.all()
            return render_template("dets.html" , dets=dets)

    return render_template("admin.html")

@app.route("/delete/<string:sno>" , methods=['GET','POST'])
def delete(sno):
    dets=appoint.query.filter_by(sno=sno).first()
    db.session.delete(dets)
    db.session.commit()
    return redirect("/admin")

@app.route("/contact", methods=['GET' , 'POST'])
def contact_us():
    if request.method=='POST':
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        message=request.form.get('message')
        date=request.form.get('date')
        entry=appoint(name=name,email=email,phone=phone,message=message,date=date)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('This message is from ' + name,
        sender=email, recipients=["rupinvijan@gmailcom"],
        body="\n we are please to inform you that your appointment is confirmed.\ncontact number" + phone
        )
    
    else :
        return render_template("contact.html")
    return render_template("contact.html")


if __name__=="__main__":
    app.run(debug=True)
