from .database import Database

class QueryLogic:
    def __init__(self, tree):
        if tree is None:
            raise Exception("input None tree!!!")
        if tree.getRoot() is None:
            raise Exception("input None root node!!!")
        # print("parse logical form for tree:\n{}".format(tree.printTree()))
        self.tree = tree
        self.fromLocation = None
        self.toLocation = None
        self.fromTime = None
        self.toTime = None
        self.busName = None
        self.queryFunc = None
        self.queryTheme = None
        self.pluralQuery = False

    def findEdgeNode(self, node, edgeName):
        if node is None or node.numChildren() == 0: None
        for cnode in node.childrenIter():
            if cnode.edgeType == edgeName:
                return cnode
            lowerResult = self.findEdgeNode(cnode, edgeName)
            if lowerResult is not None: return lowerResult
        return None

    def getFromLoc(self):
        rootNode = self.tree.getRoot()
        fromToNode = self.findEdgeNode(rootNode, "from-loc")
        if fromToNode is None:
            return None
        nameNode = self.findEdgeNode(fromToNode, "<var>name")
        if nameNode is None:
            raise Exception("<var>name not exist while from-loc node is represent")
        return nameNode.nodeName()

    def getToLoc(self):
        rootNode = self.tree.getRoot()
        toToNode = self.findEdgeNode(rootNode, "to-loc")
        if toToNode is None:
            toToNode = self.findEdgeNode(rootNode, "to-city")
            if toToNode is None:
                return None
        nameNode = self.findEdgeNode(toToNode, "<var>name")
        if nameNode is None:
            raise Exception("<var>name not exist while to-loc node is represent")
        return nameNode.nodeName()

    def getBusName(self):
        rootNode = self.tree.getRoot()
        busToNode = self.findEdgeNode(rootNode, "lsubj")
        if busToNode is None:
            return None
        nameNode = self.findEdgeNode(busToNode, "<var>name")
        if nameNode is None:
            # print("[WARN] <var>name not exist while lsubj node is represent")
            return None
        return nameNode.nodeName()

    def getToTime(self):
        rootNode = self.tree.getRoot()
        toTimeToNode = self.findEdgeNode(rootNode, "arrive-time")
        if toTimeToNode is None:
            return None
        nameNode = self.findEdgeNode(toTimeToNode, "<var>time-hour")
        if nameNode is None:
            raise Exception("<var>time-hour not exist while arrive-time node is represent")
        return nameNode.nodeName()

    def getFromTime(self):
        rootNode = self.tree.getRoot()
        fromTimeToNode = self.findEdgeNode(rootNode, "depart-time")
        if fromTimeToNode is None:
            return None
        nameNode = self.findEdgeNode(fromTimeToNode, "<var>time-hour")
        if nameNode is None:
            raise Exception("<var>time-hour not exist while depart-time node is represent")
        return nameNode.nodeName()

    def getQueryTheme(self):
        rootNode = self.tree.getRoot()
        queryToNode = self.findEdgeNode(rootNode, "which-query")
        if queryToNode is not None:
            lsubjNode = self.findEdgeNode(queryToNode, "lsubj")
            if lsubjNode is None: raise Exception("does not know which subject to query!!!")
            return "print-all", lsubjNode.nodeName(), True
        queryToNode = self.findEdgeNode(rootNode, "time-query")
        if queryToNode is not None:
            return "find-the", "time", False
        return None

    def parse(self):
        self.fromLocation = self.getFromLoc()
        self.toLocation = self.getToLoc()
        self.busName = self.getBusName()
        self.toTime = self.getToTime()
        self.fromTime = self.getFromTime()
        self.queryFunc, self.queryTheme, self.pluralQuery = self.getQueryTheme()

    def getCityCode(self, name):
        table = {
            "đà_nẵng": "DANANG",
            "hồ_chí_minh": "HCMC",
            "huế": "HUE",
        }
        return table[name]

    def produceQuery(self):
        pattern = "( {} ?x {} )"
        if self.queryTheme == "time":
            return pattern.format(self.queryFunc.upper(), "( {} {} {} {} {} )".format(
                "RUN-TIME",
                self.busName,
                self.getCityCode(self.fromLocation),
                self.getCityCode(self.toLocation),
                "?x"
                )
            )
        else:
            describe = []
            describe.append("( BUS ?x )")
            # if self.fromLocation is not None:
            #     describe.append("( {} {} {} {} )".format(
            #         "DTIME",
            #         "?x",
            #         self.getCityCode(self.fromLocation),
            #         "?t"
            #     ))
            if self.fromLocation is not None or self.fromTime is not None:
                time = "?t"
                if self.fromTime is not None:
                    time = self.fromTime.upper()
                describe.append("( {} {} {} {} )".format(
                    "DTIME",
                    "?x",
                    self.getCityCode(self.fromLocation),
                    time
                ))
            if self.toLocation is not None or self.toTime is not None:
                location = "?l"
                if self.toLocation is not None:
                    location = self.getCityCode(self.toLocation)
                time = "?t"
                if self.toTime is not None:
                    time = self.toTime.upper()

                describe.append("( {} {} {} {} )".format(
                    "ATIME",
                    "?x",
                    location,
                    time
                ))
        return pattern.format(self.queryFunc.upper(), "( {} )".format(" ".join(describe)))


    def answer(self, queryStr):
        return Database().process(queryStr)

    def produceProceduralSemantic(self):
        var = "x1"
        if self.queryFunc is None or self.queryTheme is None:
            raise Exception("cannot identify a question!!!")
        func = self.queryFunc.upper()

        return "({} ?{})"