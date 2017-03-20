##Author: Guo Zichun
##Date:12.5.2015

##generator.send(value)
##Resumes the execution and “sends” a value into thegenerator function. The value
##argument becomes the result of the current yield expression. The send() method
##returns the next value yielded by the generator,or raises StopIteration if the
##generator exits without yielding another value.When send() is called to start the
##generator, it must be called with None as the argument, because there is no yield
##expression that could receive thevalue.

##---------------------------------------------------------------------------------

def consumer():
    r = 1
    print('ff')
    while True:
        print('Generator is starting.')
        n = yield r
        print(n)
        if not n:
           return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'

def produce(c):
    a=c.send(None)
    print('a=%s'%a)
    n = 0
    while n < 5:
        #n = 0
        n = n +1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()

c = consumer()
produce(c)


##------------------------------------------------------------------------------------
##c.send(None)，启动了generator consumer，从cosumer最开始运行至yield停止（yield不执行），
##输出结果可以印证这点，yield前的打印语句执行，其后的语句不执行，根据文档中The send() method
##returns the next value yielded by the generator，此时r=1，即下一个被yield的就是1，所以
##c.send(None)返回值为1，输出结果可见a=1
##
##c.send(n)部分，以c.send(1)为例：程序从上次停止的yield处开始执行，先执行yield，根据官方
##文档generator.send（value）中的value当成为当前yield的结果，所以n = 1,输出结果可印证；程序继续
##向下执行，直至在下一次循环中再次遇到yield停止（同样yield不执行），在此期间，程序执行了
##print('[CONSUMER] Consuming %s...' % n)
##r = '200 OK'
##print('Generator is starting.')
##输出结果印证，因为r被“赋值”为‘200 OK’，同上，The send() method returns the next value yielded
##by the generator，下次yield将产生‘200 OK’,所以c.send(1)返回‘200 OK’；
##
##不要忘记此时consumer已经停止，produce继续执行，并且r=返回值即200 OK，之后
##print('[PRODUCER] Consumer return: %s' % r)
##
##-----------------------------------------------------------------------------------
##关于consumer中的if not n: return，个人觉得最用仅仅是当出现c.send(0)时，实现generator consumer
##结束（即return），不执行下面的程序，且程序会提示StopIteration。
##其实很合理，生产者为0，消费者则不能消费。
##-----------------------------------------------------------------------------------
##
##最后，协程与子程序（函数）的不同，函数必须等另一个函数return才能向下执行；
##不过协程时（在此例中），consumer的while循环并未结束，produce就可以向下执行了；
##要是consumer为一个函数，那就惨了，因为while true 是个死循环，一直不return，此时producer就无法
##向下执行了


