from api.berts import UniversalSentenceEncoder as USE
import pandas as pd

def similar_pair(question, content, embeddf, category):

    similar_df_USE = USE.get_similar_USE(question, embeddf, category)
    similar_df_USE["similar_title"] = question
    similar_df_USE["similar_content"] = content
    similar_df_USE = similar_df_USE.reindex(columns = ["similar_title", "similar_content", "title", "content","answer","panrye","percent"])

    return similar_df_USE


# if __name__ == "__main__":

#     embed_df = pd.read_pickle("api/berts/embed_df.pkl")

#     category = input("카테고리를 선택하세요")
#     question = input("제목을 입력하세요")
#     content = input("내용을 입력하세요")

#     print(similar_pair(category, question, content, embed_df))