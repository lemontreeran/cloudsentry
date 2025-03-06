# verify_policy.py
from z3 import Solver, sat, Bool, String  # Just to illustrate usage

def verify_no_manager_delete(allow_rules, deny_rules):
    """
    Returns True if the policy is correct (no manager-delete scenario), 
    False if there's a violation (manager can delete).
    """
    # If we find a rule that says (Manager, delete, ResourceRequests) is allowed
    # and we do NOT see a corresponding deny, that's a violation.
    
    manager_delete_allowed = any(
        r['role'] == "Manager" and r['action'] == "delete" and r['resource'] == "ResourceRequests"
        for r in allow_rules
    )
    manager_delete_denied = any(
        r['role'] == "Manager" and r['action'] == "delete" and r['resource'] == "ResourceRequests"
        for r in deny_rules
    )
    
    if manager_delete_allowed and not manager_delete_denied:
        return False
    return True

if __name__ == "__main__":
    # Example usage:
    allow_rules = [
        {"role": "Manager", "action": "approve", "resource": "ResourceRequests"}
    ]
    deny_rules = [
        {"role": "Manager", "action": "delete", "resource": "ResourceRequests"}
    ]
    verified = verify_no_manager_delete(allow_rules, deny_rules)
    if verified:
        print("Verification Passed.")
    else:
        print("Verification Failed. Manager can delete ResourceRequests!")
