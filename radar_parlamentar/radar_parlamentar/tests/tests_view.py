# !/usr/bin/python
# coding=utf8

from django.core.urlresolvers import reverse
from django.test import TestCase
from radar_parlamentar.views import *

class ViewTest(TestCase):
    def test_generate_blog_news(self):
        first_blog_news = "Elasticsearch no Radar Parlamentar: filtrando votações por palavras-chaves"
        self._test_content("blog", first_blog_news)

    def test_index_content(self):
        radar_description = "A tecnologia a serviço do cidadão / cidadã - uma ferramenta para análise partidária das casas legislativas."
        self._test_content("index", radar_description)

    def test_origem_content(self):
        radar_history_subtitle = "Radar Parlamentar só é possível se existirem dados abertos"
        self._test_content("origem", radar_history_subtitle)

    def test_ogrupo_content(self):
        radar_group_subtitle = "POLIGNU - grupo de estudos de software livre da Poli-USP"
        self._test_content("ogrupo", radar_group_subtitle)

    def test_premiacoes_content(self):
        radar_awards_subtitle = "Radar Parlamentar só é possível se existirem dados abertos"
        self._test_content("premiacoes", radar_awards_subtitle)

    def test_radar_na_midia_content(self):
        radar_media = "Adrenaline UOL"
        self._test_content("radar_na_midia", radar_media)

    def test_votoaberto_content(self):
        radar_voto_aberto = "Durante nossos trabalhos para desenvolver o Radar Parlamentar percebemos que a grande maioria"
        self._test_content("votoaberto", radar_voto_aberto)

    def test_importadores_content(self):
        radar_import = "Quer ver a análise da Assembléia Legislativa de seu estado"
        self._test_content("importadores", radar_import)

    def test_genero_content(self):
        radar_genero_text_block = "Do ponto de vista quantitativo é possível observar ao longo do tempo o percentual de mulheres " \
                            "e homens no total de legislaturas, bem como nas bancadas partidárias."
        self._test_content("genero", radar_genero_text_block)



    def _test_content(self, page, content):
        url = reverse(str(page))
        request = self.client.get(url)
        self.assertContains(request, str(content), status_code=200)