import csv
import pandas as pd
import os
import glob
import sys
import numpy as np

def preprocessor(array):
    colnames = [
        'Question Type',
        'Answer Type',
        'Topic Number',
        'Variation',
        'Question (Text Only)',
        'Correct Answer 1',
        'Correct Answer 2',
        'Correct Answer 3',
        'Correct Answer 4',
        'Wrong Answer 1',
        'Wrong Answer 2',
        'Wrong Answer 3',
        'Time in seconds',
        'Difficulty Level',
        'Question (Image/ Audio/ Video)',
        'Contributor\'s Registered mailId',
        'Solution (Text only)',
        'Solution (Image/ Audio/ Video)'
    ]
    for path in array:
        print(path)
        df = pd.read_csv(path,header=1,names=colnames)
        df['Variation Number'] = df['Variation'].copy()
        del df['Variation']

        vc = str(df['Variation Number'].unique()[0])
        df['Variation Number'] = '0'+ vc if (vc[0] != 0 and int(vc)<10 ) else vc

        tv = str(df['Topic Number'].unique()[0])
        df['Topic Number'] = '0'+ tv if tv[0] != 0 else tv
        df.insert(0, "Sr. No", [str(i+1) for i in range(0,len(df))], True)
        df2 = pd.DataFrame([['****',None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]], columns=df.columns)
        df = pd.concat([df, df2],ignore_index=True)
        df_empty = pd.DataFrame()
        filename = path.split('\\')[-1].split('.')[0]
        with pd.ExcelWriter(filename+'.xlsx') as writer:  
            df_empty.to_excel(writer, sheet_name='Sheet1',index=False)
            df.to_excel(writer, sheet_name=filename,index=False)
    return

def converter(fileargs=None):
    if(fileargs):
        #print(sys.argv[1:],len(sys.argv))
        #print(fileargs)
        array = [fileargs]
    else:
        #print('null')
        array = glob.glob(os.path.join('.', '*.csv'))
    preprocessor(array)
    for i in array:
        os.remove(i)

#converter()


def database_fn(
    Question_Type='text',
    Answer_Type=None,
    Topic_Number=None,
    Variation=None,
    Question=None,
    Correct_Answer_1=None,
    Correct_Answer_2='',
    Correct_Answer_3='',
    Correct_Answer_4='',
    Wrong_Answer_1=None,
    Wrong_Answer_2=None,
    Wrong_Answer_3=None,
    Time_in_seconds=60,
    Difficulty_Level=3,
    Question_IAV='',
    ContributorMail=None,
    Solution_text=None,
    Solution_IAV=''
):

    dataset_dict={
        'Question_Type':Question_Type,
        'Answer_Type':Answer_Type,
        'Topic_Number':Topic_Number,
        'Variation':Variation,
        'Question':Question,
        'Correct_Answer_1':Correct_Answer_1,
        'Correct_Answer_2':Correct_Answer_2,
        'Correct_Answer_3':Correct_Answer_3,
        'Correct_Answer_4':Correct_Answer_4,
        'Wrong_Answer_1':Wrong_Answer_1,
        'Wrong_Answer_2':Wrong_Answer_2,
        'Wrong_Answer_3':Wrong_Answer_3,
        'Time_in_seconds':Time_in_seconds,
        'Difficulty_Level':Difficulty_Level,
        'Question_IAV':Question_IAV,
        'ContributorMail':ContributorMail,
        'Solution_text':Solution_text,
        'Solution_IAV':Solution_IAV
    }
    return dataset_dict

