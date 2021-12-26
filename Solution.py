
Group = {"GROUP_NAME": "No Run Team 9",                   # choose a short name for your group
         "GROUP_MEMBER_1": "Kim JiAn",
         "GROUP_MEMBER_2": "Lee KyuHwan"
         }

from assignment02_student_2.decision_tree import DecisionTree
import pandas as pd
class MRP:

    def __init__(self):
        self._subassemblies = self.subassemblies()
        self._parts = self.parts()
        self.fw = open('submit.txt', 'w')

    def subassemblies(self):

        file = open("subassemblies.txt", 'r')
        sub_name = []
        sub_num = []
        sub_dict = {}
        for line in file:
            words = line.split(',')
            sub_name.append(words[0])
            count = words[1].split('\n')
            sub_num.append(int(count[0]))
        sub_dict['Sub_name'] = sub_name
        sub_dict['Sub_num'] = sub_num

        file.close()
        return pd.DataFrame(sub_dict)
        pass

    def parts(self):

        file = open("parts.txt", 'r')

        parts_full_name = []
        parts_short_name = []
        parts_num = []
        parts_dict = {}

        for line in file:
            words = line.split(',')
            parts_full_name.append(words[0])
            parts_short_name.append(words[1])
            count = words[2].split('\n')
            parts_num.append(int(count[0]))

        parts_dict['Parts_full name'] = parts_full_name
        parts_dict['Parts_num'] = parts_num
        file.close()

        return pd.DataFrame(parts_dict)
        pass

    def boring_order(self, number):
        list1 = [self._subassemblies.loc[3, 'Sub_num'], self._subassemblies.loc[4, 'Sub_num'], self._subassemblies.loc[5, 'Sub_num']]
        # Set Add and procurement
        if number > 6:
            Add = number // 6
            procurement = 2
        else:
            if number == 6:
                Add = 1
            else:
                Add = 0
            procurement = 1

        index = [0,3,6,7,8]
        count = 0

        # ABOUT THE SO4
        SO4 = [self._parts.loc[7, 'Parts_num'], self._parts.loc[8, 'Parts_num']]
        if list1[0] >= number:
            self._subassemblies.loc[3, 'Sub_num'] -= number
        else:
            for i in range(2):
                a = index[-i-1]
                if SO4[-i-1] >= number:
                    self._parts.loc[a, 'Parts_num'] -= (-i+2)*number
                else:
                    if count == 0:
                        self.fw.write('NOT HONOURABLE\nBUYING PARTS FROM SUPPLIERS:\n')
                        count +=1
                    if SO4[-i-1] == 0:
                        self.fw.write('{0}  {1}\n'.format(self._parts.loc[a, 'Parts_full name'], (-i + 2) * number))
                    else:
                        self.fw.write('{0}  {1}\n'.format( self._parts.loc[a, 'Parts_full name'], (-i+2)*number - SO4[-i-1] + procurement))
                        self._parts.loc[a, 'Parts_num'] = procurement
        # ABOUT THE SO5(CWA AND SO6)
        SO6 = [self._parts.loc[0, 'Parts_num'], self._parts.loc[3, 'Parts_num']]
        if list1[1] >= number:
            self._subassemblies.loc[4, 'Sub_num'] -= number
        else:
            cwa = self._parts.loc[6, 'Parts_num']
            if cwa >= number:
                self._parts.loc[6, 'Parts_num'] -= number
            else:
                if count == 0:
                    self.fw.write('NOT HONOURABLE\nBUYING PARTS FROM SUPPLIERS:\n')
                    count +=1
                if cwa != 0:
                    self.fw.write('{0}  {1}\n'.format(self._parts.loc[6, 'Parts_full name'], number - cwa + procurement))
                    self._parts.loc[6, 'Parts_num'] = procurement
                else:
                    self.fw.write('{0}  {1}\n'.format(self._parts.loc[6, 'Parts_full name'], number))

            if list1[2] >= number:
                self._subassemblies.loc[5, 'Sub_num'] -= number
            else:
                for i in range(2):
                    a = index[i]
                    if SO6[i] >= number:
                        self._parts.loc[a, 'Parts_num'] -= number
                    else:
                        if count == 0:
                            self.fw.write('NOT HONOURABLE\nBUYING PARTS FROM SUPPLIERS:\n')
                            count +=1
                        if SO6[i] != 0:
                            self.fw.write('{0}  {1}\n'.format(self._parts.loc[a, 'Parts_full name'], number - SO6[i] + procurement))
                            self._parts.loc[a, 'Parts_num'] = procurement
                        else:
                            self.fw.write('{0}  {1}\n'.format(self._parts.loc[a, 'Parts_full name'],number))
        # CASE OF HONOURABLE
        if count == 0:
            self.fw.write('HONOURABLE\nORDER FOR boringbike,{0} IS COMPLETED\n'.format(number))

        self.fw.write('\n')
        # ADD THE ALL SUB-ASSEMBLIES
        self._subassemblies.loc[3, 'Sub_num'] += Add
        self._subassemblies.loc[4, 'Sub_num'] += Add
        self._subassemblies.loc[5, 'Sub_num'] += Add

        pass

    def cooling_order(self, number):
        list1 = []
        for i in range(4):
            list1.append(self._subassemblies.loc[i, 'Sub_num'])

        index = [1,2,4,5,7,8]

        SO1 = [self._parts.loc[1, 'Parts_num'], self._parts.loc[2, 'Parts_num']]
        SO2 = [self._parts.loc[4, 'Parts_num'], self._parts.loc[5, 'Parts_num']]
        SO4 = [self._parts.loc[7, 'Parts_num'], self._parts.loc[8, 'Parts_num']]
        # SET ADD AND PROCUREMENT
        if number >= 7:
            Add = number // 6
            procurement = 2
        else:
            if number == 6:
                Add = 1
            else:
                Add = 0
            procurement = 1
        count = 0
        # ABOUT SO4
        if list1[3] >= number:
            self._subassemblies.loc[3, 'Sub_num'] -= number
        else:
            for i in range(2):
                a = index[-i-1]
                if SO4[-i-1] >= number:
                    self._parts.loc[a, 'Parts_num'] -= (-i + 2) * number
                else:
                    if count == 0:
                        self.fw.write('NOT HONOURABLE\nBUYING PARTS FROM SUPPLIERS:\n')
                        count += 1
                    if SO4[-1-i] != 0:
                        self.fw.write('{0}  {1}\n'.format(self._parts.loc[a, 'Parts_full name'],(-i + 2) * number - SO4[-i - 1] + procurement))
                        self._parts.loc[a, 'Parts_num'] = procurement
                    else:
                        self.fw.write('{0}  {1}\n'.format(self._parts.loc[a, 'Parts_full name'],(-i + 2) * number))
        # ABOUT S03(CONTAIN SO1 AND SO2)
        if list1[2] >= number:
            self._subassemblies.loc[2, 'Sub_num'] -= number
        else:
            # SO1
            if list1[0] >= number:
                self._subassemblies.loc[0, 'Sub_num'] -= number
            else:
                for i in range(2):
                    a = index[i]
                    if SO1[i] >= number:
                         self._parts.loc[a, 'Parts_num'] -= number
                    else:
                        if count == 0:
                            self.fw.write('NOT HONOURABLE\nBUYING PARTS FROM SUPPLIERS:\n')
                            count += 1
                        if SO1[i] != 0:
                            self.fw.write('{0}  {1}\n'.format(self._parts.loc[a, 'Parts_full name'],number - SO1[i] + procurement))
                            self._parts.loc[a, 'Parts_num'] = procurement
                        else:
                            self.fw.write('{0}  {1}\n'.format(self._parts.loc[a, 'Parts_full name'], number))
            # SO2
            if list1[1] >= number:
                self._subassemblies.loc[1, 'Sub_num'] -= number
            else:
                for i in range(2):
                    a = index[i+2]
                    if SO2[i] >= 2*number:
                        self._parts.loc[a, 'Parts_num'] -= 2*number
                    else:
                        if count == 0:
                            self.fw.write('NOT HONOURABLE\nBUYING PARTS FROM SUPPLIERS:\n')
                            count += 1
                        if SO2[i] != 0:
                            self.fw.write('{0}  {1}\n'.format(self._parts.loc[a, 'Parts_full name'],2*number - SO2[i] + procurement))
                            self._parts.loc[a, 'Parts_num'] = procurement
                        else:
                            self.fw.write('{0}  {1}\n'.format(self._parts.loc[a, 'Parts_full name'],2*number))
        # CASE OF HONOURABLE
        if count == 0:
            self.fw.write('HONOURABLE\nORDER FOR coolbike,{0} IS COMPLETED\n'.format(number))
        # ADD THE ALL SUB-ASSEMBLIES
        self._subassemblies.loc[0, 'Sub_num'] += Add
        self._subassemblies.loc[1, 'Sub_num'] += Add
        self._subassemblies.loc[2, 'Sub_num'] += Add
        self._subassemblies.loc[3, 'Sub_num'] += Add

        self.fw.write('\n')

        pass
    pass
if __name__ == '__main__':
    file = open('order.txt', 'r')
    Bike = MRP()
    for line in file:
        words = line.split(',')
        oreder_num = int(words[1].strip())
        if words[0] == 'boringbike':
            Bike.boring_order(oreder_num)
        else:
            Bike.cooling_order(oreder_num)
    Bike.fw.close()
    file.close()
    pass
