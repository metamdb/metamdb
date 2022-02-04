'' "Routes for contact." ""

import logging

from flask import Blueprint, jsonify, request
from src.errors import handler

contact_blueprint = Blueprint('contact', __name__, url_prefix='/api/contact')
contact_blueprint.register_error_handler(handler.InvalidUsage,
                                         handler.handle_invalid_usage)

contact_handler = logging.FileHandler('logs/contact.log')
contact_formatter = logging.Formatter(
    '%(asctime)-15s %(name)-5s %(levelname)-8s Name: %(contact_name)s Email: %(contact_email)s Msg: %(contact_msg)s'
)
CONTACT_LOGGER = logging.getLogger(__name__)
contact_handler.setFormatter(contact_formatter)
CONTACT_LOGGER.setLevel(logging.INFO)
CONTACT_LOGGER.addHandler(contact_handler)


@contact_blueprint.route('', methods=['POST'])
def contact():
    name: str = request.get_json()['name']
    email: str = request.get_json()['email']
    msg: str = request.get_json()['message']

    contact_logger = logging.LoggerAdapter(CONTACT_LOGGER, {
        'contact_name': name,
        'contact_email': email,
        'contact_msg': msg
    })
    contact_logger.info('Contact Form')

    return jsonify({'contact': 'success'})
