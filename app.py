from flask import Flask, render_template, redirect, url_for, request, session
import os
import stripe


app = Flask(__name__)
app.secret_key = os.urandom(24)

stripe_keys = {
    'secret_key': os.environ['STRIPE_KEY'],
    'publishable_key': os.environ['STRIPE_PUBLIC_KEY']
}

stripe.api_key = stripe_keys['secret_key']



@app.route("/home")
@app.route("/")
def index():
    session['user'] = 'Mate'
    return render_template('home.html', key=stripe_keys['publishable_key'])

@app.route("/charge", methods=['GET', 'POST'])
def charge():

    if request.method == 'POST':
        #amount in cents
        amount = 6900

        customer = stripe.Customer.create(
            email=request.form['stripeEmail'],
            source=request.form['stripeToken']
        )

        stripe.Charge.create(
            customer=customer.id,
            amount=amount,
            currency='usd',
            description='Flask Charge'
        )
        return render_template('charge.html', amount=amount)

    return redirect(url_for('index'))


# File upload
@app.route("/upload", methods=['POST'])
def upload():
    file = request.files['inputFile']

    return file.filename


@app.route("/checkout")
def checkout():
    if 'user' in session:
        return session['user']
    
    return 'You must be logged in to checkout.'

@app.route("/dropsession")
def dropsession():
    session.pop('user', None)
    return 'Dropped'


if __name__ == '__main__':
    app.run(debug=True)
