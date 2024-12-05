from django.db.models import Avg, Count

from wildBg.accounts.models import Profile
from wildBg.landmark.models import Landmark


class SidebarContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        # Check if the user is authenticated
        if user.is_authenticated:
            # User profile information
            try:
                profile = user.profile  # Access the Profile model via the one-to-one relationship
                context['user_profile'] = {
                    'user': user,
                    'first_name': profile.first_name,
                    'last_name': profile.last_name,
                    'profile_picture': profile.profile_picture if profile.profile_picture else None,
                    'points': profile.points,
                    'level': profile.level,
                    'description': profile.description,
                }
                print(user.profile.get_full_name())
            except Profile.DoesNotExist:
                context['user_profile'] = {
                    'full_name': 'Anonymous',
                    'profile_picture': None,
                    'points': 0,
                    'level': 'Beginner',
                }

        # Top 3 rated landmarks with calculated star ratings
        top_landmarks = (
            Landmark.objects.annotate(
                average_rating=Avg('reviews__rating'),  # Calculate average rating
                review_count=Count('reviews')  # Count total reviews
            )
            .filter(average_rating__isnull=False)
            .order_by('-average_rating')[:3]
        )

        # Prepare the data for each landmark
        context['top_rated_landmarks'] = [
            {
                'landmark': landmark,
                'average_rating': landmark.average_rating,
                'review_count': landmark.review_count,
                'full_stars': range(int(landmark.average_rating)),
                'half_star': (landmark.average_rating % 1) >= 0.5,
                'empty_stars': range(5 - int(landmark.average_rating) - int((landmark.average_rating % 1) >= 0.5)),
            }
            for landmark in top_landmarks
        ]

        return context
