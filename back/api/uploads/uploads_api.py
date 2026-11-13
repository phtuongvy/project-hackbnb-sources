from flask import Blueprint, request, send_from_directory, abort
from werkzeug.utils import secure_filename

uploads_api = Blueprint('uploads', __name__)

@uploads_api.route('/')
def get_upload():
    name = request.args.get("name", "")

    # Neutralise le nom : "../instance/db.sqlite" -> "instance_db.sqlite"
    # secure_filename supprime les / et les ..
    name = secure_filename(name)

    # Si le nom devient vide (ou ../), on refuse
    if not name:
        abort(400)  # Bad Request

    # send_from_directory garantit que le fichier reste DANS uploads/
    #    (il renvoie 404 si on tente de sortir du dossier)
    return send_from_directory('uploads', name)
 