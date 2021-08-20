# coding: utf-8
#用於獲取該目錄下得所有txt檔案，忽略掉資料夾及裡面的
import glob
#主要是一些路徑的操作
import os
#對句子進行分詞或關鍵詞提取
from jieba import analyse
import jieba

jieba.set_dictionary('/home/test/linebot_project/linebot_project/dict.txt.big')
# 獲取當前pyhtho檔案所在的目錄：當前是：C:\gongoubo\python-work\direc\files
dir_path = os.path.dirname(os.path.abspath(__file__))
# print(dir_path)
txt_path = "/home/test/linebot_project/linebot_project/nutrient_txt"
#儲存txt檔案的絕對路徑為列表，同時為每個檔案建立索引
def file_store():
    files_name =[]
    files_dict = {}
#     a = [x.split('\/')[-1] for x in glob.glob('/home/test/linebot_project/linebot_project/nutrient_txt/nutrient_txt/*.txt')]
    a = [x.split("/")[-1] for x in glob.glob('/home/test/linebot_project/linebot_project/nutrient_txt/*.txt')]
#     print(a)
    #獲取file資料夾下所有為txt的檔案
    for i,name in enumerate(a):
        files_dict[i] = name.split('/')[-1]
        file_name = txt_path + "/" + name
        files_name.append(file_name)
    return files_name,files_dict


#讀取每個txt檔案
def transform(files_name):
    #注意開啟的時候需要申明為utf-8編碼
    for i,j in enumerate(files_name):
        #開啟檔案
        tmp = open(j,'r',encoding='utf-8').read()
        #提取關鍵詞
        # content = analyse.extract_tags(tmp)
        content = jieba.cut_for_search(tmp)
        words = []
        for word in tmp:
            words.append(word)
# 　　　　 #也可以進行分詞content=jieba.cut_for_search(tmp)，關於jieba分詞，可以看我的自然語言處理之基礎技能
        #新建process資料夾
        path=dir_path+'/file/'+'process'
        if not os.path.exists(path):
            os.makedirs(path)
        #為儲存關鍵詞的txt取名，對應這每個檔案的索引
        fp=open(path+'\\'+str(i)+'.txt','w',encoding='utf-8')
        #將關鍵詞寫入到txt中
        fp.write(" ".join(content))
        fp.write(" ".join(tuple(words)))
        fp.close()


#建立倒排索引
def invert_index():
    path=dir_path+'/file/'+'process'
    word_dict = {}
    # 取包含關鍵詞的txt
    for file in glob.glob(path+'/*.txt'):
        #取出txt檔名，也就是檔案的索引
        index = file.split('/')[-1].split('.')[0]
        # print(file)
        # print(index)
        #開啟檔案，並將關鍵詞儲存為列表
        with open(file,'r',encoding='utf-8') as fp:
            word_list=fp.read().split(" ")
        #建立倒排索引，如果單詞不在單詞字典中，就儲存檔案的索引，否則就新增索引到索引列表後
        for word in word_list:
            if word not in word_dict:
                word_dict[word]=[index]
            else:
                word_dict[word].append(index)
    # print(word_dict)
    return word_dict

def get_topk(count,topk=None):
    # print(count)
    file_index = []
    #如果topk超出了返回的數目，則有多少顯示多少
    if topk > len(count):
        for i in range(0,len(count)):
            file_index.append(int(count[i][0]))
        return file_index
    if len(count)<0:
        print("沒有找到相關的檔案")
        return False
    else:
        for i in range(0,topk):
            file_index.append(int(count[i][0]))
    return file_index

#得到檔名
def get_files(file_index,files_dict):
    res=[]
    for i in file_index:
        res.append(files_dict[i])
    return res

def main(words):
    # print("請輸入要查詢的內容，不同單詞間','隔開：")
    # words = input()
    seg_list = jieba.cut_for_search(words)
    keywords = ",".join(tuple(seg_list))
    for keyword in words:
        dohow = ',' + keyword
        keywords += dohow


    # key_word = ",".join(tuple(seg_list))
    # print(keywords)
    words = keywords.split(',')
    #獲得檔名和檔名索引字典
    files_name, files_dict = file_store()
    #提取關鍵詞或分詞
    transform(files_name)
    #倒排索引建立
    word_dict = invert_index()
    count={}
    #統計檔案索引的次數
    for word in words:
        if word in word_dict:
            for file in word_dict[word]:
                if file not in count:
                    count[file]=1
                else:
                    count[file]+=1
        else:
            continue
    #按次數從大到小排列
    count=sorted(count.items(),key=lambda i:i[1],reverse=True)
    #返回前k個檔案索引
    file_index=get_topk(count,topk=3)
    if file_index != False:
        # print("與之描述最可能的檔案是：")
        #返回檔名，並輸出結果
        res=get_files(file_index,files_dict)
        # print(res)
        result = res[0].split('.')[0] + '以及' + res[1].split('.')[0]
        return result


if __name__ == '__main__':

    main()
