from django.shortcuts import render,redirect,get_object_or_404
from diaries.models import Diary
from .models import Like,Comment
from django.http import JsonResponse
import json


def render_communities_main(request):
    diaries = Diary.objects.filter(disclosure = True)
    context = {
        'diaries': diaries
    }
    return render(request, 'communities/communities_main.html', context)

def toggle_like(request, pk):
    diary = Diary.objects.get(id=pk)

    # 좋아요를 추가하거나 가져오기
    get_like, created = Like.objects.get_or_create(diary=diary, like_user=request.user)

    if created:
        # 좋아요가 새로 추가된 경우
        status = 'liked'
    else:
        # 이미 존재하면 삭제하고 'unliked' 반환
        get_like.delete()
        status = 'unliked'

    # 현재 좋아요 개수
    like_count = Like.objects.filter(diary=diary).count()

    # 결과 반환
    return JsonResponse({'like_count': like_count, 'status': status})

def add_comment(request, pk):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            comment_content = body.get('comment', '').strip()
        except json.JSONDecodeError:
            return JsonResponse({'error': '잘못된 JSON 데이터입니다.'}, status=400)

        if not comment_content:
            return JsonResponse({'error': '댓글 내용을 입력하세요.'}, status=400)

        diary = get_object_or_404(Diary, id=pk)

        # 댓글 저장
        comment = Comment.objects.create(diary=diary, content=comment_content, comment_user=request.user)

        # 전체 댓글 가져오기 (외래키 정보 포함)
        whole_comments = Comment.objects.filter(diary=diary).select_related('comment_user').values(
            'id', 'content', 'comment_user__nickname'
        )
        comment_count = whole_comments.count()

        return JsonResponse({'whole_comments': list(whole_comments), 'comment_count': comment_count})

    return JsonResponse({'error': '잘못된 요청입니다.'}, status=405)
