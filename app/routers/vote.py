from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2

router = APIRouter(prefix="/vote", tags=["Vote"])

@router.post("/", status_code = status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.getCurrentUser)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:  # if post itself doesnt exist 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exist")

    voteQuery = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)  
    
    foundVote = voteQuery.first()     # check if post already voted for
    
    if(vote.dir == 1):   # if user wants to like a post
        if foundVote:   # if current user has already voted for this post
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = f"user {current_user.id} already voted on post {vote.post_id}")
        newVote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        # To actually implement the changes to database
        db.add(newVote)
        db.commit()
        return {"message": "Successfully added vote"}
    
    else:  # if user wants to unlike a previously liked post
        if not foundVote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Vote does not exist")
        voteQuery.delete(synchronize_session = False)
        db.commit()

        return {"message": "Successfully deleted vote"} 
