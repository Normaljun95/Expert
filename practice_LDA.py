# -*- coding: utf-8 -*-

from multiprocessing.dummy import freeze_support
# from konlpy.tag import Komoran
import gensim
from gensim.corpora.dictionary import Dictionary
import nltk
from collections import Counter

if __name__=='__main__':
    freeze_support()
    
    stop_words = []
    with open('ko_stopword.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            x = line.strip()
            stop_words.append(x)
        
    
    _keywords = ['HDFS에서 적응형 캐시 관리 기법 스마트팩토리는 정보통신기술(ICT)를 이용한 공정의 모든 데이터를 수집, 분석하여 제어하고 있다. 기존보다 방대한 양의 데이터를 처리하기 위해 기업들은 하둡을 이용한다. 다양한 크기의  데이터가 나타나는 환경에서 HDFS을 효율적으로 관리하기 위한 적응형 캐시 관리 기법을 제안한다. 제안하는 기법은 데이터 노드의 로컬 디스크의 공간 이용 효율성을 높이고 평균 데이터 크기를 분석하여 데이터 노드 확장시  적합한 블록 크기를 적용할 수 있게 관리한다. 성능 평가를 통해 제안하는 기법의 데이터 노드에서 로컬 디스크 효율 향상과 읽기와 쓰기 속도의 속도에 효과를 보인다. Adaptive Cache Management Scheme in HDFS', '이미지   데이터 마이닝을 이용한 모바일 기반 금형 검색 시스템 4차 산업혁명 시대의 도래에 따라, ICBM(IoT, Cloud, Big-data, Mobile) 기술이 핵심요소로 부각 되고 있으며, 그에 힘입어 부품 제조 산업분야에서도 Idustry4.0 등의   스마트팩토리 기술이 각광을 받고 있다. 본 논문에서는 금형의 설계도면 정보와 그림파일을 수집하여 데이터베이스로 구축하고 사용자가 필요로 하는 금형에 대한 이미지만으로 금형에 대한 정보를 검색하여 매칭시켜 줄 수 있 는 모바일 기반의 시스템을 제안한다. A Mold Search System based on Mobile using Image Data Mining', '빅데이터 활성화 정책 및 응용 사례 다양한 정보 채널의 등장과 함께 빅데이터에 대한 중요성이 부각되고 있다. 본고  에서는 빅데이터를 활용한 응용을 활성화기 위해 국가별 빅데이터 정책을 분석하고 분야별로 빅데이터를 활용한 사례를 기술한다. 빅데이터를 활용하여 일상 생활에서 일반 사용자들이 사용할 수 있는 응용 서비스 원천 기술   및 서비스 기술을 개발하고 있는 충북대학교 빅데이터생활형 서비스 연구센터(BLSRC)를 소개하고 센터에서 개발한 응용 서비스를 기술한다. 또한 빅데이터 사용을 활성화하고 실생활에 응용하기 위한 방안을 제언한다. []', '  빅데이터 병렬 처리 기술 동향 [] []', '4차 산업혁명에서 빅데이터 [] []', '화장품 추천을 위한 개인의 피부 유형 및 유전자를 이용한 빅데이터 분석 기반 모바일 서비스 사람의 피부는 개인마다 상태의 차이가 있으며, 개인 의 피부 상태에 따가 피부고민도 다르다. 이에 따라, 일반 소비자들의 화장품 사용에 대한 선호도는 나만의 것, 내 피부에 맞는 화장품, 자세한 카운슬링 순으로 선호도가 나타나고 있다. 민간기관에서도 유전자 검사가 가능해 짐으로써 상기와 같이 피부에 대한 유전자 분석도 활성화되고 있는 실정으로, 본 논문에서는 개인의 피부 유형과 유전자 정보를 고려하고 소셜 네트워크에서의 데이터를 수집하여 빅데이터 분석을 통한 맞춤형 추천 서비스를   제안한다. Big-data Analysis based Mobile Services using Individual Skin-type and Genes for Cosmetic Recommendation', 'NoSQL 데이터베이스 엔진을 이용한 스토리지 벤치마킹 시스템 빅데이터 시대의 도래로 다양한 NoSQL 데이터베이스 엔진이 활용되고 있다. NoSQL 데이터베이스 엔진 기반의 다양한 응용들이 수행될 때 스토리지의 성능을 평가하기 위한 스토리지 벤치마킹 툴이 요구된다. 본 논문에서는 NoSQL 데이터베이스를 이용한 스토리지  벤치마킹 시스템을 설계한다. 제안하는 스토리지 벤치마킹 시스템은 IO 추적기를 통해 스토리지의 성능을 측정하고, 웹 UI를 통해 사용자 정의 워크로드 생성, 벤치마킹 실행, 결과 확인을 수행할 수 있다. Storage Benchmarking System Using NoSQL Database Engines', '노화 관련 유전자의 후성유전학적 접근 유전자 염기서열의 직접적인 변화 대신 후성기작을 통해 유전자 발현이 조절되는 후성유전은 크게 DNA 메틸화(methylation), 히스톤 변형(modification), ncRNA(non-coding RNA)로 제어가 가능하다. 후성유전을 이해하기 위해 노화 관련 유전자를 대상으로 데이터베이스를 구축하고 전반적인 연구결과를 살펴보고자 한다. 유전자의 프로모터(promoter), CpG island(CGI) 부위에 메틸화가 될 경우 다른 부위에 비해 유전자 발현에 큰 영향을 주므로, 특히 CGI 부위를 중심으로 전체 유전자 그룹과 노화 관련 유전자 그룹간의 분포도를 비교 분석하였다. 또한 ncRNA 중 miRNA와 노화 유전자와의  상호작용을 분석하였다. 이와 같은 분석접근 방법은 노화 관련 유전자의 조절을 이해하는데 도움이 될 것으로 사료된다. Epigenomic Approaches for Regulating Aging Related Genes', '이미지 데이터 마이닝을 이용한 모바일  기반 금형 검색 시스템 4차 산업혁명 시대의 도래에 따라, ICBM(IoT, Cloud, Big-data, Mobile) 기술이 핵심요소로 부각 되고 있으며, 그에 힘입어 부품 제조 산업분야에서도 Idustry4.0 등의 스마트팩토리 기술이 각광을 받고  있다. 본 논문에서는 금형의 설계도면 정보와 그림파일을 수집하여 데이터베이스로 구축하고 사용자가 필요로 하는 금형에 대한 이미지만으로 금형에 대한 정보를 검색하여 매칭시켜 줄 수 있는 모바일 기반의 시스템을 제안  한다. A Mold Search System based on Mobile using Image Data Mining', 'YCSB 기반의 데이터베이스 엔진 벤치마킹 GUI 설계 최근 데이터베이스에서 다루는 데이터의 크기가 커짐에 따라 SQL DB 대신 NoSQL DB의 사용이 증가  하고 있다. 이런 변화에 따라 NoSQL과 저장장치에 대한 벤치마킹 및 분석을 통한 저장장치 성능 최적화 및 성능 평가 방법 개선이 필요하다. 본 논문에서는 기존 벤치마킹 툴의 조작 불편함을 해소하기 위해서 사용자의 편의성 을 고려한 간편한 벤치마킹 시스템 GUI를 설계한다. 시각화 툴을 활용하여 벤치마킹 결과의 분석을 용이하게 할 수 있는 환경을 제공해준다. Design of GUI for Benchmarking Database Engines Using YCSB', 'NoSQL 데이터베이 스 엔진을 이용한 스토리지 벤치마킹 시스템 빅데이터 시대의 도래로 다양한 NoSQL 데이터베이스 엔진이 활용되고 있다. NoSQL 데이터베이스 엔진 기반의 다양한 응용들이 수행될 때 스토리지의 성능을 평가하기 위한 스토리지  벤치마킹 툴이 요구된다. 본 논문에서는 NoSQL 데이터베이스를 이용한 스토리지 벤치마킹 시스템을 설계한다. 제안하는 스토리지 벤치마킹 시스템은 IO 추적기를 통해 스토리지의 성능을 측정하고, 웹 UI를 통해 사용자 정의  워크로드 생성, 벤치마킹 실행, 결과 확인을 수행할 수 있다. Storage Benchmarking System Using NoSQL Database Engines', '그래프 데이터 기반의 지반 탐사 시스템 최근 지반이 가라앉아 지면에 구멍이 발생하는 싱크홀(Sink Hole)의 발생이 빈번하게 발생하고 있으며, 이에 대한 피해사례도 증가하고 있다. 이를 예방하고 대응하기 위하여 국가적으로 대대적인 지반조사를 하고 있으며 해당 지반을 탐사하기 위하여 지표투과레이더와 내시경 등을   활용한 방법을 사용하고 있다. 본 논문에서는 현재까지 가장 효율적인 방법으로 알려진 지표투과레이더의 데이터를 그래프 형태로 표현하고 분석하여 효과적으로 탐사를 할 수 있는 시스템을 제안한다. A Ground Discovery System based on Graph Data', '스트림 그래프에서 서브 그래프 패턴 분석을 이용한 이상 패턴 감지 그래프에서 이상 패턴은 정상 그래프와 상이하게 다른 양상을 갖는 그래프를 의미한다. 이상 패턴을 판단하기 위해서는 정상데  이터 정확한 정의가 요구된다. 본 논문에서는 스트림 그래프에서 실시간으로 이상 패턴을 감지하는 기법을 제안한다. 제안하는 기법은 정상 서브그래프의 패턴(정상 패턴)을 정의하고 정점 간 연결 관계를 고려한다. Anomaly Detection Using Subgraph Pattern Analysis in Graph Streams', '구조적 차이를 고려한 서브 그래프 매칭을 위한 요약 색인 기법 생명 공학 분야에서는 노이즈가 많고 불완전한 데이터 집합의 사용이 많이 이루어진다. 불완전  한 그래프에서 구조적 차이를 고려한 근사 서브 그래프 매칭에 대한 활용이 이루어지고 있다. 본 논문에서는 기존 기법에서 모든 데이터 및 경우의 수를 색인하는 과도한 색인 문제와 계산 비용 감소를 위한 요약 색인 기법을  제안한다. 구조적 차이 정보를 저장하기 위해서 특정 정점간의 최단 거리 값을 관리하고, 색인 부하 감소 및 일관성을 위해 요약 색인에 대한 간결화 작업을 수행한다. Summary Indexing Scheme for Subgraph Matching Considering Structural Differences', '화장품 추천을 위한 개인의 피부 유형 및 유전자를 이용한 빅데이터 분석 기반 모바일 서비스 사람의 피부는 개인마다 상태의 차이가 있으며, 개인의 피부 상태에 따가 피부고민도 다르다. 이  에 따라, 일반 소비자들의 화장품 사용에 대한 선호도는 나만의 것, 내 피부에 맞는 화장품, 자세한 카운슬링 순으로 선호도가 나타나고 있다. 민간기관에서도 유전자 검사가 가능해짐으로써 상기와 같이 피부에 대한 유전자   분석도 활성화되고 있는 실정으로, 본 논문에서는 개인의 피부 유형과 유전자 정보를 고려하고 소셜 네트워크에서의 데이터를 수집하여 빅데이터 분석을 통한 맞춤형 추천 서비스를 제안한다. Big-data Analysis based Mobile  Services using Individual Skin-type and Genes for Cosmetic Recommendation', '전자상거래에서 상품 신뢰도를 고려한 개인화 추천 전자상거래가 대중화되면서 다양한 아이템을 손쉽게 구매할 수 있는 환경이 조성되었다. 전 자상거래에서 소비자의 구매율을 향상시키기 위해 개인 맞춤 추천 서비스가 요구되고 있다. 본 논문에서는 사용자 성향과 제품의 신뢰성을 고려한 상품 추천 기법을 제안한다. 사용자의 성향은 찜하기, 리뷰, 클릭 등과 같은   다양한 사용자의 행위 분석을 통해 추출하고 상품의 신뢰성은 SNS에서의 언급 수와 서비스내의 사용자 행위를 통해 계산한다. 계산된 성향을 기반으로 협업 필터링을 수행하여 상품별 예측 점수를 생성하고 상품의 신뢰성을 고 려하여 최종적인 추천 목록을 생성한다. Personalized Recommendation Considering Item Reliability in E-Commerce', '스트림 그래프에서 서브 그래프 패턴 분석을 이용한 이상 패턴 감지 그래프에서 이상 패턴은 정상 그래프 와 상이하게 다른 양상을 갖는 그래프를 의미한다. 이상 패턴을 판단하기 위해서는 정상데이터 정확한 정의가 요구된다. 본 논문에서는 스트림 그래프에서 실시간으로 이상 패턴을 감지하는 기법을 제안한다. 제안하는 기법은  정상 서브그래프의 패턴(정상 패턴)을 정의하고 정점 간 연결 관계를 고려한다. Anomaly Detection Using Subgraph Pattern Analysis in Graph Streams', '구조적 차이를 고려한 서브 그래프 매칭을 위한 요약 색인 기법 생명  공학 분야에서는 노이즈가 많고 불완전한 데이터 집합의 사용이 많이 이루어진다. 불완전한 그래프에서 구조적 차이를 고려한 근사 서브 그래프 매칭에 대한 활용이 이루어지고 있다. 본 논문에서는 기존 기법에서 모든 데이터  및 경우의 수를 색인하는 과도한 색인 문제와 계산 비용 감소를 위한 요약 색인 기법을 제안한다. 구조적 차이 정보를 저장하기 위해서 특정 정점간의 최단 거리 값을 관리하고, 색인 부하 감소 및 일관성을 위해 요약 색인에  대한 간결화 작업을 수행한다. Summary Indexing Scheme for Subgraph Matching Considering Structural Differences', '간선 유형 및 가중치를 고려한 연속 서브 그래프 매칭 기법 논문 검색 서비스 응용에서는 공저자, 출판  정보 등을 표현하기 위해서 다양한 정점 레이블 (논문,저자) 및 간선 정보(주저자, 공저자)를 이용하여 그래프로 표현한다. 이와 함께 다양한 간선 특징 정보를 질의로 입력하는 연속 서브 그래프 매칭에 대한 요구가 존재한  다. 본 논문에서는 간선의 다양한 특성을 지원하고 색인의 부하를 감소시킨 연속 서브 그래프 매칭 기법을 제안한다. 제안하는 기법은 거리 값과 질의 연관 정보만을 관리하여 간선의 다양한 특성을 지원하는 효율적인 서브 그 래프 매칭을 수행한다. Continuous Subgraph Matching Scheme Considering Edge Types and Weights', '그래프 스트림에서 효율적인 근사 Top-k 서브 그래프 매칭 기법 IoT 및 SNS의 발달로 인해 관계를 표현하는 그래프 모델링  기법이 활용되고 있다. 실시간 스트림 그래프에서 유사한 모형의 그래프를 탐색하기 위한 근사 Top-k 서브 그래프 매칭에 대한 요구가 증가하고 있다. 본 논문에서는 그래프 스트림에서 간선의 유형 및 구조적 차이를 고려한  효율적인 근사 Top-k 서브 그래프 매칭 기법을 제안한다. 임계값 기반의 필터링과 스트림 환경에 맞는 연속 서브 그래프 매칭 구조를 제안함으로써 그래프 스트림에 적합한 질의 처리를 수행한다. Efficient Approximate Top-k Subgraph Matching Scheme in Graph Stream', 'YCSB 기반의 데이터베이스 엔진 벤치마킹 GUI 설계 최근 데이터베이스에서 다루는 데이터의 크기가 커짐에 따라 SQL DB 대신 NoSQL DB의 사용이 증가하고 있다. 이런 변화에 따  라 NoSQL과 저장장치에 대한 벤치마킹 및 분석을 통한 저장장치 성능 최적화 및 성능 평가 방법 개선이 필요하다. 본 논문에서는 기존 벤치마킹 툴의 조작 불편함을 해소하기 위해서 사용자의 편의성을 고려한 간편한 벤치마킹  시스템 GUI를 설계한다. 시각화 툴을 활용하여 벤치마킹 결과의 분석을 용이하게 할 수 있는 환경을 제공해준다. Design of GUI for Benchmarking Database Engines Using YCSB', 'NoSQL 데이터베이스 엔진을 이용한 스토리지  벤치마킹 시스템 빅데이터 시대의 도래로 다양한 NoSQL 데이터베이스 엔진이 활용되고 있다. NoSQL 데이터베이스 엔진 기반의 다양한 응용들이 수행될 때 스토리지의 성능을 평가하기 위한 스토리지 벤치마킹 툴이 요구된다.  본 논문에서는 NoSQL 데이터베이스를 이용한 스토리지 벤치마킹 시스템을 설계한다. 제안하는 스토리지 벤치마킹 시스템은 IO 추적기를 통해 스토리지의 성능을 측정하고, 웹 UI를 통해 사용자 정의 워크로드 생성, 벤치마킹   실행, 결과 확인을 수행할 수 있다. Storage Benchmarking System Using NoSQL Database Engines', 'YCSB 기반의 데이터베이스 엔진 벤치마킹 GUI 설계 최근 데이터베이스에서 다루는 데이터의 크기가 커짐에 따라 SQL DB 대신  NoSQL DB의 사용이 증가하고 있다. 이런 변화에 따라 NoSQL과 저장장치에 대한 벤치마킹 및 분석을 통한 저장장치 성능 최적화 및 성능 평가 방법 개선이 필요하다. 본 논문에서는 기존 벤치마킹 툴의 조작 불편함을 해소하기  위해서 사용자의 편의성을 고려한 간편한 벤치마킹 시스템 GUI를 설계한다. 시각화 툴을 활용하여 벤치마킹 결과의 분석을 용이하게 할 수 있는 환경을 제공해준다. Design of GUI for Benchmarking Database Engines Using YCSB', 'NoSQL 데이터베이스 엔진을 이용한 스토리지 벤치마킹 시스템 빅데이터 시대의 도래로 다양한 NoSQL 데이터베이스 엔진이 활용되고 있다. NoSQL 데이터베이스 엔진 기반의 다양한 응용들이 수행될 때 스토리지의 성능을  평가하기 위한 스토리지 벤치마킹 툴이 요구된다. 본 논문에서는 NoSQL 데이터베이스를 이용한 스토리지 벤치마킹 시스템을 설계한다. 제안하는 스토리지 벤치마킹 시스템은 IO 추적기를 통해 스토리지의 성능을 측정하고, 웹  UI를 통해 사용자 정의 워크로드 생성, 벤치마킹 실행, 결과 확인을 수행할 수 있다. Storage Benchmarking System Using NoSQL Database Engines', '화장품 추천을 위한 개인의 피부 유형 및 유전자를 이용한 빅데이터 분석  기반 모바일 서비스 사람의 피부는 개인마다 상태의 차이가 있으며, 개인의 피부 상태에 따가 피부고민도 다르다. 이에 따라, 일반 소비자들의 화장품 사용에 대한 선호도는 나만의 것, 내 피부에 맞는 화장품, 자세한 카운슬  링 순으로 선호도가 나타나고 있다. 민간기관에서도 유전자 검사가 가능해짐으로써 상기와 같이 피부에 대한 유전자 분석도 활성화되고 있는 실정으로, 본 논문에서는 개인의 피부 유형과 유전자 정보를 고려하고 소셜 네트워  크에서의 데이터를 수집하여 빅데이터 분석을 통한 맞춤형 추천 서비스를 제안한다. Big-data Analysis based Mobile Services using Individual Skin-type and Genes for Cosmetic Recommendation', '화장품 추천을 위한 개인 의 피부 유형 및 유전자를 이용한 빅데이터 분석 기반 모바일 서비스 사람의 피부는 개인마다 상태의 차이가 있으며, 개인의 피부 상태에 따가 피부고민도 다르다. 이에 따라, 일반 소비자들의 화장품 사용에 대한 선호도는 나 만의 것, 내 피부에 맞는 화장품, 자세한 카운슬링 순으로 선호도가 나타나고 있다. 민간기관에서도 유전자 검사가 가능해짐으로써 상기와 같이 피부에 대한 유전자 분석도 활성화되고 있는 실정으로, 본 논문에서는 개인의 피 부 유형과 유전자 정보를 고려하고 소셜 네트워크에서의 데이터를 수집하여 빅데이터 분석을 통한 맞춤형 추천 서비스를 제안한다. Big-data Analysis based Mobile Services using Individual Skin-type and Genes for Cosmetic Recommendation', '화장품 추천을 위한 개인의 피부 유형 및 유전자를 이용한 빅데이터 분석 기반 모바일 서비스 사람의 피부는 개인마다 상태의 차이가 있으며, 개인의 피부 상태에 따가 피부고민도 다르다. 이에 따라, 일 반 소비자들의 화장품 사용에 대한 선호도는 나만의 것, 내 피부에 맞는 화장품, 자세한 카운슬링 순으로 선호도가 나타나고 있다. 민간기관에서도 유전자 검사가 가능해짐으로써 상기와 같이 피부에 대한 유전자 분석도 활성  화되고 있는 실정으로, 본 논문에서는 개인의 피부 유형과 유전자 정보를 고려하고 소셜 네트워크에서의 데이터를 수집하여 빅데이터 분석을 통한 맞춤형 추천 서비스를 제안한다. Big-data Analysis based Mobile Services using Individual Skin-type and Genes for Cosmetic Recommendation']
    # _keywords = []
    # komoran = Komoran()

    divide_result = []

    for text in _keywords:
        # noun_words = komoran.nouns(text)
        # divide_result.append(noun_words)
        if text is not None and text != 'None' and text != "" and isinstance(text, str) :
            # divide_result.append([word for word, pos in nltk.pos_tag(nltk.word_tokenize(text)) if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')])
            divide_result.append([word for word, pos in nltk.pos_tag(nltk.word_tokenize(text)) if (pos.startswith('N')) if word not in stop_words and len(word) > 2])
    # print(divide_result)

    dictResult = Dictionary(divide_result)
    # print(dictResult.token2id)
    # print(dictResult)
    
    bow_corpus = [dictResult.doc2bow(document) for document in divide_result]
    # print(bow_corpus)
    lda_model = gensim.models.LdaMulticore(corpus=bow_corpus, id2word=dictResult, num_topics=5)

    topic_list = []
    topic_result = []
    josa = ["을", "를", "에서", "에"]
    for idx in range(5):
        # print(idx)
        # print("Topic_num: {} ".format(idx))
        topic_set = lda_model.show_topic(idx, 5)
        for word in topic_set:
        # for word, score in topic_set:
            if word in josa:
            topic_list.append(word)
            # topic_list.append(topic_set)
        print(topic_set)
        # print("Topic: {} \nWords: {}".format(idx, topic_set))
    # print(topic_list)
    # count_topic = Counter(topic_list).most_common(n=5)
    # for topic, num in count_topic:
    #     topic_result.append(topic)
    # print(topic_result)