def removeDuplicateEntries(filepath, questionType, Main_Function, NoI):
    df = pd.read_csv(filepath)
    legit_col = ['Question_Type',
            'Answer_Type',
            'Topic_Number',
            'Variation',
            'Question',
            'Correct_Answer_1',
            'Correct_Answer_2',
            'Correct_Answer_3',
            'Correct_Answer_4',
            'Wrong_Answer_1',
            'Wrong_Answer_2',
            'Wrong_Answer_3',
            'Time_in_seconds',
            'Difficulty_Level',
            'Question_IAV',
            'ContributorMail',
            'Solution_text',
            'Solution_IAV'
            ]

    for col in df.columns:
        if col not in legit_col:
            del df[col]
    if questionType == 'text' or questionType == 'Text':
        df.drop_duplicates(subset='Question',keep='first',inplace=True)
    elif questionType == 'image' or questionType == 'Image':
        df.drop_duplicates(subset='Question_IAV',keep='first',inplace=True)
    #length = len(df)
    ct=0
    while(len(df)<NoI and ct!=100):
        print(ct)
        ct+=1
        dd = Main_Function()
        l = list(dd.values())
        if l[4] in df[['Question']].values and l[5] in df[['Correct_Answer_1']].values and l[14] in df[['Question_IAV']].values:
            if (list(df[['Question']].values).index(l[4]) == list(df[['Correct_Answer_1']].values).index(l[5])) and (list(df[['Question']].values).index(l[4]) == list(df[['Question_IAV']].values).index(l[14])):
                continue
        else:
            df2 = pd.DataFrame([list(dd.values())], columns=df.columns)
            df = pd.concat([df, df2],ignore_index=True)

    df.to_csv(filepath,index=False)
    return

def getTextTupple(field_dict):
    Q = field_dict['Question']
    QIav = field_dict['Question_IAV'] if field_dict['Question_IAV'] is not None else ''
    a1,a2,a3,a4 = [field_dict[a] for a in ['Correct_Answer_1','Correct_Answer_2','Correct_Answer_3','Correct_Answer_4',]]
    w1,w2,w3 = [field_dict[w] for w in ['Wrong_Answer_1','Wrong_Answer_2','Wrong_Answer_3',]]
    S = field_dict['Solution_text']
    field_line = f'''
    \n =======================Question======================= \n {Q} \n {QIav}
    \n =======================Correct answers======================= \n {a1},\n {a2},\n {a3},\n {a4}
    \n =======================Wrong answers======================= \n {w1},\n {w2},\n {w3},\n
    \n =======================Solution======================= \n {S} \n
    '''
    return field_line

#open csv file
def putInCsv(
    Topic_Number,
    Number_Of_Iterations,
    Main_Function,
    Filename,
    Remove_Duplicates=True,
    Create_Textfile=False,
    new_csv=True,
    Create_xlsx=True
):
    csv_filename= Topic_Number + '_' + Filename.split('.')[0] + '.csv'
    questionType = ''

    m = 'w'
    if(os.path.exists(csv_filename) and new_csv != True):
        #print('here')
        m = 'a+'

    with open(csv_filename,mode=m,newline='',encoding='utf-8') as f:
        fieldnames = [
            'Question_Type',
            'Answer_Type',
            'Topic_Number',
            'Variation',
            'Question',
            'Correct_Answer_1',
            'Correct_Answer_2',
            'Correct_Answer_3',
            'Correct_Answer_4',
            'Wrong_Answer_1',
            'Wrong_Answer_2',
            'Wrong_Answer_3',
            'Time_in_seconds',
            'Difficulty_Level',
            'Question_IAV',
            'ContributorMail',
            'Solution_text',
            'Solution_IAV'
        ]
        thewriter = csv.DictWriter(f, fieldnames=fieldnames)
        if(m=='w'):
            thewriter.writeheader()

        for _ in range(Number_Of_Iterations):
            field_dict = Main_Function()
            questionType = field_dict["Question_Type"]
            thewriter.writerow(field_dict)

    if(Remove_Duplicates == True):
        removeDuplicateEntries(csv_filename, questionType, Main_Function, Number_Of_Iterations)
            

    if(Create_Textfile==True):
        textfilestr = ''        
        with open(csv_filename,'r',newline='') as csvr:
            thereader = csv.DictReader(csvr)
            for row in thereader:
                textfilestr+=getTextTupple(row)
        
        txt_filename = Topic_Number + '_' + Filename.split('.')[0] + '.txt'
        with open(txt_filename,'w',newline='') as t:
            t.write(textfilestr)

    if(Create_xlsx==True):
        #print(csv_filename)
        converter(csv_filename)
