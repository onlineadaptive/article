import pandas as pd
from matplotlib import pyplot as plt
import sys

sizes = [128, 1024,8192,16384,131072,1048576]
tests = ['iterate', 'update', 'even']
implementations = ['ONLINE_ADAPTIVE_LIST', 'ONLINE_ADAPTIVE_MAP', 'WRAPPED_MAP', 'WRAPPED_LIST']
names = {'ONLINE_ADAPTIVE_LIST': 'OnlineAdaptiveList',
         'ONLINE_ADAPTIVE_MAP': 'OnlineAdaptiveMap',
         'WRAPPED_MAP':'ConcurrentHashMap',
         'WRAPPED_LIST':'CopyOnWriteArrayList'}
combined = {'ADAPTIVE' : ['ONLINE_ADAPTIVE_LIST', 'ONLINE_ADAPTIVE_MAP'],
          'WRAPPED' : ['WRAPPED_MAP', 'WRAPPED_LIST']}
props = {'ONLINE_ADAPTIVE_LIST': ['dashed', 'blue'],
         'ONLINE_ADAPTIVE_MAP': ['dashed', 'red'],
         'WRAPPED_MAP': ['dashdot', 'black'],
         'WRAPPED_LIST': ['dashdot', 'green']}

#read file
df = pd.read_csv(sys.argv[1], sep=',')

df0 = df[df['Param: impl'] == implementations[0]]
df1 = df[df['Param: impl'] == implementations[1]]
dfOA = pd.concat([df0, df1])
df2 = df[df['Param: impl'] == implementations[2]]
df3 = df[df['Param: impl'] == implementations[3]]
dfNA = pd.concat([df2, df3])


plt.style.use('ggplot')

for size in sizes:
    for test in tests:
        for impl in implementations:
            ax = plt.gca()
            selected = df[(df['Param: size'] == size) & (df['Param: testType'] == test) & (df['Param: impl'] == impl)]
            grouped = selected.groupby('Threads').mean()
            grouped.plot(kind='line',marker='+',y='Score',ax=ax,label=names[impl],linestyle=props[impl][0],color=props[impl][1])
        plt.legend(loc='upper left')
        plt.title(test + ": " + str(size) + " elements")
        plt.xlabel('Threads')
        plt.ylabel('Throughput')
        plt.savefig(test + "_" + str(size)+".png")
        plt.clf()


#Average tests
for size in sizes:
    for test in tests:
        for merged in ['ADAPTIVE', 'WRAPPED']:
            ax = plt.gca()
            selectedOA = dfOA[(dfOA['Param: size'] == size) & (dfOA['Param: testType'] == test)]
            selectedOA.groupby('Threads').mean().plot(kind='line', marker='+', y='Score', ax=ax,
                                                      label='Average OnlineAdaptive',
                                                      color='chocolate')
            selectedNA = dfNA[(dfNA['Param: size'] == size) & (dfNA['Param: testType'] == test)]
            selectedNA.groupby('Threads').mean().plot(kind='line', marker='+', y='Score', ax=ax,
                                                      label='Average Non-Adaptive',
                                                      color='teal')
        plt.legend(loc='upper left')
        plt.title('average_'+test + ": " + str(size) + " elements")
        plt.xlabel('Threads')
        plt.ylabel('Throughput')
        plt.savefig('average_'+test+'_' + str(size)+'.png')
        plt.clf()

#Average all four lines
for size in sizes:
    for impl in implementations:
        ax = plt.gca()
        selected = df[(df['Param: size'] == size) & (df['Param: impl'] == impl)]
        grouped = selected.groupby('Threads').mean()
        grouped.plot(kind='line',marker='+',y='Score',ax=ax,label=names[impl],linestyle=props[impl][0],color=props[impl][1])
    plt.legend(loc='upper left')
    plt.title('average_four: ' + str(size) + " elements")
    plt.xlabel('Threads')
    plt.ylabel('Throughput')
    plt.savefig('average_four_' + str(size)+".png")
    plt.clf()


# Average all two lines
for size in sizes:
    for merged in ['ADAPTIVE', 'WRAPPED']:
        ax = plt.gca()
        selected = df[(df['Param: size'] == size)]
        selection1 = selected[selected['Param: impl'] == combined[merged][0]]
        selection2 = selected[selected['Param: impl'] == combined[merged][1]]
        selected = pd.concat([selection1,selection2])
        grouped = selected.groupby('Threads').mean()
        grouped.plot(kind='line',marker='+',y='Score',ax=ax,label=merged)
    plt.legend(loc='upper left')
    plt.title('average' + ": " + str(size) + " elements")
    plt.xlabel('Threads')
    plt.ylabel('Throughput')
    plt.savefig('average_two_' + str(size)+".png")
    plt.clf()



