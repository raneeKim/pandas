import pandas as pd
import numpy as np

# 1. earthquakes.csv 파일에서 mb 진도 유형(magnitude type)의 진도가 4.9 이상인 일본의 모든 지진을 선택한다.
earthquakes = pd.read_csv(r'c:\Users\MSI\Desktop\study\pandas\data-analysis-pandas-main\ch_04\exercises\earthquakes.csv')
earthquakes.dtypes
over_49 = earthquakes[(earthquakes['mag']>=4.9) & (earthquakes['parsed_place']=='Japan') & (earthquakes['magType']=='mb')]

# 2.  ml 측정 방법의 모든 진도 값에 대한 구간(예를 들어 첫 번째 구간은 (0,1], 두번째는(1,2], 세번째는(2,3])을 만들고 각 구간의 빈도수를 계산한다.
'''
one = earthquakes[(earthquakes['magType'] == 'ml') & (earthquakes['mag']>=0) & (earthquakes['mag']<0)]
two = earthquakes[(earthquakes['magType'] == 'ml') & (earthquakes['mag']>=1) & (earthquakes['mag']<2)]
three = earthquakes[(earthquakes['magType'] == 'ml') & (earthquakes['mag']>=2) & (earthquakes['mag']<3)]
four = earthquakes[(earthquakes['magType'] == 'ml') & (earthquakes['mag']>=3) & (earthquakes['mag']<4)]
five = earthquakes[(earthquakes['magType'] == 'ml') & (earthquakes['mag']>=4) & (earthquakes['mag']<5)]
six = earthquakes[(earthquakes['magType'] == 'ml') & (earthquakes['mag']>=5) & (earthquakes['mag']<6)]
seven = earthquakes[(earthquakes['magType'] == 'ml') & (earthquakes['mag']>=6) & (earthquakes['mag']<7)]
'''

bins = np.arange(0, 10)
bins_label = [str(x) + "이상" + str(x + 1) + "미만" for x in bins[:-1]]
earthquakes['level'] = pd.cut(earthquakes['mag'], bins, right=False, labels=bins_label)
result = earthquakes[earthquakes['magType'] == 'ml']
a = result['level'].value_counts()
a.sort_index()



earthquakes.query("magType == 'ml'").assign(
    mag_bin=lambda x: pd.cut(x.mag, np.arange(0, 10))
).mag_bin.value_counts b()  

# 3. faang.csv 파일에서 티커(ticker)로 그룹을 만들고 월별 빈도수 재표본추출한다. 다음과 같이 집계한다.
# a) 시가 평균 b) 고가의 최대값 c) 저가의 최소값 d) 종가 평균 e) 거래량 합

faang = pd.read_csv(r'c:\Users\MSI\Desktop\study\pandas\data-analysis-pandas-main\ch_04\exercises\faang.csv')
faang.dtypes
faang['date'] = pd.to_datetime(faang['date'])
faang.index = faang['date'] # resample 사용하려면 index가 datetime이어야함.
# faang['month'] = faang['date2'].dt.month
faang.groupby('ticker').resample('M').agg(
    {
        'open': np.mean,
        'high': np.max,
        'low': np.min,
        'close': np.mean,
        'volume': np.sum
    }
)
faang.groupby(by='month')

# 4. 지진 데이터에서 tsunami 열과 magType 열의 교차표를 만든다. 교차표에서는 빈도수가 아니라 각 조합에서 관측된 최대 진도가 표시되도록 한다. 
# 열에서는 진도 유형 (magnitude type) 값이 와야한다.
cross = pd.crosstab(earthquakes.tsunami,earthquakes.magType, values=earthquakes.mag, aggfunc=max)

# 5. FAANG 데이터의 티커로 OHLC의 60일 이동집계를 만든다. 연습 문제 3번과 같은 집계를 한다.
# a) 시가 평균 b) 고가의 최대값 c) 저가의 최소값 d) 종가 평균 e) 거래량 합
faang.groupby(faang['ticker']).mean()
a = faang.groupby('ticker').rolling('60D').agg(
        {
        'open' : np.mean,
        'high' : np.max,
        'low' : np.min,
        'close' : np.mean,
        'volume' : np.sum
        }
    )
