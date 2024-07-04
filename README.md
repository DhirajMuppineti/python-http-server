
# Simple Python HTTP Server

This is a simple HTTP server implemented in Python using the `socket` and `threading` modules. It supports basic HTTP methods such as `GET` and `POST` and handles specific routes for demonstration purposes. I have coded this with the help of codecrafters code your own http server challenge.

## Features

- Handles `GET` requests to the root ("/") and specific routes.
- Handles `POST` requests for file creation.
- Responds with appropriate HTTP status codes.
- Supports echoing URL parameters and displaying user-agent information.

## Routes

### GET /

Responds with a `200 OK` status.

### GET /echo/{message}

Responds with the message provided in the URL.

### GET /user-agent

Responds with the user-agent string of the client.

### GET /files/{filename}

Serves a file from the `tmp/data` directory in the current project directory. Responds with `200 OK` if the file exists, otherwise responds with `404 Not Found`.

### POST /files/{filename}

Creates a file with the provided filename in the `tmp/data` directory in the current project directory. The content of the file is taken from the body of the POST request. Responds with `201 Created`.


## How to Run

1. Ensure you have Python installed on your machine.
2. Save the server code in a file, e.g., `server.py`.
3. Open a terminal and navigate to the directory containing `server.py`.
4. Run the server using the command:
   ```sh
   python server.py
