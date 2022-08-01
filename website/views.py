from lib2to3.pgen2 import token
from time import strftime
import traceback
from . import db, token_price_api_calls
from .models import Note, User, Asset, Node
import datetime
import time
from flask import Blueprint, flash, Flask, jsonify, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from unicodedata import category
from dotenv import load_dotenv
import os

#from polygonscan import PolygonScan - You need this if using github poly scan code

import json
import requests


views = Blueprint('views', __name__)

# Home view
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('home.html', user=current_user) 
    #checks to see if current user is authenticated (for base.html)

@views.route('/add-node', methods = ['GET', 'POST'])
@login_required
def add_node():
    if request.method == 'POST':
        node_network = request.form.get('networkName')
        node_address = request.form.get('nodeAddress')
        network_token = request.form.get('networkToken')

        new_node = Node(network=node_network, wallet_address=node_address, token=network_token)

        db.session.add(new_node)
        db.session.commit()
        flash('New Node Added', category='success')
        return redirect(url_for('views.view_nodes'))

    return render_template('/nodes/add_node.html', user=current_user)


@views.route('/view-nodes', methods = ['GET', 'POST'])
@login_required
def view_nodes():
    nodes = Node.query.all()

    return render_template('/nodes/view_nodes.html', user=current_user, nodes=nodes)


@views.route('/view-node/<int:id>', methods = ['GET', 'POST'])
@login_required
def view_individual_node(id):
    node_to_edit = Node.query.get_or_404(id)

    return render_template('/nodes/view_individual_node.html', user=current_user, node_to_edit=node_to_edit)

    



@views.route('/transaction-tracking', methods = ['GET', 'POST'])
@login_required
def transactions():
    load_dotenv()
    john_matic_address = os.getenv("JOHN_MATIC_ADDRESS")
    pyr_contract_address = "0x430EF9263E76DAE63c84292C3409D61c598E9682"
    lava_contract_address = "0xb4666B7402D287347DbBDC4EA5b30E80C376c0B3"
    adam_address = os.getenv("ADAM_MATIC_ADDRESS")
    # Remember to hide this when going into production
    api_key = os.getenv("API_KEY")

    ## Will likely move this to a new page (Polgon API calls)
    # For token amount
    token_amount_api_call = requests.get(
        f"https://api.polygonscan.com/api?module=account&action=tokenbalance&contractaddress={pyr_contract_address}&address={john_matic_address}&tag=latest&apikey={api_key}"
        )
    token_data = json.loads(token_amount_api_call.text)
    token_amount = (float(token_data['result'])/(10**18))
    # For transactions
    pyr_transactions_api_call = requests.get(
        f"https://api.polygonscan.com/api?module=account&action=tokentx&contractaddress={pyr_contract_address}&address={john_matic_address}&startblock=0&endblock=999999999999999999999&page=1&offset=30&sort=asc&apikey={api_key}"
        )
    transaction_data = pyr_transactions_api_call.json()['result']
    print(type(transaction_data))
    i = 0
    for row in transaction_data:
        readable_datetime = time.ctime(float(row['timeStamp']))
        # Adds readable date and time to row dictionary
        row['dateTime'] = readable_datetime
        row['value'] = float(row['value'])/(10**float(row['tokenDecimal']))

        # Adds changes to transaction_data list
        transaction_data[i] = row
        i += 1
    
    print(transaction_data)


    return render_template('/transactions/transaction_home.html', 
    user=current_user,
    address=john_matic_address, 
    token_amount=token_amount,
    data=transaction_data
    )



    # This is the code to use with the Github functions written
    # with PolygonScan("7UW6I72B4W8HSIWH41NKX5QMD97NZ6F85Z",False) as pyr:
    #     print(float(pyr.get_matic_balance(john_matic_address))/1000000000000000000)
    #     print(float(pyr.get_acc_balance_by_token_and_contract_address(lava_contract_address, john_matic_address))/1000000000000000000) 
    #     pyr_in_wallet = float(pyr.get_acc_balance_by_token_and_contract_address(pyr_contract_address, john_matic_address)) / 1000000000000000000
    #     return str(pyr_in_wallet)


