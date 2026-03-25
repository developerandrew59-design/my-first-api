

import pytest
import schemas


def test_get_all_posts(authorization,test_posts_andy):
    response=authorization.get("/posts/")
    def validate(post):
        return schemas.Postout(**post)
    posts_map=map(validate,response.json())
    posts_list=list(posts_map)
    assert len(response.json())==len(test_posts_andy)
    assert response.status_code==200


def test_unauthorized_user_acess_all_posts(client,test_posts_andy):
    response=client.get("/posts")
    assert response.status_code==401

def test_unauthorized_user_acess_single_posts(client,test_posts_andy):
    response=client.get(f"/posts/{test_posts_andy[0].id}")
    assert response.status_code==401 

def test_get_one_post_not_exists(authorization,test_posts_andy):
    response=authorization.get("/posts/8943")
    assert response.status_code==404

def test_get_one_post(authorization,test_posts_andy):
    response=authorization.get(f"/posts/{test_posts_andy[0].id}")
    post=schemas.Postout(**response.json())
    
    assert post.Post.id==test_posts_andy[0].id
    assert post.Post.content==test_posts_andy[0].content
    assert response.status_code==200



@pytest.mark.parametrize("title,content,published",
                        [("fighter jets","F-16,F-22,F-25",True),
                        ("API frameworks","django,fastapi,flask",False),
                        ("junk food","pizza,chips,burger",True)])
def test_create_one_post(authorization,test_posts_andy,title,content,published,test_users):
    response=authorization.post("/posts/",json={"title":title,"content":content,"published":published})
    
    new_post=schemas.Post(**response.json())
    assert new_post.title==title
    assert new_post.content==content
    assert new_post.published==published
    assert new_post.account_id==test_users['id']
    assert response.status_code==201

def test_create_post_default_published_True(authorization,test_users):
    response=authorization.post("/posts",json={"title":"fake title","content":"fake content"})
    new_post=schemas.Post(**response.json())
    assert new_post.published==True
    assert new_post.account_id==test_users['id']
    assert response.status_code==201

def test_unauthorized_user_create_post(client):
    response=client.post("/posts",json={"title":"fake title","content":"fake content"})
    assert response.status_code==401

def test_unauthorized_user_deleting_post(client,test_posts_andy):
    response=client.delete(f"/posts/{test_posts_andy[0].id}")
    assert response.status_code==401 

def test_authorized_user_deleting_post(authorization,test_posts_andy):
    response=authorization.delete(f"/posts/{test_posts_andy[0].id}")
    assert response.status_code==204    

def test_authorized_user_deleting_post_non_exitent(authorization):
    response=authorization.delete("/posts/8229348")
    assert response.status_code==404    

def test_delete_other_users_post(authorization,test_posts_andy):
    response=authorization.delete(f"/posts/{test_posts_andy[3].id}")
    assert response.status_code==403


def test_update_post_authorized_user(authorization,test_users,test_posts_andy):

    data={"title":"updated post",
    "content":"updated contents"}

    response=authorization.put(f"/posts/{test_posts_andy[0].id}",json=data)
    updated_post=schemas.Post(**response.json())
    assert updated_post.account_id==test_users['id']
    assert updated_post.title==data['title']
    assert updated_post.content==data["content"]
    assert response.status_code==200

def test_update_other_users_post(authorization,test_posts_andy):
    data={"title":"updated post",
    "content":"updated contents",
    "id":test_posts_andy[3].id}

    response=authorization.put(f"/posts/{test_posts_andy[3].id}",json=data)
    assert response.status_code==403

def test_unauthorized_user_updating_post(client,test_users,test_users2,test_posts_andy):
    response=client.put(f"/posts/{test_posts_andy[0].id}") 
    assert response.status_code==401   


def test_authorized_user_updating_post_non_exitent(authorization):
    data={"title":"updated post",
    "content":"updated contents"}
    response=authorization.put(f"/posts/7323939",json=data)
    assert response.status_code==404    

                              






