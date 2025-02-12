from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.oauth2 import get_current_user
from ..database import get_db
from .. import models, schemas, oauth2
from typing import List, Optional


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# request Get method url: "/posts"
@router.get("/", response_model = List[schemas.PostOut])
#@router.get("/")
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int=10, skip: int=0, search: Optional[str]=""):  # retrieve all posts
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    #posts = db.query(models.Post).filter(
    #    models.Post.title.contains(search)).limit(limit).offset(skip).all()   #.filter(models.Post.owner_id==current_user.id).all()   # retrieve all the entries from post table (SELECT * FROM posts WHERE id==...)
    posts=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()  # Select posts.*, count(votes.post_id) as votes from posts LEFT OUTER JOIN votes ON posts.id=votes.post_id group by post_id
    return posts  # will turn posts array into JSON format

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) 
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):  
    """
        Retrieves the post and checks if data is valid (based on the class Post's schema we defined), 
        we expect the user to send this data schema: title str, content str
        
        Also, if someone wants to access a resource, for which they must be logged in, they must provide 
        access token (get_current_user: int = Depends(oauth2.get_current_user))

    """
    #post_dict = post.dict()
    #post_dict['id'] = randrange(0, 1000000)
    #my_posts.append(post_dict)  # append new post in my_posts list
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,     # pass in the variables (%s)
    #(post.title, post.content, post.published))  
    #new_post = cursor.fetchone()
    #conn.commit()   # commit changes
    #print(**post.dict())  
    print(current_user.id)
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict())        #**post.dict(): unpacks every value from the dictionary,title=post.title, content=post.content, published=post.published
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



# request Get method url: "/posts/{id}"
@router.get("/{id}", response_model=schemas.PostOut)   # /posts/{id}
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):  
    """   
        Retrieve the particular post with ID: {id}, validate that id type is int, if it is not, convert it to int
    """

    #post = db.query(models.Post).filter(models.Post.id == id).first()  # find 1st instance with requested id
    #cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))  # convert id to str to pass it to the SQL query
    #post = cursor.fetchone()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        #response.status_code = status.HTTP_404_NOT_FOUND # 404 not found
        #return {"message": f"post with id {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id {id} was not found")
    

    
    return post 


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
        Deleting post with ID {id}
    """

    #cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id), ))
    #deleted_post = cursor.fetchone()
    #conn.commit()  # commit changes
    post_query = db.query(models.Post).filter(models.Post.id==id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")

    # only post owner can delete his own post
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")


    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model = schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id= %s RETURNING * """, (post.title, post.content, post.published, str(id)))

    #updated_post = cursor.fetchone()
    #conn.commit()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()