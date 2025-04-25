from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import MenuItem, Rating

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rate_item(request):
    try:
        item_id = request.data.get('item_id')
        rating_value = request.data.get('rating')
        comment = request.data.get('comment', '')

        if not item_id:
            return Response(
                {'error': 'Item ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not rating_value:
            return Response(
                {'error': 'Rating value is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            rating_value = int(rating_value)
            if rating_value < 1 or rating_value > 5:
                return Response(
                    {'error': 'Rating must be between 1 and 5'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response(
                {'error': 'Rating must be a number'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            menu_item = MenuItem.objects.get(id=item_id)
        except MenuItem.DoesNotExist:
            return Response(
                {'error': 'Menu item not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Create or update rating for this user and item
        rating, created = Rating.objects.update_or_create(
            user=request.user,
            menu_item=menu_item,
            defaults={
                'rating': rating_value,
                'comment': comment
            }
        )

        # Get all ratings and comments for this item
        all_ratings = Rating.objects.filter(menu_item=menu_item).order_by('-created_at')
        ratings_data = [{
            'rating': r.rating,
            'comment': r.comment,
            'created_at': r.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'username': r.user.username if r.user else 'Anonymous'
        } for r in all_ratings]

        return Response({
            'message': 'Rating submitted successfully',
            'rating': rating.rating,
            'comment': rating.comment,
            'all_ratings': ratings_data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 