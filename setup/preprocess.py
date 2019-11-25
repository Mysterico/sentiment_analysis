import re
import csv

# 전처리하는 부분
# 커멘트의 내용들이 한국어가 없을 경우, 이를 제거해야 함.

hangul = re.compile('[^ㄱ-ㅣ가-힣]+')  # 한글 정규식

def santize_sentences():
    """
    한글 제외, 전부 없애는 메소드
    :return:
    """

    textList = []

    with open("result.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=",")
        miniList = []

        for row in reader:
            likeCount = row[0]
            commentCount = row[1]
            commentList = eval(row[2])
            createDate = row[3]
            content = row[4]

            for comment in commentList:
                if comment == '':
                    del comment
                else:
                    comment = hangul.sub(" ", comment)
                    if comment.strip() == "":
                        del comment
                    else:
                        miniList.append(comment.strip())

            content = hangul.sub(" ", content)

            if content.strip() != "":
                miniList.append(content.strip())

            for text in miniList:
                textList.append(text)

    return textList