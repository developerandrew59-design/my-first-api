from http import client
from urllib import response

import pytest
import models

@pytest.fixture()
def test_vote(test_posts_andy,session,test_users):
    new_vote=models.Vote(post_id=test_posts_andy[3].id,user_id=test_users['id'])
    session.add(new_vote)
    session.commit()

def test_vote_on_post_user_authorized(authorization,test_posts_andy):
    response=authorization.post("/votes/",json={"post_id":test_posts_andy[3].id,
                                     "dir":1})
    
    assert response.status_code==201

def test_vote_twice_same_user(authorization,test_posts_andy,test_users,test_vote):   
    response=authorization.post("/votes/",json={"post_id":test_posts_andy[3].id,
                                                "dir":1})
    assert response.status_code==409

def test_vote_deleting_vote_post(authorization,test_posts_andy,test_vote):
    response=authorization.post("/votes/",json={"post_id":test_posts_andy[3].id,
                                                "dir":0})
    assert response.status_code==201


def test_vote_delete_not_exict_vote(authorization,test_posts_andy):
    response=authorization.post("/votes/",json={"post_id":test_posts_andy[3].id,
                                                "dir":0})
    assert response.status_code==404

def test_vote_vote_on_post_not_exict(authorization,test_posts_andy):
    response=authorization.post("/votes/",json={"post_id":9824792,
                                                "dir":1})
    assert response.status_code==404

def test_vote_unauthicated_user(client,test_posts_andy):
    response=client.post("/votes/",json={"post_id":test_posts_andy[3].id,
                                         "dir":1})

    assert response.status_code==401    
    
    
    





   

