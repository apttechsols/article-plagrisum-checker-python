import sys
import os
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import unquote

def AptSubStringByChar(data = {}):
    
    if not isinstance(data,dict):
        return {'status':'error','msg':'Invalid data formate received [FindSubStringBwtChar]','code':400}

    if((data.keys() >= {"start",'end','string'}) != True):
        return {'status':'error','msg':'Invalid data formate received [FindSubStringBwtChar]','code':400}
    
    msg = []
    string = str(data['string']);

    if 'startspe' in data:
        startspe = data['startspe'];
    else:
        startspe = len(data['start']);

    if 'endspe' in data:
        endspe = data['endspe'];
    else:
        endspe = 0;

    j = 0
    i=0
    while(i < 1):
        tmp_msg = ''
        if(data['start'] != '' and data['end'] != ''):
            tmp_msg_start = string.find(data['start'])
            
            if(tmp_msg_start != -1):
                if 'isendrequired' in data and data['isendrequired'] == True:
                    if(data['end'] == ''):
                        string = ''
                        i = 2
                    
                    tmp_string = string[(tmp_msg_start+len(data['start'])):-1]
                    if isinstance(data['end'], list):
                        ItemList = []
                        for item in data['end']:
                            tmp_msg_end = tmp_string.find(item)
                            ItemList.append(tmp_msg_end)
                        
                        ItemList.sort()
                        tmp_msg_end = ItemList[0]
                    else:
                        tmp_msg_end = tmp_string.find(data['end'])
                    
                    if(tmp_msg_end != -1):
                        tmp_msg = string[tmp_msg_start+startspe:(tmp_msg_start+tmp_msg_end) + len(data['start']) + endspe]
                        msg.append(tmp_msg)
                        if 'isendincudeagain' in data and data['isendincudeagain'] == True:
                            string = string[(tmp_msg_start+tmp_msg_end) + len(data['start']):-1]
                        else:
                            string = string[(tmp_msg_start+tmp_msg_end) + len(data['start']) + len(data['end']):-1]
                    else:
                        string = ''
                        i = 2
                else:    
                    if(data['end'] == ''):
                        tmp_msg = string[(tmp_msg_start+startspe):-1]
                        msg.append(tmp_msg)
                        string = ''
                        i = 2

                    tmp_string = string[(tmp_msg_start+len(data['start'])):-1]
                    if isinstance(data['end'], list):
                        ItemList = []
                        for item in data['end']:
                            tmp_msg_end = tmp_string.find(item)
                            ItemList.append(tmp_msg_end)
                            
                        ItemList.sort()
                        tmp_msg_end = ItemList[0]
                    else:
                        tmp_msg_end = tmp_string.find(data['end'])
                    
                    if(tmp_msg_end != -1):
                        tmp_msg = string[tmp_msg_start+startspe:(tmp_msg_start+tmp_msg_end) + len(data['start']) + endspe]
                        msg.append(tmp_msg)
                        if 'isendincudeagain' in data and data['isendincudeagain'] == True:
                            string = string[(tmp_msg_start+tmp_msg_end) + len(data['start']):-1]
                        else:
                            string = string[(tmp_msg_start+tmp_msg_end) + len(data['start']) + len(data['end']):-1]
                    else:
                        tmp_msg = string[(tmp_msg_start+startspe):-1]
                        msg.append(tmp_msg)
                        string = ''
                        i = 2    
            else:
                i = 2
        elif(data['start'] != ''):
            tmp_msg_start = string.find(data['start'])
            if(tmp_msg_start != -1):
                tmp_msg = string[(tmp_msg_start+startspe):-1]
                msg.append(tmp_msg)
                
            string = ''
            i = 2
        elif(data['end'] != ''):
            tmp_msg_end = string.find(data['end'])

            if(tmp_msg_end != -1):
                tmp_msg = string[0:(tmp_msg_end+endspe)]
            else:
                if 'isendrequired' in data and data['isendrequired'] == True:
                    string = ''
                    i = 2
                else:    
                    tmp_msg = string
                    msg.append(tmp_msg)
            string = ''
            i = 2
        else:
            msg.append(string)
            string = ''
            i = 2  
        j = j+1

    if(len(msg) != 0):
        return {'status':'success','msg':msg,'code':200}
    else:        
        return {'status':'error','msg':'No substring found','code':404}
    
def remove_tags(text):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', text)

