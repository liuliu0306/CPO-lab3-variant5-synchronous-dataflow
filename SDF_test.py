# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 10:35:53 2022

@author: liurh
"""

import unittest
from hypothesis import given, settings
import hypothesis.strategies as st
from SDF import SDF, Node


class SDFTest(unittest.TestCase):
    def test_execute(self):
        # Test_execute provides two SDF cases and
        # verifies the correctness of the final result.
        case1 = SDF('case1')

        case1.add_node('root1', lambda x: None)
        case1.add_node('root2', lambda x: None)
        case1.add_node('end', lambda x: None)
        case1.add_node('A_square', lambda x: x**2)
        case1.add_node('B_square', lambda x: x**2)
        case1.add_node('C_add', lambda x, y: x+y)

        case1.add_token('root1', 'A_square', [1, 2, 3])
        case1.add_token('root2', 'B_square', [4, 5, 6])
        case1.add_token('A_square', 'C_add', [])
        case1.add_token('B_square', 'C_add', [])
        case1.add_token('C_add', 'end', [])

        case1.execute()

        # Finall result is [1,2,3]**2 + [4,5,6]**2 = [17,29,45]
        for inx, edge in enumerate(case1.token_vec):
            if 'end' in edge[1]:
                self.assertEqual(edge[2], [17, 29, 45])

        case2 = SDF('case2')
        case2.add_node('root1', lambda x: None)
        case2.add_node('end', lambda x: None)
        case2.add_node('A_cube', lambda x: x**3)

        case2.add_token('root1', 'A_cube', [2, 3, 4])
        case2.add_token('A_cube', 'end', [])
        case2.execute()

        # Finall result is [2,3,4]**3 = [8,27,64]
        for inx, edge in enumerate(case2.token_vec):
            if 'end' in edge[1]:
                self.assertEqual(edge[2], [8, 27, 64])

    def test_add_node(self):
        sdf = SDF('add_node')
        sdf.add_node('node1', lambda x: None)
        self.assertEqual(sdf.nodes.pop().name, 'node1')

    def test_add_token(self):
        sdf = SDF('add_token')
        sdf.add_node('node1', lambda x: None)
        sdf.add_node('node2', lambda x: None)
        sdf.add_token('node1', 'node2', [])
        self.assertEqual(sdf.token_vec, [['node1', 'node2', []]])

    def test_if_fire(self):
        sdf = SDF('_if_fire')
        sdf.add_node('node1', lambda x: x)
        sdf.add_node('node2', lambda x: x)
        sdf.add_token('node1', 'node2', [1, 2, 3])
        self.assertEqual(sdf._if_fire('node1'), False)
        self.assertEqual(sdf._if_fire('node2'), True)

    def test_update_fire(self):
        sdf = SDF('_update_fire')
        sdf.add_node('node1', lambda x: x)
        sdf.add_node('node2', lambda x: x)
        sdf.add_token('node1', 'node2', [1, 2, 3])
        sdf._update_fire()
        self.assertEqual(sdf.if_fire_vec, [False, True])

    def test_get_data_from_token_vec(self):
        sdf = SDF('_update_fire')
        sdf.add_node('node1', lambda x: x)
        sdf.add_node('node2', lambda x: x)
        sdf.add_token('node1', 'node2', [1, 2, 3])
        data = sdf._get_data_from_token_vec(sdf.nodes[1])
        self.assertEqual(data, [1])

    def test_update_token_vec(self):
        sdf = SDF('_update_fire')
        sdf.add_node('node1', lambda x: x)
        sdf.add_node('node2', lambda x: x)
        sdf.add_token('node1', 'node2', [1, 2, 3])
        sdf._update_token_vec(sdf.nodes[0], 4)
        self.assertEqual(sdf.token_vec,
                         [['node1', 'node2', [1, 2, 3, 4]]])

    # PBT test: input graph
    @settings(max_examples=100)
    @given(st.lists(st.integers()),
           st.lists(st.integers()))
    def test_graph_PBT(self, a, b):
        target = '''\n
digraph G {'''+f'''
 rankdir=LR;
 root1[shape=rarrow];
 root1 -> n_0;
 root2[shape=rarrow];
 root2 -> n_1;
 end[shape=rarrow];
 n_3 -> end;
 n_0[label="root1"];
 n_1[label="root2"];
 n_2[label="add"];
 n_3[label="end"];
 n_0 -> n_2[label="{a}"];
 n_1 -> n_2[label="{b}"];
 n_2 -> n_3[label="[]"];
'''+'''}'''

        sdf = SDF('SDF')
        sdf.add_node('root1', lambda x: x)
        sdf.add_node('root2', lambda x: x)
        sdf.add_node('add', lambda x, y: x + y)
        sdf.add_node('end', lambda x: x)
        sdf.add_token('root1', 'add', a)
        sdf.add_token('root2', 'add', b)
        sdf.add_token('add', 'end', [])

        sdf.visualize(0)
        path = f'./figure/{sdf.name}-0.dot'
        with open(path) as f:
            dot_graph = f.read()
        self.assertEqual(dot_graph, target)

    # Additional cases
    @settings(max_examples=100)
    @given(st.lists(st.integers()), \
           st.lists(st.integers()))
    def test_SDF_PBT(self, a, b):
        a_cp = a.copy()
        b_cp = b.copy()
        sdf = SDF('SDF')
        sdf.add_node('root1', lambda x: x)
        sdf.add_node('root2', lambda x: x)
        sdf.add_node('add', lambda x, y: x + y)
        sdf.add_node('end', lambda x: x)

        sdf.add_token('root1', 'add', a)
        sdf.add_token('root2', 'add', b)
        sdf.add_token('add', 'end', [])
        sdf.execute()

        res = []
        res_a = []
        res_b = []
        len_a, len_b = len(a_cp), len(b_cp)
        min_len = min(len_a, len_b)

        if (len_a > 0) & (len_b > 0):
            for ri in range(min_len):
                res.append(a_cp[ri] + b_cp[ri])
            res_a, res_b = a_cp[min_len:], b_cp[min_len:]
        else:
            res_a, res_b = a_cp, b_cp

        # test token
        self.assertEqual(
            sdf.token_vec, \
            [['root1', 'add', res_a],
              ['root2', 'add', res_b],
              ['add', 'end', res]])


class NodeTest(unittest.TestCase):

    def test_Node(self):
        def operator(x):
            return x**2
        name = 'test_node_1'
        node = Node(name, operator)
        self.assertEqual(node.name, name)
        self.assertEqual(node.operator, operator)

    def test_operator(self):
        def operator(x):
            return x**2
        name = 'test_node_2'
        node = Node(name, operator)
        _input = 5
        _output = node.operator(_input)
        self.assertEqual(25, _output)


if __name__ == '__main__':
    unittest.main()
