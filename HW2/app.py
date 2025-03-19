from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 從表單取得使用者輸入的 grid 大小
        try:
            n = int(request.form.get('grid_size', 5))
        except ValueError:
            n = 5
        # 限制 n 的範圍
        if n < 5 or n > 9:
            n = 5
        return redirect(url_for('grid', n=n))
    return '''
    <h2>請輸入格子大小 n (介於 5 ~ 9):</h2>
    <form method="post">
        <input type="number" name="grid_size" min="5" max="9" value="5" required>
        <input type="submit" value="建立格子">
    </form>
    '''

@app.route('/grid/<int:n>')
def grid(n):
    # 產生一個 n x n 的列表，用於模板中產生格子
    grid = [[{'row': i, 'col': j} for j in range(n)] for i in range(n)]
    return render_template('grid.html', grid=grid, n=n)

if __name__ == '__main__':
    app.run(debug=True)
