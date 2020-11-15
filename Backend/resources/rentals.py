from flask_restful import Resource, reqparse
from models.rentals import RentalsModel
from datetime import datetime

parser = reqparse.RequestParser()
parser.add_argument('moto_id', type=int, required=False, help='Moto id of rented moto.')
parser.add_argument('user_id', type=int, required=False, help='User id of rented moto.')


class Rentals(Resource):
    """
    API Restful methods for Rentals
    """

    def get(self, id):
        """
        GET method
        Gets a rental by id
        Param: int id
        Return: dict (account ok / message)
        """

        rental = RentalsModel.find_by_id(id=id)

        if rental:
            return {'rental': rental.json()}, 200
        else:
            return {'message': 'Rental with id [{}] not found'.format(id)}, 404

    def post(self):
        """
        POST method
        Adds a new rental. This method is used for initialize a rental.
        Return: dict (rental created / message)
        """
        data = parser.parse_args()

        if not data['moto_id']:
            return {'message': {
                "moto_id": "Moto_id cant be empty"
            }}, 400
        if not data['user_id']:
            return {'message': {
                "user_id": "User_id cant be empty"
            }}, 400

        rental = RentalsModel(moto_id=data['moto_id'],
                              user_id=data['user_id'],
                              book_hour=datetime.now().isoformat())


        try:
            rental.save_to_db()
            return {'rental': RentalsModel.find_by_id(rental.id).json()}, 201

        except:
            return {'message': 'Internal server error'}, 500

    def put(self, id):
        """
        PUT method
        Updates a rental. This method is used for finish a rental.
        :param id:
        :return: dict (rental updated / message)
        """
        rental = RentalsModel.find_by_id(id)
        if rental.finish_rental_hour is not None:
            return {'message': 'The rental is already finsished.'}, 409

        try:
            rental.update_finish_rent_hour(datetime.now().isoformat())
            new_rental = RentalsModel.find_by_id(rental.id)
            return {'rental': new_rental.json()}, 200
        except:
            return {'message': 'Internal server error'}, 500


    def delete(self, id):
        """
        DELETE method
        Removes a rental
        Param: int id
        Return: dict (message ok / message)
        """
        rental = RentalsModel.find_by_id(id=id)
        if rental:
            try:
                rental.delete_from_db()
                return {'message': "Rental with id [{}] and all associated info deleted".format(id)}, 200
            except:
                return {'message': "Internal server error"}, 500
        else:
            return {'message': "Rental with id [{}] Not found".format(id)}, 404

class RentalsList(Resource):
    """
    API Restful methods for RentalsList
    """
    def get(self):
        """
        GET method
        Return: dict (rentals)
        """
        rentals = RentalsModel.all_rentals()
        return {'rentals': [rental.json() for rental in rentals]}, 200