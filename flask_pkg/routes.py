from datetime import datetime
from time import sleep
from sqlalchemy import desc
from . import app
from flask import render_template, redirect, url_for, request, jsonify
from .form import *
from .models import *
from . import db
from . import bcrypt
from flask import session
from sqlalchemy import extract, and_
import json



@app.route('/', methods=['GET','POST'])
def home():
    names = [items.name for items in CEntry.query.join(DEntry).order_by(desc(DEntry.price))]
    prices = [int(items.price) for items in DEntry.query.all()]
    prices = sorted(prices, reverse=True)

    # create string of list of names of highest puchases to send to graph in home page through home.js
    names_str = ""
    price_str = ""
    for name,price in zip(names,prices):
        names_str += name[:15]+','
        price_str += str(price)+','

    # Monthly-sales data extracting from db here:
    Query_time = db.session.query(DEntry.time)
    Query_price = db.session.query(DEntry.price)
    current_year_and_month = [datetime.now().year, datetime.now().month]
    months_for_monthly_sale = []
    list_datetime = []
    list_price = []

    #getting list of datetimes and respective prices of purchase on monthly basis of past 12 months
    for i in range(current_year_and_month[1], current_year_and_month[1]-12, -1):
        if i == 0:
            current_year_and_month[0] -= 1
            current_year_and_month[1] = 12
        list_datetime += [Query_time.filter(
          and_(  
            extract('year', DEntry.time) == current_year_and_month[0],
            extract('month', DEntry.time) == current_year_and_month[1]
              )
            ).all()]
        list_price += [Query_price.filter(
          and_(  
            extract('year', DEntry.time) == current_year_and_month[0],
            extract('month', DEntry.time) == current_year_and_month[1]
              )
            ).all()]
        months_for_monthly_sale += [current_year_and_month[1]]
        current_year_and_month[1] -= 1
    
    # totaling of prices per month
    monthly_sale = []
    monthly_total = 0
    for price in list_price:
    #   price is sublists containing elements prices 
    #   price = [(Decimal('1.00'),), (Decimal('2000.00'),)]  ---> list
    #   sublist/items = (Decimal('1.00'),) ---> tuple
        for items in price:
            monthly_total += int(items[0])
        monthly_sale += [monthly_total]
        monthly_total = 0     
    if request.method == 'POST':
        data = json.loads(request.data.decode('utf-8'))
        if data['key'] == "montlySalesGraph":
            return jsonify({'monthly_sale':monthly_sale, 'months':months_for_monthly_sale})

    return render_template('home.html', data=names_str, price=price_str)



LASTENTRY = []
e_form_note = ""

@app.route('/eform', methods=['GET', 'POST'])
def e_form():
    form_data = DataEntry()
    data_list = CEntry.query.all()
    part_list = PEntry.query.all()
    address_list = {}
    parts = {}
    err_msg = ""
    error_note = ""
    
    # get the customer list and parts/price list 
    for item in data_list:
        address_list[item.name] = item.address
    for part in part_list:
        parts[part.name] = float(part.price)
    
    if request.method == "POST":
        global LASTENTRY
        global e_form_note
        
        # setting part price
        received_part = request.data.decode('utf-8')
        try:
            if received_part in parts:
                part_price = parts[received_part]
                return jsonify({"price": part_price})
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        
        # Running validations ( form values: validate on submit(), Dropdown ele for customer selection: request.form['custid])
        error_note = ""

        if form_data.validate_on_submit() and request.form['custid']:
            data = DEntry(
                parts=request.form['Parts_purchased'],
                qty=form_data.Qty.data,
                price=float(request.form['Price']) * form_data.Qty.data,
                cust_id=request.form['custid'],
                # time=datetime.strptime(datetime.datetime.now().strftime('%d-%m-%Y ~ %H:%M'), '%d-%m-%Y ~ %H:%M')
            )
            selected_customer = CEntry.query.filter_by(cust_id=request.form['custid']).first()
            # print(selected_customer, "   -    ", '\n', datetime.datetime.now().second)
            # LASTENTRY['Name'] = selected_customer.name
            # LASTENTRY['Address'] = selected_customer.name
            # LASTENTRY['Name'] = selected_customer.name
            # LASTENTRY['Name'] = selected_customer.name
            inv = PEntry.query.filter_by(name=request.form['Parts_purchased']).first()
            if inv.qty - form_data.Qty.data >= 0:
                inv.qty = inv.qty - form_data.Qty.data
                db.session.add(data)
                db.session.commit()
                e_form_note = f"Purchased was made for customer {selected_customer}"
                return redirect(url_for('e_form'))
            else:
                e_form_note = f"Not enough Inventory. Available qty: {inv.qty}"

                # print("=" * 10, form_data.Qty.data,
                #       PEntry.query.filter_by(name=request.form['Parts_purchased']).first().qty)
                return redirect(url_for('e_form'))

        else:
            err_msg = "Validation error!!!, Please fill all the fields before submitting."
            
    return render_template('eform.html', form=form_data, name_list=data_list, part_list=parts,
                           address_list=address_list,
                           lastentry=LASTENTRY, e_form_note=e_form_note, err_msg=err_msg)