# View to add first part of asset
@views.route('/add-asset', methods = ['GET', 'POST'])
@login_required
def add_asset():
        return render_template('add_asset_1.html', user=current_user)


# View to add a specific asset type
@views.route('/add-asset/<string:assetType>', methods=['GET', 'POST'])
@login_required
def process_asset(assetType):
    if request.method == 'POST':
        if assetType=='Hardware Asset':
            hardware_value = request.form.get('assetValue')
            print(hardware_value)
            try:
                hardware_value = float(hardware_value)
                #if hardware_value == ' ':
                #    flash('Please input a number', category='error')
                new_asset = Asset(type='Hardware Asset', purchase_price='N/A', purchase_type='N/A', usd_price=hardware_value)
                db.session.add(new_asset)
                db.session.commit()
                return redirect(url_for('views.view_assets')) 
            except:
                flash('Please input a number', category='error')
        try:
            token_amount = request.form.get('tokenAmount')
            token_amount = float(token_amount)
            print(token_amount)
            if assetType=='NFT' or assetType=='Digital Land':
                crypto_selected = request.form.get('cryptoSelected')                    
                if len(crypto_selected) > 20:
                    flash('Please select a token', category='error')

                # Put other errors here with "elif"

                else:
                    usd_price = token_price_api_calls.asset_usd_price(crypto_selected, token_amount)
                    asset_description = request.form.get('assetDescription')
                    date = request.form.get('date_bought')
                    print(date)
                    asset_date_bought = datetime.datetime.strptime(date, "%Y-%m-%d")
                    new_asset = Asset(description=asset_description, type=assetType, purchase_price=token_amount, purchase_type=crypto_selected, usd_price=usd_price, date_bought=asset_date_bought)
                    db.session.add(new_asset)
                    db.session.commit()
                    flash('New Asset Added', category='success')
                    return redirect(url_for('views.view_assets'))

        except:
            traceback.print_exc()
            flash('Check traceback for error', category='error')


    asset_json = '{"assetType":' + '"' + assetType + '"}'
    asset_type = json.loads(asset_json)
    current_date = datetime.date.today()
    # current_date_proper_display = datetime.strftime(current_date, "%m-%d-%Y")
    # # Converting to date-time obj
    # current_date_proper_display = datetime.strptime(current_date_proper_display, "%m-%d-%Y")
    # print(current_date_proper_display)
    return render_template('add_asset_2.html', user=current_user, asset_type=assetType, current_date=current_date)


# Delete specific asset
@views.route('/delete-asset/<int:id>', methods = ['GET'])
@login_required
def delete_asset(id):
    asset_to_delete = Asset.query.get_or_404(id)
    print(asset_to_delete)

    try:
        flash(f'Asset has been deleted', category='error')
        db.session.delete(asset_to_delete)
        db.session.commit()
        return redirect(url_for('views.view_assets'))
    except:
        return "We ran into a problem bro. A big time problem"


