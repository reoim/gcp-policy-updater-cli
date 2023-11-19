import click
import yaml
import json

from google.cloud import orgpolicy_v2

def read_yaml(filename):
    with open(f'{filename}', 'r') as f:
        try:
            data = yaml.safe_load(f)
            return data
        except yaml.YAMLError as e:
            print("Error parsing YAML:", e)

def exists_in_yaml(data, field_path):
                if isinstance(data, dict) and field_path in data:
                    return True
                elif isinstance(data, dict):
                    for k, v in data.items():
                        if exists_in_yaml(v, field_path):
                            return True
                return False


@click.group()
def cli():
    pass

@cli.command()
@click.option(
    '--policy_file', type=click.Path(exists=True, dir_okay=False),  
    help='path of policy yaml file'
    )
def create(policy_file):
    # Create a Client
    client = orgpolicy_v2.OrgPolicyClient()

    # Read Policy YAML
    data = read_yaml(filename=policy_file)
    
    # Create a Policy
    org_policy = orgpolicy_v2.Policy()
    
    try:
        org_policy.name = data["name"]
    except:
        raise ValueError("The name field is required")
    
    try:
        org_policy.spec.inherit_from_parent = data["spec"]["inherit_from_parent"]
    except:
        raise ValueError("The inherit_from_parent field is required")

    # Create a PolicyRule
    policy_rule = orgpolicy_v2.PolicySpec.PolicyRule()

    if exists_in_yaml(data, "values"):
        if exists_in_yaml(data, "allowed_values"):
            policy_rule.values.allowed_values = data["spec"]["rules"]["values"]["allowed_values"]
        elif exists_in_yaml(data, "denied_values"):
            policy_rule.values.denied_values = data["spec"]["rules"]["values"]["denied_values"]
    elif exists_in_yaml(data, "allow_all"):
        policy_rule.allow_all = data["spec"]["rules"]["allow_all"]
    elif exists_in_yaml(data, "deny_all"):
        policy_rule.deny_all = data["spec"]["rules"]["deny_all"]
    elif exists_in_yaml(data, "enforce"):
        policy_rule.enforce = data["spec"]["rules"]["enforce"]
    
    org_policy.spec.rules.append(policy_rule)

    parent_path = data["name"].split("/")[0:2]
    parent_path = "/".join(parent_path)

    # Initialize request argument(s)
    request = orgpolicy_v2.CreatePolicyRequest(
        
        parent = parent_path,
        policy=org_policy
    )

    # Make the request
    response = client.create_policy(request=request)

    # Handle the response
    click.echo(response)


@cli.command()
@click.option(
    '--policy_file', type=click.Path(exists=True, dir_okay=False),  
    help='path of policy yaml file'
    )
def update(policy_file):
    # Create a client
    client = orgpolicy_v2.OrgPolicyClient()

    # Read Policy YAML
    data = read_yaml(filename=policy_file)

    # Create a Policy
    org_policy = orgpolicy_v2.Policy()
    
    try:
        org_policy.name = data["name"]
    except:
        raise ValueError("The name field is required")
    
    try:
        org_policy.spec.inherit_from_parent = data["spec"]["inherit_from_parent"]
    except:
        raise ValueError("The inherit_from_parent field is required")

    # Create a PolicyRule
    policy_rule = orgpolicy_v2.PolicySpec.PolicyRule()

    if exists_in_yaml(data, "values"):
        if exists_in_yaml(data, "allowed_values"):
            policy_rule.values.allowed_values = data["spec"]["rules"]["values"]["allowed_values"]
        elif exists_in_yaml(data, "denied_values"):
            policy_rule.values.denied_values = data["spec"]["rules"]["values"]["denied_values"]
    elif exists_in_yaml(data, "allow_all"):
        policy_rule.allow_all = data["spec"]["rules"]["allow_all"]
    elif exists_in_yaml(data, "deny_all"):
        policy_rule.deny_all = data["spec"]["rules"]["deny_all"]
    elif exists_in_yaml(data, "enforce"):
        policy_rule.enforce = data["spec"]["rules"]["enforce"]
    
    org_policy.spec.rules.append(policy_rule)

    # Initialize request argument(s)
    request = orgpolicy_v2.UpdatePolicyRequest(
        policy=org_policy
    )

    # Make the request
    response = client.update_policy(request=request)

    # Handle the response
    click.echo(response)

@cli.command()
@click.option(
    '--policy_file', type=click.Path(exists=True, dir_okay=False),  
    help='path of policy yaml file'
    )
def delete(policy_file):
    # Create a client
    client = orgpolicy_v2.OrgPolicyClient()

    # Read Policy YAML
    data = read_yaml(filename=policy_file)

    # Initialize request argument(s)
    request = orgpolicy_v2.DeletePolicyRequest(
        name=data["name"]
    )

    # Make the request
    response = client.delete_policy(request=request)
    
    # Handle the response
    click.echo(response)


if __name__ == '__main__':
    cli()