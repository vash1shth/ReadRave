from . import views
from django.urls import path
from .views import home, login_view, signup_view, promote_view, exchange_view, user_dashboard, read_and_earn_view, blogs_view, gold_view, diamond_view, platinum_view, reviews_view , read_and_earn_view
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('promote/', promote_view, name='promote'),
    path('exchange/', exchange_view, name='exchange'),
    path('user_dashboard/', user_dashboard, name='user_dashboard'),
    path('blogs/', blogs_view, name='blogs'), 
    path('read_and_earn/', read_and_earn_view, name='read_and_earn'),
    path('gold/', gold_view, name='gold'), 
    path('diamond/', diamond_view, name='diamond'), 
    path('platinum/', platinum_view, name='platinum'),
    path('reviews/', reviews_view, name='reviews'),
    path('read_and_earn/', read_and_earn_view, name='read_and_earn'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add_book/', views.add_book, name='add_book'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
    path('remove_user/<int:user_id>/', views.remove_user, name='remove_user'),
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
    path('earn_now/<int:book_id>/', views.earn_now, name='earn_now'),
    path('reviews/', views.reviews_view, name='reviews'),
    path('review/<int:review_id>/', views.detailed_review_view, name='detailed_review'),
    path('blogs/', views.blogs_view, name='blogs'),
    path('blog/<int:blog_id>/', views.detailed_blog_view, name='detailed_blog'),
    path('packages_payment/', views.packages_payment_view, name='packages_payment'),
    path('add_comment/<int:blog_id>/', views.add_comment, name ='add_comment'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

