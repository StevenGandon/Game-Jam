import builtins

class Setting(object):
    def __init__(self, setting_type = bool, setting_value = None) -> None:
        self.type = setting_type
        self.value = setting_value

    def __str__(self) -> str:
        return (f'{self.type.__qualname__}({self.value})')

    def __repr__(self) -> str:
        return (self.__str__())

class Settings(object):
    def __init__(self) -> None:
        self.datas = {}

    def __str__(self) -> str:
        return ('<Settings datas=[' + ','.join(f"{item}: {self.datas[item]}" for item in self.datas) + ']>')

    def __repr__(self) -> str:
        return (self.__str__())

    def add_setting(self, name: str, setting: Setting) -> None:
        self.datas[name] = setting

    def create_setting(self, name: str, setting_type = bool, setting_value = None) -> None:
        self.datas[name] = Setting(setting_type, setting_value)

    def get_setting(self, name: str, default = None):
        setting = self.datas.get(name, None)
        return (setting.type(setting.value) if setting else default)

    def to_file(self, file_path: str) -> None:
        with open(file_path, 'w') as fp:
            for item in self.datas:
                fp.write(f"{item}:{self.datas[item].type.__qualname__}:{self.datas[item].value}\n")

    def from_file(self, file_path: str) -> None:
        with open(file_path, 'r') as fp:
            for item in fp.read().split('\n'):
                if (len(item.split(':')) < 3):
                    continue
                self.create_setting(item.split(':')[0].strip(), getattr(builtins, item.split(':')[1].strip(), str), ':'.join(item.split(':')[2:]).strip())
