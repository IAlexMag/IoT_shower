from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('configuracion.html')

@app.route("/conectar", methods = ['GET','POST'])
def conectar():
    if request.method == 'POST':
        ssid_wifi = request.form['ssid_wifi']
        wifi_pass = request.form['wifi_pass']
        resultado = conect_wifi(ssid_wifi, wifi_pass)
        return render_template('result_connection.html', resultado = resultado)
    else:
        return render_template('configuracion.html')

def conect_wifi(ssid_wifi, wifi_pass):
    try:
        comand = f"nmcli device wifi connect '{ssid_wifi}' password '{wifi_pass}'"
        result = subprocess.run(comand, shell=True, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f'Error: {e}'

if __name__ == '__main__':
    app.run(port=5555, debug=True)