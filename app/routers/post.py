from .. import models, schemas, oauth2
from ..database import get_db
from fastapi import  Response, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",
    tags=["Posts"] # Groups all post methods in the documentation
)

# my_posts = [{"title" : "title of post 1", "content" : "content of post 1", "id" : 1}, 
#     {"title" : "favorite foods", "content": "i like pizza", "id" : 2}]

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p

 
# * #################################  GET Methods #################################


@router.get("/", response_model=List[schemas.PostOut])
# @router.get("/") # response_model=List[schemas.Post]
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit:int=10, skip: int=0, search: Optional[str] = ""):

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id ).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # To restrict by only person who has logged in can see this post
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    # if posts.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    return results


@router.get("/{id}", response_model=schemas.PostOut)
def get_one_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
   
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id ).filter(
            models.Post.id == id).first()
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error" : f"unable to find post with id {id}"})

    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    return post


# *#################################  POST Methods #################################

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(owner_id=current_user.id, **post.dict())  # "**" unpacks the dict and gives it in the form required above
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


#*#################################  UPDATE Methods #################################

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute('''UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *''', 
    # (post.title, post.content, post.is_published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first() # the .first() or .all() command runs the actual query

    if post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= {"error": f"unable to find post with id {id}"})

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()



#*#################################  DELETE  Methods #################################

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute('''DELETE FROM posts WHERE id = %s RETURNING *''', str(id))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": f"unable to find post with id {id}"})

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post.delete(synchronize_session=False)
    db.commit()

    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)