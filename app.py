from flask import Flask, render_template, url_for, request, flash

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from telegram_send import send

import smtplib
import config
import phonenumbers
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fawheoilnfweaughsaweogihanfk'


def send_email(subject, text):
    msg = MIMEMultipart()
    msg['From'] = config.login
    msg['To'] = config.login
    msg['Subject'] = subject
    msg.attach(
        MIMEText(text, 'plain')
    )
    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    server.ehlo() #config.login
    server.login(config.login, config.password)
    server.auth_plain()
    server.send_message(msg)
    server.quit()


def check_phone(phone):
    try:
        phone_number = phonenumbers.parse(phone)
        # Validating a phone number
        valid = phonenumbers.is_valid_number(phone_number)
        # Checking possibility of a number
        possible = phonenumbers.is_possible_number(phone_number)
        flag = valid and possible
    except:
        flag = False
    return flag


@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/contact', methods = ['GET', 'POST'])
def contact():
    
    if request.method =='POST':
        username = request.form['username']
        phone = request.form['phone']
        msg = request.form['message']
        #if len(msg) > 150:
        #    msg = msg[:150]
        today = datetime.datetime.today()
        if len(phone) >= 11 and phone.startswith('8'):
            phone = phone.replace('8', '+7', 1)

        if check_phone(phone):
            if len(username) >= 2:
                flash('Сообщение отправлено', category='success')
                send_email('Данные клиента', f"Имя клиента:   {username}\nСообщение:   {msg}\nТелефон:   {phone}\nДата:   {today.strftime('%d/%m/%Y')}")
                # Отправка сообщения на почту kalonovmir@yandex.ru
                send(messages=[
                    f'Имя клиента:   {username}\nТелефон:   {phone}\nСообщение:   {msg}\nДата:   {today.strftime("%d/%m/%Y")}'])
                # Отправка сообщения в telegram https://t.me/+jF1xPhX46qgxYjMy
            else:
                flash('Ваше имя не может быть меньше 2 знаков', category='error')
        else:
            flash('Ваш номер не определен', category = 'error')
        
    return render_template('contact.html')

@app.route('/contact_to_mail', methods = ['GET', 'POST'])
def contact_to_mail():
    
    if request.method =='POST':
        username = request.form['username']
        phone = request.form['phone']
        today = datetime.datetime.today()
        #flag = True
        if len(phone) >= 11 and phone.startswith('8'):
            phone = phone.replace('8', '+7', 1)

        if check_phone(phone):
            if len(username) >= 2:
                flash('Сообщение отправлено', category='success')
                send_email('Данные клиента', f"Имя клиента:   {username}\nТелефон:   {phone}\nДата:   {today.strftime('%d/%m/%Y')}")
                
                send(messages=[
                    f'Имя клиента:   {username}\nТелефон:   {phone}\nДата:   {today.strftime("%d/%m/%Y")}'])
                # Отправка сообщения в telegram https://t.me/+jF1xPhX46qgxYjMy
            else:
                flash('Ваше имя не может быть меньше 2 знаков', category='error')
        else:
            flash('Ваш номер не определен', category = 'error')
    return render_template('contact_to_mail.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


@app.route('/discount')
def discount():
    return render_template('discount.html')


@app.route('/service')
def service():
    return render_template('service.html')


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html')


if __name__ == "__main__":
    app.run(debug=True)
