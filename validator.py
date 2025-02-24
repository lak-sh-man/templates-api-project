import json
from flask import request, Response

def validate_header():
    """Validates Content-Type and Accept headers for JSON requests."""
    content_type = request.headers.get('Content-Type')
    accept_header = request.headers.get('Accept')

    if content_type is None:
        return Response(
            json.dumps({"error": "Content-Type header is required"}),
            status=400,
            content_type='application/json'
        )

    if content_type.lower() != 'application/json':
        return Response(
            json.dumps({"error": "Content-Type must be application/json"}), 
            status=400, 
            content_type='application/json'
        )

    if accept_header is None:
        return Response(
            json.dumps({"error": "Accept header is required"}),
            status=400,
            content_type='application/json'
        )

    if accept_header.lower() != 'application/json':
        return Response(
            json.dumps({"error": "Accept must be application/json"}), 
            status=406, 
            content_type='application/json'
        )

    return None

def validate_request_body():
    if not request.data:  # request.data is empty if no body is sent
        return Response(
            json.dumps({"error": "Request body cannot be empty"}),
            status=400,
            content_type='application/json'
        )

    return None