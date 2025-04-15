from urllib import request


headers = {
    "Content-Type": "application/json"
}

body = {
    "birth_date": "1990-01-01",
    "birth_time": "12:00",
    "birth_location": "New York, NY"
}

response = request.post(
    "http://127.0.0.1:5000/birthchart",
    headers=headers,
    json=body
)