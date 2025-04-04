from flask import Flask, render_template

app = Flask(__name__)

# Route cho trang chủ
@app.route('/')
def home():
    return render_template('index.html')

# Route khi bấm nút
@app.route('/hello')
def say_hello():
    return '<h1>Hello World</h1>'

if __name__ == '__main__':
    app.run(debug=True)
