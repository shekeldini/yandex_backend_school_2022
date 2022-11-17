def get_available_services():
    return [f"http://{link}/" for link in "localhost:7000;localhost:9000".split(";")]