def PlagiarismCheckWithGoogle(data=dict()):
    if not isinstance(data,dict):
        return {'status':'error','msg':'Invalid data formate received [PlagiarismCheckWithGoogle]','code':400}
    DataList = []
    StringBreakBy = []
    if((data.keys() >= {'data'}) != True):
        return {'status':'error','msg':'Invalid data formate received [PlagiarismCheckWithGoogle]','code':400}
    
    if((data.keys() >= {'filter'}) == True):
        if not isinstance(data['filter'],list) or not len(data['filter']) > 0:
            return {'status':'error','msg':'Invalid data formate received [filter] [PlagiarismCheckWithGoogle]','code':400}

        for StringBreakByList in data['filter']:
            if not isinstance(StringBreakByList,dict):
                return {'status':'error','msg':'Invalid data formate received [filter] [PlagiarismCheckWithGoogle]','code':400}
            if((StringBreakByList.keys() >= {'pattern'}) != True):
                return {'status':'error','msg':'Invalid data formate received [filter] [PlagiarismCheckWithGoogle]','code':400}

            if((StringBreakByList.keys() >= {'pattern'}) == True or StringBreakByList['pattern'] == ''):
                pattern = StringBreakByList['pattern']
            else:
                return {'status':'error','msg':'Invalid data formate received [filter] [PlagiarismCheckWithGoogle]','code':400}

            if((StringBreakByList.keys() >= {'epos'}) == True):
                if not StringBreakByList['epos'] > 0:
                    return {'status':'error','msg':'Invalid data formate received [filter] [PlagiarismCheckWithGoogle]','code':400}
                epos = StringBreakByList['epos']
            else:
                epos = 1

            if((StringBreakByList.keys() >= {'mineposreq'}) == True):
                if not StringBreakByList['mineposreq'] > epos:
                    return {'status':'error','msg':'Invalid data formate received [filter] [PlagiarismCheckWithGoogle]','code':400}
                mineposreq = StringBreakByList['mineposreq']
            else:
                mineposreq = epos

            if((StringBreakByList.keys() >= {'patterninclude'}) == True):
                if(StringBreakByList['patterninclude'] != True and StringBreakByList['patterninclude'] != False):
                    return {'status':'error','msg':'Invalid data formate received [filter] [PlagiarismCheckWithGoogle]','code':400}
                else:
                     patterninclude = StringBreakByList['patterninclude']
            else:
                patterninclude = True

            StringBreakBy.append({'pattern':pattern,'epos':epos,'mineposreq':mineposreq,'patterninclude':patterninclude})
    
    if not len(data['data']) > 0:
        return {'status':'error','msg':'Invalid data formate received [data] [PlagiarismCheckWithGoogle]','code':400}
    tmpData = [data['data']]
    newTmpData = []
    
    if len(StringBreakBy) > 0:
        for StringBreakByStr in StringBreakBy:
            for tmpDataStr in tmpData:
                tmpDataStrSplit = tmpDataStr.split(StringBreakByStr['pattern'])
                tmpDataStrSplitLen =len(tmpDataStrSplit)

                if(tmpDataStrSplitLen >= StringBreakByStr['mineposreq']):
                    while(True):
                        tmpDataStr1 = ''
                        if(tmpDataStrSplitLen >= StringBreakByStr['mineposreq']):
                            for i in range(0,StringBreakByStr['epos']):
                                if(StringBreakByStr['patterninclude'] == True):
                                    tmpDataStr1 += f"{tmpDataStrSplit[0]}{StringBreakByStr['pattern']}"
                                else:
                                    tmpDataStr1 += f"{tmpDataStrSplit[0]}"
                                tmpDataStrSplit.pop(0)
                                tmpDataStrSplitLen += -1
                            newTmpData.append(tmpDataStr1.strip(StringBreakByStr['pattern']))
                        else:
                            for i in range(0,tmpDataStrSplitLen):
                                if(StringBreakByStr['patterninclude'] == True):
                                    tmpDataStr1 += f"{tmpDataStrSplit[i]}{StringBreakByStr['pattern']}"
                                else:
                                     tmpDataStr1 += f"{tmpDataStrSplit[i]}"
                            if(tmpDataStr1 != ''):
                                newTmpData.append(tmpDataStr1.strip(StringBreakByStr['pattern']))
                            break
                else:
                    newTmpData.append(tmpDataStr)

            tmpData.clear()
            tmpData = newTmpData.copy()
            newTmpData.clear()
            
        
    TotalMatchWord = 0
    TotalUnMatchedWord = 0
    TotalWord = 0
    
    for SearchData in tmpData:
        print(f'Searching for : {SearchData}\n')
        StartSearch = 0
        
        tmpSearchData = ['Till now Earth is the only home for life in the universe. Around 8.5 million species live on earth and ']
        SearchDataBreak = [{'pattern':'. ','mineposreq':1,'epos':1,'patterninclude':False},{'pattern':' ','mineposreq':1,'epos':1,'patterninclude':False}]
        NewtmpSearchData = []

        for SearchDataBreakList in SearchDataBreak:
            for tmpSearchDataStr in tmpSearchData:
                tmpSearchDataStrSplit = tmpSearchDataStr.split(SearchDataBreakList['pattern'])
                tmpSearchDataStrSplitLen =len(tmpSearchDataStrSplit)

                if(tmpSearchDataStrSplitLen >= SearchDataBreakList['mineposreq']):
                    while(True):
                        tmpDataStr1 = ''
                        if(tmpSearchDataStrSplitLen >= SearchDataBreakList['mineposreq']):
                            for i in range(0,SearchDataBreakList['epos']):
                                if(SearchDataBreakList['patterninclude'] == True):
                                    tmpDataStr1 += f"{tmpSearchDataStrSplit[0]}{SearchDataBreakList['pattern']}"
                                else:
                                    tmpDataStr1 += f"{tmpSearchDataStrSplit[0]}"
                                tmpSearchDataStrSplit.pop(0)
                                tmpSearchDataStrSplitLen += -1
                            NewtmpSearchData.append(tmpDataStr1.strip(SearchDataBreakList['pattern']))
                        else:
                            for i in range(0,tmpSearchDataStrSplitLen):
                                if(SearchDataBreakList['patterninclude'] == True):
                                    tmpDataStr1 += f"{tmpSearchDataStrSplit[i]}{SearchDataBreakList['pattern']}"
                                else:
                                     tmpDataStr1 += f"{tmpSearchDataStrSplit[i]}"
                            if(tmpDataStr1 != ''):
                                NewtmpSearchData.append(tmpDataStr1.strip(SearchDataBreakList['pattern']))
                            break
                else:
                    NewtmpSearchData.append( tmpSearchDataStr)
            tmpSearchData.clear()
            tmpSearchData = NewtmpSearchData.copy()
            NewtmpSearchData.clear()
        
        while(StartSearch >= 0):
            page = requests.get(f'https://www.google.com/search?q={SearchData}&start={StartSearch}')
            soup = BeautifulSoup(page.content, 'html.parser')

            if(StartSearch < 0 or StartSearch > 990):
                print('Warning : Google have maximum 1000 results for any search')
                StartSearch = -1
                break
            else:
                IsSearched = {'code':300}
                SearchTitles = {'code':300}
                SearchResult = {'code':300}
                SearchTitles = AptSubStringByChar({'start':'<title>','end':'</title>','string':soup,'isendincudeagain':True,'isendrequired':True})

            if(SearchTitles['code'] == 200):
                if(StartSearch == 0):
                    print(f"Search Title : {SearchTitles['msg'][0]} \n")
                IsSearched = AptSubStringByChar({'start':'<span class="JZCD0c r0bn4c rQMQod">'+SearchData+'</span><span class="r0bn4c rQMQod"> - did not match any documents.','end':'Try more general keywords.</span>','string':soup,'isendincudeagain':True,'isendrequired':True})      
                if(IsSearched['code'] == 200):
                    if(StartSearch == 0):
                        print('Warning : No search result avaiable for this search')
                    StartSearch = -1
                    break
                elif(IsSearched['code'] == 404):
                      SearchResult = AptSubStringByChar({'start':'<div class="ZINbbc','end':['<div class="ZINbbc','<footer>'],'string':soup,'startspe':0,'isendincudeagain':True,'isendrequired':True})
                elif(SearchResult['code'] == 300):
                    print()
                else:
                    print('Error : Oops! we can not able to search, due to technical error occur...')
                    StartSearch = -1
                    break
            elif(SearchResult['code'] == 300):
                print()
            else:
                print('Error : Oops! we can not able to search, due to technical error occur...')
                StartSearch = -1
                break

            IsSearchResult = True
            if(SearchResult['code'] == 200):
                AllSearchResultWord = ''
                for SearchResponse in SearchResult['msg']:
                    AllSearchResultWord += SearchResponse

                    Heading = AptSubStringByChar({'start':'<div class="BNeawe vvjwJb AP7Wnd">','end':'</div>','string':SearchResponse})
                    if(Heading['code'] == 200):
                        print('Heading : '+remove_tags(Heading['msg'][0]))

                    Description = AptSubStringByChar({'start':'<span class="r0bn4c rQMQod"> · </span>','end':'</div>','string':SearchResponse})
                    if(Description['code'] == 200):
                        print('Description : '+remove_tags(Description['msg'][0]))

                    MatchLink = AptSubStringByChar({'start':'<a href="/url?q=','end':'">','string':SearchResponse})
                    if(MatchLink['code'] == 200):
                        SearchLink = unquote(MatchLink['msg'][0])
                        #print('Search Link : '+SearchLink)
                        SplitSearchLink0 = SearchLink.split('&amp')
                        SplitSearchLink1 = SearchLink.split('/')
                        if(len(SplitSearchLink0) > 0):
                            print('Link : '+SplitSearchLink0[0])
                        else:
                            print('Link : not found')

                        if(len(SplitSearchLink1) > 2):
                            print('Domain : '+SplitSearchLink1[0]+'/'+SplitSearchLink1[1]+'/'+SplitSearchLink1[2])
                        else:
                            print('Domain : not found')
                    else:
                           print('Info : Domain and Links not found')
                    print("\n\n")

            elif(SearchResult['code'] == 404):
                print('No result found for this search')
                StartSearch = -1
                break
            elif(SearchResult['code'] == 300):
                print()
            else:
                print("Error : "+SearchResult['msg'])
                StartSearch = -1
                break
            StartSearch += 10

        MatchedWordString = ''
        MatchedWordStringReal = ''
        UnMatchedWordString = ''    
        UnMatchedWordStringReal = ''

        for tmpSearchDataStr in tmpSearchData:
            if tmpSearchDataStr.lower() in AllSearchResultWord.lower():
                MatchedWordString += f' {tmpSearchDataStr}'
                MatchedWordStringReal += tmpSearchDataStr
                UnMatchedWordString += f' _'
            else:
                MatchedWordString += f' _'
                UnMatchedWordStringReal += tmpSearchDataStr
                UnMatchedWordString += f' {tmpSearchDataStr}'

        print(f'Matched word : {MatchedWordString}',end=" | ")
        print(f'UnMatched word : {UnMatchedWordString}')

        TmpSearchDataString = SearchData.replace(",", "")
        TmpSearchDataString = TmpSearchDataString.replace(" ", "")

        print(f'Matched % : {(len(MatchedWordStringReal)*100)/len(TmpSearchDataString)}%',end=" | ")
        print(f'Unique % : {(len(UnMatchedWordStringReal)*100)/len(TmpSearchDataString)}%\n')

        TotalMatchWord += len(MatchedWordStringReal)
        TotalUnMatchedWord += len(UnMatchedWordStringReal)
        TotalWord += len(TmpSearchDataString)

    print('\nFinal result : ',end="")
    print(f'Total Matched word : {TotalMatchWord}',end=" | ")
    print(f'Total UnMatched word : {TotalUnMatchedWord}',end=" | ")
    print(f'Total word : {TotalWord}')

    print(f'Total Matched % : {(TotalMatchWord*100)/TotalWord}%',end=" | ")
    print(f'Total Unique % : {(TotalUnMatchedWord*100)/TotalWord}%')
    return {'status':'success','msg':{'TotalMatchWord':TotalMatchWord,'TotalUniqueWord':TotalUnMatchedWord,'TotalWord':TotalWord,'TotalMatchRatio':(TotalMatchWord*100)/TotalWord,'TotalUniqueRatio':(TotalUnMatchedWord*100)/TotalWord},'code':200}

