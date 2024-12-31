from sqlalchemy.orm import Session
from app.schema.allotedTags import AllotedTags
from app.models.allotedTagsBase import DueAmount

def dueAmount(db:Session) -> DueAmount:
    alloted_tag = db.query(AllotedTags).filter_by(due=True).all()
    due=0
    for data in alloted_tag:
        due=due+int(data.total)

    if due:
        return DueAmount(
            due=str(due*10)
        )
    else:
        return DueAmount(
            due="0"
        )