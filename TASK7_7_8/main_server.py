import flask
from certificate import *
import sqlalchemy
from flask_swagger_ui import get_swaggerui_blueprint


@REST.route("/")
def hello_world():
    return "Hello, REST"


@REST.route("/static/<path:path>")
def send_static(path):
    return flask.send_from_directory("static", path)

SWAGGER_URL = "/api/swagger"
API_URL = "/static/swagger.json"
swagerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={
    "app_name": "Restful-Shevchenko"
})
REST.register_blueprint(swagerui_blueprint, url_prefix=SWAGGER_URL)

REST.register_blueprint(flask.Blueprint("restful_api", "restful_api"))



@REST.route("/api/certificates/", methods=["POST"])
def create_new_certificate():
    data = flask.request.get_json()
    try:
        db.session.add(RegistrationCertificate(data["id"], data["registration_number"], data["date_of_registration"], data["VIN_code"], data["car"], data["year_of_manufacture"]))
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return flask.jsonify({"status": 400, "errors": "Id already exists"})
    except InvalidCertificate as error:
        return flask.jsonify({"status": 400, "errors": error.list})
    return flask.jsonify({"status": 200, "message": "You have successfully added a certificate", "certificate": RegistrationCertificate.query.filter(RegistrationCertificate.id == data["id"]).all()[0].make_dict()})


@REST.route("/api/certificates/<certificate_id>", methods=["DELETE"])
def delete_certificate_by_id(certificate_id):
    if len(RegistrationCertificate.query.filter_by(id=certificate_id).all()) == 0:
        return flask.jsonify({"status": 404, "message:": "Error, certificate with such id doesn't exist"})
    RegistrationCertificate.query.filter_by(id=certificate_id).delete()
    db.session.commit()
    return flask.jsonify({"status:": flask.Response().status_code, "message:": "Successfully deleted"})


@REST.route("/api/certificates/<certificate_id>", methods=["GET"])
def get_certificate_by_id(certificate_id):
    return flask.jsonify({"certificate": RegistrationCertificate.query.filter_by(id=certificate_id).all()[0].make_dict()}) if len(RegistrationCertificate.query.filter_by(id=certificate_id).all()) != 0 else flask.jsonify({"status": 404, "message:": "Error, certificate with such id doesn't exist"})


@REST.route("/api/certificates/", methods=["GET"])
def get_all_certificates():
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
        return flask.jsonify({"status": 404,"message": "Nothing found" })

    _quantity = len(RegistrationCertificate.query.filter().all())
    if limit:
        if _quantity % limit == 0:
            if offset*limit > _quantity:
                return flask.jsonify({"status": 404, "message": "Wrong offset or limit!"})
        else:
            if offset * limit - limit > _quantity:
                return flask.jsonify({"status": 404, "message": "Wrong offset or limit!"})

    paginate_certificates = certificates.paginate(offset, limit)
    a = [i.make_dict() for i in paginate_certificates.items]
    return flask.jsonify({"status": 200, "message": "Successfully got certificates", "sort": [sort_by, sort_type], "count": len(paginate_certificates.items), "certificates:": a})


@REST.route("/api/certificates/<certificate_id>", methods=["PUT"])
def update_existing_certificate(certificate_id):
    if len(RegistrationCertificate.query.filter_by(id=certificate_id).all()) == 0:
        return flask.jsonify({"status:": 404, "message": "Certificate with such id is not found"})
    data = flask.request.get_json()

    to_edit = RegistrationCertificate.query.filter(RegistrationCertificate.id == certificate_id).all()[0].make_dict()

    for i in data.keys():
        to_edit[i] = data[i]

    try:
        RegistrationCertificate(**to_edit)
    except InvalidCertificate as error:
        return flask.jsonify({"status": 400, "message": "One of the fields entered is not valid", "errors": error.list})

    RegistrationCertificate.query.filter(RegistrationCertificate.id == certificate_id).update(to_edit)
    db.session.commit()
    if "id" in data.keys():
        certificate_id = data["id"]

    return flask.jsonify({"status": 200, "message:": "Successfully edited", "certificate:": RegistrationCertificate.query.filter(RegistrationCertificate.id == certificate_id).all()[0].make_dict()})


if __name__ == "__main__":
    REST.run(debug=True, host="localhost", port=5000)


