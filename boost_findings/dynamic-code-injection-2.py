from flask import request

@app.route('/')
def index():
    module = request.args.get("module")  # User input
    # eval() is also equally dangerous
    exec("import urllib%s as urllib" % module) # Allows the user to execute arbitrary Python code
