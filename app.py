import joblib
from flask import jsonify
from flask import Flask, request
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask_restful import Resource, Api, reqparse
from tensorflow import keras



app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()  # used to parse incoming requests
parser.add_argument('minimum_nights', required=True,
                    help='minimum_nights cannot be blank!')
parser.add_argument('number_of_reviews', required=True,
                    help='number_of_reviews cannot be blank!')
parser.add_argument('reviews_per_month', required=True,
                    help='reviews_per_month cannot be blank!')
parser.add_argument('neighbourhood_group', required=True,
                    help='neighbourhood_group cannot be blank!')
parser.add_argument('room_type', required=True,
                    help='room_type cannot be blank!')
class predict_category(Resource):
    def post(self):
        our_dict = {0:"workout",1:"diet for next days",2:"diet for today"}
        args = parser.parse_args()
        minimum_nights = float(args['minimum_nights'])

        number_of_reviews = float(args['number_of_reviews'])

        reviews_per_month = float(args['reviews_per_month'])

        neighbourhood_group = args['neighbourhood_group']
        dict_neighbourhood_group = {'ciutat vella':0, 'eixample':0, 'gràcia':0, 'horta-guinardó':0,'les corts':0 ,'nou barris':0, 'sant andreu':0, 'sant martí':0,'sants-montjuïc':0, 'sarrià-sant gervasi':0}
        dict_neighbourhood_group[neighbourhood_group.lower()] = 1
        neighbourhood_group = dict_neighbourhood_group.values()
        

        room_type = args['room_type']
        dict_room_type = {"entire home/apt":0,  "hotel room":0,   "private room":0,   "shared room":0}
        dict_room_type[room_type.lower()] = 1
        room_type = dict_room_type.values()

        print(minimum_nights,number_of_reviews,reviews_per_month,neighbourhood_group,room_type)
        model = keras.models.load_model('weight.hdf5')
        x = [minimum_nights,number_of_reviews,reviews_per_month]
        x.extend(neighbourhood_group)
        x.extend(room_type)
        x = [x]
        # print(x)
        y_predict = model.predict(x)
        # print(y_predict)
        # x = [[minimum_nights,number_of_reviews,reviews_per_month,]]
        
        return jsonify({'price': str(y_predict[0][0])})

api.add_resource(predict_category, '/predict')

if __name__ == '__main__':
    app.run()