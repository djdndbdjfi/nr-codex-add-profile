from flask import Flask, request, jsonify
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import requests
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
import time

#━━━━━━━━━━━━━━━━━━━
#𝗠𝗔𝗗𝗘 𝗕𝗬 𝗙𝗢𝗫 x 𝗟7𝗔𝗝
#𝗣𝗥𝗢𝗝𝗘𝗖𝗧𝗦 𝗙𝗢𝗫𝗫
#━━━━━━━━━━━━━━━━━━━

app = Flask(__name__)

# Protobuf setup
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    6,
    30,
    0,
    '',
    'data.proto'
)
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\ndata.proto"7\n\x12InnerNestedMessage\x12\x0f\n\x07\x66ield_6\x18\x06 \x01(\x03\x12\x10\n\x08\x66ield_14\x18\x0e \x01(\x03"\x87\x01\n\nNestedItem\x12\x0f\n\x07\x66ield_1\x18\x01 \x01(\x05\x12\x0f\n\x07\x66ield_2\x18\x02 \x01(\x05\x12\x0f\n\x07\x66ield_3\x18\x03 \x01(\x05\x12\x0f\n\x07\x66ield_4\x18\x04 \x01(\x05\x12\x0f\n\x07\x66ield_5\x18\x05 \x01(\x05\x12$\n\x07\x66ield_6\x18\x06 \x01(\x0b\x32\x13.InnerNestedMessage"@\n\x0fNestedContainer\x12\x0f\n\x07\x66ield_1\x18\x01 \x01(\x05\x12\x1c\n\x07\x66ield_2\x18\x02 \x03(\x0b\x32\x0b.NestedItem"A\n\x0bMainMessage\x12\x0f\n\x07\x66ield_1\x18\x01 \x01(\x05\x12!\n\x07\x66ield_2\x18\x02 \x03(\x0b\x32\x10.NestedContainerb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'data_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_INNERNESTEDMESSAGE']._serialized_start=14
    _globals['_INNERNESTEDMESSAGE']._serialized_end=69
    _globals['_NESTEDITEM']._serialized_start=72
    _globals['_NESTEDITEM']._serialized_end=207
    _globals['_NESTEDCONTAINER']._serialized_start=209
    _globals['_NESTEDCONTAINER']._serialized_end=273
    _globals['_MAINMESSAGE']._serialized_start=275
    _globals['_MAINMESSAGE']._serialized_end=340

# Encryption setup
key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
freefire_version = "OB50"

@app.route('/add-profile', methods=['GET'])
def add_profile():
    # Get parameters from request
    jwt_token = request.args.get('token')
    itemid_str = request.args.get('itemid')
    
    if not jwt_token or not itemid_str:
        return jsonify({
            "status": "error",
            "message": "Missing token or itemid parameter"
        }), 400
        
    # Process item IDs
    item_ids = itemid_str.split('/')[:15]  # Take up to 15 items
    
    if len(item_ids) < 1:
        return jsonify({
            "status": "error",
            "message": "At least one item ID required"
        }), 400

    # Build protobuf message
    data = _globals['MainMessage']()
    data.field_1 = 1
    
    # First container
    container1 = data.field_2.add()
    container1.field_1 = 1
    
    # Field combinations for items
    combinations = [
        {"field_1": 2, "field_4": 1},
        {"field_1": 2, "field_4": 1, "field_5": 4},
        {"field_1": 2, "field_4": 1, "field_5": 2},
        {"field_1": 13, "field_3": 1},
        {"field_1": 13, "field_3": 1, "field_4": 2},
        {"field_1": 13, "field_3": 1, "field_5": 2},
        {"field_1": 13, "field_3": 1, "field_5": 4},
        {"field_1": 13, "field_3": 1, "field_4": 2, "field_5": 2},
        {"field_1": 13, "field_3": 1, "field_4": 2, "field_5": 4},
        {"field_1": 13, "field_3": 1, "field_4": 4},
        {"field_1": 13, "field_3": 1, "field_4": 4, "field_5": 2},
        {"field_1": 13, "field_3": 1, "field_4": 4, "field_5": 4},
        {"field_1": 13, "field_3": 1, "field_4": 6},
        {"field_1": 13, "field_3": 1, "field_4": 6, "field_5": 2},
        {"field_1": 13, "field_3": 1, "field_4": 6, "field_5": 4}
    ]
    
    # Add user items
    for i, item_id in enumerate(item_ids):
        if i >= len(combinations):
            break
            
        item_data = combinations[i].copy()
        item_data["field_6"] = {"field_6": int(item_id)}
        
        item = container1.field_2.add()
        item.field_1 = item_data["field_1"]
        
        if "field_3" in item_data:
            item.field_3 = item_data["field_3"]
        if "field_4" in item_data:
            item.field_4 = item_data["field_4"]
        if "field_5" in item_data:
            item.field_5 = item_data["field_5"]
        
        item.field_6.field_6 = item_data["field_6"]["field_6"]
    
    # Second container (fixed items)
    container2 = data.field_2.add()
    container2.field_1 = 9
    
    item7 = container2.field_2.add()
    item7.field_4 = 3
    item7.field_6.field_14 = 3048205855
    
    item8 = container2.field_2.add()
    item8.field_4 = 3
    item8.field_5 = 3
    item8.field_6.field_14 = 3048205855

    # Encrypt data
    data_bytes = data.SerializeToString()
    padded_data = pad(data_bytes, AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(padded_data)

    # Prepare request to external server
    url = "https://client.ind.freefiremobile.com/SetPlayerGalleryShowInfo"
    headers = {
        "Expect": "100-continue",
        "Authorization": f"Bearer {jwt_token}",
        "X-Unity-Version": "2018.4.11f1",
        "X-GA": "v1 1",
        "ReleaseVersion": freefire_version,
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; SM-A305F Build/RP1A.200720.012)",
        "Host": "https://client.ind.freefiremobile.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }

    try:
        response = requests.post(url, headers=headers, data=encrypted_data)
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"External request failed: {str(e)}"
        }), 500

    # Prepare response
    current_time = int(time.time())
    add_profile_list = []
    
    for i, item_id in enumerate(item_ids):
        add_profile_list.append({
            "add_time": current_time,
            f"item_id{i+1}": int(item_id)
        })

    if response.status_code == 200:
        return jsonify({
            "message": "Item added to profile",
            "status": "success",
            "Add-profile": add_profile_list
        })
    else:
        return jsonify({
            "status": "error",
            "message": f"External server returned status {response.status_code}",
            "external_response": response.text
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)