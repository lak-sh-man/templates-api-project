from flask import Flask, request, Response
from validator import validate_header, validate_request_body
import json
import uuid
from db import users, templates
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
        if email in users:
            return Response(
            json.dumps({"error": "User already exist."}),
            status=409,
            content_type='application/json'
        )
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
        if email in users and users[email]["password"] == json_body["password"]:
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

@app.post("/template")
@jwt_required()  # Requires valid JWT token
def create_template():
    # Validate headers
    header_error = validate_header()
    if header_error:
        return header_error

    # Validate request body
    request_body_error = validate_request_body()
    if request_body_error:
        return request_body_error

    try:
        current_user = get_jwt_identity()  # Get logged-in user email
        json_body = request.get_json()
        template_id = uuid.uuid4().hex

        # Ensure user exists in users
        if current_user not in users:
            return Response(
                json.dumps({"error": "Register first"}),
                status=400,
                content_type="application/json"
            )

        # Initialize the user's template dictionary if they don't have one yet
        if current_user not in templates:
            templates[current_user] = {}

        # Add new template
        templates[current_user][template_id] = {**json_body}

        response_body = json.dumps({
            "success": True,
            "message": "Template created successfully",
            "template_id": template_id  
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

@app.get("/template")
@jwt_required()  
def all_template():
    # Validate headers
    header_error = validate_header()
    if header_error:
        return header_error

    try:
        current_user = get_jwt_identity() 

        # Ensure user exists in users
        if current_user not in users:
            return Response(
                json.dumps({"error": "Register first"}),
                status=400,
                content_type="application/json"
            )
            
        # Ensure user exists in templates
        if current_user not in templates:
            return Response(
                json.dumps({"error": "Post a template first."}),
                status=400,
                content_type="application/json"
            )

        response_body = json.dumps({
            "success": True,
            "message": "Template fetched successfully",
            "templates": templates[current_user]
        })

        response = Response(response_body, status=200, content_type="application/json")
        response.headers['Content-Type'] = request.headers.get('Content-Type')
        response.headers['Accept'] = request.headers.get('Accept')
        return response

    except Exception:
        return Response(
            json.dumps({"error": "Invalid JSON body"}),
            status=400,
            content_type='application/json'
        )
        
@app.get("/template/<template_id>")
@jwt_required()  
def single_template(template_id):
    # Validate headers
    header_error = validate_header()
    if header_error:
        return header_error

    try:
        current_user = get_jwt_identity() 

        # Ensure user exists in users
        if current_user not in users:
            return Response(
                json.dumps({"error": "Register first"}),
                status=400,
                content_type="application/json"
            )

        # Ensure user exists in templates
        if current_user not in templates:
            return Response(
                json.dumps({"error": "Post a template first."}),
                status=400,
                content_type="application/json"
            )

        response_body = json.dumps({
            "success": True,
            "message": "Template fetched successfully",
            "templates": templates[current_user][template_id]
        })

        response = Response(response_body, status=200, content_type="application/json")
        response.headers['Content-Type'] = request.headers.get('Content-Type')
        response.headers['Accept'] = request.headers.get('Accept')
        return response

    except Exception:
        return Response(
            json.dumps({"error": "Invalid JSON body"}),
            status=400,
            content_type='application/json'
        )
        
@app.put("/template/<template_id>")
@jwt_required()  
def update_single_template(template_id):
    # Validate headers
    header_error = validate_header()
    if header_error:
        return header_error
    
    # validate request body
    request_body_error = validate_request_body()
    if request_body_error:
        return request_body_error

    try:
        json_body = request.get_json()
        current_user = get_jwt_identity() 

        # Ensure user exists in users
        if current_user not in users:
            return Response(
                json.dumps({"error": "Register first"}),
                status=400,
                content_type="application/json"
            )
            
        # Ensure user exists in templates
        if current_user not in templates:
            return Response(
                json.dumps({"error": "Post a template first."}),
                status=400,
                content_type="application/json"
            )

        # Update template
        templates[current_user][template_id] = {**json_body}
        
        response_body = json.dumps({
            "success": True,
            "message": "Template updated successfully",
            "templates": templates[current_user][template_id]
        })

        response = Response(response_body, status=200, content_type="application/json")
        response.headers['Content-Type'] = request.headers.get('Content-Type')
        response.headers['Accept'] = request.headers.get('Accept')
        return response

    except Exception:
        return Response(
            json.dumps({"error": "Invalid JSON body"}),
            status=400,
            content_type='application/json'
        )
        
@app.delete("/template/<template_id>")
@jwt_required()  
def delete_single_template(template_id):
    # Validate headers
    header_error = validate_header()
    if header_error:
        return header_error

    try:
        current_user = get_jwt_identity() 

        # Ensure user exists in users
        if current_user not in users:
            return Response(
                json.dumps({"error": "Register first"}),
                status=400,
                content_type="application/json"
            )
            
        # Ensure user exists in templates
        if current_user not in templates:
            return Response(
                json.dumps({"error": "Post a template first."}),
                status=400,
                content_type="application/json"
            )

        # delete template
        templates[current_user].pop(template_id)
        
        response_body = json.dumps({
            "success": True,
            "message": "Template deleted successfully",
        })

        response = Response(response_body, status=200, content_type="application/json")
        response.headers['Content-Type'] = request.headers.get('Content-Type')
        response.headers['Accept'] = request.headers.get('Accept')
        return response

    except Exception:
        return Response(
            json.dumps({"error": "Invalid JSON body"}),
            status=400,
            content_type='application/json'
        )
        
if __name__ == "__main__":
    app.run(debug=True)
