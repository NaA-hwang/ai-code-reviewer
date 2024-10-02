import os
from github import Github

def post_comment(review_text, pull_number):
    g = Github(os.getenv('GITHUB_TOKEN'))
    repo = g.get_repo('your-username/your-repo')  # 자신의 GitHub 리포지토리 정보
    pull = repo.get_pull(pull_number)
    
    # PR에 코멘트 작성
    pull.create_issue_comment(review_text)

if __name__ == "__main__":
    # GitHub Actions에서 제공하는 PR 번호를 사용
    pull_number = int(os.getenv('GITHUB_PR_NUMBER'))

    # 저장된 리뷰 파일을 읽고 코멘트로 남김
    with open('review.txt', 'r') as f:
        review = f.read()
    post_comment(review, pull_number)
