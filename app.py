from flask import Flask, render_template, request, send_file
import qrcode
import os

app = Flask(__name__)

#Diretório onde os arquivos de QR Code serão armazenados temporariamente
QR_FOLDER = 'static/qr_codes'
if not os.path.exists(QR_FOLDER):
    os.makedirs(QR_FOLDER)
    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Pega o link e o nome do arquivo enviados pelo usuário
        link = request.form.get('link')
        nome_arquivo = request.form.get('nome_arquivo') or 'qrcode_imagem' # Nome padrão caso o usuário não insira
        
        # Cria o QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4
        )
        qr.add_data(link)
        qr.make(fit=True)
        
        # Gera a imagem do QR Code
        img = qr.make_image(fill='black', black_color='white')
        caminho_arquivo = os.path.join(QR_FOLDER, f"{nome_arquivo}.png")
        
        # Salva o arquivo de QR Code no diretório temporário
        img.save(caminho_arquivo)
        
        # Envia o arquivo para o usuário baixar
        return send_file(caminho_arquivo, as_attachment=True)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port =5000)