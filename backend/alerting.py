from db import LocalDatabase
class Alerter(object):
    """
    Alerts the user when the satellite is about to pass.
    """
    def __init__(self):
        self.db = LocalDatabase()
        self.db.load()
        pass

    def alert(self,):
        pass

class WebHookAlerter(Alerter):
    """
    Alerts the user by sending a webhook.
    """
    def __init__(self,url):
        self.kind = "webhook"
        self.url = url
        pass

    def alert(self,):
        pass

def create_alert(Alerter, satelite_id, after_when):
    """
    Creates an alert for the next pass of the satellite.
    """
    pass

def get_alerts():
    """
    Returns a list of alerts.
    """
    pass

def delete_alert(alert_id):
    """
    Deletes an alert for the given alert_id.
    """
    pass
