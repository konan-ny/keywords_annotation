import os  
import streamlit as st 
import data
import pandas as pd 


def main_page():
    st.title("주요 구문 라벨링")
    # NAME_FLAG = False
    uploaded_file = st.file_uploader("파일을 업로드해주세요.")
    if uploaded_file is not None:
        labeldata = pd.read_csv(uploaded_file)

        user_home = os.path.expanduser("~")
        labeldata = data.LabelData(save_path = os.path.join(user_home, 'Downloads'), dataframe=labeldata) 
        
    prev_idx = 0
    idx = st.text_input("기사 번호를 입력해주세요.")
    if idx != '':
        if prev_idx != idx:
            prev_idx =idx
            # labeldata(flag=True)            
            st.write(idx, "번 기사입니다.") 
            idx = int(idx)
            st.write("url1", labeldata.get_item(col="url", idx=idx))
            st.write("url2", labeldata.get_item(col="url2", idx=idx))
            labeldata.show_articles(idx)
            try:
                print("labeled_df의 길이", len(labeldata.labeled_df))
            except:
                pass
            labeldata.save_to_csv(int(idx))


    if st.button("라벨링 종료"):
        st.write("라벨링 작업을 종료하고 결과물을 확인합니다.")
        #export 작업 
        st.download_button(
        label="Download data as CSV",
        data=labeldata.download_df(),
        file_name='labeled_data.csv',
        mime='text/csv',
        )

if __name__ == "__main__":
    main_page()