from requests import get
from os import getenv


class RestClient:
    
    api_key = None
    api_key_argname = 'api_key'

    def __init__(self, host, api_key=None, api_key_env=None):
        self.host = host
        self.api_key = api_key
        if api_key_env is not None:
            self.api_key = getenv(api_key_env)

    def api_key_arg(self):
        if self.api_key is None:
            return {}
        return {self.api_key_argname: self.api_key}

    def query_string(self, command='', args={}):
        
        query_args = RestArgs(**self.api_key_arg(), **args)
        string = f'{self.host}{command}?{query_args}'
        return string

    def get(self, command='', rest_args={}):
        response = get(self.query_string(command, rest_args))
        # TODO error handling
        return response.json()


class RestArgs(dict):
    def __str__(self):
        strings = []
        for key in self.keys():
            strings.append(f'{key}={self[key]}')
        return '&'.join(strings)


if __name__ == '__main__':

    class Tmdb(RestClient):

        def __init__(self, api_key=None):
            RestClient.__init__(self,
                                'https://api.themoviedb.org/3',
                                api_key,
                                'TMDB_API_KEY')
    args = RestArgs()
    args['test'] = 'test'
    args['num'] = 4
    args.update({'a': 2})
    args2 = RestArgs(**args, **{'b': 2})
    print(args2)

    rest_api = Tmdb('http://localhost')

    query = rest_api.query_string(args, '/test')

    print(query)
