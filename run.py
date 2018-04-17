from app import app

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['vcf'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if __name__ == '__main__' :
  app.run()

