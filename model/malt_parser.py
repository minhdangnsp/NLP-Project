from model.stack import Stack
from model.queue import Queue
from model.tree import Tree


# ruleTable = {
#     "ROOT": { "đến": "root", "đi": "root", "xuất_phát": "root"},
#     "xuất_phát": {"nào": "which-query", "từ": "from-loc", "lúc":"depart-time"},
#     "từ": {"thành_phố": "to_loc", "<VAR-LOC>": "<var>name"},
#     "đến": { "nào": "which-query", "thành_phố": "to-loc", "lúc": "arrive-time", "<VAR-LOC>": "<var>name"},
#     "đi": {"nào": "which-query", "đến": "to-city", "từ": "from-loc", "thời_gian" : "time-query", "xe_bus": "lsubj"},
#     "nào": { "xe_bus": "lsubj", "xe": "lsubj", "những": "plural"},
#     "xe_bus": {"<VAR-BUS>": "<var>name"},
#     "thành_phố": { "<VAR-LOC>": "<var>name" },
#     "lúc": { "<VAR-TIM>": "<var>time-hour" },
# }

class MaltParser:
    def __init__(self, relationTable):
        self.relationTable = relationTable

    def __getRelation(self, item1, item2):
        value1 = item1
        value2 = item2
        # print("get relation {} --- {}".format(item1, item2))
        if item1[0:9] in set(("<VAR-LOC>", "<VAR-TIM>", "<VAR-BUS>")):
            value1 = item1[9:]
            # print(f'value1 = {value1}')
            item1 = item1[0:9]
            # print(f'item1 = {item1}')
        if item2[0:9] in set(("<VAR-LOC>", "<VAR-TIM>", "<VAR-BUS>")):
            value2 = item2[9:]
            # print(f'value2 = {value2}')
            item2 = item2[0:9]
            # print(f'item2 = {item2}')

        if item1 not in self.relationTable:
            return None
        if item2 not in self.relationTable[item1]:
            return None
        # print("value1 = {}, value2 = {}, self.relationTable[item1][item2] = {}".format(value1, value2, self.relationTable[item1][item2]))
        return value1, value2, self.relationTable[item1][item2]

    def parse(self, strlst):
        tree = Tree()
        stack = Stack()
        queue = Queue()
        rootWord = None
        if strlst is None or len(strlst) <= 0:
            raise Exception("invalid string list: {}".format(strlst))

        # print(f'strlst = {strlst}')
        for  s in strlst:
            queue.enqueue(s)
        # print("queue - ",queue)
        stack.push("ROOT")
        # print("stack - ", stack)
        while(len(queue) > 0):
            # print("=================================")
            # print(stack)
            # print(queue)
            # print("=================================")
            rItem = queue.getHead()
            lItem = stack.getHead()
            # print("rItem = ", rItem)
            # print("lItem = ", lItem)
            if rItem is None or lItem is None:
                raise Exception("rItem is {} and lItem is {}".format(rItem, lItem))

            larc = self.__getRelation(rItem, lItem)
            if larc is not None:
                tree.pushEdge(*larc)
                stack.pop()
                # a = stack.pop()
                # print("stack after pop = ", a)
                # print("stack --", stack)
                # print("queue -- ", queue)
                # print("*"*50)
                continue

            rarc = self.__getRelation(lItem, rItem)
            if rarc is not None:
                tree.pushEdge(*rarc)
                if "<var>" not in rarc[2]:
                    stack.push(queue.dequeue())
                    if rarc[2] == "root":
                        # print("Root ======= ")
                        rootWord = rItem
                else:
                    queue.dequeue()
                # print("stack --", stack)
                # print("queue -- ", queue)
                # print("*"*50)
                continue

            if rootWord is not None:
                # print("Root is not none hear ========")
                rootRelation = self.__getRelation(rootWord, rItem)
                if rootRelation is not None:
                    while len(stack) > 2:
                        stack.pop()
                    tree.pushEdge(*rootRelation)
                    stack.push(queue.dequeue())
                    # print("stack --", stack)
                    # print("queue -- ", queue)
                    # print("*"*50)
                    continue

            stack.push(queue.dequeue())
            # print("stack --", stack)
            # print("queue -- ", queue)
            # print("*"*50)
        return tree

# strlst = ['xe_bus', 'nào', 'đến', 'thành_phố', '<VAR-LOC>huế', 'lúc', '<VAR-TIM>20:00hr']
# parser = MaltParser(ruleTable).parse(strlst)
# print('+'*50)
# parser.printTree()
# for i in parser.getTree():
#     print(i)