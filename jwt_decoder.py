import jwt

# Your JWT token
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNzQwNDE2MDQxLCJqdGkiOiI3M2Y2Y2E0My1lMmQwLTQ2ZGEtYTBmZC1jNzYxY2VhNGQ1NjciLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoibGFrc2htYW4xMTIyMDAwQGdtYWlsLmNvbSIsIm5iZiI6MTc0MDQxNjA0MSwiY3NyZiI6IjIzYTc2ZjY1LWQ2ZWUtNDE3My1iYmU4LWU1ZDc3NmJiM2M0NiIsImV4cCI6MTc0MDQxNjk0MX0.yim2h3o-l4ZU3TwGTb3cIMZCisb2AiUnQE3cXfrnQJc"

# Secret key used to encode the token
secret_key = "lakshman"

# Decode the JWT
decoded_data = jwt.decode(token, secret_key, algorithms=["HS256"])

print(decoded_data)  # Shows the stored user info
