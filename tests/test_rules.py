from re import Pattern

from mrchecker.rules.loader import load_rules


def test_load_builtin_rules() -> None:
    rules = load_rules()

    assert len(rules) == 2

    aws = rules[0]
    github = rules[1]

    assert aws.id == "aws-access-key"
    assert aws.name == "AWS Access Key"
    assert aws.severity == "high"
    assert aws.description == "Detects AWS IAM Access Key IDs."
    assert aws.category == "Cloud"
    assert aws.recommendation == "Rotate the exposed AWS Access Key immediately."
    assert isinstance(aws.pattern, Pattern)

    assert github.id == "github-pat"
    assert github.name == "GitHub Personal Access Token"
    assert github.severity == "high"
    assert github.description == "Detects GitHub Personal Access Tokens."
    assert github.category == "Source Control"
    assert github.recommendation == "Revoke and regenerate the GitHub Personal Access Token."
    assert isinstance(github.pattern, Pattern)
