# coding=utf8

# Copyright (C) 2015, Vanessa Soares, Thaiane Braga
#
# This file is part of Radar Parlamentar.
#
# Radar Parlamentar is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Radar Parlamentar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Radar Parlamentar.  If not, see <http://www.gnu.org/licenses/>.

from modelagem.models import Proposicao
from modelagem.models import Parlamentar
from modelagem.models import CasaLegislativa


class Genero:

    @staticmethod
    def definir_palavras(genero):
        temas = []
        for parlamentar in Parlamentar.objects.filter(genero=genero, casa_legislativa_id=2):
            for proposicao in Proposicao.objects.filter(
                    autor_principal=parlamentar.nome):
                for tema in proposicao.indexacao.split(','):
                    if len(tema) != 0:
                        temas.append(tema.strip().lower())

        print temas

        temas_dicionario = {}

        for tema in temas:
            if temas_dicionario.has_key(tema):
                temas_dicionario[tema] = temas_dicionario[tema] + 1
            else:
                temas_dicionario[tema] = 1

        temas_frequencia = sorted(
            temas_dicionario.items(), reverse=True, key=lambda i: i[1])
        temas_frequencia = temas_frequencia[:51]

        return temas_frequencia

    @staticmethod
    def definir_palavras_matriz():
        palavras = {}
        id_casa = CasaLegislativa.objects.get(nome_curto="cdep").id

        for parlamentar in Parlamentar.objects.filter(casa_legislativa_id=id_casa):
            for proposicao in Proposicao.objects.filter(autor_principal=parlamentar.nome):
                for tema in proposicao.indexacao.split(','):
                    if len(tema) != 0:
                        if palavras.has_key(tema):
                            palavras[tema][0] = palavras[tema][0] + 1
                        else:
                            palavras[tema] = [1, {}]

                        if palavras[tema][1].has_key(parlamentar.partido):
                            palavras[tema][1][parlamentar.partido.nome] = palavras[tema][1][parlamentar.partido.nome] + 1
                        else:
                            palavras[tema][1][parlamentar.partido.nome] = 1

        palavras_ordenados = sorted(
            palavras.items(), reverse=True, key=lambda palavras: palavras[1])
        palavras_ordenados = palavras_ordenados[:5]

        termos = []
        i = 0
        partidos_dict = {}

        for palavra in palavras_ordenados:
            info_palavras = {}
            info_palavras["group"]= 1
            info_palavras["name"] = palavra[0]
            info_palavras["id"] = i
            i = i + 1
            termos.append(info_palavras)

            for partido in palavra[1][1].items():
                if partidos_dict.has_key(partido[0]):
                    partidos_dict[partido[0]] = partidos_dict[partido[0]] + partido[1]
                else:
                    partidos_dict[partido[0]] = 1

        partidos_frequentes = sorted(
            partidos_dict.items(), reverse=True, key=lambda i: i[1])
        partidos_frequentes = partidos_frequentes[:33]

        partidos = []
        j = 0
        for partido in partidos_frequentes:
            info_partido = {}
            info_partido["group"] = 1
            info_partido["name"] = partido[0]
            info_partido["id"] = j
            j = j + 1
            partidos.append(info_partido)

        links = []
        k = 0
        for palavra in palavras_ordenados:
            l = 0
            for partido in partidos_frequentes:
                info_links = {}
                info_links["source"] = l
                info_links["target"] = k
                # info_links["value"] = palavra[partido]
                print palavra
                print partido

                # if palavra[1][1].has_key(partido[0]):
                #     print palavra[1][1][partido[0]]

                if palavra[1][1].has_key(partido):
                    info_links["value"] = palavra[1][1][partido[0]]
                else:
                    info_links["value"] = 0

                links.append(info_links)

                l = l + 1
            k = k + 1

        # json_final = {}
        # json_final["termos"] = termos
        # json_final["links"] = links
        # json_final["partidos"] = partidos

        json_final = {
            "termos": termos,
            "links": links,
            "partidos": partidos
        }

        print "------------ JSON FINAL ----------------"
        import json
        json_final = json.dumps(json_final)
        print json_final

