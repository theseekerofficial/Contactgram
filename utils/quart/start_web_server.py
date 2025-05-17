import os
import socket
import asyncio
import secrets
from loguru import logger
from dotenv import load_dotenv
from pymongo import AsyncMongoClient
from utils.processor.load_env import env_dict
from hypercorn.config import Config as Hyper_Conf
from hypercorn.asyncio import serve as Hyper_Serve
from utils.processor.tools import create_ttl_index
from utils.processor.data_holders import user_contact_data
from utils.processor.context_processors import load_user_contacts
from quart import Quart, render_template, request, jsonify, send_from_directory

load_dotenv('settings.env')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

mongo_uri = os.getenv('MONGO_URI')
mongo_web_app_client = AsyncMongoClient(mongo_uri)
web_app_db = mongo_web_app_client.Contactgram
web_app_chat_storage = mongo_web_app_client.ChatStorage

quart_app = Quart(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)
quart_app.secret_key = os.getenv('QUART_SECRET_KEY') or secrets.token_urlsafe(16)

@quart_app.before_serving
async def load_contacts_before_start():
    await load_user_contacts()

    await create_ttl_index()

@quart_app.route('/', methods=['GET'])
async def chat():
    security_hash = request.args.get('security_hash')
    interface_access = request.args.get('interface_access')

    if not security_hash and not interface_access:
        return jsonify({"message": 'Required creds missing'}), 401

    config_doc = await web_app_db.Config.find_one({'security_hash': security_hash})
    if not config_doc:
        return jsonify({"message": 'Invalid security creds'}), 401

    if os.getenv("INTERFACE_PROCESS_PASSWORD") != interface_access:
        return jsonify({"message": 'Invalid interface access'}), 401

    return await render_template('chat.html', user_contact_data=user_contact_data)

@quart_app.route('/update-contact', methods=['POST'])
async def update_contact():
    data = await request.get_json()
    if data.get('pass_access') != os.getenv('INTERFACE_PROCESS_PASSWORD'):
        return jsonify({"success": 'False'}), 401
    if not data.get('user_name') and not data.get('user_id'):
        return jsonify({"success": 'False'}), 400

    user_contact_data[data.get('user_id')] = {}
    user_contact_data[data.get('user_id')]["user_name"] = data.get('user_name')
    user_contact_data[data.get('user_id')]["user_id"] = data.get('user_id')
    return jsonify({"success": 'True'}), 200

@quart_app.route('/fetch-messages/<user_id>')
async def fetch_messages(user_id):
    try:
        skip = int(request.args.get('skip', 0))

        message_collection = web_app_chat_storage[str(user_id)]

        messages_cursor = message_collection.find().sort("timestamp", -1).skip(skip).limit(20)
        messages = await messages_cursor.to_list(length=20)

        result = []
        for message in messages:
            result.append({
                'message': message['message'],
                'timestamp': message['timestamp'],
                'is_sent': True if message['is_admin'] and message['replied_admin_id'] else False,
                'message_id': message['message_id'],
                'username': message['username'],
                'user_name': message['user_name'],
                'is_admin': message['is_admin'],
                'replied_admin_id': message['replied_admin_id'],
                'replied_admin_name': message['replied_admin_name'],
                'msg_type': message['msg_type'],
                'is_forwarded': message.get('is_forwarded', False),
                'is_media': message.get('is_media', False),
                'is_reply': message.get('is_reply', False),
                'reply_msg_id': message.get('reply_msg_id', None)
            })

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error fetching messages: {e}")
        return jsonify([])

@quart_app.route('/fetch_message/<user_id>/<message_id>')
async def fetch_message(user_id, message_id):
    try:
        message_collection = web_app_chat_storage[str(user_id)]

        message = await message_collection.find_one({"message_id": int(message_id)}, { "_id": 0})

        if message:
            message['timestamp'] = message['timestamp']
            return jsonify(message)

        return jsonify({"error": "Message not found"}), 404
    except Exception as e:
        logger.error(f"Error fetching message: {e}")
        return jsonify({"error": "Internal server error"}), 500

@quart_app.route('/favicon.ico')
async def favicon():
    return await send_from_directory(os.path.join(BASE_DIR, "static"), 'favicon.ico')

async def start_quart_web_app():
    def _get_default_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception as ee:
            logger.error(f"Error getting default IP: {str(ee)}")
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    if env_dict.get("START_WEB_APP") and env_dict.get("WEB_APP_PORT"):
        web_app_port = env_dict.get("WEB_APP_PORT", 2222)
        server_ip = _get_default_ip()
        config = Hyper_Conf()
        config.bind = [f"{server_ip}:{web_app_port}"]
        config.use_reloader = False

        try:
            logger.info(f"Contactgram Web app started successfully on {server_ip}:{web_app_port}.")
            await Hyper_Serve(quart_app, config, shutdown_trigger=lambda: asyncio.Future())
        except Exception as e:
            logger.warning(f"Failed to start server on {server_ip}:{web_app_port}, error: {e}")