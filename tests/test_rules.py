from re import Pattern

from mrchecker.rules.loader import load_rules


def test_load_builtin_rules() -> None:
    rules = load_rules()

    assert len(rules) == 3

    rules_by_id = {rule.id: rule for rule in rules}

    # AWS Access Key
    aws = rules_by_id["aws-access-key"]
    assert aws.name == "AWS Access Key"
    assert aws.severity == "high"
    assert aws.description == "Detects AWS IAM Access Key IDs."
    assert aws.category == "Cloud"
    assert aws.recommendation == "Rotate the exposed AWS Access Key immediately."
    assert isinstance(aws.pattern, Pattern)

    # GitHub PAT
    github = rules_by_id["github-pat"]
    assert github.name == "GitHub Personal Access Token"
    assert github.severity == "high"
    assert github.description == "Detects GitHub Personal Access Tokens."
    assert github.category == "Source Control"
    assert github.recommendation == ("Revoke and regenerate the GitHub Personal Access Token.")
    assert isinstance(github.pattern, Pattern)

    # Slack Bot Token
    slack = rules_by_id["slack-bot-token"]
    assert slack.name == "Slack Bot Token"
    assert slack.severity == "high"
    assert slack.description == "Detects Slack Bot Tokens."
    assert slack.category == "Messaging"
    assert slack.recommendation == ("Rotate the exposed Slack Bot Token immediately.")
    assert isinstance(slack.pattern, Pattern)
