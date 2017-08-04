class HttpHelper(object):
    @staticmethod
    def print_request(response, logger):
        logger.debug('{}\n{}\n{}\n\n{}'.format(
            '-----------REQUEST-----------',
            response.request.method + ' ' + response.request.url,
            '\n'.join('{}: {}'.format(k, v) for k, v in response.request.headers.items()),
            response.request.body,
        ))


        logger.debug('{}\n{}\n\n{}'.format(
            '-----------RESPONSE-----------',
            '\n'.join('{}: {}'.format(k, v) for k, v in response.headers.items()),
            response.text,
        ))
