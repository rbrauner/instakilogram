from django.urls import path
from app.views import Home, SearchUsers, UserPublicProfile, UserEditProfile, TweetAdd, TweetDetails, TweetEdit, \
    TweetDelete, CommentDelete, Hashtags, UserFollowingList, UserTweets

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('search/', SearchUsers.as_view(), name='search-users-results'),
    path('profile/<slug>/', UserPublicProfile.as_view(), name='user-public-profile'),
    path('profile/<slug>/tweets', UserTweets.as_view(), name='user-tweets'),
    path('user/profile/edit/', UserEditProfile.as_view(), name='user-edit-profile'),
    path('tweet/add/', TweetAdd.as_view(), name='tweet-add'),
    path('tweet/<int:pk>/', TweetDetails.as_view(), name='tweet-details'),
    path('tweet/<int:pk>/edit/', TweetEdit.as_view(), name='tweet-edit'),
    path('tweet/<int:pk>/delete/', TweetDelete.as_view(), name='tweet-delete'),
    path('comment/<int:pk>/delete/', CommentDelete.as_view(), name='comment-delete'),
    path('hashtag/<slug>/', Hashtags.as_view(), name='tweet-hashtag'),
    path('following/', UserFollowingList.as_view(), name='user-following-list'),

]
