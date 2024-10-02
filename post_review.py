import os
import json
from github import Github

def post_review_comments(review_comments, pull_number):
    repo_name = os.getenv('GITHUB_REPOSITORY')
    g = Github(os.getenv("GITHUB_TOKEN"))
    repo = g.get_repo(repo_name)
    pull = repo.get_pull(pull_number)
    
    # PR에 리뷰 생성
    pull.create_review(
        event="COMMENT",
        comments=review_comments
    )

if __name__ == "__main__":
    # GitHub Actions에서 제공하는 PR 번호 가져오기
    pull_number = int(os.getenv('GITHUB_PR_NUMBER'))
    
    # 저장된 리뷰 코멘트 파일 읽기
    with open('review_comments.json', 'r') as f:
        review_comments = json.load(f)
    
    # 리뷰 코멘트 PR에 추가하기
    post_review_comments(review_comments, pull_number)
