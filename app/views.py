from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, UpdateView, CreateView, TemplateView

from app.models import Tweet, TwitterUser, Comment


@method_decorator(login_required, name='dispatch')
class Home(ListView):
    model = Tweet
    template_name = 'app/home.html'
    paginate_by = 15

    def get_queryset(self):
        tweets_list = Tweet.objects.all().filter(author__in=self.request.user.following.all()).order_by('-created')
        if tweets_list.count() == 0:
            messages.success(self.request, 'Nothing to show')
        return tweets_list

    def post(self, request, *args, **kwargs):
        if request.GET.get('page'):
            url_query = reverse('home') + f"?page={request.GET.get('page')}"
        else:
            url_query = reverse('home')
        tweet = Tweet.objects.get(id=request.POST.get('tweet_id'))
        manage_likes(request.user, tweet)
        return redirect(url_query)


@method_decorator(login_required, name='dispatch')
class UserPublicProfile(DetailView):
    model = TwitterUser
    template_name = 'app/user_public_profile.html'

    def post(self, request, *args, **kwargs):
        profile_user = TwitterUser.objects.get(id=request.POST.get('user_id'))
        message = manage_user_following(request.user, profile_user)
        messages.success(request, message)
        return redirect('user-public-profile', slug=kwargs['slug'])


@method_decorator(login_required, name='dispatch')
class UserEditProfile(UpdateView):
    model = TwitterUser
    template_name = 'app/user_edit_profile.html'
    success_url = reverse_lazy('user-edit-profile')
    fields = ['full_name', 'about_me', 'email', 'avatar']

    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated successfully!')
        return super(UserEditProfile, self).form_valid(form)

    def get_object(self, queryset=None):
        return self.request.user


@method_decorator(login_required, name='dispatch')
class SearchUsers(ListView):
    model = TwitterUser
    template_name = 'app/search_users_results.html'

    def get_queryset(self):
        try:
            query = self.request.GET.get('q')
            if len(query) < 3:
                messages.warning(self.request, "Minimum length of query is 3 characters.")
            else:
                users_list = TwitterUser.objects.exclude(username=self.request.user.username).filter(
                    Q(username__contains=query) | Q(full_name__contains=query))
                messages.info(self.request, f"{users_list.count()} results.")
                return users_list
        except (ValueError, TypeError):
            messages.warning(self.request, "Incorrect query.")

    def post(self, request, *args, **kwargs):
        result_user = TwitterUser.objects.get(id=request.POST.get('user_id'))
        url_query = reverse("search-users-results") + f"?q={request.GET.get('q')}"
        message = manage_user_following(request.user, result_user)
        messages.success(request, message)
        return redirect(url_query)


@method_decorator(login_required, name='dispatch')
class TweetDetails(DetailView):
    model = Tweet
    template_name = 'app/tweet_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.all().filter(tweet=self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('tweet_id'):
            tweet = self.get_object()
            manage_likes(request.user, tweet)

        if request.POST.get('add_comment'):
            if request.POST.get('comment_content'):
                Comment.objects.create(author=request.user, content=request.POST.get('comment_content'),
                                       tweet=self.get_object())
                messages.success(request, 'Comment has been added')
            else:
                messages.warning(request, "Please fill out comment field")

        return redirect('tweet-details', pk=self.get_object().id)


