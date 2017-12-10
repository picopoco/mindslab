from flask import Flask, jsonify
from flaskext.mysql import MySQL
from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse

app = Flask(__name__)


@app.route('/')
def lsmStartPage():
    return  jsonify({'url':['1open','1sq'],'cur_turn':'1sq'})

# @app.route('/coif/lms' ,methods=['GET','POST'])
# def lms():
#    # jsonify({'task': make_public_task(task[0])})
#     return  jsonify({'url':['1open','1sq'],'cur_turn':'1sq'})

if __name__ == '__main__':
    app.run(debug=False)

    #app.run(debug=True ,host='0.0.0.0',port=5000)
