from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
import os 
from git import Repo
from pathlib import Path

gemini_api_key = os.getenv("GEMINI_API_TOKEN")
gemini_model = "gemini-2.5-flash"

repo_root = Path(__file__).resolve().parent.parent.parent

repo = Repo(repo_root)

old_commit_hexsha = repo.commit("HEAD~1").hexsha
new_commit_hexsha = repo.commit("HEAD").hexsha  


changed_fileName = repo.git.diff(old_commit_hexsha, new_commit_hexsha, name_only=True)
changed_summary = repo.git.diff(old_commit_hexsha, new_commit_hexsha)

files = changed_fileName.strip().split("\n") if changed_fileName else []
files_summary = changed_summary.strip().split("\n") if changed_summary else []

print(files)

class DocUpdateResult(BaseModel):
    docs_update_required: bool = Field(
        description="True if the code changes require README updates (e.g. new endpoints, setup, or behavior)."
    )
    new_readme_content: str = Field(
        description="The complete README.md content. If docs_update_required is False, return the current README unchanged. If True, return the rewritten README that reflects the code changes (same structure: title, setup, run, endpoints table, examples)."
    )

parser = PydanticOutputParser(pydantic_object=DocUpdateResult)

# prompt = ChatPromptTemplate.from_messages([
#     ("system", """
#     You are a helpful assistant that analyzes code changes and determines if documentation needs to be updated.
#     1. Here are the files that were changed: {files}
#     2. Here is the summary of the changes: {files_summary}
#     3. If documentation needs to be updated, return the complete README.md content that reflects the code changes.
#     4. If documentation does not need to be updated, return the current README unchanged.
#     5. Return the result in the format specified below (no other text).

#     {format_instructions}
#     """),
# ]).partial(format_instructions=parser.get_format_instructions())



prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that analyzes code changes and determines if documentation needs to be updated. If documentation needs to be updated, return the complete README.md content that reflects the code changes but make sure to maintain the same structure and format. If not, return the current README unchanged. Return only valid JSON in the format specified, no other text."),
    ("human", """Files changed: {files}

Summary of changes:
{files_summary}

{format_instructions}"""),
]).partial(format_instructions=parser.get_format_instructions())



model = ChatGoogleGenerativeAI(model=gemini_model, api_key=gemini_api_key)

chain = prompt | model | parser

# result = chain.invoke({
#     "files": files,
#     "files_summary": files_summary,
# })

# print(result)
class MockResult:
    docs_update_required = True
    new_readme_content = "# Updated README\n\nThis is a mocked README update for testing purposes."

result = MockResult()

readme_path = repo_root / "README.md"


if not (result.docs_update_required and result.new_readme_content):
    print("No README update (docs_update_required=False or empty content)")
else:
    # Unique branch name for this run
    short_sha = repo.commit("HEAD").hexsha[:7]
    branch_name = f"docs/auto-update-{short_sha}"

    # Create and checkout new branch (from current HEAD)
    new_branch = repo.create_head(branch_name)
    new_branch.checkout()

    # Write README, stage, commit
    readme_path.write_text(result.new_readme_content, encoding="utf-8")
    repo.index.add(["README.md"])
    # Git config required for commit in CI
    try:
        name = repo.config_reader().get_value("user", "name", default=None)
        email = repo.config_reader().get_value("user", "email", default=None)
    except Exception:
        name = None
        email = None
    if not name:
        repo.config_writer().set_value("user", "name", "github-actions[bot]").release()
    if not email:
        repo.config_writer().set_value("user", "email", "github-actions[bot]@users.noreply.github.com").release()
    repo.index.commit("docs: auto-update README from merge")
    print(f"Committed README on branch {branch_name}")

    # Push branch (use GITHUB_TOKEN in CI)
    token = os.getenv("GITHUB_TOKEN")
    origin = repo.remote("origin")
    url = origin.url
    if token:
        if url.startswith("https://"):
            origin.set_url(url.replace("https://", f"https://x-access-token:{token}@"))
        elif url.startswith("git@"):
            origin.set_url(f"https://x-access-token:{token}@github.com/" + url.replace("git@github.com:", "").replace(".git", "") + ".git")
    try:
        origin.push(new_branch.name)
        print(f"Pushed {branch_name}")
    except Exception as e:
        print(f"Push failed: {e}")
        raise
    finally:
        if token and origin.url != url:
            origin.set_url(url)  # restore original URL

    # Create PR via GitHub API
    repo_slug = os.getenv("GITHUB_REPOSITORY")
    if repo_slug and token:
        resp = requests.post(
            f"https://api.github.com/repos/{repo_slug}/pulls",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json",
            },
            json={
                "title": "docs: auto-update README",
                "head": branch_name,
                "base": "main",
                "body": "Auto-generated PR from doc-update-agent after merge to main.",
            },
        )
        if resp.status_code == 201:
            print(f"Opened PR: {resp.json().get('html_url')}")
        else:
            print(f"PR creation failed: {resp.status_code} {resp.text}")
