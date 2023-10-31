# my_flask_app/__init__.py

from flask import Flask, render_template, request

def create_app():
    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        search_results = []
        if request.method == 'POST':
            query = request.form['search']
            search_results = [
                {'title': 'Result 1', 'content': f'Content for {query} 1'},
                {'title': 'Result 2', 'content': f'Content for {query} 2'},
            ]
        return render_template('index.html', search_results=search_results)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
