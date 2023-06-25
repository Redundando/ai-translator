from flask import Flask, render_template, request, render_template_string

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def square():
    if request.method == 'POST':
        pass
    return render_template_string(str(review))


if __name__ == '__main__':
    app.run()