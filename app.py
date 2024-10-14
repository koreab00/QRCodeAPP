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
    qr_img_name = None
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
        img.save(file_path) # Salva a imagem no diretório temporário
        
        qr_img_name = f'{file_name}.png'
        
    return render_template('index.html', qr_img_name=qr_img_name)

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(file_path, as_attachments=True)

if __name__ == '__main__':
    app.run(debug=True)