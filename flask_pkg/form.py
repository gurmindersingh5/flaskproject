from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FieldList, SubmitField, TextAreaField, DecimalField, PasswordField
from wtforms.validators import DataRequired
from flask_login import login_manager, login_user, login_required, logout_user
import bcrypt

# add new Customer
class Customer_Entry(FlaskForm):
    id = IntegerField(label='id')
    name = StringField(label='Name', validators=[DataRequired()], render_kw={"palceholder":"New Customer name"})
    address = TextAreaField(label='Address', validators=[DataRequired()])
    contact = IntegerField(label='Contact')
    submit = SubmitField(label='Submit')

# add new parts in Inventory
class Part(FlaskForm):
    name = TextAreaField(label="Product Name", validators=[DataRequired()])
    price = DecimalField(label="Price/item", validators=[DataRequired()])
    qty = IntegerField(label='Qty', validators=[DataRequired()])
    submit = SubmitField(label='Add to Inventory')

# add new data entry in Enter purchase
class DataEntry(FlaskForm):

    # Customer_name = StringField(label="Customer_name", validators=[DataRequired()])
    # Address = StringField(label="Address", validators=[DataRequired()])
    Parts_purchased = StringField(label="Parts_purchased", validators=[DataRequired()])
    Qty = IntegerField(label='Qty', default='1', validators=[DataRequired()])
    Price = DecimalField(label='Price/Item', validators=[DataRequired()])
    Submit = SubmitField(label="Submit")


# search in Customer inquiry
class search_form(FlaskForm):
    S_name = StringField(label='Search by Name: ')
    S_address = StringField(label='Search by Address: ')
    Submit = SubmitField(label="Submit")



# form to reset password, single username and is constant
class reset_password(FlaskForm):
    Username = "Admin"
    Password = PasswordField(validators=[DataRequired()], )
    Submit = SubmitField(label="Submit")


# login form
class login_form(FlaskForm):
    Username = StringField(label="Username")
    Password = PasswordField(validators=[DataRequired()], label="Password", )
    Submit = SubmitField(label="Submit")


# set_password form
class set_password(FlaskForm):
    Username = StringField(label="Username")
    Password = PasswordField(validators=[DataRequired()], label="Password", )
    Submit = SubmitField(label="Submit")





# class Mechanic_Entry(FlaskForm):
#     id = IntegerField(nullable=False, primary_key=True)
#     name = StringField(length=30, unique=False, nullable=True)
#     address = StringField(db.String(length=100), nullable=True)
#     contact = IntegerField()