NOTE = ""


@app.route('/pform', methods=['GET', 'POST'])
def p_form():
    global NOTE
    form_data = Part()
    if form_data.validate_on_submit():
        data = PEntry(name=form_data.name.data.strip(),
                      price=form_data.price.data,
                      qty=form_data.qty.data
                      )
        db.session.add(data)
        db.session.commit()
        NOTE = f"Last entry: PART: {data.name} for ₹{data.price} was saved to Inventory"
        return redirect(url_for('p_form'))
    return render_template('pform.html', form=form_data, note=NOTE)


success_note = ""


@app.route('/cform', methods=['GET', 'POST'])
def c_form():
    global success_note
    form_data = Customer_Entry()
    if request.method == "POST":
        if form_data.validate_on_submit():
            print(form_data.validate_on_submit())
            data = CEntry(name=form_data.name.data,
                          address=form_data.address.data,
                          contact=form_data.contact.data
                          )
            db.session.add(data)
            db.session.commit()
            success_note = [f"Success: Customer - {data.name}, {data.address}, {data.contact} was created."] 

            return redirect(url_for('c_form'))
    if form_data.errors != {}:
        for err_msg in form_data.errors.values():
            print(f" There was an error {err_msg}")
    return render_template('cform.html', form=form_data, success_note=success_note)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    Query = db.session.query(PEntry)

    if request.method == "GET":
        if request.args.get('sort') and request.args.get('sort') == 'name':
            results = Query.order_by(PEntry.name).all()
        else:
            results = Query.all()
        if request.args.get('delete_btn'):
            Query.filter_by(part_id=request.args.get('delete_btn')).delete()
            db.session.commit()
            return redirect(url_for('delete'))
        if request.args.get('edit'):
            item = Query.filter_by(part_id=request.args.get('edit')).first()
            return render_template('edit.html', item=item)
        if request.args.get('newval'):
            Query.filter_by(part_id=request.args.get('hid')).first().qty = request.args.get('newval')
            db.session.commit()
            return redirect(url_for('delete'))
    NOTE = ""
    print(request.method, request.args, request.form)
    if request.method == "POST":
        results = []
        if request.form['name']:
            results += Query.filter(PEntry.name.like(f"%{request.form['name']}%"))
            print(results, Query)
            if not results:
                NOTE = "Not found in database"
            else:
                NOTE = f"{len(results)} entry/ies found"
    # print(results)
    return render_template('delete.html', results=results, note=NOTE)


@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    Query = db.session.query(PEntry)
    if request.method == "GET":
        if request.args.get('sort') == 'name':
            results = Query.order_by(PEntry.name).all()
        else:
            results = Query.all()
    NOTE = ""
    print(request.method, request.args, request.args.get('sort'))
    if request.method == "POST":
        results = []
        if request.form['name']:
            results += Query.filter(PEntry.name.like(f"%{request.form['name']}%"))
            print(results, Query)
            if not results:
                NOTE = "Not found in database"
            else:
                NOTE = f"{len(results)} entry/ies found"
    return render_template('inventory.html', results=results, note=NOTE)


