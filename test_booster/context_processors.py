from os import environ

def exvars(_request):
    """ Context proccesor for export variables """
    return {
        'VK_APP_ID': environ['VK_APP_ID'],
        'VK_REDIRECT_URL': environ['VK_REDIRECT_URL'],
    }
