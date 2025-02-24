from flask import Flask, request, Response
from validator import validate_header, validate_request_body
import json
import uuid
from db import init_db
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

app.config["SECRET_KEY"] = "lakshman-mongodb"
app.config["MONGO_URI"] = "mongodb+srv://lakshman:0002211namhskal@cluster0.rlfxw.mongodb.net/templatesDB?retryWrites=true&w=majority&appName=Cluster0"
app.config["JWT_SECRET_KEY"] = "lakshman"

# Initialize database
db = init_db(app)

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
        if not email:
            return Response(
                json.dumps({"error": "Email is required"}),
                status=400,
                content_type='application/json'
            )

        # Check if user already exists in MongoDB
        if db.users.find_one({"_id": email}):
            return Response(
                json.dumps({"error": "User already exists."}),
                status=409,
                content_type="application/json"
            )

        # Insert user into MongoDB
        new_user = {
            "_id": email,
            "first_name": json_body["first_name"],
            "last_name": json_body["last_name"],
            "password": json_body["password"] 
        }
        db.users.insert_one(new_user)

        # Fetch the updated users collection
        # users = list(db.users.find({}, {"_id": 1, "first_name": 1, "last_name": 1, "password": 1}))

        response_body = json.dumps({
            "success": True,
            "message": "User registered successfully",
            "user": email
            })
        response = Response(response_body, status=201, content_type="application/json")
        response.headers['Content-Type'] = request.headers.get('Content-Type')
        response.headers['Accept'] = request.headers.get('Accept')
        return response
    
    except Exception:
        return Response(
            json.dumps({"error": "Something went wrong"}),
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
        password = json_body["password"]

        if not email or not password:
            return Response(
                json.dumps({"error": "Email and password are required."}),
                status=400,
                content_type="application/json"
            )

        # Fetch user from MongoDB
        user = db.users.find_one({"_id": email})

        if user and user["password"] == password:
            access_token = create_access_token(identity=email, fresh=True)
            response_body = json.dumps({
                "success": True,
                "message": "User Login successful",
                "user": email,
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
            json.dumps({"error": "Something went wrong"}),
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
        user_exists = db.users.find_one({"_id": current_user})
        if not user_exists:
            return Response(
                json.dumps({"error": "Register first"}),
                status=400,
                content_type="application/json"
            )

        # Check if user already has templates
        user_templates = db.templates.find_one({"_id": current_user})

        if user_templates:
            # Update the existing template dictionary
            db.templates.update_one(
                {"_id": current_user},
                {"$set": {f"templates.{template_id}": json_body}}
            )
        else:
            # Create a new entry for this user
            db.templates.insert_one({
                "_id": current_user,
                "templates": {template_id: json_body}
            })

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
            json.dumps({"error": "Something went wrong"}),
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
        user_exists = db.users.find_one({"_id": current_user})
        if not user_exists:
            return Response(
                json.dumps({"error": "Register first"}),
                status=400,
                content_type="application/json"
            )
            
        # Fetch user templates from the database
        user_templates = db.templates.find_one({"_id": current_user}, {"_id": 0, "templates": 1})

        # Check if the user has any templates
        if not user_templates or "templates" not in user_templates:
            return Response(
                json.dumps({"error": "Post a template first."}),
                status=400,
                content_type="application/json"
            )

        response_body = json.dumps({
            "success": True,
            "message": "Templates fetched successfully",
            "templates": user_templates["templates"]
        })

        response = Response(response_body, status=200, content_type="application/json")
        response.headers['Content-Type'] = request.headers.get('Content-Type')
        response.headers['Accept'] = request.headers.get('Accept')
        return response

    except Exception:
        return Response(
            json.dumps({"error": "Something went wrong"}),
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
        user_exists = db.users.find_one({"_id": current_user})
        if not user_exists:
            return Response(
                json.dumps({"error": "Register first"}),
                status=400,
                content_type="application/json"
            )

        # Fetch the user's templates from the database
        user_templates = db.templates.find_one({"_id": current_user}, {"_id": 0, "templates": 1})

        # Check if the user has any templates
        if not user_templates or "templates" not in user_templates:
            return Response(
                json.dumps({"error": "Post a template first."}),
                status=400,
                content_type="application/json"
            )

        # Fetch the requested template by ID
        template = user_templates["templates"].get(template_id)
        if not template:
            return Response(
                json.dumps({"error": "Template not found."}),
                status=404,
                content_type="application/json"
            )

        response_body = json.dumps({
            "success": True,
            "message": "Template fetched successfully",
            "templates": template
        })

        response = Response(response_body, status=200, content_type="application/json")
        response.headers['Content-Type'] = request.headers.get('Content-Type')
        response.headers['Accept'] = request.headers.get('Accept')
        return response

    except Exception:
        return Response(
            json.dumps({"error": "Something went wrong"}),
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
        user_exists = db.users.find_one({"_id": current_user})
        if not user_exists:
            return Response(
                json.dumps({"error": "Register first"}),
                status=400,
                content_type="application/json"
            )

        # Fetch the user's templates
        user_templates = db.templates.find_one({"_id": current_user}, {"_id": 0, "templates": 1})

        # Check if user has templates
        if not user_templates or "templates" not in user_templates:
            return Response(
                json.dumps({"error": "Post a template first."}),
                status=400,
                content_type="application/json"
            )

        # Check if the template exists
        if template_id not in user_templates["templates"]:
            return Response(
                json.dumps({"error": "Template not found."}),
                status=404,
                content_type="application/json"
            )

        # Update the specific template
        db.templates.update_one(
            {"_id": current_user},
            {"$set": {f"templates.{template_id}": json_body}}
        )
        
        # Fetch the updated template from the database
        updated_template = db.templates.find_one(
            {"_id": current_user},
            {"_id": 0, f"templates.{template_id}": 1}
        )
        
        response_body = json.dumps({
            "success": True,
            "message": "Template updated successfully",
            "templates": updated_template
        })

        response = Response(response_body, status=200, content_type="application/json")
        response.headers['Content-Type'] = request.headers.get('Content-Type')
        response.headers['Accept'] = request.headers.get('Accept')
        return response

    except Exception:
        return Response(
            json.dumps({"error": "Something went wrong"}),
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
        user_exists = db.users.find_one({"_id": current_user})
        if not user_exists:
            return Response(
                json.dumps({"error": "Register first."}),
                status=400,
                content_type="application/json"
            )

        # Fetch the user's templates
        user_templates = db.templates.find_one({"_id": current_user}, {"_id": 0, "templates": 1})

        # Check if user has templates
        if not user_templates or "templates" not in user_templates:
            return Response(
                json.dumps({"error": "Post a template first."}),
                status=400,
                content_type="application/json"
            )

        # Check if the template exists
        if template_id not in user_templates["templates"]:
            return Response(
                json.dumps({"error": "Template not found."}),
                status=404,
                content_type="application/json"
            )

        # Delete the specific template
        db.templates.update_one(
            {"_id": current_user},
            {"$unset": {f"templates.{template_id}": ""}}
        )

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
            json.dumps({"error": "Something went wrong"}),
            status=400,
            content_type='application/json'
        )
        
if __name__ == "__main__":
    app.run(debug=True)