@app.route('/customerlist', methods=["GET", "POST"])
def customerlist():
    query = db.session.query(CEntry)
    results = query.order_by(CEntry.name).all()
    form_data = search_form()
    NOTE = ""
    if request.args.get('sort'):
        if request.args.get('sort') == 'name':
            items = query.order_by(desc(CEntry.name)).all()
            return render_template('customerlist.html', form=form_data, results=items, note=NOTE)
        else:
            slug_id = request.args.get('sort')
            total = 0
            # total = ""
            customer_data = CEntry.query.filter_by(cust_id=slug_id).first()
            customer_purchased_data = DEntry.query.filter_by(cust_id=slug_id)
            # print("slug", slug_id, datetime.datetime.now().strftime('%H:%M'))
            # print(customer_data, customer_purchased_data.all())
            for item in customer_purchased_data:
                total += float(item.price)
                print(type(total))
            # c = 0
            # l = len(str(int(t)))
            # for item in reversed(str(int(t))):
                # c += 1
                # total += item
                # l -= 1
                # if c == 3 and l > 0:
                    # total += ","
                    # c = 0
            return render_template('customerdata.html', customer_data=customer_data,
                                   customer_purchased_data=customer_purchased_data.all(), total=total)
    if request.method == "POST":
        results = []
        if form_data.data['S_name']:
            results += query.filter(CEntry.name.like(f"%{form_data.data['S_name']}%"))
        if form_data.data['S_address']:
            results += query.filter(CEntry.address.like(f"%{form_data.data['S_address']}%"))
    if not results:
        NOTE = "Not found in database"
    else:
        results = set(results)
        NOTE = f"{len(results)} entry/ies"
    return render_template('customerlist.html', form=form_data, results=results, note=NOTE)


# @app.route('/redirect', methods=['GET', 'POST'])
# def redirect_page():
#     redirect_val = request.args.get('val')
#     i = 0
#     print('before for')
#     for i in range(1,1001):
#         print('inside for')
#         if i == 1000:
#             print(i)
#             return redirect_func()
#     print('after for')
#     return render_template('redirect.html', redirect_val = redirect_val)
    

@app.route('/redirect_f', methods=['GET', 'POST'])
def redirect_func():
    boolean = "user_id" in session
    print('in the redirect func',boolean)
    if boolean == True:
        return redirect(url_for('p_form'))
    else:
        sleep(0.5)
        return redirect(url_for('login'))

    

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_data = login_form()
    form_data.Username.default = "Admin"
    try:
        redirect_val = request.args.get('val')
    except:
        pass
    login_note = ""
    if not "user_id" in session:
        login_note = "Session timed out.! Please login again"
    try:
        if loginModel.query.filter_by(username = 'Admin').first().password:
            pass
    except: 
        return redirect(url_for('set_password_func'))
    if request.method == 'POST':
        entered_password = form_data.Password.data
        stored_password_hash = loginModel.query.filter_by(username = 'Admin').first().password
        if bcrypt.check_password_hash(stored_password_hash, entered_password):
            session['user_id'] = "Admin"
            login_note = "Login successful-loginnote"
            return redirect(url_for('redirect_func', )), print(login_note ,"login successful")
        else:
            login_note = "Incorrect Password!"
    return render_template('login.html', form=form_data, redirect_val = redirect_val, failed_login=login_note)



@app.route('/register-password', methods=['GET', 'POST'])
def set_password_func():
    redirect_val = request.args.get('val')

    form_data = set_password()
    form_data.Username.default = "Admin"

    # if not loginModel.query.filter_by(username = 'Admin').first().password:  
        # <--- to add a password if there is none--->


    if request.method == "POST":
        password = bcrypt.generate_password_hash(password=form_data.Password.data).decode('utf-8')
        data = loginModel(
            username = "Admin",
        password = password)
        db.session.add(data)
        db.session.commit()

    return render_template('register-password.html', form=form_data, redirect_val = redirect_val)




