import json
import re

def parse_rego_policy(rego_code: str):
    """
    Very naive string-based parser that looks for allow/deny blocks
    and extracts role, action, resource.
    Returns two lists: allow_rules, deny_rules.
    Each rule is a dict like {'role': 'Manager', 'action': 'approve', 'resource': 'ResourceRequests'}.
    """
    allow_rules = []
    deny_rules = []
    
    # Regex patterns for the sample policy
    # e.g. allow[role] { role == "Manager" ... }
    pattern_allow = r'allow\[role\].*?role == "([^"]+)".*?input.action == "([^"]+)".*?input.resource == "([^"]+)"'
    pattern_deny = r'deny\[role\].*?role == "([^"]+)".*?input.action == "([^"]+)".*?input.resource == "([^"]+)"'
    
    # Find all matches
    allow_matches = re.findall(pattern_allow, rego_code, re.DOTALL)
    deny_matches = re.findall(pattern_deny, rego_code, re.DOTALL)
    
    # Convert to dicts
    for m in allow_matches:
        allow_rules.append({
            "role": m[0],
            "action": m[1],
            "resource": m[2]
        })
    for m in deny_matches:
        deny_rules.append({
            "role": m[0],
            "action": m[1],
            "resource": m[2]
        })
        
    return allow_rules, deny_rules


def generate_aws_iam_policy(allow_rules, deny_rules, aws_account_id="123456789012"):
    """
    Generates a JSON representation of an AWS IAM policy
    from allow/deny rules.
    """
    statements = []
    
    # Build allow statements
    for rule in allow_rules:
        statements.append({
            "Sid": f"{rule['role']}Allow{rule['action'].capitalize()}{rule['resource']}",
            "Effect": "Allow",
            "Principal": {
                "AWS": f"arn:aws:iam::{aws_account_id}:role/{rule['role']}"
            },
            "Action": [ rule['action'] ],
            "Resource": f"arn:aws:iam::{aws_account_id}:resource/{rule['resource']}"
        })
    
    # Build deny statements
    for rule in deny_rules:
        statements.append({
            "Sid": f"{rule['role']}Deny{rule['action'].capitalize()}{rule['resource']}",
            "Effect": "Deny",
            "Principal": {
                "AWS": f"arn:aws:iam::{aws_account_id}:role/{rule['role']}"
            },
            "Action": [ rule['action'] ],
            "Resource": f"arn:aws:iam::{aws_account_id}:resource/{rule['resource']}"
        })
    
    policy_document = {
        "Version": "2012-10-17",
        "Statement": statements
    }
    
    return json.dumps(policy_document, indent=2)


if __name__ == "__main__":
    # Example usage:
    sample_rego = """
    package multi_cloud_policy

    allow[role] {
        role == "Manager"
        input.action == "approve"
        input.resource == "ResourceRequests"
    }
    
    deny[role] {
        role == "Manager"
        input.action == "delete"
        input.resource == "ResourceRequests"
    }
    
    default allow = false
    """

    allow_rules, deny_rules = parse_rego_policy(sample_rego)
    aws_policy_json = generate_aws_iam_policy(allow_rules, deny_rules)
    print("AWS IAM Policy:\n", aws_policy_json)
