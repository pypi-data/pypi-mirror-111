from typing import Dict,Optional, Callable
from ._core import Action
import glob,os,uuid

class delete(Action):
    def __init__(self, name) -> None:
        self.name = name

    def _now(self):
        # meh stupid here.
        pattern_list = glob.glob(self.name)
        print(f'Match File List: {pattern_list}')

        for f in pattern_list:
            os.remove(f)

class do(Action):
    def __init__(self,func:Callable) -> None:
        # super().__init__() Don't need this anymore... I guess ?
        Action._callable_check(func)
        self.func = func

    def _now(self):
        return self.func()


class rename(Action):
    def __init__(self, 
        old_name: str,
        new_name: str,
        with_pattern:bool=False)->None:

        self.old_name = old_name
        self.new_name = new_name
        self.with_pattern  = with_pattern

    def _now(self):
        pattern_list = Action.glob_file(self.old_name)
        rand_id = lambda:str(uuid.uuid4())[:8]
        for name in pattern_list:
            os.rename(name,f"{ rand_id() if self.with_pattern else ''}{self.new_name}")

class create_folder(Action):
    def __init__(self,name:str) -> None:
        self.name = name

    def _now(self):
        os.mkdir(self.name)
        return self.name

class create_file(Action):
    def __init__(self,name:str) -> None:
        self.name = name
    def _now(self):
        f = open(self.name,'w+')
        f.close()
        # return file name ,but autually I want it return content.
        return self.name

class get_size(Action):
    '''
    return actual size of file
    '''
