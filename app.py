from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

API_KEY = "f4918678db31ad1c3c463bf32912dac9"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&lang=pt&units=metric"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AgriSenso - Recomendação de Irrigação</title>
</head>
<body style="font-family: Arial; padding: 20px;">
    <h1>🌿 AgriSenso</h1>
    <p>Preencha os dados abaixo para receber uma recomendação:</p>
    <form method="POST">
        <label>Tipo de cultura:</label><br>
        <input type="text" name="cultura" required><br><br>

        <label>Umidade atual do solo (%):</label><br>
        <input type="number" name="umidade" required><br><br>

        <label>Cidade (para previsão do tempo):</label><br>
        <input type="text" name="cidade" required><br><br>

        <button type="submit">Obter Recomendação</button>
    </form>

    {% if recomendacao %}
        <h2>🌱 Recomendação:</h2>
        <p><strong>{{ recomendacao }}</strong></p>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    recomendacao = None
    if request.method == 'POST':
        cultura = request.form['cultura']
        umidade = int(request.form['umidade'])
        cidade = request.form['cidade']

        # Consulta à API do tempo
        response = requests.get(WEATHER_URL.format(city=cidade, key=API_KEY))
        if response.status_code == 200:
            weather_data = response.json()
            condicao = weather_data['weather'][0]['main'].lower()

            if umidade > 70:
                recomendacao = "Solo está úmido. Não é necessário irrigar."
            elif 'chuva' in condicao or 'rain' in condicao:
                recomendacao = f"Previsão de chuva em {cidade}. Espere antes de irrigar."
            else:
                recomendacao = f"Sem previsão de chuva. Irrigue sua plantação de {cultura} nas próximas horas."
        else:
            recomendacao = "Erro ao obter dados do clima. Verifique o nome da cidade."

    return render_template_string(HTML_TEMPLATE, recomendacao=recomendacao)

if __name__ == '__main__':
    app.run(debug=True)
