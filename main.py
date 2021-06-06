from model.tokenize import Tokenize
import model.database
from model.malt_parser import MaltParser
from model.logical_form_generator import LogicalFormParser
from model.query_logic import QueryLogic
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cau", required=True, help='Câu b, c, d')
    args = parser.parse_args()

    questions = []
    with open("./input/input.txt", "r", encoding="utf-8") as lq:
        for question in lq:
            questions.append(question)
    out = []
    for question in questions:
        string = Tokenize(question).parse()
        parser = MaltParser(model.database.ruleTable)
        tree = parser.parse(string)
        query = QueryLogic(tree)
        query.parse()

        if args.cau == "d":
            logical = LogicalFormParser(tree)
            out.append(logical.parse())
        elif args.cau == "e":
            out.append(query.produceQuery())
        elif args.cau == "f":
            out.append(query.answer(query.produceQuery()))
        elif args.cau == "b":
            tree.printTree()
            out.append("\n".join(tree.getTree()))
        else:
            raise Exception("Don't support cau = {}".format(args.cau))

        outputFile = './output/output_{}.txt'.format(args.cau)
        with open(outputFile, "w", encoding="utf-8") as fp:
            for q, r in zip(questions, out):
                fp.writelines(q + "\n")
                fp.writelines(str(r) + "\n\n")



if __name__ =="__main__":
    main()


"""
print("câu b:")
string = "Thời gian xe bus B3 đi từ Đà Nẵng đến Huế?"
# string = "Xe bus nào đến thành phố Hồ Chí Minh"
# string = "Xe bus nào đến thành phố Huế lúc 20:00HR"
strlst = Tokenize(string).parse()
print(strlst)
parser = MaltParser(model.database.ruleTable).parse(strlst)
parser.printTree()
for i in parser.getTree():
    print(i)

print("câu c:")
print(LogicalFormParser(parser).parse())

print("Câu d:")
query = QueryLogic(parser)
query.parse()
print(query.produceQuery())

print("Câu e:")
print(query.answer(query.produceQuery()))

"""






# string = "Thời gian xe bus B3 đi từ Đà Nẵng đến Huế?"
# string = "Xe bus nào đến thành phố Hồ Chí Minh"
# string = "Xe bus nào đến thành phố Huế lúc 20:00HR"

#câu a và b
# strlst = Tokenize(string).parse()
# print(strlst)
# parser = MaltParser(model.database.ruleTable).parse(strlst)
# parser.printTree()
# for i in parser.getTree():
#     print(i)

#câu logicalform
# strlst = Tokenize(string).parse()
# parser = MaltParser(model.database.ruleTable)
# tree = parser.parse(strlst)
# print(LogicalFormParser(tree).parse())

#câu query logic
# strlst = Tokenize(string).parse()
# parser = MaltParser(model.database.ruleTable)
# tree = parser.parse(strlst)
# tree.printTree()
# for i in tree.getTree():
#     print(i)
# query = QueryLogic(tree)
# query.parse()
# print(query.answer(query.produceQuery()))
# print(query.produceQuery())


