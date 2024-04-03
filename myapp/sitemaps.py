from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from bbs.models import Article

# 動的クラスサイトマップを定義
class BlogPostSitemap(Sitemap):

    # 省略可。オブジェクトの更新頻度を検索エンジンに教える設定。hourly, weekly, monthlyなどが設定できる。
    changefreq = "Weekly"

    # 省略可。オブジェクトの重要度 (priority) を検索エンジンに教える設定。デフォルトは0.5。数値が高い程優先度が高い。
    priority = 0.8

    # 必須。 [モデル名].objects.all()とすると、全てのテーブルを動的に読み込む。
    def items(self):
        return Article.objects.all()

    # 省略可。オブジェクトに対するURLのパスを返す。
    def location(self, obj):
        return reverse('bbs:detail', args=[obj.slug])

    # 省略可。オブジェクトの最終更新日時を Python の datetime.datetime オブジェクトで返す。
    def lastmod(self, obj):
        return obj.updated_at

# 静的クラスサイトマップを定義。パラメータは動的クラスのものと同じ。
class StaticViewSitemap(Sitemap):
    changefreq = 'Always'
    priority = 1

    def items(self):
       # [ ]の左側は urls.py (setting.py側) のnamespace、右側は urls.py(アプリ側)のnameを設定する。
        return ['bbs:index'] 

    def location(self, item):
        return reverse(item)