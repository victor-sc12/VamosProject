import openpyxl
import json
import re

class ProcessData:
    def __init__(self, docxl1, docxl2):
        # activar data de xl para su manipulación con openpyxl:
        self.docxl1, self.docxl2 = openpyxl.load_workbook(docxl1).active, openpyxl.load_workbook(docxl2).active
        
        # obtener dataframe xl en json y como una lista de diccionarios. Además definimos headers de cada dtfr:
        self.header1, self.jsondata1, self.dictdata1  = self.data_convert(self.docxl1)
        self.header2, self.jsondata2, self.dictdata2 = self.data_convert(self.docxl2)

        # definir una lista de diccionarios con bnc como key y otro dict como value con respectivo bnc y bn:
        self.cut_airDict, self.bnc_air, self.bn_air = self.cut_dict(self.dictdata1, 'booking_number_carrier', 'booking_number')
        self.cut_novoDict, self.bnc_novo, self.bn_novo = self.cut_dict(self.dictdata2, 'C', 'AA')

    @staticmethod
    def data_convert(dataframe):
        datajsonlist = []
        datadictlist = []
        headers = [cell.value for cell in dataframe[1]]         
        
        for row in range(1, dataframe.max_row):
            dict = {}
            for col, h in zip(dataframe.iter_cols(1, dataframe.max_column), headers):
                dict[h] = col[row].value
            datadictlist.append(dict)
            jsonelement = json.dumps(dict, indent=3, default=str)
            datajsonlist.append(jsonelement)

        return headers, datajsonlist, datadictlist
    

    @staticmethod
    def cut_dict(dict_data, bnc_header, bn_header):
        new_data_dict = {}
        bnc_list = []
        bn_list = []
        pattern = r'\bVA[A-Z0-9]{6}\b' # Patrón que permitirá identificar y definir adecuadamente los bn
        
        # En el siguiente bucle se esta definiendo una lista de diccionarios iterados, en donde la parte importante a recalcar
        # es que el 'bn' se ubicara adecuadamente en caso de que sean substring de un string:
        for dic in dict_data:
            bn_value = dic[bn_header]
            matched_bn = re.search(pattern, bn_value)  # Buscar coincidencia con el patrón

            bnc = dic[bnc_header]
            bn = matched_bn.group() if matched_bn else None  # Asignar valor o None

            # Asignar bnc y bn a una lista:
            bnc_list.append(bnc), bn_list.append(bn)

            # Definir elementos de diccionario iterado:
            new_dict = {bnc: {'bnc': bnc, 'bn': bn}}
            new_data_dict.update(new_dict)

            # redifinir la lista de bnc por si hay mas de uno compartiendo una misma casilla:
            bnc_list = [e.strip() for v in bnc_list for e in v.split('/')]
        
        return new_data_dict, bnc_list, bn_list

    
# pd = ProcessData("TransEsmeraldas_Airtable_Feb2025_t.xlsx", "TransEsmeraldas_Novo_Feb2025_t.xlsx")
# print(pd.cut_airDict)
# print(pd.bnc_novo)
# print(pd.bn_novo)