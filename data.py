import streamlit as st 
import pandas as pd 
import kss 
import os 
from io import StringIO

class LabelData():
    def __init__(self, load_path = "./data/newsdata_edit_w_index.csv", save_path:str="", dataframe=None) -> None:
        self.load_path = load_path
        #self.dataframe = pd.read_csv(self.load_path)
        self.dataframe = dataframe
        self.updateflag = False 
        print("check the data", self.dataframe.head())
        self.save_path = save_path
        if os.path.isfile(save_path):
            self.labeled_df = pd.read_csv(save_path)
        # else: 
        #     self.labeled_df = pd.DataFrame({"index":[], "idx":[], "title":[], "body":[], "url":[], "url2":[], "key_sentences":[], "keywords": []})
        #     # self.labeled_df = self.dataframe[["index", "idx", "title", "body", "url", "url2"]].copy()
        #     # self.labeled_df["key_sentences"] = ''
        #     # self.labeled_df["keywords"] = ''
        
        if 'options' not in st.session_state:
            st.session_state['options'] = ''
        if 'keywords' not in st.session_state:
            st.session_state['keywords'] = ''
    
        
    def clear_options(self):
        st.session_state.input_options = st.session_state.options
        st.session_state.options = ""
        
    def clear_keywords(self):
        st.session_state.input_keywords = st.session_state.keywords
        st.session_state.keywords = ""
        
    def get_item(self, col:str='body', idx:int = 0):
        return self.dataframe.iloc[idx][col] #.values[0]

    def paragraph_to_sentences(self, context:str=""):
        sentences = kss.split_sentences(context)
        total_sentences = len(sentences)
        return pd.DataFrame({'문장번호': [i for i in range(total_sentences)], '문장': [s for s in sentences]})

    def show_articles(self, idx:int = 0):
        body = self.get_item(col = 'body', idx = idx)
        st.table(self.paragraph_to_sentences(body))
        
    def get_key_sent_and_words(self, idx:int = 0):
        # body = self.get_item(col = 'body', idx = idx)
        # options = st.multiselect("주요 구문 3문장을, 중요도 순으로 선택해주세요", [i for i in range(len(body))])
        st.text_input("주요 구문 3문장을, 중요도 순으로 입력해주세요 (예시: 1, 8, 9)", key='options', on_change=self.clear_options)
        options = st.session_state.get('input_options', '')
        st.text_input("주요 키워드(명사)를, 중요도 순으로 입력해주세요. (최대 5개, 예시: 삼성, ASML, 반도체)", key='keywords', on_change=self.clear_keywords)
        keywords = st.session_state.get('input_keywords', '') 
        
        st.write("선택하신 문장 정보: ", options)
            # if keywords and st.button("주요 키워드 입력 완료"):
        st.write("입력하신 키워드 정보: ", keywords)
        if options and keywords:
            return options, keywords 
        return False, False 

    def save_to_csv(self, idx:int = 0):
        options, keywords = self.get_key_sent_and_words(idx)
        # self.labeled_df.loc[idx, "key_sentences"] = str(options) #ValueError: Length of values (3) does not match length of index (1)
        # self.labeled_df.loc[idx, "keywords"] = keywords #ValueError: Length of values (3) does not match length of index (1)
        if keywords != False:
            print(f"save_to_csv options: {options}, keywords: {keywords}")
            labeled_df = pd.DataFrame(
                {
                "index": idx,
                "idx": self.dataframe.iloc[idx]["idx"],
                "title": self.dataframe.iloc[idx]["title"],
                "body": self.dataframe.iloc[idx]["body"],
                "url1": self.dataframe.iloc[idx]["url"],
                "url2": self.dataframe.iloc[idx]["url2"],
                "key_sentences": str(options),
                "keywords": keywords
                },
                index = [idx]
            )
                
            print("주요 구문 및 키워드 입력완료")
            st.table(labeled_df[['index', 'key_sentences', 'keywords']])
            
            os.makedirs(self.save_path, exist_ok=True) 
            labeled_df.to_csv(f"{self.save_path}/labeled.csv", index = False, mode = 'a', encoding = 'utf-8-sig')
    
    @st.cache
    def download_df(self):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return (pd.read_csv(f"{self.save_path}/labeled.csv")).to_csv().encode('utf-8-sig')


