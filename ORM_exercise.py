# ORM
class Field(object):
    def __init__(self, name, colume_type):
        self.name = name
        self.colume_type = colume_type
    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)

class StringField(Field):
    def __init__(self,name):
        super().__init__(name, 'varchar(100)')

class IntegerField(Field):
    def __init__(self,name):
        super().__init__(name, 'bigint')

class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name=='Model':
            return type.__new__(cls, name, bases, attrs)
        print('Found model: %s' % name)
        mappings=dict()
        for k, v in attrs.items():
            if isinstance(v, Field):
                print('Found mapping: %s ==>%s' % (k,v))
                mappings[k]=v
        for k in mappings.keys():
            attrs.pop(k)               # 删除User类中的id name等属性后，因实例
            # self没有 id name 等属性，args.append(getattr(self,k,None)）
            # 会通过__getattr__取得实例属性self[k]，即id name等的实际值；
            # 若不删除，执行args.append(getattr(self,k,None)）时，
            # 会通过self.k获得User类中定义的属性，即id name等对应数据库中表的列
        attrs['__mapping__'] = mappings
        attrs['__table__'] = name
        return type.__new__(cls, name, bases, attrs)


class Model(dict,metaclass=ModelMetaclass):

    def __init__(self,**kw):
        super().__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)
    def __setattr__(self, key, value):
        self[key] = value

    def save(self):
        fields = []
        params = []
        args = []
        for k,v in self.__mapping__.items():
            fields.append(v.name)
            params.append('?')
            args.append(getattr(self,k,None))
        sql = 'insert into %s (%s) values (%s)'%(self.__table__,
        ','.join(fields),','.join(params))
        print('SQL: %s'%sql)
        print('ARGS: %s'%str(args))
class User(Model):
    id = IntegerField('id')
    name = StringField('name')
    email = StringField('email')
    password = IntegerField('password')

u = User(id=12345, name='Michael', email='test@orm.org',
         password='my-pwd')
u.save()
