from flask import Flask, request, Response
from validator import validate_header, validate_request_body
import json
from db import users
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, jwt_required, create_refresh_token, get_jwt_identity

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "lakshman"
jwt = JWTManager(app)

@app.post("/register")
def register_user():
    # validate header
    header_error = validate_header()
    if header_error:
        return header_error

    # validate request body
    request_body_error = validate_request_body()
    if request_body_error:
        return request_body_error
    
    # Parse the JSON body
    try:
        json_body = request.get_json()
        email = json_body["email"]
        users[email] = {**json_body}
        response_body = json.dumps({
            "success": True,
            "message": "User registered successfully",
            "user": users[email]["email"]
            })
        response = Response(response_body, status=201, content_type="application/json")
        response.headers['Content-Type'] = request.headers.get('Content-Type')
        response.headers['Accept'] = request.headers.get('Accept')
        return response
    
    except Exception:
        return Response(
            json.dumps({"error": "Invalid JSON body"}),
            status=400,
            content_type='application/json'
        )

@app.post("/login")
def login_user():
    # validate header
    header_error = validate_header()
    if header_error:
        return header_error

    # validate request body
    request_body_error = validate_request_body()
    if request_body_error:
        return request_body_error

    # Parse the JSON body
    try:
        json_body = request.get_json()
        email = json_body["email"]
        if users[email]["email"] == json_body["email"] and users[email]["password"] == json_body["password"]:
            access_token = create_access_token(identity=users[email]["email"], fresh=True)
            response_body = json.dumps({
                "success": True,
                "message": "User Login successful",
                "user": users[email]["email"],
                "access_token": access_token
                })           
            response = Response(response_body, status=200, content_type="application/json")
            response.headers['Content-Type'] = request.headers.get('Content-Type')
            response.headers['Accept'] = request.headers.get('Accept')
            return response
            
        else:
            return Response(
                json.dumps({"error": "Invalid credentials."}),
                status=401,
                content_type='application/json'
            )
            
    except Exception:
        return Response(
            json.dumps({"error": "Invalid JSON body"}),
            status=400,
            content_type='application/json'
        )

if __name__ == "__main__":
    app.run(debug=True)
