import pandas as pd
from first_class import ProcessData

class CompareData:
    def __init__(self):
        # instancia de objeto ProcessData:
        pd = ProcessData("TransEsmeraldas_Airtable_Feb2025_t.xlsx", "TransEsmeraldas_Novo_Feb2025_t.xlsx")
        
        # validar bnc duplicados en ambos archivos y obtener lista sin duplicados:
        self.dup_airtable, self.bcn_airtable = self.duplicates(pd.bnc_air)  
        self.dup_novo, self.bcn_novo = self.duplicates(pd.bnc_novo)

        # compare de datos:
        self.data_match, self.not_in_novo, self.not_in_air, self.unmatch_data = self.data_compare()

        # dataframe ?:
        self.dta = self.ubicar_dataframe(self.bcn_airtable, pd.cut_airDict)

    @staticmethod
    def duplicates(data):
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
        values_list = []
        bnc_values = []
        bn_values = []
        for key in bnc_dict:
            if key in bnc_list:
                bnc_values.append(bnc_dict[key]['bnc']), bn_values.append(bnc_dict[key]['bn'])
        dataframe = {'bnc': bnc_values, 'bn': bn_values} 
        return dataframe

    
class DeployData():
    def __init__(self):
        cd = CompareData()
        

cpr = CompareData()
print(pd.DataFrame(cpr.dta))