Data = """Till now Earth is the only home for life in the universe. Around 8.5 million species live on earth and among these only 1.3 million species have been identified. The journey of earth begins around 4.5 billion years ago, gravity pulled the rocks, asteroids and space dust together form the giant planet which we called earth. When this planet was just formed, it was an ocean of lava and liquid rock and the temperature was around 12000C. Inside asteroids a strange salt like crystals which we put in our French fries and minute droplets of water were present. These contain the vital ingredient for life. The asteroids and meteorites shower didn’t stop for billions of years, and soon created an ocean of water. Molten lava erupted form the core for millions of years and created the crust and formed the land. Also many asteroids came with a very vital ingredient for life primitive protein which have amino acids. It’s impossible to know how and when but somehow these chemicals have come together to create life. And soon microscopic organisms came into existence, these single cell bacteria evolved for millions of years. On the seabed, colonies of bacteria called ‘stromalolite’ were doing something which was responsible for the evolution of multi cellelular organisms. These stromalolite somehow transformed the energy of sunlight and carbon dioxide into oxygen in the process of photosynthesis. Oxygen then came to the atmosphere through the sea and then came all the plants and trees. Slowly over a period of million years the sea creatures came to land and started evolving into reptiles, then came the dinosaurs, apes and so on. These apes then evolved into the most intelligent species in the known universe, humans. And then the civilizations started and rest is the history as we all know ."""

print(PlagiarismCheckWithGoogle({'data':'Gta','filter':[{'pattern':'\n'},{'pattern':'. '},{'pattern':'? '},{'pattern':'। '},{'pattern':' ','epos':25,'mineposreq':35}]}))