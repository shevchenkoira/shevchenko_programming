import bdb

import flask
from certificate import *
import sqlalchemy
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps


@REST.route("/")
def hello_world():
    return "Hello, REST"


@REST.route("/static/<path:path>")
def send_static(path):
    return flask.send_from_directory("static", path)


SWAGGER_URL = "/api/swagger"
API_URL = "/static/swagger.json"
swagerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={
    "app_name": "RestfulLUL"
})
REST.register_blueprint(swagerui_blueprint, url_prefix=SWAGGER_URL)

REST.register_blueprint(flask.Blueprint("restful_api", "restful_api"))


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'JWT' in flask.request.headers:
            token = flask.request.headers['JWT']

        if not token:
            return flask.jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, REST.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(email=data['email']).first()
        except:
            return flask.jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated


@REST.route("/api/certificates/", methods=["POST"])
@token_required
def create_new_certificate(current_user):
    if not current_user.is_admin:
        flask.abort(flask.make_response(flask.jsonify(message="You can`t do it!", status=400), 400))
    data = flask.request.get_json()
    try:
        db.session.add(RegistrationCertificate(data["id"], data["registration_number"], data["date_of_registration"], data["VIN_code"], data["car"], data["year_of_manufacture"]))
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        flask.abort(flask.make_response(flask.jsonify(message="Error, id already exists", status=400), 400))
    except InvalidCertificate as error:
        flask.abort(flask.make_response(flask.jsonify(message="Error, one of the field is not valid", status=400, error=error.list), 400))
    return flask.jsonify({"status": 200, "message": "You have successfully added a certificate", "certificate": RegistrationCertificate.query.filter(RegistrationCertificate.id == data["id"]).all()[0].make_dict()})


@REST.route("/api/certificates/<certificate_id>", methods=["DELETE"])
@token_required
def delete_certificate_by_id(current_user, certificate_id):
    if not current_user.is_admin:
        flask.abort(flask.make_response(flask.jsonify(message="You can`t do it!", status=400), 400))
    if len(RegistrationCertificate.query.filter_by(id=certificate_id).all()) == 0:
        flask.abort(flask.make_response(flask.jsonify(message="Error, with such id doesnt exist", status=404), 404))
    RegistrationCertificate.query.filter_by(id=certificate_id).delete()
    db.session.commit()
    return flask.jsonify({"status:": flask.Response().status_code, "message:": "Successfully deleted"})


@REST.route("/api/certificates/<certificate_id>", methods=["GET"])
@token_required
def get_certificate_by_id(current_user, certificate_id):
    return flask.jsonify({"certificate": RegistrationCertificate.query.filter_by(id=certificate_id).all()[0].make_dict()}) if len(RegistrationCertificate.query.filter_by(id=certificate_id).all()) != 0 else flask.abort(flask.make_response(flask.jsonify(message="Error, certificate is not found", status=404), 404))


@REST.route("/api/certificates/", methods=["GET"])
@token_required
def get_all_certificates(current_user):
    sort_by = flask.request.args.get("sort_by", type=str)
    sort_type = flask.request.args.get("sort_type", type=str)
    search = flask.request.args.get("search", type=str)
    offset = flask.request.args.get("offset", type=int)
    limit = flask.request.args.get("limit", type=int)

    certificates = RegistrationCertificate.query

    for i in RegistrationCertificate.fields():
        if i == sort_by:
            break
        if i == "car":
            sort_by = None

    if sort_by and sort_type == "desc":
        certificates = certificates.order_by(sqlalchemy.desc(sort_by))
    elif sort_by:
        certificates = certificates.order_by(sqlalchemy.text(sort_by))

    if search:
        certificates = certificates.filter(sqlalchemy.or_(*[sqlalchemy.cast(getattr(RegistrationCertificate, x), db.String).like(f"%{search}%".lower()) for x in RegistrationCertificate.fields()]))
    if len(certificates.all()) == 0:
        flask.abort(flask.make_response(flask.jsonify(message="Nothing found", status=404), 404))

    _quantity = len(RegistrationCertificate.query.filter().all())
    if limit:
        if _quantity % limit == 0:
            if offset*limit > _quantity:
                flask.abort(flask.make_response(flask.jsonify(message="Wrong offset or limit", status=404), 404))
        else:
            if offset * limit - limit > _quantity:
                flask.abort(flask.make_response(flask.jsonify(message="Wrong offset or limit", status=404), 404))

    paginate_certificates = certificates.paginate(offset, limit)
    a = [i.make_dict() for i in paginate_certificates.items]
    return flask.jsonify({"status": 200, "message": "Successfully got certificates", "sort": [sort_by, sort_type], "count": len(paginate_certificates.items), "certificates:": a})


