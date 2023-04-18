from flask import Flask, render_template, url_for, request, flash
#Это ветка log-in

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fawheoilnfweaughsaweogihanfk'

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/contact', methods = ['GET', 'POST'])
def contact():
    
    if request.method =='POST':
        #print(request.form)
        
        #Нужно добавить ещё критерии
        
        if len(request.form['username']) >= 2:
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка отправки', category='error')
        
    
    return render_template('contact.html')


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
