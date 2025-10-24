from rest_framework import serializers
from snippets.models import Snippet, SnippetCategory, LANGUAGE_CHOICES, STYLE_CHOICES

class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField()
    linenos = serializers.IntegerField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance

    def validate_linenos(self, value):
        """
        Check that line number cannot be negative.
        """
        if value and value < 0:
            raise serializers.ValidationError("Line number cannot be negative")
        return value
    
    # Serializer-level validation
    def validate(self, data):
        """
        Check that if the language is Python the snippet's title must contains 'django'
        """
        if data['language'] == 'python' and 'django' not in data['title'].lower():
            raise serializers.ValidationError("For Python, snippets must be about Django")
        return data
    
class SnippetCategorySerializer(serializers.ModelSerializer):
    snippet_set = SnippetSerializer(many=True, read_only=True)

    class Meta:
        model = SnippetCategory
        fields = ['id', 'name', 'snippet_set']

class SnippetSerializer(serializers.ModelSerializer):
    category_detail = SnippetCategorySerializer(source="category", read_only=True)

    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style', 'category', 'category_detail']

    def validate_linenos(self, value):
        """
        Check that line number cannot be negative.
        """
        if value and value < 0:
            raise serializers.ValidationError("Line number cannot be negative")
        return value
    
    # Serializer-level validation
    def validate(self, data):
        """
        Check that if the language is Python the snippet's title must contains 'django'
        """
        if data['language'] == 'python' and 'django' not in data['title'].lower():
            raise serializers.ValidationError("For Python, snippets must be about Django")
        return data