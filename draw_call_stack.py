import sys
from pygraphviz import AGraph

# ordinal_dict={1:'first',
#               2:'second',
#               3:'third',
#               4:'fourth',
#               5:'fifth',
#               6:'sixth',
#               7:'seventh',
#               8:'eighth',
#               9:'ninth',
#               10:'tenth'
#             }

def outer():
    G = AGraph(strict=False, directed=True)

    def cheese():
        stack = []
        frame = sys._getframe().f_back
        while frame:
            file_name = frame.f_code.co_filename
            function_name = frame.f_code.co_name
            line_number = frame.f_code.co_firstlineno
            node ='{0}:{1}:{2}'.format(file_name, function_name, line_number)
            if not G.has_node(node):
                if not G.get_subgraph('cluster'+file_name):
                    G.add_subgraph(name='cluster'+file_name,
                                   label=file_name)
                subgraph = G.get_subgraph('cluster'+file_name)
                subgraph.add_node(node, label='{}:{}'.format(line_number, function_name))
            stack.append(frame)
            frame = frame.f_back
        stack.reverse()

        for index, start in enumerate(stack):
            if index+1 < len(stack):
                start_file = start.f_code.co_filename
                start_function = start.f_code.co_name
                start_lineno = start.f_code.co_firstlineno

                end = stack[index+1]
                end_file = end.f_code.co_filename
                end_function = end.f_code.co_name
                end_lineno = end.f_code.co_firstlineno

                if index == 0:
                    color = 'red'
                elif index == len(stack)-2:
                    color = 'blue'
                else:
                    color = 'black'

                start_node = '{0}:{1}:{2}'.format(start_file, start_function, start_lineno)
                end_node = '{0}:{1}:{2}'.format(end_file, end_function, end_lineno)

                if not G.has_edge(start_node, end_node):
                    G.add_edge(start_node, end_node,
                               color=color,
                               label='#{0} at {1}'.format(index+1, start.f_lineno)
                              )
                elif G.get_edge(start_node, end_node).attr['label'] !='#{0} at {1}'.format(index+1, start.f_lineno):
                     G.add_edge(start_node, end_node,
                               color=color,
                               label=(G.get_edge(start_node, end_node).attr['label']+'\n'+
                                     '#{0} at {1}'.format(index+1, start.f_lineno))
                               )
        G.draw('test.png', prog='dot')
        return G

    return cheese



