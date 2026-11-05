"""Phase 2: create the outbound engine's custom fields on Account.

Reads Salesforce credentials from .env, creates the six custom fields and the
ICP score validation rule, and grants the running user access through a
permission set. Safe to run twice: anything that already exists is skipped.

Usage (from the repo root):
    pip install -r requirements.txt
    python scripts/salesforce_setup.py
"""
import os
import sys

from dotenv import load_dotenv
from simple_salesforce import Salesforce

PERMISSION_SET = "Outbound_Engine_Fields"

FIELDS = [
    {"name": "ICP_Score__c", "label": "ICP Score", "type": "Number", "precision": 3, "scale": 0},
    {"name": "Signal_Summary__c", "label": "Signal Summary", "type": "LongTextArea", "length": 2000},
    {"name": "AI_Research_JSON__c", "label": "AI Research JSON", "type": "LongTextArea", "length": 32768},
    # Salesforce counts precision as total digits: 3 digits, 2 after the point, so 0.00 to 9.99.
    {"name": "Confidence__c", "label": "Confidence", "type": "Number", "precision": 3, "scale": 2},
    {"name": "Approval_Status__c", "label": "Approval Status", "type": "Picklist",
     "values": ["Pending", "Approved", "Rejected"]},
    {"name": "Draft_Email__c", "label": "Draft Email", "type": "LongTextArea", "length": 2000},
]


def connect():
    load_dotenv()
    missing = [k for k in ("SALESFORCE_USERNAME", "SALESFORCE_PASSWORD", "SALESFORCE_SECURITY_TOKEN")
               if not os.getenv(k)]
    if missing:
        sys.exit(f"Missing in .env: {', '.join(missing)}")
    return Salesforce(
        username=os.environ["SALESFORCE_USERNAME"],
        password=os.environ["SALESFORCE_PASSWORD"],
        security_token=os.environ["SALESFORCE_SECURITY_TOKEN"],
        domain=os.getenv("SALESFORCE_DOMAIN", "login"),
    )


def build_field(mdapi, spec):
    kwargs = {"fullName": f"Account.{spec['name']}", "label": spec["label"],
              "type": mdapi.FieldType(spec["type"])}
    if spec["type"] == "Number":
        kwargs.update(precision=spec["precision"], scale=spec["scale"])
    elif spec["type"] == "LongTextArea":
        kwargs.update(length=spec["length"], visibleLines=5)
    elif spec["type"] == "Picklist":
        values = [mdapi.CustomValue(fullName=v, label=v, default=False) for v in spec["values"]]
        kwargs["valueSet"] = mdapi.ValueSet(
            restricted=True,
            valueSetDefinition=mdapi.ValueSetValuesDefinition(sorted=False, value=values),
        )
    return mdapi.CustomField(**kwargs)


def build_validation_rule(mdapi):
    return mdapi.ValidationRule(
        fullName="Account.ICP_Score_Range",
        active=True,
        errorConditionFormula="AND(NOT(ISBLANK(ICP_Score__c)), OR(ICP_Score__c < 0, ICP_Score__c > 100))",
        errorMessage="ICP Score must be between 0 and 100.",
        errorDisplayField="ICP_Score__c",
    )


def create_fields(sf):
    existing = {f["name"] for f in sf.Account.describe()["fields"]}
    todo = [spec for spec in FIELDS if spec["name"] not in existing]
    for spec in FIELDS:
        if spec["name"] in existing:
            print(f"  exists   {spec['name']}")
    if todo:
        sf.mdapi.CustomField.create([build_field(sf.mdapi, spec) for spec in todo])
        for spec in todo:
            print(f"  created  {spec['name']}")


def create_validation_rule(sf):
    try:
        sf.mdapi.ValidationRule.create([build_validation_rule(sf.mdapi)])
        print("  created  ICP_Score_Range")
    except Exception as e:  # Metadata API reports duplicates as a generic error
        if "DUPLICATE" in str(e).upper() or "already" in str(e).lower():
            print("  exists   ICP_Score_Range")
        else:
            raise


def grant_access(sf):
    """API-created fields are hidden from every profile, so grant read/edit via a permission set."""
    found = sf.query(f"SELECT Id FROM PermissionSet WHERE Name = '{PERMISSION_SET}'")["records"]
    if found:
        ps_id = found[0]["Id"]
    else:
        ps_id = sf.PermissionSet.create({"Name": PERMISSION_SET, "Label": "Outbound Engine Fields"})["id"]

    granted = {r["Field"] for r in sf.query(
        f"SELECT Field FROM FieldPermissions WHERE ParentId = '{ps_id}'")["records"]}
    for spec in FIELDS:
        field = f"Account.{spec['name']}"
        if field not in granted:
            sf.FieldPermissions.create({"ParentId": ps_id, "SobjectType": "Account", "Field": field,
                                        "PermissionsRead": True, "PermissionsEdit": True})

    user_id = sf.query("SELECT Id FROM User WHERE Username = '{}'".format(
        os.environ["SALESFORCE_USERNAME"].replace("'", "\\'")))["records"][0]["Id"]
    assigned = sf.query(f"SELECT Id FROM PermissionSetAssignment "
                        f"WHERE PermissionSetId = '{ps_id}' AND AssigneeId = '{user_id}'")["records"]
    if not assigned:
        sf.PermissionSetAssignment.create({"PermissionSetId": ps_id, "AssigneeId": user_id})
    print(f"  granted  read/edit on all fields via permission set {PERMISSION_SET}")


def main():
    sf = connect()
    print(f"Connected to {sf.sf_instance}")
    print("Fields:")
    create_fields(sf)
    print("Validation rule:")
    create_validation_rule(sf)
    print("Access:")
    grant_access(sf)
    print("Done. Open Setup > Object Manager > Account > Fields & Relationships to check.")


if __name__ == "__main__":
    main()
