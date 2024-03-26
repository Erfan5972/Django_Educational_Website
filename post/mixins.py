from django.shortcuts import get_object_or_404, redirect
from .models import Post
from django.contrib import messages
from accounts.models import UserSubscription


class SubscriptionRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        post_id = kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        has_subscription = UserSubscription.objects.filter(user=request.user)
        if post.is_premium and not has_subscription.exists():
            messages.error(request, 'این پست برای کاربران دارای اشتراک است', 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)