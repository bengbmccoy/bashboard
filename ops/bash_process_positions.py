
import pandas as pd

player_ids = [
'00-0033530',
'00-0033164',
'00-0028118',
'00-0031953',
'00-0033471',
'00-0033705',
'00-0033696',
'00-0035125',
'00-0035120',
'00-0034319',
'00-0033094',
'00-0027691',
'00-0030533',
'00-0034386',
'00-0034487',
'00-0035527',
'00-0030089',
'00-0026544',
'00-0032986',
'00-0035006',
'00-0031319',
'00-0033681',
'00-0031431',
'00-0035726',
'00-0032945',
'00-0035399',
'00-0033111',
'00-0035298',
'00-0027891',
'00-0032320',
'00-0034631',
'00-0028064',
'00-0032144',
'00-0034959',
'00-0032540',
'00-0034073',
'00-0035645',
'00-0032951',
'00-0034414',
'00-0033080',
'00-0028292',
'00-0034772',
'00-0032398',
'00-0030443',
'00-0035235',
'00-0034788',
'00-0030968',
'00-0034418',
'00-0034383',
'00-0032956',
'00-0034654',
'00-0033994',
'00-0033455',
'00-0035432',
'00-0035181',
'00-0033572',
'00-0034521',
'00-0033400',
'00-0034747',
'00-0034995',
'00-0030520',
'00-0028872',
'00-0035669',
'00-0033567',
'00-0022787',
'00-0034808',
'00-0029692',
'00-0025825',
'00-0033132',
'00-0031665',
'00-0032450',
'00-0033387',
'00-0022943',
'00-0031690',
'00-0035657',
'00-0035025',
'00-0033382',
'00-0034011',
'00-0032214',
'00-0032417',
'00-0035249',
'00-0031511',
'00-0035275',
'00-0030741',
'00-0033838',
'00-0035686',
'00-0029141',
'00-0033367',
'00-0026625',
'00-0035551',
'00-0028128',
'00-0032464',
'00-0033789',
'00-0033421',
'00-0034613',
'00-0032434',
'00-0034854',
'00-0032972',
'00-0035652',
'00-0033923',
'00-0032436',
'00-0034766',
'00-0035259',
'00-0034988',
'00-0022824',
'00-0034132',
'00-0035342',
'00-0035311',
'00-0032256',
'00-0032975',
'00-0032980',
'00-0031407',
'00-0033246',
'00-0034399',
'00-0032728',
'00-0035039',
'00-0035273',
'00-0034432',
'00-0034342',
'00-0032139',
'00-0024417',
'00-0034449',
'00-0033375',
'00-0034270',
'00-0032098',
'00-0034457',
'00-0033258',
'00-0035624',
'00-0031299',
'00-0033114',
'00-0031167',
'00-0035562',
'00-0035596',
'00-0034773',
'00-0031590',
'00-0033733',
'00-0029419',
'00-0034177',
'00-0035548',
'00-0035021',
'00-0033386',
'00-0032319',
'00-0035374',
'00-0031577',
'00-0034256',
'00-0034794',
'00-0035594',
'00-0035590',
'00-0031484',
'00-0035208',
'00-0034052',
'00-0029857',
'00-0035539',
'00-0035588',
'00-0034437',
'00-0031502',
'00-0035099',
'00-0034660',
'00-0030414',
'00-0032599',
'00-0035510',
'00-0033338',
'00-0035489',
'00-0034922',
'00-0034593',
'00-0029623',
'00-0032377',
'00-0035222',
'00-0034735',
'00-0033904',
'00-0035231',
'00-0034201',
'00-0034104',
'00-0031363',
'00-0029764',
'00-0033604',
'00-0031589',
'00-0033576',
'00-0032404',
'00-0033526',
'00-0032442',
'00-0032245',
'00-0035104',
'00-0034597',
'00-0031209',
'00-0033374',
'00-0032147',
'00-0033215',
'00-0034705',
'00-0034653',
'00-0031288',
'00-0034081',
'00-0034420',
'00-0034034',
'00-0028063',
'00-0035146',
'00-0034267',
'00-0035184',
'00-0035553',
'00-0025399',
'00-0033742',
'00-0035597'
]

def main():

    print(len(player_ids))
    print(len(set(player_ids)))

    pos_data = get_data('../data/pos_data.csv')

    print(pos_data)

    df_new = (pos_data[pos_data['gsis_id'].isin(player_ids)])

    print(df_new)

    rows_list = []
    for index, row in df_new.iterrows():
        
        dict1 = {}

        print(row.gsis_id)

        dict1['season'] = 2019
        dict1['season_type'] = 'reg'
        dict1['full_player_name'] = row.full_player_name
        dict1['abbr_player_name'] = row.abbr_player_name
        dict1['team'] = row.team
        dict1['position'] = row.position
        dict1['gsis_id'] = row.gsis_id

        rows_list.append(dict1)

    new_data = pd.DataFrame(rows_list)

    # print(new_data)

    pos_data = pd.concat([pos_data, new_data], axis=0).reset_index()
    pos_data.drop('index', axis=1, inplace=True)
    pos_data.drop_duplicates(keep=False, inplace=True)
    # print(pos_data)
    
    save_csv(pos_data, '../data/pos_data.csv')


'''
season,season_type,full_player_name,abbr_player_name,team,position,gsis_id
'''

def save_csv(df, file_name):
    # pass
    df.to_csv(file_name, index=False)

def get_data(filename):
    return pd.read_csv(filename)


if __name__ == "__main__":
    main()