@REST.route("/api/certificates/<certificate_id>", methods=["PUT"])
@token_required
def update_existing_certificate(current_user, certificate_id):
    if not current_user.is_admin:
        flask.abort(flask.make_response(flask.jsonify(message="You can`t do it!", status=400), 400))
    if len(RegistrationCertificate.query.filter_by(id=certificate_id).all()) == 0:
        flask.abort(flask.make_response(flask.jsonify(message="Error, certificate with such if is not found", status=404), 404))
    data = flask.request.get_json()

    to_edit = RegistrationCertificate.query.filter(RegistrationCertificate.id == certificate_id).all()[0].make_dict()

    for i in data.keys():
        to_edit[i] = data[i]

    try:
        RegistrationCertificate(**to_edit)
    except InvalidCertificate as error:
        flask.abort(flask.make_response(flask.jsonify(message="One of the field is has wrong value", status=400, error=error.list), 400))

    RegistrationCertificate.query.filter(RegistrationCertificate.id == certificate_id).update(to_edit)
    db.session.commit()
    if "id" in data.keys():
        certificate_id = data["id"]

    return flask.jsonify({"status": 200, "message:": "Successfully edited", "certificate:": RegistrationCertificate.query.filter(RegistrationCertificate.id == certificate_id).all()[0].make_dict()})


@REST.route("/api/register/", methods=["POST"])
def register():
    data = flask.request.get_json()

    hashed_password = generate_password_hash(data["password"], method="sha256")
    try:
        db.session.add(User(data["id"], data["name"], data["last_name"], data["email"], hashed_password))
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        flask.abort(flask.make_response(flask.jsonify({"status": 400, "message": "User with such id already exists"}),400))
    except InvalidUser as error:
        flask.abort(flask.make_response(flask.jsonify({"status": 400, "message": "NOT VALID", "error": error.list}), 400))

    return flask.jsonify({"status": 200, "message": "Successfully registered"})


@REST.route("/api/login", methods=["POST"])
def login():
    auth = flask.request.get_json()

    if not auth or not auth["email"] or not auth["password"]:
        flask.abort(flask.make_response(flask.jsonify({"status": 420, "message": "One of the field is empty"}), 420))

    user = User.query.filter_by(email=auth["email"]).first()

    if not user:
        flask.abort(flask.make_response(flask.jsonify({"status": 404, "message": "Account doesn't exist"}), 404))
    if check_password_hash(user.password, auth["password"]):
        token = jwt.encode({"exp": (datetime.datetime.utcnow() + datetime.timedelta(minutes=30)), "email": user.email}, REST.config['SECRET_KEY'], algorithm="HS256")
        return flask.jsonify({"email": user.email, "token": token})
    flask.abort(flask.make_response(flask.jsonify({"status": 400, "message": "Wrong password"}), 400))


@REST.route("/api/orders", methods=["PUT"])
@token_required
def send_an_order(current_user):
    data = flask.request.get_json()
    a = CarOrder.query.filter_by(car= data["car"]).all()
    if len(a) == 0:
        flask.abort(flask.make_response(flask.jsonify({"status": 404, "message": "Car you want to buy doesn't exist"}), 404))
    elif a[0].amount == 0:
        flask.abort(flask.make_response(flask.jsonify({"status": 400, "message": "Out of cars"}), 400))

    a[0].amount -= 1
    db.session.commit()
    return flask.jsonify({"status": 200, "message": "You have successfully bought a car", "Your Car": RegistrationCertificate.query.filter_by(car=a[0].car).first().make_dict()})


@REST.route("/api/orders", methods=["POST"])
@token_required
def create_an_order(current_user):
    if not current_user.is_admin:
        flask.abort(flask.make_response(flask.jsonify(message="You can`t do it!", status=400), 400))
    data = flask.request.get_json()
    try:
        db.session.add(CarOrder(data["item_id"], data["car"], data["amount"]))
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        flask.abort(flask.make_response(flask.jsonify({"status": 400, "message": "Order with such id already exists"}),400))
    except InvalidOrder as error:
        flask.abort(flask.make_response(flask.jsonify({"status": 400, "message": "NOT VALID", "error": error.list}), 400))
    return flask.jsonify({"status": 200, "message": "You have successfully created an order"})


