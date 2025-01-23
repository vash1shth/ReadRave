from django.contrib.auth import get_user_model  # Use get_user_model to fetch the custom user model
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Book
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from .models import ReadAndEarnBook
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .models import BookReview , Comment
from django.utils import timezone
from .models import Blog
from .models import Package
from django.http import HttpResponse


# Get the custom user model dynamically
User = get_user_model()
import logging
logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'RR/home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_type = request.POST['user_type']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user_type == 'admin' and user.is_staff:
                auth_login(request, user)
                return redirect('admin_dashboard')  # Change to your admin dashboard URL
            elif user_type == 'user' and not user.is_staff:
                auth_login(request, user)
                return redirect('user_dashboard')  # Change to your user dashboard URL
        else:
            form = AuthenticationForm(request.POST)
            return render(request, 'RR/login.html', {'form': form, 'error': 'Invalid login'})
    else:
        form = AuthenticationForm()
    return render(request, 'RR/login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email)
                user.is_staff = False
                user.is_superuser = False
                user.save()
                logger.info(f"Created user: {user.username}, is_staff: {user.is_staff}, is_superuser: {user.is_superuser}")
                messages.success(request, 'Account created successfully')
                user = authenticate(username=username, password=password1)
                if user is not None:
                    auth_login(request, user)
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
    return render(request, 'RR/signup.html')

@login_required
def promote_view(request):
    if request.method == 'POST':
        book_title = request.POST['book_title']
        book_author = request.POST['book_author']
        book_description = request.POST['book_description']
        # Add logic to save the book promotion data
        messages.success(request, 'Book promotion request submitted successfully!')
        return redirect('promote')
    return render(request, 'RR/promote.html')


@login_required
def exchange_view(request):
    if request.method == 'POST':
        # Handle form submission
        book_name = request.POST['bookName']
        author_name = request.POST['authorName']
        volume = request.POST['volume']
        book_type = request.POST['type']
        contact_number = request.POST['contactNumber']
        email = request.POST['email']
        image = request.FILES['bookImage']

        if book_type == 'exchange':
            exchange_books = request.POST['exchangeBooks']
            book = Book(name=book_name, author=author_name, volume=volume, type=book_type, exchange_books=exchange_books, contact=contact_number, email=email, image=image)
        else:
            cost = request.POST['cost']
            book = Book(name=book_name, author=author_name, volume=volume, type=book_type, cost=cost, contact=contact_number, email=email, image=image)
        
        book.save()

    # Fetch all books to showcase
    books = Book.objects.all()
    return render(request, 'RR/exchange.html', {'books': books})


def user_dashboard(request): 
    return render(request, 'RR/user_dashboard.html')

def blogs_view(request): 
    return render(request, 'RR/blogs.html') 

def read_and_earn_view(request): 
    return render(request, 'RR/read_and_earn.html')

def gold_view(request): 
    return render(request, 'RR/gold.html') 

def diamond_view(request): 
    return render(request, 'RR/diamond.html') 

def platinum_view(request): 
    return render(request, 'RR/platinum.html')

def reviews_view(request):
    return render(request, 'RR/reviews.html')


@user_passes_test(lambda u: u.is_superuser)
@csrf_protect
def admin_dashboard(request):
    books = ReadAndEarnBook.objects.all()
    users = User.objects.all()
    context = {
        'books': books,
        'users': users
    }
    return render(request, 'RR/admin_dashboard.html', context)

@user_passes_test(lambda u: u.is_superuser)
@user_passes_test(lambda u: u.is_superuser)
def add_book(request):
    if request.method == 'POST':
        try:
            title = request.POST.get('book_title')
            author = request.POST.get('author')
            volume = request.POST.get('volume', '')
            date_of_submission = request.POST.get('date_of_submission')
            cost = request.POST.get('cost')
            image = request.FILES.get('image')

            if not all([title, author, date_of_submission, cost, image]):
                raise KeyError("One or more required fields are missing.")

            ReadAndEarnBook.objects.create(
                title=title,
                author=author,
                volume=volume,
                date_of_submission=date_of_submission,
                cost=cost,
                image=image
            )
            messages.success(request, 'Book added successfully!')
            return redirect('admin_dashboard')
        except KeyError as e:
            logger.error(f"Missing field: {e}")
            messages.error(request, f"Missing field: {e}")
        except Exception as e:
            logger.error(f"Error adding book: {e}")
            messages.error(request, 'Failed to add book. Please check the inputs.')
        return redirect('add_book')
    return render(request, 'RR/admin_dashboard.html')




@user_passes_test(lambda u: u.is_superuser)
def delete_book(request, book_id):
    ReadAndEarnBook.objects.get(id=book_id).delete()
    messages.success(request, 'Book deleted successfully!')
    return redirect('admin_dashboard')

@user_passes_test(lambda u: u.is_superuser)
def remove_user(request, user_id):
    User.objects.get(id=user_id).delete()
    messages.success(request, 'User removed successfully!')
    return redirect('admin_dashboard')

@user_passes_test(lambda u: u.is_superuser)
def block_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()
    messages.success(request, 'User blocked successfully!')
    return redirect('admin_dashboard')


def read_and_earn_view(request):
    books = ReadAndEarnBook.objects.all()
    context = {
        'books': books
    }

   
    return render(request, 'RR/read-and-earn.html', context)

def earn_now(request, book_id):
    # Handle the logic for users to earn money by reviewing the book.
    # This is a placeholder; replace with your actual logic.
    return redirect('read_and_earn')


def reviews_view(request):
    if request.method == 'POST':
        book_name = request.POST['bookName']
        author = request.POST['author']
        genre = request.POST['genre']
        volume = request.POST.get('volume', '')
        availability = request.POST['availability']
        review = request.POST['bookReview']
        pros = request.POST['pros']
        cons = request.POST['cons']
        reviewed_by = request.POST['reviewedBy']
        review_date = request.POST['reviewDate']
        image = request.FILES.get('image')

        BookReview.objects.create(
            book_name=book_name,
            author=author,
            genre=genre,
            volume=volume,
            availability=availability,
            review=review,
            pros=pros,
            cons=cons,
            reviewed_by=reviewed_by,
            review_date=review_date,
            image=image
        )

        return redirect('reviews')

    reviews = BookReview.objects.all()
    context = {
        'reviews': reviews
    }
    return render(request, 'RR/reviews.html', context)

def detailed_review_view(request, review_id):
    review = get_object_or_404(BookReview, id=review_id)
    comments = review.comments.all()

    if request.method == 'POST':
        user = request.POST['user']
        comment_text = request.POST['comment']
        Comment.objects.create(book_review=review, user=user, comment=comment_text, date=timezone.now())

        return redirect('detailed_review', review_id=review_id)

    context = {
        'review': review,
        'comments': comments
    }
    return render(request, 'RR/detailed_review.html', context)


def blogs_view(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        author = request.POST.get('author', '').strip()
        content = request.POST.get('content', '').strip()
        date = request.POST.get('date', '').strip()
        image = request.FILES.get('image')

        # Create and save the blog instance
        blog = Blog(
            title=title,
            author=author,
            content=content,
            date=date,
            image=image
        )
        blog.save()

        return redirect('blogs')

    # Fetch blogs for GET request
    blogs = Blog.objects.all()
    return render(request, 'RR/blogs.html', {'blogs': blogs})




# def blogs_view(request):
#     blogs = Blog.objects.all()
#     return render(request, 'RR/blogs.html', {'blogs': blogs})

def detailed_blog_view(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    comments = blog.comments.all()

    if request.method == 'POST':
        user = request.POST['user']
        comment_text = request.POST['comment']
        Comment.objects.create(blog=blog, user=user, comment=comment_text, date=timezone.now())

        return redirect('detailed_blog', blog_id=blog_id)

    context = {
        'blog': blog,
        'comments': comments
    }
    return render(request, 'RR/detailed_blog.html', context)


def packages_payment_view(request):
    if request.method == 'POST':
        book_name = request.POST['book_name']
        book_cost = request.POST['book_cost']
        book_link = request.POST['book_link']
        package = request.POST['package']
        book_image = request.FILES['book_image']
        book_pdf = request.FILES['book_pdf']

        Package.objects.create(
            book_name=book_name,
            book_cost=book_cost,
            book_link=book_link,
            package=package,
            book_image=book_image,
            book_pdf=book_pdf
        )

        #return HttpResponse("Payment successful. Thank you for purchasing!")
        return redirect ('pacakges_payment')

    return render(request, 'RR/packages_payment.html')


def add_comment(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        user = request.POST['user']
        comment_text = request.POST['comment']
        Comment.objects.create(blog=blog, user=user, comment=comment_text, date=timezone.now())
        return redirect('detailed_blog', blog_id=blog.id)
    return render(request, 'RR/detailed_blog.html', {'blog': blog, 'comments': blog.comments.all()})



