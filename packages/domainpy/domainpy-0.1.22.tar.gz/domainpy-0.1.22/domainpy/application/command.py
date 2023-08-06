from uuid import uuid4

from domainpy.utils.constructable import Constructable
from domainpy.utils.immutable import Immutable
from domainpy.utils.dictable import Dictable

class ApplicationCommand(Constructable, Immutable, Dictable):

    class Struct(Constructable, Immutable, Dictable):
        pass

    def __init__(self, *args, **kwargs):
        self.__dict__.update({
            '__trace_id__': kwargs.pop('__trace_id__', str(uuid4())),
            '__message__': 'command'
        })
        
        super(ApplicationCommand, self).__init__(*args, **kwargs)
