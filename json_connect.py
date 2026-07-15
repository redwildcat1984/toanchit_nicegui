import json

class JsonConnect:
    def __init__(self) -> None:
        self.path:str|None = None
        self.data = None

    def load(self):
        if self.path:
            try:
                with open(self.path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                    return True
            except FileNotFoundError:
                return False
        else:
            pass

    def save(self):
        if self.path:
            try:
                with open(self.path, 'w', encoding='utf-8') as f:
                    json.dump(self.data, f, indent=4, ensure_ascii=False)
                    return True
            except Exception as e:
                print(e)
                return False
