# Rover

## Filestructure
The following is a full tree of the files in this repository, followed by subtrees of each directory and/or appropriate descriptions.
```
./
 ├── main.py
 ├── motors.py
 ├── requirements.txt
 ├── README.md
 ├── /oldversion
 │    └── ...
 ├── /static
 │    └── ...
 └── /templates
      └── ...
```

### `main.py`
The `main.py` Python script runs the Flask webapp and listens for key presses while a user is connected to that website. On certain key presses ('w', 'a', 's', and 'd'), this script calls the appropriate movement function imported from `motors.py`.

### `motors.py`
The `motors.py` Python script handles all RPi GPIO, controlling the motors and handling the rover's movement.

### `/static`
The `/static` directory is always accessible to Flask through templates. If any asset or file is referenced in a template, it should be from this directory using this style of `src` or `href`: `"{{ url_for('static', filename='assets/favicon.png') }}"`.
```
/static
 ├── /assets
 │    └── ...
 └── cloudflare.com.socket.io.js
```
- `/assets`: Directory containing images and assets.
- `cloudflare.com.socket.io.js`: An offline copy of `https://cdnjs.cloudflare.com/ajax/libs/socket.io/3.1.3/socket.io.js` for offline functionality

### `/templates`
The `/templates` directory is where Flask will look to find anything referenced via `render_templates('FILENAME.html')`.

### `/oldversion`
The `/oldversion` directory contains code from the previous implementations that ran the rover.



## Setup

> Recomended: Use a python virtual enviroment for installing dependencies.

`python -m .venv venv`
`source .venv/bin/activate` (for Linux/Mac)
`.venv/Scripts/activate.bat` (for Windows - cmd)
`.venv/Scripts/activate.ps1` (for Windows - Powershell)
`pip install -r requirements.txt`
`python main.py`
