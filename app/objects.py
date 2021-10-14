# zObject represents the base object in the application
# we can create it
# we can name it
# we can add values to it
import uuid

#the Object class 
class ZObject:
    def __init__(self, name=''):
        # create a data structure for the object
        self.data = {}
        self.data['uuid'] = uuid.uuid4().bytes
        if len(name) > 0:
            self.data['name'] = name
        else:    
            self.data['name'] = '[BLANK]'


if __name__ == '__main__':
    myObjs = []
    myObjs.append(ZObject(name='Hello World!'))
    myObjs.append(ZObject())
    for item in myObjs:
        for attrib in item.data.keys():
            print ('{}: {}'.format(attrib, item.data[attrib]))
    