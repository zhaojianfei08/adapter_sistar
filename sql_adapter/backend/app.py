from create_app import create_app
from config import config_dict

config_obj = config_dict['config']

app = create_app(config_obj)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
