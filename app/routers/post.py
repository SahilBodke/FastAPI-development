
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas, utils, oauth2
from ..database import get_db


router = APIRouter(prefix = "/posts", tags = ["Posts"])

# @router.get("/", response_model = List[schemas.Post])
@router.get("/", response_model = List[schemas.PostOut])
def getPosts(db: Session = Depends(get_db), currentUser : int = Depends(oauth2.getCurrentUser), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()

    # print(search)
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()  # Outer Left Join

    posts = list(map (lambda x : x._mapping, posts)) # This line is req since when querying the db with two arguments in the .query method, sqlalchemy returns a list of sqlalchemy.engine.row.Row objects

    return posts


@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.Post)
def createPosts(post: schemas.PostCreate, db: Session = Depends(get_db), currentUser : int = Depends(oauth2.getCurrentUser)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))   # This type of string prevents from SQL injection attacks
    # newPost = cursor.fetchone()
    # connection.commit()   # Commit the changes to the database


    newPost = models.Post(owner_id = currentUser.id, **post.dict())   # Unpack the post dictionary
    db.add(newPost)
    db.commit()
    db.refresh(newPost)

    return newPost


@router.get("/{id}", response_model = schemas.PostOut)
def getPost(id: int, db: Session = Depends(get_db), currentUser : int = Depends(oauth2.getCurrentUser)):  # Validates if the input is integer
    # cursor.execute(""" SELECT * FROM posts where id = %s """, (str(id)))
    # post = cursor.fetchone()

    # post = db.query(models.Post).filter(models.Post.id == id).first()
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} not found")
    return post


@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def deletePost(id: int, db: Session = Depends(get_db), currentUser = Depends(oauth2.getCurrentUser)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    # deletedPost = cursor.fetchone()
    # connection.commit()

    postQuery = db.query(models.Post).filter(models.Post.id == id)
    post = postQuery.first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")

    if post.owner_id != currentUser.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform request")

    postQuery.delete(synchronize_session = False) 
    db.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT) 



@router.put("/{id}", response_model = schemas.Post)
def updatePost(id: int, updatedPost: schemas.PostCreate, db: Session = Depends(get_db), currentUser = Depends(oauth2.getCurrentUser)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    # updatedPost = cursor.fetchone()
    # connection.commit()

    postQuery = db.query(models.Post).filter(models.Post.id == id)
    post = postQuery.first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")
    
    if post.owner_id != currentUser.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform request")

    postQuery.update(updatedPost.dict(), synchronize_session = False)
    db.commit()

    return postQuery.first()



    