from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class GetData(Resource):
    def get(self):
        data = open("../data.csv", "r").read()
        return data


api.add_resource(GetData, '/get_data')


if __name__ == '__main__':
    app.run(debug=True)