
from flask import Flask, Response
import subprocess

app = Flask(__name__)

@app.route('/proxy')
def proxy():
    stream_url = "http://fm983.cityfm.tw:8080/983.mp3"  # 原始電台串流
    process = subprocess.Popen(
        ['ffmpeg', '-i', stream_url, '-f', 'mp3', '-'],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    )
    return Response(process.stdout, mimetype='audio/mpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