@REST.route("/api/orders/<order_id>", methods=["GET"])
@token_required
def get_order_by_id(current_user, order_id):
    return flask.jsonify({"Order": CarOrder.query.filter_by(item_id=order_id).first().make_dict()}) if CarOrder.query.filter_by(item_id=order_id).first() else flask.abort(flask.make_response(flask.jsonify(message="Error, order is not found", status=404), 404))


@REST.route("/api/orders/", methods=["GET"])
@token_required
def get_all_orders(current_user):
    sort_by = flask.request.args.get("sort_by", type=str)
    sort_type = flask.request.args.get("sort_type", type=str)
    search = flask.request.args.get("search", type=str)
    offset = flask.request.args.get("offset", type=int)
    limit = flask.request.args.get("limit", type=int)

    orders = CarOrder.query

    for i in CarOrder.fields():
        if i == sort_by:
            break
        if i == "car":
            sort_by = None

    if sort_by and sort_type == "desc":
        orders = orders.order_by(sqlalchemy.desc(sort_by))
    elif sort_by:
        certificates = orders.order_by(sqlalchemy.text(sort_by))

    if search:
        orders = orders.filter(sqlalchemy.or_(*[sqlalchemy.cast(getattr(CarOrder, x), db.String).like(f"%{search}%".lower()) for x in CarOrder.fields()]))
    if len(orders.all()) == 0:
        flask.abort(flask.make_response(flask.jsonify(message="Nothing found", status=404), 404))

    _quantity = len(CarOrder.query.filter().all())
    if limit:
        if _quantity % limit == 0:
            if offset*limit > _quantity:
                flask.abort(flask.make_response(flask.jsonify(message="Wrong offset or limit", status=404), 404))
        else:
            if offset * limit - limit > _quantity:flask.abort(flask.make_response(flask.jsonify(message="Wrong offset or limit", status=404), 404))

    paginate_orders = orders.paginate(offset, limit)
    a = [i.make_dict() for i in paginate_orders.items]
    return flask.jsonify({"status": 200, "message": "Successfully got orders", "sort": [sort_by, sort_type], "count": len(paginate_orders.items), "orders:": a})


@REST.route("/api/users/", methods=["GET"])
@token_required
def get_all_users(current_user):
    if not current_user.is_admin:
        flask.abort(flask.make_response(flask.jsonify(message="You can`t do it!", status=400), 400))

    sort_by = flask.request.args.get("sort_by", type=str)
    sort_type = flask.request.args.get("sort_type", type=str)
    search = flask.request.args.get("search", type=str)
    offset = flask.request.args.get("offset", type=int)
    limit = flask.request.args.get("limit", type=int)

    users = User.query

    for i in User.fields():
        if i == sort_by:
            break
        if i == "car":
            sort_by = None

    if sort_by and sort_type == "desc":
        users = users.order_by(sqlalchemy.desc(sort_by))
    elif sort_by:
        users = users.order_by(sqlalchemy.text(sort_by))

    if search:
        users = users.filter(sqlalchemy.or_(*[sqlalchemy.cast(getattr(User, x), db.String).like(f"%{search}%".lower()) for x in User.fields()]))
    if len(users.all()) == 0:
        flask.abort(flask.make_response(flask.jsonify(message="Nothing found", status=404), 404))

    _quantity = len(User.query.filter().all())
    if limit:
        if _quantity % limit == 0:
            if offset * limit > _quantity:
                flask.abort(flask.make_response(flask.jsonify(message="Wrong offset or limit", status=404), 404))
        else:
            if offset * limit - limit > _quantity:
                flask.abort(flask.make_response(flask.jsonify(message="Wrong offset or limit", status=404), 404))

    paginate_users = users.paginate(offset, limit)
    a = [i.make_dict() for i in paginate_users.items]
    return flask.jsonify({"status": 200, "message": "Successfully got users", "sort": [sort_by, sort_type], "count": len(paginate_users.items), "Users:": a})


@REST.route("/api/users/<user_id>", methods=["GET"])
@token_required
def get_user_by_id(current_user, user_id):
    if not current_user.is_admin:
        flask.abort(flask.make_response(flask.jsonify(message="You can`t do it!", status=400), 400))

    return flask.jsonify({"User": User.query.filter_by(id=user_id).first().make_dict()}) if User.query.filter_by(id=user_id).first() else flask.abort(flask.make_response(flask.jsonify(message="Error, user is not found", status=404), 404))


if __name__ == "__main__":
    REST.run(debug=True, host="localhost", port=5000)
