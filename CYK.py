# CYK Algorithm
# Parsing from CNF File to make check whether a strings is accepted by CFL

import argparse
import Converter

class Node:
    def __init__(self, symbol, child1, child2=None):
        self.symbol = symbol
        self.child1 = child1
        self.child2 = child2

    def __repr__(self):
        return self.symbol

class Parser:
    def __init__(self, grammar):
        self.parse_table = None
        self.prods = {}
        self.grammar = None
        self.grammerFile(grammar)
    def __call__(self, sentence, parse=False):
        self.input = sentence.split()
        if parse:
            self.parsing()
    def grammerFile(self,grammar):
        self.grammar = Converter.convert_grammar(Converter.read_grammar(grammar))
    def parsing(self):
        length = len(self.input)
        if length > 0:
            self.parse_table = [[[] for i in range(length - j)] for j in range(length)]
            for x, word in enumerate(self.input):
                for rule in self.grammar:
                    if f"'{word}'" == rule[1]:
                        self.parse_table[0][x].append(Node(rule[0], word))
            for words in range(2, length+1):
                for cell in range(0, length - words + 1):
                    for leftSize in range(1, words):
                        rightSize = words - leftSize
                        leftCell = self.parse_table[leftSize - 1][cell]
                        rightCell = self.parse_table[rightSize - 1][cell + leftSize]
                        for rule in self.grammar:
                            left_nodes = [n for n in leftCell if n.symbol == rule[1]]
                            if left_nodes:
                                right_nodes = [n for n in rightCell if n.symbol == rule[2]]
                                self.parse_table[words - 1][cell].extend(
                                    [Node(rule[0], left, right) for left in left_nodes for right in right_nodes]
                                )

    def print_tree(self, output = True):
        start_symbol = "S"
        if (len(self.input) == 0) :
            if output:
                print("It is Empty")
            return True
        else:
            final_nodes = [i for i in self.parse_table[-1][0] if i.symbol == start_symbol]
            if final_nodes:
                if output:
                    print("Parse yang memungkinkan adalah: \n")
                    write_trees = [generate_tree(node) for node in final_nodes]
                    for tree in write_trees:
                        print(tree)
                if output:
                    output_trees = [generate_tree(node) for node in final_nodes]
                    for tree in output_trees:
                        print(tree) 
                    return True
                else:
                    return True
            else:
                if output:
                    print("Sentence tidak berisi language yang dihasilkan Grammar")
                return False

def generate_tree(node):
    if node.child2 is None:
        return f"[{node.symbol} '{node.child1}']"
    return f"[{node.symbol} {generate_tree(node.child1)} {generate_tree(node.child2)}]"

if __name__ == '__main__' :
    parser = argparse.ArgumentParser()
    parser.add_argument("grammar")
    parser.add_argument("sentence")
    args = parser.parse_args()
    CYK = Parser(args.grammar, args.sentence)
    CYK.parsing()
    CYK.print_tree()