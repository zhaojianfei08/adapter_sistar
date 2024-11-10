from create_app import create_app
from config import config_dict

config_obj = config_dict['config']

app = create_app(config_obj)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)


"""
 <Rule '/api/create_batch' (POST, OPTIONS) -> api_bp.create_batch_func>,
 <Rule '/api/create_batch_ex' (POST, OPTIONS) -> api_bp.create_batch_ex_func>,
 <Rule '/api/delete_batch' (POST, OPTIONS) -> api_bp.delete_batch_func>,
 <Rule '/api/get_last_error' (POST, OPTIONS) -> api_bp.get_last_error_func>,
 <Rule '/api/get_last_full_error_string' (POST, OPTIONS) -> api_bp.get_last_full_error_string_func>,
 <Rule '/api/set_batch_parameters' (POST, OPTIONS) -> api_bp.set_batch_parameters_func>,
 <Rule '/api/set_batch_size' (POST, OPTIONS) -> api_bp.set_batch_size_func>,
 <Rule '/api/set_batch_start_data' (POST, OPTIONS) -> api_bp.set_batch_start_data_func>,
 <Rule '/api/set_batch_status' (POST, OPTIONS) -> api_bp.set_batch_status_func>,
 <Rule '/api/set_timeout' (POST, OPTIONS) -> api_bp.set_timeout_func>,
 <Rule '/api/add_parameter' (POST, OPTIONS) -> api_bp.add_parameter_func>,
 <Rule '/api/get_number_at' (POST, OPTIONS) -> api_bp.get_number_at_func>,
 <Rule '/api/get_size' (POST, OPTIONS) -> api_bp.get_size_func>,
 <Rule '/api/get_value_at' (POST, OPTIONS) -> api_bp.get_value_at_func>,
"""


