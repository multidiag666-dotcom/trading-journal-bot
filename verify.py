import hmac
import hashlib
import urllib.parse
import json
from flask import request, abort

# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
BOT_TOKEN = '8278666246:AAG7oK_1ODMCagxo9XlDckUnhsvB7eX3iE8'   # ← СЮДА потом вставим токен от BotFather
# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←

def verify_telegram():
    auth = request.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        abort(403, 'No auth')

    init_data = auth[7:]   # убираем "Bearer "
    
    parsed = urllib.parse.parse_qs(init_data)
    received_hash = parsed.pop('hash', [None])[0]

    if not received_hash:
        abort(403, 'No hash')

    data_check_string = '\n'.join(f"{k}={v[0]}" for k, v in sorted(parsed.items()))
    
    secret_key = hmac.new(b'WebAppData', BOT_TOKEN.encode(), hashlib.sha256).digest()
    calc_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    if calc_hash != received_hash:
        abort(403, 'Invalid hash')

    user_str = parsed.get('user')
    if not user_str:
        abort(403, 'No user')

    user = json.loads(user_str[0])
    return user['id']