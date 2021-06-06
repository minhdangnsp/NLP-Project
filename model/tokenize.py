import re

combineWordTable = {
                    'xe bus': 'xe_bus',
                    'thành phố': 'thành_phố',
                    'thời gian': 'thời_gian',
                    'đà nẵng': '<VAR-LOC>đà_nẵng',
                    'hồ chí minh': '<VAR-LOC>hồ_chí_minh',
                    'hà nội': '<VAR-LOC>hà_nội',
                    'xuất phát': 'xuất_phát',
                    'huế': '<VAR-LOC>huế',
                    'b1': '<VAR-BUS>B1',
                    'b2': '<VAR-BUS>B2',
                    'b3': '<VAR-BUS>B3',
                    'b4': '<VAR-BUS>B4',
                    'b5': '<VAR-BUS>B5',
                    'b6': '<VAR-BUS>B6'}

class Tokenize:
    def __init__(self, str):
        self._str = str
        self.unsignStr = ""

    def parse(self):
        output = self._str.lower()

        #remove '?'
        if output.find('?')>=0:
            output = output.replace('?',' ')
        output = output.strip()

        for word in combineWordTable:
            output = output.replace(word, combineWordTable[word])

        #check 20H30
        hour = re.search("(\d+)\:(\d+)", output)

        if hour is not None:
            output = output[:hour.start()] + "<VAR-TIM>"+output[hour.start():hour.end()] + output[hour.end():]

        output = output.split()
        return output



# str = "Xe bus nào đến thành phố Huế lúc 20:00HR?"
# t1 = Tokenize(str).parse()
# print(t1)
# print(Tokenize("Những xe nào xuất phát từ thành phố Hồ Chí Minh ?").parse())
