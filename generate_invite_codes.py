import os
from p3app import create_app, db, models
from werkzeug.security import generate_password_hash
import click

app = create_app()
app.app_context().push()

@click.group()
def cli():
    """Command line interface for invitation codes management"""
    pass

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

    counter_obj = models.Counter.query.first()

    new_codes = []
    for _ in range(count):
        new_code = generate_password_hash(master_key + str(counter_obj.value), method='sha256')
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

if __name__ == '__main__':
    cli()