print(a)

# 6. 주가를 비교하는 FAANG 데이터의 피봇 테이블을 만든다. 행에는 티커가 오도록하고 OHLC의 평균과 거래량 데이터를 표시한다.
faang.pivot_table(index='ticker')

# 7. apply()를 사용해 아마존 데이터의 2018년 4분기 (Q4) 각 숫자열의 Z-점수를 계산한다.

faang.info()

a = faang[(faang.ticker == 'AMZN')&(faang.date.dt.quarter==4)]
# dir(stat)
a.apply(lambda x: x.sub(x.mean()).div(x.std()))
# lambda 를 통해 z-점수를 구하는 함수를 만든다 -> apply는 함수를 각 행 or 열에 적용하는 역할 -> 즉 lambda함수(z-점수만드는)를 각 열에 적용해라

'''
mean = sum(values) / len(values)
differences = [(value - mean)**2 for value in values]
sum_of_differences = sum(differences)
standard_deviation = (sum_of_differences / (len(values) - 1)) ** 0.5
'''

# 8 이벤트 설명을 추가한다.
# a) ticker와 date, event의 세 열로 구성된 DataFrame을 만든다. 각 열은 다음과 같은 값을 가져야한다.
# ⅰ) ticker : 'FB'
# ⅱ) date : ['2018-07-25','2018-03-19','2018-03-20']
# ⅲ) event : ['Disappointing user growth announced after colse.', 'Cambridge','Analytica story', 'FTC invsetigation']
# b) 인덱스를 ['date','ticker']로 설정한다.
# c) 이 데이터를 FAANG 데이터와 외부 결합으로 병합한다.

events = pd.DataFrame({
    'ticker': 'FB',
    'date': pd.to_datetime(
         ['2018-07-25', '2018-03-19', '2018-03-20']
    ), 
    'event': [
         'Disappointing user growth announced after close.',
         'Cambridge Analytica story',
         'FTC investigation'
    ]
}).set_index(['date', 'ticker'])

faang.reset_index().set_index(['date', 'ticker']).join(
    events, how='outer'
).sample(10, random_state=0)

# 9
faang = faang.reset_index().set_index(['ticker', 'date'])
faang_index = (faang / faang.groupby(level='ticker').transform('first'))

# view 3 rows of the result per ticker
faang_index.groupby(level='ticker').agg('head', 3)

# 10-1
covid = pd.read_csv('../../ch_04/exercises/covid19_cases.csv')\
    .assign(date=lambda x: pd.to_datetime(x.dateRep, format='%d/%m/%Y'))\
    .set_index('date')\
    .replace('United_States_of_America', 'USA')\
    .replace('United_Kingdom', 'UK')\
    .sort_index()

# 10-2
top_five_countries = covid\
    .groupby('countriesAndTerritories').cases.sum()\
    .nlargest(5).index

covid[covid.countriesAndTerritories.isin(top_five_countries)]\
    .groupby('countriesAndTerritories').cases.idxmax()

# 10-3
covid\
    .groupby(['countriesAndTerritories', pd.Grouper(freq='1D')]).cases.sum()\
    .unstack(0).diff().rolling(7).mean().last('1W')[top_five_countries]

# 10-4
covid\
    .pivot(columns='countriesAndTerritories', values='cases')\
    .drop(columns='China')\
    .apply(lambda x: x[x > 0].index.min())\
    .sort_values()\
    .rename(lambda x: x.replace('_', ' '))


# 10-5
covid\
    .pivot_table(columns='countriesAndTerritories', values='cases', aggfunc='sum')\
    .T\
    .transform('rank', method='max', pct=True)\
    .sort_values('cases', ascending=False)\
    .rename(lambda x: x.replace('_', ' '))