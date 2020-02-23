import pandas as pd
from pandas import DataFrame
pathBB = '~/Documents/2020/Jeff-prueba-tecnica/exercise-2/dfB_B.csv'
pathBG = '~/Documents/2020/Jeff-prueba-tecnica/exercise-2/dfB_G.csv'
pathBL = '~/Documents/2020/Jeff-prueba-tecnica/exercise-2/dfB_L.csv'

pathDB = '~/Documents/2020/Jeff-prueba-tecnica/exercise-2/dfD_B.csv'
pathDG = '~/Documents/2020/Jeff-prueba-tecnica/exercise-2/dfD_G.csv'
pathDL = '~/Documents/2020/Jeff-prueba-tecnica/exercise-2/dfD_L.csv'

pathLB = '~/Documents/2020/Jeff-prueba-tecnica/exercise-2/dfL_B.csv'
pathLG = '~/Documents/2020/Jeff-prueba-tecnica/exercise-2/dfL_G.csv'
pathLL = '~/Documents/2020/Jeff-prueba-tecnica/exercise-2/dfL_L.csv'

pathTB = '~/Documents/2020/Jeff-prueba-tecnica/exercise-2/dfT_B.csv'
pathTG = '~/Documents/2020/Jeff-prueba-tecnica/exercise-2/dfT_G.csv'
pathTL = '~/Documents/2020/Jeff-prueba-tecnica/exercise-2/dfT_L.csv'


# Germany:
#   * Duesseldorf 573,057: 51.2385861,6.6742681
#   * Bremen 546,501: 53.1201552,8.5962039
# France:
#   * Lyon 472,317: 45.75801,4.8001016
#   * Toulouse 433,055: 43.6008029,1.3628013
Dpop = 573057.0
Bpop = 546501.0
Lpop = 472317.0
Tpop = 433055.0

dfB_B = pd.read_csv(pathBB)
dfB_G = pd.read_csv(pathBG)
dfB_L = pd.read_csv(pathBL)

dfD_B = pd.read_csv(pathDB)
dfD_G = pd.read_csv(pathDG)
dfD_L = pd.read_csv(pathDL)

dfT_B = pd.read_csv(pathTB)
dfT_G = pd.read_csv(pathTG)
dfT_L = pd.read_csv(pathTL)

dfL_B = pd.read_csv(pathLB)
dfL_G = pd.read_csv(pathLG)
dfL_L = pd.read_csv(pathLL)


ngymsB = len(dfB_G)/Bpop*100000.0
nlaunB = len(dfB_L)/Bpop*100000.0
nhairB = len(dfB_B)/Bpop*100000.0

ngymsD = len(dfD_G)/Dpop*100000.0
nlaunD = len(dfD_L)/Dpop*100000.0
nhairD = len(dfD_B)/Dpop*100000.0

ngymsT = len(dfT_G)/Tpop*100000.0
nlaunT = len(dfT_L)/Tpop*100000.0
nhairT = len(dfT_B)/Tpop*100000.0

ngymsL = len(dfL_G)/Lpop*100000.0
nlaunL = len(dfL_L)/Lpop*100000.0
nhairL = len(dfL_B)/Lpop*100000.0

listG = [ngymsB, ngymsD, ngymsL, ngymsT]
listL = [nlaunB, nlaunD, nlaunL, nlaunT]
listH = [nhairB, nhairD, nhairL, nhairT]
listp = [Bpop, Dpop, Lpop, Tpop]

labels = ["Laundry shops/100k hab", "Gyms shops/100k hab", "Hairdressing/100k hab", 'Pop. size']
rowlab = ["Bern", "Duesseldorf", "Lyon", "Toulousse"]

dic = {labels[0]: listL,
       labels[1]: listG,
       labels[2]: listH,
       labels[3]: listp}

table = DataFrame(dic, columns=labels, index=rowlab)
table = table.round(2)
table[labels[3]] = pd.to_numeric(table[labels[3]], downcast='integer')
print(table.head(5))

# export to latex
with open('tableFranceGermany.tex', 'w') as op:
    op.write(table.to_latex(bold_rows=True, index_names=True))
