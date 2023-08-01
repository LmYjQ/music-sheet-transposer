import os
from flask import Flask, flash, request, redirect, url_for, session,send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import logging
from pypdf import PdfReader
import zipfile

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('HELLO WORLD')



UPLOAD_FOLDER = '/Users/qiyusama/Downloads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "your_unique_and_secret_key_here"  # 设置秘钥

origins = ["*", "*"]
cors = CORS(
  app, 
  resources={r"/*": {"origins": origins}},
  expose_headers="location,link",
  allow_headers="content-type,if-modified-since",
  methods="OPTIONS,GET,HEAD,POST"
)

def file2zip(zip_file_name: str, file_names: list):
    """ 将多个文件夹中文件压缩存储为zip
    
    :param zip_file_name:   /root/Document/test.zip
    :param file_names:      ['/root/user/doc/test.txt', ...]
    :return: 
    """
    # 读取写入方式 ZipFile requires mode 'r', 'w', 'x', or 'a'
    # 压缩方式  ZIP_STORED： 存储； ZIP_DEFLATED： 压缩存储
    with zipfile.ZipFile(zip_file_name, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        for fn in file_names:
            parent_path, name = os.path.split(fn)
            
            # zipfile 内置提供的将文件压缩存储在.zip文件中， arcname即zip文件中存入文件的名称
            # 给予的归档名为 arcname (默认情况下将与 filename 一致，但是不带驱动器盘符并会移除开头的路径分隔符)
            zf.write(fn, arcname=name)
            
            # 等价于以下两行代码
            # 切换目录， 直接将文件写入。不切换目录，则会在压缩文件中创建文件的整个路径
            # os.chdir(parent_path)
            # zf.write(name)


def pdf2img(file_name):
    full_name = os.path.join(UPLOAD_FOLDER,'test_docs',file_name) # "/Users/qiyusama/Documents/谱子/vivaldi_rv356/IMSLP745001-PMLP126411-02._Concerto_for_Violin_in_A_minor,_RV356_-_Violas.pdf" # 替换成你的PDF文件路径
    output_folder = os.path.join(UPLOAD_FOLDER,"output_images")  # 图像输出文件夹

    reader = PdfReader(full_name)
    index = 0
    file_list = []
    for page in reader.pages:
        print(f"page {index} has {len(page.images)} images")
        for image in page.images:
            image_name = os.path.join(output_folder,file_name.split('.')[0]+f"{index}.jpg")
            file_list.append(image_name)
            print(image_name)
            with open(image_name, "wb") as fp:
                fp.write(image.data)
        index += 1
    zip_name = os.path.join(output_folder,file_name.split('.')[0]+"_result.zip")
    file2zip(zip_name,file_list)

@app.route('/upload', methods=['POST'])
def fileUpload():
    target=os.path.join(UPLOAD_FOLDER,'test_docs')
    if not os.path.isdir(target):
        os.mkdir(target)
    logger.info("welcome to upload`")
    file = request.files['file'] 
    filename = secure_filename(file.filename)
    destination="/".join([target, filename])
    file.save(destination)
    session['uploadFilePath']=destination
    pdf2img(filename)
    response={"status_code":200}
    return response

@app.route('/download/<filename>')
def download(filename):
    filename = os.path.join('/Users/qiyusama/Downloads/output_images',filename)
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True,host="0.0.0.0",use_reloader=False)

