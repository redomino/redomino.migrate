from zope.interface import implements
from zope.interface import classProvides

from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.interfaces import ISection

class Limit(object):
    """ limits the number of retrieved objects"""

    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.transmogrifier = transmogrifier
        self.name = name
        self.options = options
        self.previous = previous
        self.context = transmogrifier.context
        self.limit = int(self.options['limit'])


    def __iter__(self):
        for n, item in enumerate(self.previous):
            if self.limit == n:
                break
            yield item

class Replace(object):
    """ replace text """

    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.transmogrifier = transmogrifier
        self.name = name
        self.options = options
        self.previous = previous
        self.context = transmogrifier.context
        self.field = self.options['field']
        self.word = self.options['word']
        self.replace = self.options['replace']

    def __iter__(self):
        for item in self.previous:
            if self.field in item:
                item[self.field] = item[self.field].replace(self.word, self.replace)
            yield item


class RemoveProperties(object):
    """ remove Zope properties """

    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.transmogrifier = transmogrifier
        self.name = name
        self.options = options
        self.previous = previous
        self.context = transmogrifier.context
        self.removeProperties = [ p.strip() for p in self.options['properties'].split(',') ]

    def __iter__(self):
        for item in self.previous:        
            if '_properties' in item:
                item['_properties'] = [t for t in item['_properties'] if t[0] not in self.removeProperties]
            yield item


class RenameUsers(object):
    """ rename the user associated to an object """

    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.transmogrifier = transmogrifier
        self.name = name
        self.options = options
        self.previous = previous
        self.context = transmogrifier.context
        l1 = [ p.strip() for p in self.options['from'].split(',') ]
        l2 = [ p.strip() for p in self.options['to'].split(',') ]
        self.fromto = zip(l1, l2)
        self.default = self.options['default']

    def translate(self, item):
        for f, t in self.fromto:
            if f == item:
                return t
                
        return self.default or item

    def __iter__(self):
        for item in self.previous:
            for field in ['creators', 'contributors']:
                if field in item:
                    item[field] = [self.translate(i) for i in item[field]]


            yield item


class IgnoreFields(object):
    """ remove fields from the chain """

    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.transmogrifier = transmogrifier
        self.name = name
        self.options = options
        self.previous = previous
        self.context = transmogrifier.context
        self.fields = [ field.strip() for field in self.options['fields'].split(',') ]

    def __iter__(self):
        for item in self.previous:
            for field in self.fields:
                if item.has_key(field):
                    del item[field]
            yield item
