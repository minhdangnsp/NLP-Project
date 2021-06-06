import re

ruleTable = {
    "ROOT": { "đến": "root", "đi": "root", "xuất_phát": "root"},
    "xuất_phát": {"nào": "which-query", "từ": "from-loc", "lúc":"depart-time"},
    "từ": {"thành_phố": "to_loc", "<VAR-LOC>": "<var>name"},
    "đến": { "nào": "which-query", "thành_phố": "to-loc", "lúc": "arrive-time", "<VAR-LOC>": "<var>name"},
    "đi": {"nào": "which-query", "đến": "to-city", "từ": "from-loc", "thời_gian" : "time-query", "xe_bus": "lsubj"},
    "nào": { "xe_bus": "lsubj", "xe": "lsubj", "những": "plural"},
    "xe_bus": {"<VAR-BUS>": "<var>name"},
    "thành_phố": { "<VAR-LOC>": "<var>name" },
    "lúc": { "<VAR-TIM>": "<var>time-hour" },
}

queryTable = {  "BUS": ["B1",
                        "B2",
                        "B3",
                        "B4",
                        "B5",
                        "B6"],
                "ATIME": [
                        "B1 HUE 19:00HR",
                        "B2 HUE 22:30HR",
                        "B3 HUE 20:00HR",
                        "B4 HCMC 18:30HR",
                        "B5 HN 23:30HR",
                        "B6 HN 22:30HR",
                        "B7 HCMC 20:30HR"],
                "DTIME": [
                        "B1 HCMC 10:00HR",
                        "B2 HCMC 14:30HR",
                        "B3 DANANG 16:00HR",
                        "B4 DANANG 8:30HR",
                        "B5 DANANG 5:30HR",
                        "B6 HUE 6:30HR"],
                "RUN-TIME": [
                        "B1 HCMC HUE 9:00HR",
                        "B2 HCMC HUE 8:00HR",
                        "B3 DANANG HUE 4:00HR",
                        "B4 DANANG HCMC 10:00HR",
                        "B5 HUE HN 18:00HR",
                        "B6 HUE DANANG 16:00HR"]
                }
class Database():
    def __init__(self):
            self.bus = False
            self.aTime = None
            self.dTime = None
            self.runTime = None

    def getIndexVar(self, formatVar):
        # print("formatVar = ", formatVar)
        for i, str in enumerate(formatVar):
            if "?" in str:
                return i

    def getTable(self, tableType):
        if tableType == "RUN-TIME":
            return self.runTime
        elif tableType == "DTIME":
            return self.dTime
        elif tableType == "ATIME":
            return self.aTime
        else:
            pass

    def getValueVar(self, tableType):
        # print("tableType = ", tableType)
        # print("self.getTable(tableType) = ", self.getTable(tableType))
        index = self.getIndexVar(self.getTable(tableType))
        # print("index = ", index)
        out = []
        # print("queryTable[tableType]) = ", queryTable[tableType])
        # print("self.getTable(tableType) = ", self.getTable(tableType))
        for indexQuery, query in enumerate(queryTable[tableType]):
            isMatch = True
            # print("query = ", query)
            for i, str in enumerate(self.getTable(tableType)):
                # print("str = ", str)
                if "?" in str:
                    continue
                # print(i)
                # if((re.search(r"(\d+)[hH](\d+)", str))!=None):
                #     str = re.sub("[hH]", ":", str) + "HR"
                    # print("str: ", str)
                # print("str1 = ", str, end=" - ")
                # print("isMatch = ", isMatch, end=" - ")
                if str not in query:
                    # print("haha",end=" - ")
                    isMatch = False
                    break
            # print("isMatch1 = ", isMatch)
            if isMatch is True:
                # print("haha")
                out.append(query.split()[index])
        # print()
        # print("out = ", out)
        return out


    def process(self, queryStr: str):
        # print("queryStrInProcess = ", queryStr)
        querySplit = queryStr.split()
        # print("querySplit = ", querySplit)
        # if len(querySplit) < 11:
        #     raise Exception("Invalid queryStr = {}".format(queryStr))

        for i in range(len(querySplit)):
            if querySplit[i] == "BUS":
                self.bus = True
            elif querySplit[i] == "RUN-TIME":
                self.runTime = querySplit[i+1:i+5]
            elif querySplit[i] == "ATIME":
                self.aTime = querySplit[i+1:i+4]
                # print("self.aTime = ", self.aTime)
            elif querySplit[i] == "DTIME":
                self.dTime = querySplit[i+1:i+4]
        # print("self.aTime = ", self.aTime)
        # print("self.dTime = ", self.dTime)
        out = []
        if self.bus is True:
            out.append(queryTable["BUS"])
        if self.runTime is not None:
            out.append(self.getValueVar("RUN-TIME"))
        if self.aTime is not None:
            out.append(self.getValueVar("ATIME"))
            # print("self.getValueVar(ATIME) = ", self.getValueVar("ATIME"))
        if self.dTime is not None:
            out.append(self.getValueVar("DTIME"))
            # print("self.getValueVar(DTIME) = ", self.getValueVar("DTIME"))
        # print("out = ", out)
        if len(out) == 0:
            return None
        elif len(out) == 1:
            return out[0]
        else:
            tmp = list(set.intersection(*[set(x) for x in out]))
            return None if len(tmp) == 0 else tmp
