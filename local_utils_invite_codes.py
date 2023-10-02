import os
from p3app import create_app, db, models
import hmac
import hashlib
import base64
import click

app = create_app()
app.app_context().push()

@click.group()
def cli():
    """Command line interface for invitation codes management"""
    pass

def generate_new_invite_code(master_key, counter):
    """Generate a 16-character invite code based on master key and counter."""
    # Create an HMAC hash with the master key and counter
    message = str(counter).encode('utf-8')
    raw_code = hmac.new(master_key.encode('utf-8'), message, hashlib.sha256).digest()

    # Encode the hash in base64 to make it URL-safe and more condensed
    b64_code = base64.urlsafe_b64encode(raw_code).decode('utf-8')

    # Return the first 16 characters of the encoded hash
    return b64_code[:16]

# !!! Careful !!!: CLI automatically converts '_' into '-' as it is more 
# idiomatic in the context of command line interface
@cli.command()
@click.argument('count', type=click.INT)
def generate_codes(count):
    """Generates a specified number of new invitation codes"""
    master_key = os.environ.get("INVITATION_MASTER_KEY")
    if not master_key:
        print("Please set INVITATION_MASTER_KEY in your .env file.")
        return

    counter_obj = models.InviteCounter.query.first()
    if not counter_obj:
        counter_obj = models.InviteCounter(value=0)
        db.session.add(counter_obj)
        db.session.commit()
        print("Initialized the invitation code counter.")

    new_codes = []
    for _ in range(count):
        new_code = generate_new_invite_code(master_key, counter_obj.value)
        new_invite = models.InviteCode(code=new_code)
        db.session.add(new_invite)
        new_codes.append(new_code)
        counter_obj.value += 1

    db.session.commit()
    print(f"{count} new codes generated:")
    for code in new_codes:
        print(code)

# !!! Careful !!!: CLI automatically converts '_' into '-' as it is more 
# idiomatic in the context of command line interface
@cli.command()
@click.argument('filename', type=click.Path(), required=False)
@click.option('--used', is_flag=True, help="Retrieve used invitation codes instead of unused ones.")
def export_codes(filename, used):
    """
    Exports used or unused invitation codes to a text file or standard output.

    \b
    FILENAME: Optional. The name of the file to which the codes will be exported.
              If not provided, codes will be printed to the standard output.
    """
    codes = models.InviteCode.query.filter_by(used=used).all()

    if filename:
        with open(filename, 'w') as f:
            for code in codes:
                f.write(code.code + '\n')
        print(f"Exported {len(codes)} {'used' if used else 'unused'} codes to {filename}")
    else:
        for code in codes:
            print(code.code)

# !!! Careful !!!: CLI automatically converts '_' into '-' as it is more 
# idiomatic in the context of command line interface
@cli.command()
def reset_invitations():
    """Reset invitation codes and counters."""
    try:
        # Delete all InviteCode records
        models.InviteCode.query.delete()

        # Delete the counter
        models.InviteCounter.query.delete()
        
        # Commit the changes
        db.session.commit()
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    cli()
