from flask import Flask, request,send_file, render_template,send_from_directory, Response
import shutil
import os
import time

from dialog_manager import flaskbot_utils as bot_utils
UPLOAD_FOLDER = os.getcwd()
app = Flask(__name__)
TIMER = 0

print(os.getcwd())
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def train():
    global TIMER
    print("Training started...")
    TIMER = 20
    train_res, _ = bot_utils.train_yolo('dataset')
    if not train_res : #Тренировка не была запущена.
        print('train_res', train_res)
    TIMER = 30
    bot_utils.bestpt_copy()
    TIMER += 10
    model_path = bot_utils.pt2onnx('dataset')
    TIMER += 10
    # bot_utils.onnx2tmfile()
    TIMER += 10
    # quant_model_path = bot_utils.quantization('dataset')
    # print(quant_model_path)
    TIMER +=25
    return model_path

@app.route('/')
def home():
   return render_template('main.html')
@app.route('/', methods=['POST'])
def save_zip():
    if 'file' not in request.files:
        return 'No file found', 400

    file = request.files['file']
    if file.filename == '':
        return 'No file selected', 400

    save_path = os.path.join('dataset', file.filename) 
    file.save(save_path)
    
    shutil.unpack_archive(save_path, 'dataset')
    os.remove(save_path)
    global TIMER
    TIMER += 10
    train()
    TIMER = 100
    return "File saved", 200

    
@app.route('/progress')
def progress():
    def generate():
        global TIMER
        x = TIMER
        
        
        yield "data:" + str(x) + "\n\n"
            # x = x + 10
            # time.sleep(0.5)

    return Response(generate(), mimetype= 'text/event-stream')
@app.route('/download/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True,port=4444)

