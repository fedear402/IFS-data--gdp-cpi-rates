import requests
import pandas as pd
import os
import json

with open('refcodes.json', 'r') as ref:
    ref_codes = json.load(ref)

url = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/'
startdate = 1950
enddate = 2022


# {Method}/{Series}/{Frequency}.{Area}.{Indicator}.{Date Range}
# ejemplo con SA : http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/IFS/Q.SA.NGDP_R_SA_XDC.?startPeriod=1900&endPeriod=2023


codes = ['NGDP_R_NSA_XDC', 'FPOLM_PA', 'NGDP_R_SA_XDC', 'FIDR_PA', 'PCPI_IX' ]
# 'FPOLM_PA', 'NGDP_R_SA_XDC', 'FIDR_PA', 
# ['NGDP_D_IX',
# 'NGDP_D_SA_IX',
# 'NGDP_XDC',
# 'NGDP_SA_XDC',
# 'NGDP_NSA_XDC',
# 'NGDP_R_XDC',
# 'NGDP_R_SA_XDC',
# 'NGDP_R_NSA_XDC']


keys={}
for ref_code, country in ref_codes.items():
    for c in codes:
        keys[f'{c} para {country}']=(f'CompactData/IFS/Q.{ref_code}.{c}.?startPeriod={startdate}&endPeriod={enddate}')


def main():
    result = {p:{} for p in ref_codes.values()}
    for c, k in keys.items():
        pais = c.split(' para ')[1]
        base = c.split(' para ')[0]
        # print(url, k, requests.get(f'{url}{k}').json()['CompactData']['DataSet']['Series'])
        try:
            print('ENTRA', pais, base)
            data = requests.get(f'{url}{k}').json()['CompactData']['DataSet']['Series']

            df = pd.DataFrame([[obs.get('@TIME_PERIOD'), obs.get('@OBS_VALUE')]for obs in data['Obs']], columns=['per', 'val'])
            
            dir = f'IFS/{pais}'
            if not os.path.exists(dir):
                os.makedirs(dir)
            
            df.to_excel(f'{dir}/{c}.xlsx')
            
            result[pais][base] = f"{data['Obs'][0]['@TIME_PERIOD'].split('-')[0]} - {data['Obs'][-1]['@TIME_PERIOD'].split('-')[0]}"
            print('Llega aca')

            print( f"SI hay datos de {c} desde {data['Obs'][0]['@TIME_PERIOD']} hasta {data['Obs'][-1]['@TIME_PERIOD']}" )
            print('SALE', pais, base)
        except:
            result[pais][base] = None
            print(f'NO hay datos de {c}')

    
    return result
 
pd.DataFrame(  main() ).transpose().to_excel('disponibilidad.xlsx')
