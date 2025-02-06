from os import environ

def export_vars(_request):
    """ Context proccesor for export variables """
    return {
        "TELEGRAM_BOT_USERNAME": environ['TELEGRAM_BOT_USERNAME'],
    }
