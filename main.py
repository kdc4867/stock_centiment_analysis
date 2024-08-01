# main.py

import os
from src.data_loader import load_existing_data, save_data, load_stock_data
from src.sentiment_analysis import analyze_new_data
from src.scraper import scrape_finviz_news
from src.strategy_evaluation import evaluate_strategy

if __name__ == "__main__":
    output_file = 'data/finviz_sentiment_analysis_results.csv'
    stock_data_file = 'data/stock_prices.csv'
    
    # 기존 데이터 로드
    existing_data = load_existing_data(output_file)
    
    # FinViz 뉴스 스크래핑
    print("FinViz 뉴스 스크래핑 중...")
    news_data = scrape_finviz_news(days=30)

    # 새로운 데이터 분석 및 기존 데이터와 병합
    print("새로운 데이터 분석 중...")
    updated_results = analyze_new_data(news_data, existing_data)

    # 주식 가격 데이터 로드 및 병합
    stock_data = load_stock_data(stock_data_file)
    merged_data = pd.merge(updated_results, stock_data, left_index=True, right_index=True, how='inner')
    
    # 결과 저장
    save_data(updated_results, output_file)
    
    # 투자 전략 평가
    print("투자 전략 평가 중...")
    evaluate_strategy(merged_data)
    
    print(f"분석 결과가 {output_file} 파일로 저장되었습니다.")
    print(f"총 {len(updated_results)} 개의 항목이 저장되었습니다.")
