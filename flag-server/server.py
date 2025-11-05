from flask import Flask, request, send_file
import os
import zipfile
from io import BytesIO
import glob

app = Flask(__name__)
CHALLENGE_ROOT = "/challenges"
PORT = 5000

@app.route('/')
def index():
    return '''
    Flag Server is running.

    If you got the flag, download the solution by sending the following request:
    curl -X POST -d "challenge=XX-YY&flag=RHUL{your_flag}" http://188.166.153.223:5000/submit --output solution.zip
'''

@app.route('/submit', methods=['POST'])
def submit():
    challenge_id = request.form.get("challenge")
    flag = request.form.get("flag")

    if not challenge_id or not flag:
        return "Missing 'challenge' and/or 'flag'.", 400

    try:
        major, minor = challenge_id.split("-")
    except ValueError:
        return "Invalid challenge format. Use NN-NN.", 400

    major_glob = os.path.join(CHALLENGE_ROOT, f"{major}-*")
    for major_dir in glob.glob(major_glob):
        minor_glob = os.path.join(major_dir, f"{minor}-*")
        for challenge_dir in glob.glob(minor_glob):
            flag_file = os.path.join(challenge_dir, "flag.txt")
            solution_dir = os.path.join(challenge_dir, "solution")

            if os.path.isfile(flag_file) and os.path.isdir(solution_dir):
                with open(flag_file, 'r') as f:
                    expected_flag = f.read().strip()
                if flag != expected_flag:
                    return "Incorrect flag.", 403

                # build solution.zip
                zip_buf = BytesIO()
                with zipfile.ZipFile(zip_buf, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, _, files in os.walk(solution_dir):
                        for file in files:
                            abs_path = os.path.join(root, file)
                            rel_path = os.path.relpath(abs_path, solution_dir)
                            zipf.write(abs_path, arcname=rel_path)
                zip_buf.seek(0)
                return send_file(
                    zip_buf,
                    mimetype='application/zip',
                    as_attachment=True,
                    download_name=f"{challenge_id}-solution.zip"
                )

    return "Challenge not found or missing required files.", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)