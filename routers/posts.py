
from token import OP
from sqlalchemy import func
from sqlalchemy.orm import Session
from database import engine,sessionLocal,get_db
import oauth2
import models,schemas
from typing import List, Optional
from fastapi import FastAPI, HTTPException,Response,status,Depends,APIRouter

router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/",response_model=List[schemas.Postout])
def get_posts(db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user),
              limit: int=10,skip:int=0,search:Optional[str]=""):
    #cur.execute("""SELECT * FROM posts """)
    #posts=cur.fetchall()
    #print(posts)
    #post_query=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip)

    posts=db.query(
    models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Post.id==models.Vote.post_id,
                      isouter=True).group_by(models.Post.id).filter(
                          models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def paid(post:schemas.PostCreate,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #cur.execute("""INSERT INTO posts (title,content,published) VALUES
                 #(%s,%s,%s) RETURNING * """,
                 #(post.title,post.content,post.published)) 
    #post_dict=cur.fetchone() 
    #conn.commit()

    print(current_user.id)
    post_dict = models.Post(account_id=current_user.id, **post.dict())
    db.add(post_dict)
    db.commit()
    db.refresh(post_dict)
    return post_dict

@router.get("/{id}",response_model=schemas.Postout)    
def get_post(id: int, response: Response,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #cur.execute("""SELECT * FROM posts WHERE id=%s""",str(id))
    #new_post=cur.fetchone()
    #post_query=db.query(models.Post).filter(models.Post.id==id)
    post=db.query(
    models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Post.id==models.Vote.post_id,
                      isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()

    if post==None:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    if not post.Post.account_id==current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform specfic action")
    
        #response.status_code=status.HTTP_404_NOT_FOUND
        #return {"message":f"post with id {id} was not found"}
    #print(new_post)
    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def del_post(id:int,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #cur.execute("""DELETE FROM posts WHERE id=%s  RETURNING *""",(str(id),))
    #deleted_post=cur.fetchone()
    #conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exict")
    if not post.account_id==current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform specfic action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update(id:int, updated_post: schemas.PostCreate,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #cur.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s returning *""",
                #(post.title,post.content,post.published,str(id)))
    #updated_post=cur.fetchone()
    #conn.commit()
    
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exict")
    if not post.account_id==current_user.id:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform specfic action")
    post_query.update({
        'title': updated_post.title, 
        'content': updated_post.content, 
        'published': updated_post.published
    }, synchronize_session=False)
    db.commit()

    return post_query.first()