# Sell a specific asset
@views.route('/sell-asset/<int:id>', methods = ['GET', 'POST'])
@login_required
def sell_asset(id):
    #### TO DO
    # Remember to add an alternate display on html for hardware asset
    if request.method == 'POST':
        asset_sold = Asset.query.filter_by(id=id).first()
        asset_sold.sale_price = float(request.form.get('tokenSaleAmount'))
        asset_sold.currently_owned = False
        asset_sold.date_sold = datetime.datetime.strptime(request.form.get('date_sold'), "%Y-%m-%d")
        date_in_api_form = datetime.datetime.strftime(asset_sold.date_sold, "%d-%m-%Y")
        asset_sold.usd_sale_price = float(token_price_api_calls.token_call_date(asset_sold.purchase_type, date_in_api_form) * asset_sold.sale_price)
        # Formats sale price
        asset_sold.usd_sale_price = '{:.2f}'.format(asset_sold.usd_sale_price)
        if datetime.datetime.strftime(asset_sold.date_sold, "%Y-%m-%d") < datetime.datetime.strftime(asset_sold.date_bought, "%Y-%m-%d"):

            ## Need to clean this code up as it repeats from the GET section below
            # Add a error function page
            item_sold = Asset.query.get_or_404(id)
            item_sold.purchase_type = token_price_api_calls.token_display_switch(item_sold.purchase_type)
            current_date = datetime.datetime.now()
            item_sold.date_sold = datetime.datetime.strftime(current_date, "%Y-%m-%d")
            flash('Date sold must be on or after date bought', category='error')

            return render_template('sell_asset.html', user=current_user, item=item_sold)
        asset_sold.capital_gain = '{:.2f}'.format(float(asset_sold.usd_sale_price) - float(asset_sold.usd_price))

        db.session.commit()
        return redirect(url_for('views.view_sold_assets'))

    if request.method == 'GET':
        item_sold = Asset.query.get_or_404(id)
        current_date = datetime.datetime.now()
        item_sold.date_sold = datetime.datetime.strftime(current_date, "%Y-%m-%d")
        item_sold.purchase_type = token_price_api_calls.token_display_switch(item_sold.purchase_type)
        return render_template('sell_asset.html', user=current_user, item=item_sold)
    else:
        try:
            hardware_value = float(hardware_value)
            #if hardware_value == ' ':
            #    flash('Please input a number', category='error')
            new_asset = Asset(type='Hardware Asset', purchase_price='N/A', purchase_type='N/A', usd_price=hardware_value)
            db.session.add(new_asset)
            db.session.commit()
            return redirect(url_for('views.view_assets')) 
        except:
            flash('Please input a number', category='error')


# View sold assets
@views.route('/sold-assets', methods = ['GET'])
@login_required
def view_sold_assets():
    assets = Asset.query.all()
    asset_pnl = 0
    for asset in assets:
        if asset.currently_owned == False:
            # Need to fix this so there is only two decimal places
            asset_pnl = float('{:.2f}'.format(asset_pnl + asset.capital_gain))
            asset.purchase_type = token_price_api_calls.token_display_switch(asset.purchase_type)
            asset.date_bought = asset.date_bought.strftime("%a %b %d %Y")
            asset.date_sold = asset.date_sold.strftime("%a %b %d %Y")


    return render_template('view_sold_assets.html', user=current_user, assets=assets, asset_pnl=asset_pnl)


# View currently owned assets
@views.route('/view-assets', methods = ['GET'])
@login_required
def view_assets():
    assets = Asset.query.all()
    for asset in assets:
        if asset.currently_owned == True:
            # This will cause a ton of API calls to be used, so it is commented out for now
            # current_usd_price = float(token_price_api_calls.asset_usd_price(asset.purchase_type, asset.purchase_price))
            asset.purchase_type = token_price_api_calls.token_display_switch(asset.purchase_type)
            asset.date_bought = asset.date_bought.strftime("%a %b %d %Y")

            ## May have to get rid of this because it will use a lot of API calls
            # asset.current_usd_price = current_usd_price

    return render_template('view_assets.html', user=current_user, assets=assets)


