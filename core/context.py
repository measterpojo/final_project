from core.utils import get_request_data, get_model_obj, has_valid_profile


class DABContext(dict):

    def __init__ (self, request, model_object=None, **kwargs):
        self.request = request
        self.app_name = get_request_data(request, 'app_name')
        self.model_name = get_request_data(request, 'model_name')
        self.model_id = get_request_data(request, 'model_id')
        self.model_object = model_object
        if not self.model_object:
            self.model_object = get_model_obj(self.app_name, self.model_name, self.model_id)
        super().__init__(**self(), **kwargs)
    
    def __call__(self):

        context = {
            'model_object': self.model_object,
            'model_name': self.model_name,
            'app_name': self.app_name,
            'model_id': self.model_id,
            'user': self.request.user,
            'has_valid_profile': has_valid_profile()


        }

        return context