@method_decorator(login_required, name='dispatch')
class TweetAdd(CreateView):
    model = Tweet
    template_name = 'app/tweet_add.html'
    fields = ['content', 'image']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        messages.success(self.request, 'Tweet has been added')
        return super(TweetAdd, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class TweetEdit(UpdateView):
    model = Tweet
    template_name = 'app/tweet_edit.html'
    fields = ['content', 'image']

    def get(self, request, *args, **kwargs):
        if request.user != self.get_object().author:
            return redirect("tweet-details", pk=self.get_object().id)
        else:
            return super(TweetEdit, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.edited = True
        self.object.save()
        messages.success(self.request, 'Tweet has been edited')
        return super(TweetEdit, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class TweetDelete(TemplateView):
    template_name = 'app/tweet_delete.html'

    def get(self, request, *args, **kwargs):
        try:
            tweet = Tweet.objects.get(id=kwargs['pk'])
            if request.user != tweet.author:
                return redirect('tweet-details', pk=kwargs['pk'])
        except ObjectDoesNotExist:
            return redirect('home')
        return super(TweetDelete, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST.get('confirm_delete'):
            Tweet.objects.get(id=kwargs['pk']).delete()
            messages.success(self.request, 'Tweet has been deleted')
        return redirect('home')


@method_decorator(login_required, name='dispatch')
class CommentDelete(TemplateView):
    template_name = "app/comment_delete.html"

    def get(self, request, *args, **kwargs):
        try:
            comment = Comment.objects.get(id=kwargs['pk'])
            tweet_id = comment.tweet.id
            if request.user != comment.author:
                return redirect('tweet-details', tweet_id)
        except ObjectDoesNotExist:
            return redirect('home')
        return super(CommentDelete, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST.get('confirm_delete'):
            comment = Comment.objects.get(id=kwargs['pk'])
            tweet_id = comment.tweet.id
            comment.delete()
            messages.success(self.request, 'Comment has been deleted')
        return redirect('tweet-details', tweet_id)


@method_decorator(login_required, name='dispatch')
class Hashtags(ListView):
    model = Tweet
    template_name = "app/tweet_hashtags.html"
    slug_field = 'slug'
    paginate_by = 15

    def get_queryset(self):
        return Tweet.objects.all().filter(Q(content__contains=f"#{self.kwargs['slug']}")).order_by('-created')

    def post(self, request, *args, **kwargs):
        if request.GET.get('page'):
            url_query = reverse('tweet-hashtag', kwargs={'slug': kwargs['slug']}) + f"?page={request.GET.get('page')}"
        else:
            url_query = reverse('tweet-hashtag', kwargs={'slug': kwargs['slug']})
        tweet = Tweet.objects.get(id=request.POST.get('tweet_id'))
        manage_likes(request.user, tweet)
        return redirect(url_query)


@method_decorator(login_required, name='dispatch')
class UserTweets(ListView):
    model = Tweet
    template_name = "app/user_tweets.html"
    slug_field = 'slug'
    paginate_by = 15

    def get_queryset(self):
        return Tweet.objects.all().filter(author__slug=self.kwargs['slug']).order_by('-created')

    def post(self, request, *args, **kwargs):
        if request.GET.get('page'):
            url_query = reverse('user-tweets', kwargs={'slug': kwargs['slug']}) + f"?page={request.GET.get('page')}"
        else:
            url_query = reverse('user-tweets', kwargs={'slug': kwargs['slug']})
        tweet = Tweet.objects.get(id=request.POST.get('tweet_id'))
        manage_likes(request.user, tweet)
        return redirect(url_query)


@method_decorator(login_required, name='dispatch')
class UserFollowingList(ListView):
    model = TwitterUser
    template_name = 'app/user_following_list.html'

    def get_queryset(self):
        return self.request.user.following.all()

    def post(self, request, *args, **kwargs):
        user_id = request.POST['user_id']
        followed_user = TwitterUser.objects.get(id=user_id)
        message = manage_user_following(request.user, followed_user)
        messages.info(self.request, message)
        return redirect('user-following-list')


def manage_user_following(user, follow_user):
    if user.following.filter(id=follow_user.id).exists():
        user.following.remove(follow_user)
        return f'{follow_user.username} is unfollowed.'
    else:
        user.following.add(follow_user)
        return f'{follow_user.username} is followed.'


def manage_likes(user, tweet):
    if tweet.likes.filter(id=user.id).exists():
        tweet.likes.remove(user)
    else:
        tweet.likes.add(user)