# Allows user to edit their asset if they input something wrong
@views.route('/edit-owned-asset/<int:id>', methods = ['GET', 'POST'])
@login_required
def edit_owned_asset(id):
    # moose
    allowed_attributes = [
        'description',
        'purchase_type',
        'purchase_price',
        'usd_price',
        'date_bought',
        'type',
    ]

    asset_to_edit = Asset.query.get_or_404(id)
    print(asset_to_edit)
    print(asset_to_edit.purchase_price)
    if request.method == 'POST':
        # Pulls data from the HTML update page
        asset_dictionary = request.form
        # The python variable and name from HTML must be the same for this to work
        for key, value in asset_dictionary.items():
            print('key:', key)
            print('value:', value)
            if key in allowed_attributes and asset_dictionary[key]:
                setattr(asset_to_edit, key, value)
                if key == 'purchase_price':
                    try:
                        print('type of crypto used to buy:', asset_dictionary['purchase_type'])
                        print('type of coin used to purchase:', asset_dictionary['purchase_type'])
                        asset_to_edit.purchase_type = asset_dictionary['purchase_type']
                        usd_asset_price = token_price_api_calls.asset_usd_price(asset_dictionary['purchase_type'], asset_dictionary['purchase_price'])
                        print('coin used to purchase this asset', asset_to_edit.purchase_type)
                        print(value)
                        print(usd_asset_price)
                        asset_to_edit.usd_price = usd_asset_price
                        asset_to_edit.purchase_price = value
                        print(asset_to_edit.usd_price)
                    except:
                        flash('You need to update both token amount and token type', category='error')
                        asset_to_edit.purchase_type = token_price_api_calls.token_display_switch(asset_to_edit.purchase_type)
                        return render_template('edit_owned_asset.html', user=current_user, asset_to_edit=asset_to_edit) 
            if key == 'purchase_type':
                if not asset_dictionary['purchase_price']:
                    asset_to_edit.usd_price = token_price_api_calls.asset_usd_price(value, asset_to_edit.purchase_price)
                    asset_to_edit.purchase_type = value
                    print('The token is:', asset_to_edit.purchase_type)
            if key == 'date_bought':
                if asset_dictionary['date_bought']:
                    date_string = value
                    asset_to_edit.date_bought = datetime.datetime.strptime(date_string, "%Y-%m-%d")
                    date_in_api_form = datetime.datetime.strftime(asset_to_edit.date_bought, "%d-%m-%Y")
                    asset_to_edit.usd_price = float(token_price_api_calls.token_call_date(asset_to_edit.purchase_type, date_in_api_form)) * float(asset_to_edit.purchase_price)
                    # Format usd price
                    asset_to_edit.usd_price = '{:.2f}'.format(asset_to_edit.usd_price)
                    print(asset_to_edit.usd_price)
                    print(asset_to_edit.date_bought)
                    print(type(asset_to_edit.date_bought))


                print('The key/value is:', key, value)
            
                db.session.commit()

        flash('Asset updated!', category='success')
        asset_to_edit.purchase_type = token_price_api_calls.token_display_switch(asset_to_edit.purchase_type)
        return redirect(url_for('views.view_assets'))

    print('new purchase type is:', asset_to_edit.purchase_type)
    print(asset_to_edit.purchase_price)
    print(asset_to_edit.usd_price)
    asset_to_edit.current_usd_price = float(token_price_api_calls.asset_usd_price(asset_to_edit.purchase_type, asset_to_edit.purchase_price))
    asset_to_edit.purchase_type = token_price_api_calls.token_display_switch(asset_to_edit.purchase_type)
    asset_to_edit.date_bought = asset_to_edit.date_bought.strftime("%Y-%m-%d")

    return render_template('edit_owned_asset.html', user=current_user, asset_to_edit=asset_to_edit)




###Users
# See the users who have signed up
@views.route('/users', methods= ['GET'])
@login_required
def users():
    names = User.query.all()
    return render_template('users.html', user=current_user, names=names)
    # current_user checks to see if current user is authenticated (for base.html)




# Will want to create different vlueprints for each "app"
# After asset tracking app is created, transaction blueprint will be created
# Still need to create for transactions
@views.route('/add-transaction', methods= ['GET', 'POST'])
@login_required
def add_transaction():
    #assets = Asset.query.all()
    return render_template('add_transaction.html', user=current_user)



# Views for the "notes" app
@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('You need to add more to your note', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template('notes.html', user=current_user) 


@views.route('/delete-note/<int:id>')
def delete_note(id):
    note_to_delete = Note.query.get_or_404(id)

    try:
        flash(f'Note #{id} has been deleted', category='error')
        db.session.delete(note_to_delete)
        db.session.commit()
        return redirect(url_for('views.notes'))
    except:
        return "We ran into a problem bro. A big time problem"

    """ This is javascript code from the Tech with Tim tutorial

    note = json.loads(request.data)
    noteId = note['noteId']
    note = note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            # This is a security check so you can only delete your own notes
            db.session.delete(note)
            db.session.commit()
    """
            
    return jsonify({}) # turns into json object that can be returned