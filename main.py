from flask import Flask, render_template,redirect, flash, url_for, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin, login_user, logout_user,login_required, LoginManager, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm,LoginForm
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from functools import wraps
def admin_only(function):
    @wraps(function)

    def decorated_function(*args,**kwargs):
        # print(f"You called {function.__name__}{args}")
        if not current_user.is_authenticated or current_user.id != 1:
            return abort(403)  # Raise a Forbidden error if not authorized

        return function(*args,**kwargs)
    return decorated_function

import os
app=Flask(__name__)
app.config['SECRET_KEY']=os.environ.get('SECRET_KEY')
PSQL_PASSWORD=os.environ.get('PSQL_PASSWORD')

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)

class CommentForm(FlaskForm):

    body = StringField(label='Comment:', validators=[DataRequired(), Length(min=5)],
                          render_kw={"placeholder": "Hi, my name is Artur Ziianbaev. I'd like to ..."})
    submit=SubmitField(label='Submit')

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(Users,user_id)

class Item(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(250),  nullable=False)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(550),  nullable=False)
    price = db.Column(db.Integer, nullable=False)
    path_picture_1 = db.Column(db.String(550), nullable=False)
    path_picture_2 = db.Column(db.String(550), nullable=False)
    path_picture_3 = db.Column(db.String(550), nullable=False)
                                                    #one to many for  One to One use uselist=False instead#
    comments=db.relationship("Comment",backref="item",uselist=True)
    carts=db.relationship("Cart",backref="item")

class Users(UserMixin,db.Model):

    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(250),unique=True,nullable=False)
    password=db.Column(db.String(550),nullable=False)
    name=db.Column(db.String(100),nullable=False)

    items = relationship("Cart", backref="user")
    comments=relationship("Comment", backref="user")
