from flask import Flask,redirect,url_for,render_template,request
from matplotlib import pyplot as plt
import pandas as pd


import matplotlib
matplotlib.use('Agg')

app=Flask(__name__)
@app.route('/',methods=['GET','POST'])
def home():

    if request.method=='POST':
        return render_template('index.html')
    return render_template('index.html')


@app.route('/plot',methods=['GET','POST'])
def generateCumulativeReports():
    x = ['1', '2']
    y = ['20', '40']

    plt.plot(x,y)
    plt.show()

    return "Done"


@app.route('/csv', methods=['GET', 'POST'])
def csv():
    # create csv

    pass

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)