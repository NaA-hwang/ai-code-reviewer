import openai
import os
from github import Github

def get_diff(pull_number):
    # 환경 변수에서 리포지토리 정보 가져오기
    repo_name = os.getenv('GITHUB_REPOSITORY')  # 'username/repo' 형식으로 전달됨
    g = Github(os.getenv('GITHUB_TOKEN'))
    repo = g.get_repo(repo_name)  # 전달된 리포지토리 정보로 PR 접근
    pull = repo.get_pull(pull_number)
    
    # PR에서 변경된 코드(diff)를 가져옴
    diff = pull.diff()
    return diff

def generate_review(diff):
    prompt = f"""
    아래의 코드 변경 사항을 리뷰해주세요. 다음 기준으로 확인해주세요:
    1. 사전 조건 확인: 함수나 메서드가 정상 동작하기 위한 변수가 올바르게 설정되었는지
    2. 런타임 에러 확인: 런타임 에러가 발생할 가능성이 있는 코드
    3. 최적화: 더 효율적으로 작성할 수 있는 부분
    4. 보안: 보안 취약점이 있는지 확인
    
    코드 차이:
    {diff}
    """
    
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        temperature=0
    )
    return response.choices[0].text.strip()

if __name__ == "__main__":
    # GitHub Actions에서 제공하는 PR 번호와 리포지토리 정보 가져오기
    pull_number = int(os.getenv('GITHUB_PR_NUMBER'))
    
    # 코드 차이 가져오기 및 리뷰 생성
    diff = get_diff(pull_number)
    review = generate_review(diff)

    # 리뷰 내용을 저장합니다
    with open('review.txt', 'w') as f:
        f.write(review)
