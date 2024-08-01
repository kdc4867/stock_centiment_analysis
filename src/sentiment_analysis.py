# src/sentiment_analysis.py

from openai import OpenAI
import json
import time
import os
from dotenv import load_dotenv

# .env 파일의 환경 변수 로드
load_dotenv()

# 환경 변수에서 API 키 가져오기
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

def predict_sentiment(headline, company):
    try:
        prompt = f"Forget all your previous instructions. Pretend you are a financial expert. You are a financial expert with stock recommendation experience. Answer “YES” if good news, “NO” if bad news, or “UNKNOWN” if uncertain in the first line. Then elaborate with one short and concise sentence on the next line. Is this headline good or bad for the stock price of {company} in the short term? Headline: {headline}"
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)['sentiment']
    except Exception as e:
        print(f"API 호출 중 오류 발생: {str(e)}")
        return None

def analyze_new_data(news_df, existing_df):
    existing_headlines = set(existing_df['Headline'])
    new_results = []
    for date, row in news_df.iterrows():
        if row['Headline'] not in existing_headlines:
            company_name = row['Headline'].split()[0]  # 예시: 헤드라인의 첫 단어를 회사 이름으로 가정
            sentiment = predict_sentiment(row['Headline'], company_name)
            new_results.append({
                'Date': date,
                'Headline': row['Headline'],
                'Company': company_name,
                'Predicted Sentiment': sentiment
            })
            time.sleep(1)  # API 호출 제한을 피하기 위한 지연
    
    new_df = pd.DataFrame(new_results).set_index('Date')
    return pd.concat([existing_df, new_df])
