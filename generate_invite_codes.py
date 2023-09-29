import hmac
import hashlib
import os
from p3app import create_app, db, models

# Load the master key from the .env file
from dotenv import load_dotenv
load_dotenv()

MASTER_KEY = os.environ.get('INVITATION_MASTER_KEY')

def generate_invitation_code(counter):
    master_key = MASTER_KEY.encode()
    message = str(counter).encode()
    
    code = hmac.new(master_key, message, hashlib.sha256).hexdigest()
    
    # To ensure the code isn't excessively long, you might want to take only the first 16 characters
    return code[:16]

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        counter_obj = models.InviteCounter.query.first()
        
        if not counter_obj:
            counter_obj = models.InviteCounter(value=0)
            db.session.add(counter_obj)
        
        counter_value = counter_obj.value
        code = generate_invitation_code(counter_value)

        invite = models.InviteCode(code=code)
        db.session.add(invite)

        # Increment the counter
        counter_obj.value += 1
        
        db.session.commit()
        print(f"Generated Invitation Code: {code}")