class Cart(db.Model):

    id=db.Column(db.Integer, primary_key=True,unique=True)
    key=title=db.Column(db.String(250),unique=False,nullable=True)
    title=db.Column(db.String(250),unique=False,nullable=False)
    price=db.Column(db.Integer,unique=False,nullable=False)
    item_id=db.Column (db.Integer, db.ForeignKey("item.id") ,nullable= False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"),nullable=False)
    # owner = relationship("User", back_populates="items")
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_name = db.Column(db.String(250), unique=False, nullable=False)
    body = db.Column(db.String(500), unique=False,nullable=False)
    date=db.Column(db.String(50),nullable=False)

    item_id=db.Column(db.Integer,db.ForeignKey("item.id"),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)



with app.app_context():
    db.create_all()

Bootstrap5(app)

ITEMS_FOR_SALE={
    "chair": {
        "title": "Black Computer Chair",
        "price": 30,
        "pic_1": "./static/assets/img/items_for_sale/chair_1.jpg",
        "pic_2": "./static/assets/img/items_for_sale/chair_2.jpg",
        "pic_3": "./static/assets/img/items_for_sale/chair_3.jpg",
        "description": "Introducing the epitome of comfort and sophistication – our Black Leather Chair. This elegant "
                       "and luxurious chair is"
                       " the perfect addition to any space, whether it's your home, office, or a high-end lounge. "
                       "Crafted with "
                       "meticulous attention to detail and designed for both style and relaxation, this chair offers a "
                       "sublime seating"
                       " experience."
    },
    "table": {
        "title": "Glass Table",
        "price": 50,
        "pic_1": "./static/assets/img/items_for_sale/table_1.jpg",
        "pic_2": "./static/assets/img/items_for_sale/table_2.jpg",
        "pic_3": "./static/assets/img/items_for_sale/table_3.jpg",
        "description": "Elevate your workspace with Black Glass Computer Table – a sleek and functional addition that "
                       "combines "
                       "modern design with practicality. This contemporary desk is designed to enhance your"
                       " productivity"
                       "and create "
                       "an atmosphere of sophistication in any home or office."

    },
    "laptop": {
        "title": "ASUS TUF Dash F15 Gaming Laptop",
        "price": 1000,
        "pic_1": "./static/assets/img/items_for_sale/laptop_1.jpg",
        "pic_2": "./static/assets/img/items_for_sale/laptop_2.jpg",
        "pic_3": "./static/assets/img/items_for_sale/laptop_3.jpg",
        "description": "Step into the world of high-performance gaming with the ASUS TUF Dash F15, a gaming laptop "
                       "that's "
                       "engineered to deliver exceptional power, style, and portability. Whether you're a competitive "
                       "gamer,"
                       " content creator, or just seeking a cutting-edge laptop for your computing needs, the ASUS TUF"
                       " Dash F15"
                       " has you covered.",
    },
    "mouse": {
        "title": "Logitech G305 Wireless Gaming Mouse",
        "price": 20,
        "pic_1": "./static/assets/img/items_for_sale/mouse_1.jpg",
        "pic_2": "./static/assets/img/items_for_sale/mouse_2.jpg",
        "pic_3": "./static/assets/img/items_for_sale/mouse_3.jpg",
        "description": "Get ready to up your gaming performance with the Logitech G305 Wireless Gaming Mouse. "
                       "This cutting-edge "
                       "gaming accessory is designed to deliver precision, speed, and freedom of movement for "
                       "gamers of all levels.",
    },
    "mousepad":
        {
        "title": "Mouse Pad",
        "price": 10,
        "pic_1": "./static/assets/img/items_for_sale/mousepad_1.jpg",
        "pic_2": "./static/assets/img/items_for_sale/mousepad_2.jpg",
        "pic_3": "./static/assets/img/items_for_sale/mousepad_3.jpg",
        "description": "Elevate your gaming setup with the USCIS Mouse Pad, a sleek and high-performance"
                       " accessory designed to"
                       " enhance your gaming experience in style and precision."
        },

    "book":
        {
        "title": "Atomic Habits by J.Clear",
        "price": 10,
        "pic_1": "./static/assets/img/items_for_sale/book_1.jpg",
        "pic_2": "./static/assets/img/items_for_sale/book_2.jpg",
        "pic_3": "./static/assets/img/items_for_sale/book_3.jpg",
        "description": "Dive into the world of personal development and transformative change with the book"
                       " 'Atomic Habits' by James Clear. This bestselling book is your ultimate guide to unlocking"
                       " the power of small habits for big, positive changes in your life."
        },
    "notebook":
        {
        "title": "Study Notebook",
        "price": 99,
        "pic_1": "./static/assets/img/items_for_sale/notebook_1.jpg",
        "pic_2": "./static/assets/img/items_for_sale/notebook_2.jpg",
        "pic_3": "./static/assets/img/items_for_sale/notebook_3.jpg",
        "description": "Unlock your potential in Python programming with the Green Python Study Notebook, "
                       "the perfect companion for both beginners and seasoned coders embarking "
                       "on their Python learning journey.",
        }

}
def dictionary_to_database():
    global ITEMS_FOR_SALE
    for key, value in ITEMS_FOR_SALE.items():

        # print(key)
        # print(value)

        new_item=Item(
            name=key,
            title = value['title'],
            description = value['description'],
            price = value['price'],
            path_picture_1 = value['pic_1'],
            path_picture_2 = value['pic_2'],
            path_picture_3 = value['pic_3'],
        )
        db.session.add(new_item)
        db.session.commit()

    return print('Data was transfared to db!')
#marketplace=# ALTER SEQUENCE item_id_seq RESTART WITH 1;
# with app.app_context():
#     dictionary_to_database()
def check_reference():
    with app.app_context():
        all=db.session.execute(db.select(Item)).scalars()
        for _ in all:
            print(_.comments[0].body)
            break
        comment=db.get_or_404(Comment,2)
        print(comment.user.email)
        print(comment.item.title)



def find_key_by_value(dictionary, search_value):
    for key, value in dictionary.items():
        if "price" in value and value["price"] == search_value:
            return key
    return None  # Return None if the value is not found in the dictionary



@app.route("/")
def home():
    # print(current_user.is_authenticated)
    user = None
    if current_user.is_authenticated:
        print("LOGGED")
        user = db.get_or_404(Users, current_user.id)





    return render_template('home.html',current_user=current_user,user=user)

@app.route("/check_father")
def check():
    return render_template("father_template.html")

@app.route("/items")
def display_items():
    # items=ITEMS_FOR_SALE
    items = db.session.execute(db.select(Item)).scalars()
    return render_template("items.html", items=items)


@app.route("/sale/<item>",methods=['GET','POST'])
def sale(item):
    # print(ITEMS_FOR_SALE[item])
    # return render_template('item_separate.html', item=ITEMS_FOR_SALE[item],name=item)
    form=CommentForm()
    item_for_sale = db.session.execute(db.select(Item).where(Item.name == item)).scalar()


    if form.validate_on_submit():
        if current_user.is_authenticated:
            user = db.get_or_404(Users, current_user.id)
            body=form.body.data
            print(body)
            x=datetime.datetime.now()
            date=x.strftime("%x")
            new_comment=Comment(
                user_name = user.email,
                body = body,
                item_id = item_for_sale.id,
                user_id = user.id,
                date=date,
            )
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for('sale',item=item))
        else:
            return redirect(url_for('register'))
        # return render_template('item_separate.html',item=item_for_sale,form=form)

    return  render_template('item_separate.html',item=item_for_sale,form=form)

