from .database import Database

class LogicalFormParser:
    def __init__(self, tree):
        if tree is None:
            raise Exception("input None tree!!!")
        if tree.getRoot() is None:
            raise Exception("input None root node!!!")
        self.varCount = {}
        self.tree = tree

    def findEdgeNode(self, node, edgeName):
        if node is None or node.numChildren() == 0: None
        for cnode in node.childrenIter():
            if cnode.edgeType == edgeName:
                return cnode
            lowerResult = self.findEdgeNode(cnode, edgeName)
            if lowerResult is not None: return lowerResult
        return None

    def chooseVarName(self, varType):
        c = varType[0].lower()
        if c < 'a' or c > 'z': c = 'n'
        if c in self.varCount:
            self.varCount[c] += 1
        else:
            self.varCount[c] = 1
        return c + str(self.varCount[c])

    def parseAllChild(self, node):
        if node is None:
            raise Exception("input node is None!!!")
        describe = []
        for cnode in node.childrenIter():
            nodeType = cnode.nodeType()
            nodeName = cnode.nodeName()
            if "<var>" == nodeType[0:5]:
                obj = nodeType[5:].upper()
                nodeName = nodeName.upper()
                varName = self.chooseVarName(nodeName)
                describe.append("({} {} {})".format(obj, varName, nodeName))
            elif "lsubj" == nodeType:
                describe.append("({} {})".format(nodeName.upper(), self.chooseVarName(nodeName)))
            elif "plural" == nodeType:
                describe.insert(0, "PLURAL")
            else:
                describe.append(cnode.nodeName().upper())

            describe.append(self.parseAllChild(cnode))

        if len(describe) == 0: return ""
        return "".join(describe)

    def parseRootBranch(self, node, var):
        if node is None:
            raise Exception("input node is None!!!")
        nodeType = node.nodeType().upper()
        return "({} {} {})".format(nodeType, var, self.parseAllChild(node))

    def parse(self):
        varCount = { 'e': 1 }
        describe = []
        lform = "(∃ e1: (&\n{}\n))"

        rootNode = self.tree.getRoot()
        mainVerbNode = self.findEdgeNode(rootNode, "root")
        if mainVerbNode is None:
            raise Exception("There is no main verb in this tree!\n{}".format(self.tree.printTree()))
        mainVerb = mainVerbNode.nodeName().upper()
        describe.append("({} e1)".format(mainVerb))

        for cnode in mainVerbNode.childrenIter():
            describe.append(self.parseRootBranch(cnode, "e1"))

        return lform.format("    " + ("\n    ").join(describe))

