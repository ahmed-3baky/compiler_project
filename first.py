from graphviz import Digraph

dot = Digraph(comment='Grammar', format='png')

dot.attr(rankdir='LR')

dot.node('program', '<program>')
dot.node('statement', '<statement>')
dot.node('assignment', '<assignment>')
dot.node('expression', '<expression>')
dot.node('term', '<term>')
dot.node('factor', '<factor>')
dot.node('control_flow', '<control_flow>')
dot.node('loop', '<loop>')

dot.node('identif', '<identif>')
dot.node('number', '<number>')
dot.node('letter', '<letter>')
dot.node('digit', '<digit>')
dot.node('range', '<range>')

dot.edge('program', 'statement')

dot.edge('statement', 'assignment')
dot.edge('statement', 'expression')
dot.edge('statement', 'control_flow')
dot.edge('statement', 'loop')

dot.edge('assignment', 'identif', label='identif')
dot.edge('assignment', 'expression', label='= expression')

dot.edge('expression', 'term', label='term')
dot.edge('expression', 'term', label='+|-')

dot.edge('term', 'factor', label='factor')
dot.edge('term', 'factor', label='*|/')

dot.edge('factor', 'number', label='number')
dot.edge('factor', 'identif', label='identif')
dot.edge('factor', 'expression', label='(expression)')

dot.edge('control_flow', 'begin')
dot.edge('control_flow', 'if')
dot.edge('control_flow', 'logic_expression')
dot.edge('control_flow', 'then')
dot.edge('control_flow', 'program')
dot.edge('control_flow', 'elif')
dot.edge('control_flow', 'program')
dot.edge('control_flow', 'else')
dot.edge('control_flow', 'program')
dot.edge('control_flow', 'end')

dot.edge('loop', 'for_loop')
dot.edge('loop', 'nested_for_loop')

dot.node('for_loop', '<for_loop>')
dot.edge('for_loop', 'identif', label='identif')
dot.edge('for_loop', 'range', label='in range')
dot.edge('for_loop', 'program', label='do program')

dot.node('nested_for_loop', '<nested_for_loop>')
dot.edge('nested_for_loop', 'identif', label='identif')
dot.edge('nested_for_loop', 'range', label='in range')
dot.edge('nested_for_loop', 'for_loop', label='do nested_for_loop')

dot.edge('range', 'number', label='number')
dot.edge('range', 'number', label='to')

with dot.subgraph() as s:
    s.attr(rank='same')
    s.node('identif')
    s.node('number')
    s.node('letter')
    s.node('digit')

dot.render('grammar_output', view=True)
