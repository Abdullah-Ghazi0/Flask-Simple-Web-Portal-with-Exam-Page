from flask import session
from ..models import db, Messages, Users

def send(r, m):
    recievingUser = Users.query.filter_by(username=r).first()
    new_msg = Messages(
        s_id = session["user_id"],
        r_id = recievingUser.id,
        content = m
    )
    db.session.add(new_msg)
    db.session.commit()

    
