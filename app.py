from flask import Flask, render_template, request, send_file
import qrcode
import os
from io import BytesIO

app = Flask(__name__)

#Diretório onde os arquivos de QR Code serão armazenados temporariamente
UPLOAD_FOLDER = 'static/qr_codes'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
@app.route('/', methods=['GET', 'POST'])
def index():
    qr_img_name = None
    if request.method == 'POST':
        # Obtém o link do formulário
        data = request.form.get('link')
        
        # Renomeia o arquivo de imagem com o nome fornecido pelo usuário
        file_name = request.form.get('filename') or 'qrcode'
        file_path = os.path.join(UPLOAD_FOLDER, f'{file_name}.png')
        
        # Cria o QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Gera a imagem do QR Code
        img = qr.make_image(fill='black', black_color='white')
        img.save(file_path) # Salva a imagem no diretório temporário
        
        qr_img_name = f'{file_name}.png'
        
    return render_template('index.html', qr_img_name=qr_img_name)

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)