import openai
import os
from github import Github

def get_diff(pull_number):
    # 환경 변수에서 리포지토리 정보 가져오기
    repo_name = os.getenv('GITHUB_REPOSITORY')
    g = Github(os.getenv('GH_TOKEN'))
    repo = g.get_repo(repo_name)
    pull = repo.get_pull(pull_number)

    # PR에서 변경된 파일 목록을 가져와 diff 생성
    files = pull.get_files()
    diff = ""
    for file in files:
        diff += f"File: {file.filename}\n"  # 파일 이름 추가
        diff += f"Changes: {file.patch}\n\n"  # 변경된 부분 추가

    return diff

def generate_review(diff):
    prompt = f"""
    You are a strict and perfect code reviewer. You cannot tell any lies.
    Please evaluate the code added or changed through Pull Requests.

    According to the given evaluation criteria, if a code patch corresponds to any of the issues below, 

    There are four evaluation criteria. If multiple issues correspond to a single criteria , you should address them in a detailed manner:
        - Feedback should describe what the issue is according to the evaluation criteria.
        - Relevant_Lines should be written as "[line_num]-[line_num]", indicating the range of lines where the issue occurs.
        - Suggested_Code should only include the revised code based on the feedback.

    If a criterion applies, none of the elements within that criterion (Feedback, Relevant_Lines, Suggested_Lines) should be omitted.

    If there are multiple entries corresponding to a criterion, include them within the same response.
    If there are no issues corresponding to any of the criteria, return only the string 'No Issues Found'.

    The evaluation criteria are:
        - Pre-condition_check: Check whether a function or method has the correct state or range of values for the variables needed to operate properly.
        - Runtime Error Check: Check code for potential runtime errors and identify other possible risks.
        - Security Issue: Check if the code uses modules with serious security flaws or contains security vulnerabilities.
        - Optimization: Check for optimization points in the code patch. If the code is deemed to have performance issues, recommend optimized code.

    You must follow the given YAML format exactly, and the output must be completely precise.
    You should ensure that all answers are in Korean.
    
    Code comparison will be given by the user.
    """
    
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": prompt},
                    {"role": "user", "content": diff}],
        temperature=0
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    # GitHub Actions에서 제공하는 PR 번호와 리포지토리 정보 가져오기
    pull_number = int(os.getenv('GITHUB_PR_NUMBER'))
    
    # 코드 차이 가져오기 및 리뷰 생성
    diff = get_diff(pull_number)
    review = generate_review(diff)

    # 리뷰 내용을 저장합니다
    with open('review.txt', 'w') as f:
        f.write(review)
