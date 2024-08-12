from django.views.generic import DetailView, ListView

from blog.models import Blog


# Create your views here.
class BlogDetailView(DetailView):
    """
    Контроллер отображения блога
    """
    model = Blog
    template_name = 'blog/blog_detail.html'

    def get_object(self, queryset=None):
        object = super().get_object(queryset)

        object.views_count += 1
        object.save(update_fields=['count_view'])

        return object


class BlogListView(ListView):
    model = Blog