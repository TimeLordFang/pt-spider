from flask import Flask,render_template
import get3pt

app = Flask(__name__)

@app.route('/')
def show_pt():
    x=  get3pt.GetMT()
    #x = [[1,u'vd'],[3,u'rf'],[u'asd',u'1ra']]
    return render_template('hello.html',x_list = x)

if __name__ == '__main__':
    
    app.run(host='0.0.0.0',debug=True)