@app.route("/register", methods=['POST','GET'])
def register():
    register_form=RegisterForm()
    if register_form.validate_on_submit():
        email=register_form.email.data
        password=register_form.password.data
        hash_password=generate_password_hash(password,method='pbkdf2:sha256',salt_length=8)
        name=register_form.name.data
        find_user=db.session.execute(db.select(Users).where(Users.email==email)).scalar()
        if find_user:

            flash("You've already signed up with that email, log in instead!")

            return redirect(url_for('login'))
        else:
            new_user=Users(
                email=email,
                password=hash_password,
                name=name,
            )
            db.session.add(new_user)
            db.session.commit()


            login_user(new_user)
            return redirect(url_for('home'))


    return render_template('register.html',form=register_form)

@app.route("/login",methods=['POST','GET'])
def login():
    login_form=LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        find_user = db.session.execute(db.select(Users).where(Users.email == email)).scalar()
        if not find_user:
            flash("Invalid email, try again.")
            return redirect(url_for('register'))
        elif not check_password_hash(find_user.password, password):
            flash('Invalid password, try again')
            return redirect(url_for('login'))
        else:

            login_user(find_user)
            return redirect(url_for('home'))


    return render_template('login.html',form=login_form)


@app.route("/logged")
@login_required
def logged():
    return "You logged in!"

@app.route("/logout")
@login_required
def logout():
    logout_user()
    # print("you logged out")
    return redirect(url_for('home'))

@app.route("/cart",methods=['POST','GET'])
def cart():
    if not current_user.is_authenticated:
        return redirect('login')
    # print(current_user.id)
    user=db.get_or_404(Users,current_user.id)
    if user:
        total=0
        for item in user.items:
            total += item.price
    if request.method=='POST':
        flash("It's just a study project not a commercial one. However, thank you for interest!")


    return render_template('cart.html', total=total,user=user)


@app.route("/add_item/<price>")
def add_item(price):
    if not current_user.is_authenticated:
        return redirect('login')

    # price_int=int(price.strip("-"))


    # result = find_key_by_value(ITEMS_FOR_SALE, price_int)
    result=db.get_or_404(Item,price)
    if result is not None:
        # print(f"The item with price {price_int} is associated with the key '{result}'")
        user=current_user
        item = Cart.query.filter_by(key=result.name, user_id=user.id).first()
        if item:
            flash("You've already added this item to your cart.")

        else:
            new_item=Cart(
                key=result.name,
                title=result.title,
                price=result.price,
                item_id=result.id,
                user_id=user.id
            )
            db.session.add(new_item)
            db.session.commit()
            flash("Item added to your cart successfully.")
            return redirect(url_for('cart'))
    else:
        print(f"No item found with price ")
    return redirect(url_for('cart'))


@app.route("/delete<item_id>")
@login_required
def delete(item_id):
    item=db.get_or_404(Item,item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return redirect("cart")




def checking_for_reference():
    with app.app_context():
        us=db.get_or_404(Users,1)
        print(us.email)
        for _ in us.items:
            print(_.title)
            print(_.item.title)

        cart_item=db.get_or_404(Cart,1)
        print(cart_item.title + "\nAnd customer who wants this item: ")
        print(cart_item.user.email + " \n----------- ")

        ArturZiianbaev=db.get_or_404(Users,2)
        print(ArturZiianbaev.email + f" 1st item in the cart is: {ArturZiianbaev.items[0].title} for"
                                     f" {ArturZiianbaev.items[0].price}$"
                                     f"\nAnd description: {ArturZiianbaev.items[0].item.description}")


@app.route("/delete_comment/<comment_id>?<item>")
@admin_only
def delete_comment(comment_id,item):
    # print(comment_id)
    db.session.delete(db.get_or_404(Comment,comment_id))
    db.session.commit()
    itemm=item
    return redirect(url_for('sale',item=itemm))





if __name__ == "__main__":
    app.run(debug=False)


