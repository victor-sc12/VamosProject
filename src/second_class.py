import pandas as pd
from first_class import ProcessData

class CompareData:
    def __init__(self):
        # instancia de objeto ProcessData:
        pd = ProcessData("TransEsmeraldas_Airtable_Feb2025_t.xlsx", "TransEsmeraldas_Novo_Feb2025_t.xlsx")
        
        # validar bnc duplicados en ambos archivos y obtener lista sin duplicados:
        self.dup_airtable, self.bcn_airtable = self.duplicates(pd.bnc1)  
        self.dup_novo, self.bcn_novo = self.duplicates(pd.bnc2)

        # compare de datos:
        self.data_match, self.not_in_novo, self.not_in_air, self.unmatch_data = self.data_compare()

        # dataframe ?:
        self.air_dataframe = self.ubicar_dataframe(self.bcn_airtable, pd.cut_dictdata1) 
        self.novo_dataframe = self.ubicar_dataframe(self.bcn_novo, pd.cut_dictdata2)

    @staticmethod
    def duplicates(dic_data):
        _set = set()
        dup = []

        
        for d in data:
            if d in _set:
                dup.append(d)
            else:
                _set.add(d)
        
        data = list(set(data))

        if not dup:
            return False, data
        else:
            return dup, data
        

    def data_compare(self):
        match_data = list(set(self.bcn_airtable) & set(self.bcn_novo))
        match_data.sort()

        # Bnc contenidos en conciliaciones de Airtable y Novo que no hicieron mathc (los sobrantes, en pocas): 
        unmatch_AirData = [v for v in self.bcn_airtable if v not in match_data]
        unmatch_NovoData = [v for v in self.bcn_novo if v not in match_data]

        unmatch_bnc = unmatch_AirData + unmatch_NovoData # todos los bcn que no hicieron match

        # Air's bnc no incluidos en Novo's bcn y viceversa:
        not_in_novo = [v for v in self.bcn_airtable if v not in self.bcn_novo] # bnc de air que no estan en novo
        not_in_airtable = [v for v in self.bcn_novo if v not in self.bcn_airtable] # bnc de novo que no estan en air

        return match_data, not_in_novo, not_in_airtable, unmatch_bnc
    
    @staticmethod
    def ubicar_dataframe(bnc_list, bnc_dict):
        bnc_dtfr = []
        bn_dtfr = []
        for bnc in bnc_list:
            for dic in bnc_dict: 
                if bnc == dic[bnc] or bnc in dic[bnc]:
                    bnc_dtfr.append(dic['bnc']), bn_dtfr.append(dic['bn'])
                    break

        dataframe = {'bnc': bnc_dtfr, 'bn': bn_dtfr}
        return dataframe

    
class DeployData():
    def __init__(self):
        cd = CompareData()
        

cpr = CompareData()
# print(cpr.dup, cpr.nodup)
# print(cpr.dup_airtable, cpr.dup_novo)
# print(cpr.data_match)
# print(cpr.not_in_air)
# print(cpr.not_in_novo)
# print(cpr.unmatch_data)
print(cpr.novo_dataframe)