import requests


class ServiceRegistry:
    def __init__(self, service_links):
        self.services: list = service_links

    def get_alive_services(self) -> list:
        alive_services = []
        for service in self.services:
            if self._health_check(service):
                alive_services.append(service)
        return alive_services

    @staticmethod
    def _health_check(url):
        try:
            r = requests.get(url)
            if r.status_code > 500:
                return None
            return url
        except requests.exceptions.RequestException:
            return None
