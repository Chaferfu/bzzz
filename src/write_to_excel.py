from pandas import DataFrame

#Pour ecrire dans un fichier excel, il suffit de :
#-- creer les colonnes qui vont accueillir nos donnees
#-- lui associer une DataFrame avec les labels qui vont avec
#-- utiliser la methode to_excel qui cree la fiche excel

temp_l = [20.4, 20.1, 20.8, 21.0, 23.4]
press_l = [1013.01, 1015.02, 1501.00, 1000.15, 992.91]
df = DataFrame({'Temperature': temp_l, 'Pression': press_l, 'Somme': '=SUM(A2:A6)'})
df.to_excel('temp_pression.xlsx', sheet_name='sheet1', index=False)
